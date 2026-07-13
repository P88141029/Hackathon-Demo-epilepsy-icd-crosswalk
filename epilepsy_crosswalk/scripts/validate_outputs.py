from pathlib import Path
import csv, sys, re
from collections import Counter, defaultdict

B = Path(__file__).resolve().parents[1]
passes=[]; fails=[]

def check(name, cond, detail=''):
    item = name + (f': {detail}' if detail else '')
    (passes if cond else fails).append(item)

def readcsv(p):
    with open(B/p, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def parse_gem_extract(p):
    rows=[]
    for lineno, line in enumerate((B/p).read_text(encoding='utf-8').splitlines(), start=1):
        if not line.strip():
            continue
        parts=line.split()
        rows.append({'source':parts[0], 'target':parts[1], 'flags':parts[2], 'line':lineno})
    return rows

expected={'345.00','345.10','345.40','345.90','345.91'}
expected_nodot={x.replace('.','') for x in expected}
required_files=[
    'outputs/icd_crosswalk.csv','outputs/drug_evidence.csv','outputs/source_inventory.csv',
    'outputs/audit_summary.csv','outputs/review_note.md','outputs/eval_results.csv'
]
check('Required output files exist', all((B/p).is_file() for p in required_files))

scope=readcsv('data/icd9_scope.csv')
maps=readcsv('outputs/icd_crosswalk.csv')
drugs=readcsv('outputs/drug_evidence.csv')
meds=readcsv('data/medication_scope.csv')
evals=readcsv('data/eval_cases.csv')
eval_results=readcsv('outputs/eval_results.csv')
inventory=readcsv('outputs/source_inventory.csv')
audit=readcsv('outputs/audit_summary.csv')
scoped_targets=readcsv('sources/icd10/icd10cm_2026_april_scoped_codes.csv')
gem=parse_gem_extract('sources/mapping/2018_I9gem_scoped_extract.txt')

check('Input schema check', bool(scope) and set(scope[0]) >= {'source_code','source_label_raw','include_in_mvp'})
check('Fixed scope exactly five', {r['source_code'] for r in scope}==expected and len(scope)==5 and all(r['include_in_mvp'].upper()=='TRUE' for r in scope))
check('All five codes represented', {r['source_code'] for r in maps}==expected)
check('No sixth source code', all(r['source_code'] in expected for r in maps))
check('Mapping IDs unique', len({r['mapping_id'] for r in maps})==len(maps))
check('Mapping direction fixed', all(r['mapping_direction']=='ICD-9-CM_to_ICD-10-CM' for r in maps))

# Candidate completeness is checked against the frozen local source extract, not a hard-coded row list.
gem_pairs={(r['source'],r['target'],r['flags']) for r in gem if r['source'] in expected_nodot}
out_pairs={(r['source_code'].replace('.',''),r['target_code'].replace('.',''),r['raw_mapping_flags']) for r in maps}
check('Candidate completeness against frozen extract', out_pairs==gem_pairs, f'extract={len(gem_pairs)}, output={len(out_pairs)}')
check('Candidate row count', len(maps)==len(gem_pairs), f'found {len(maps)}')
check('Raw flags preserved', all(r['raw_mapping_flags']=='10000' for r in maps))
check('Trace fields complete', all(all(r[k] for k in ['mapping_source_name','mapping_source_version','mapping_source_row_reference','source_url_or_file','retrieval_date','raw_mapping_flags']) for r in maps))

cnt=Counter(r['source_code'] for r in maps)
check('Cardinality matches candidates', all(r['mapping_cardinality']=='one_to_many' and cnt[r['source_code']]>1 for r in maps))
check('Multiple candidates class', all(r['mapping_class']=='multiple_candidates' for r in maps))
check('Approximate uncertainty retained', all('approximate=1' in r['limitation'] for r in maps))

lookup={r['target_code']:r['target_label'] for r in scoped_targets}
check('Target exact lookup present', all(r['target_code'] in lookup and r['target_label_verified']==lookup[r['target_code']] and r['target_code_status']=='active_in_configured_release' for r in maps))
check('All ambiguous mappings reviewed', all(r['needs_human_review']=='TRUE' and r['status']=='needs_review' for r in maps))

inc=[r for r in meds if r['include_in_mvp'].upper()=='TRUE']
check('Medication limit', len({r['medication_raw'].lower() for r in inc})<=3 and len(inc)==3)
check('Medication IDs represented', {r['medication_id'] for r in drugs}=={r['medication_id'] for r in inc})
per=Counter(r['medication_id'] for r in drugs)
check('Drug evidence row limit', all(v<=2 for v in per.values()))
check('Drug evidence IDs unique', len({r['evidence_id'] for r in drugs})==len(drugs))
check('Supported drug evidence complete', all(r['medication_normalized'] and r['normalization_id'] and r['source_id'] and r['source_url'] and r['quoted_evidence'] for r in drugs if r['status']=='supported'))
check('Drug evidence enums', all(r['disease_scope'] in {'broad_epilepsy','generalized_seizure','focal_seizure','specific_subtype','non_epilepsy_use','insufficient_evidence','conflicting'} for r in drugs))
check('No ICD fields in drug evidence', bool(drugs) and not any('target_code' in k.lower() or 'icd' in k.lower() for k in drugs[0]))
check('No drug-to-code inference', all('select any icd' not in r['claim'].lower() and 'assign' not in r['claim'].lower() for r in drugs))

check('Source inventory categories', {'mapping','icd9_code_set','icd10_code_set','drug_terminology','drug_evidence'} <= {r['source_category'] for r in inventory})
check('Source inventory access enums', all(r['access_status'] in {'opened','downloaded','not_found','error'} for r in inventory))
check('Local source files hashed', all(r['file_hash'] for r in inventory if r['source_url_or_file'].startswith('sources/')))

check('Audit summary coverage', len(audit)==8 and {r['item_id'] for r in audit if r['item_type']=='icd_mapping'}==expected and {r['item_id'] for r in audit if r['item_type']=='medication'}=={r['medication_id'] for r in inc})
check('Audit does not claim final coding', all('final coding decision' not in r['summary'].lower() for r in audit))

check('Eval cases synthetic', len(evals)==3 and all(r['synthetic']=='TRUE' for r in evals))
normal=next(r for r in evals if r['case_type']=='normal')
nf=next(r for r in evals if r['case_type']=='not_found')
conflict=next(r for r in evals if r['case_type']=='conflicting')
check('Normal eval fixture', normal['source_code'] in expected and normal['medication_raw'].lower() in {r['medication_raw'].lower() for r in meds} and normal['expected_status']=='needs_review')
check('Not-found eval fixture', nf['source_code']=='INVALID_ICD9_TEST' and nf['medication_raw']=='UNKNOWN_MEDICATION' and nf['expected_status']=='not_found')
check('Conflicting eval fixture', conflict['expected_status']=='conflicting' and conflict['expected_human_review']=='TRUE' and conflict['provided_target_code'])
check('Eval result coverage', {r['case_type'] for r in eval_results}=={'normal','not_found','conflicting'} and all(r['synthetic']=='TRUE' and r['passed']=='TRUE' for r in eval_results))
check('Not-found safe failure', next(r for r in eval_results if r['case_type']=='not_found')['observed_status']=='not_found')
check('Conflict escalated', (lambda r: r['observed_status']=='conflicting' and r['needs_human_review']=='TRUE')(next(r for r in eval_results if r['case_type']=='conflicting')))

review=(B/'outputs/review_note.md').read_text(encoding='utf-8')
check('Human Review roles listed', all(x in review.lower() for x in ['medical coder','neurologist','pharmacist','data steward']))

# Safety-language scan: positive findings are restricted to source claims; banned patient-level conclusions must be absent.
combined='\n'.join((B/p).read_text(encoding='utf-8-sig') for p in ['outputs/icd_crosswalk.csv','outputs/drug_evidence.csv','outputs/audit_summary.csv','outputs/review_note.md'])
banned=[r'patient has epilepsy',r'confirmed diagnosis',r'recommended medication',r'dosage recommendation',r'final code is']
check('No patient-level diagnosis or recommendation', not any(re.search(p, combined, flags=re.I) for p in banned))

report=['# Validation Report','', 'Command: `python scripts/validate_outputs.py`','',f'Exit status: {0 if not fails else 1}','',f'Passed checks: {len(passes)}',f'Failed checks: {len(fails)}','','## Passed']+[f'- {x}' for x in passes]+['','## Failed']+([f'- {x}' for x in fails] if fails else ['- None'])+['','## Revision','- Revision count: 1','- Revision 1 corrected the scoped ICD-10 lookup label-field name after the first validator run raised a KeyError.','- Official CMS binary packages could not be retained in the runtime; the provenance limitation remains a Human Review item, not a hidden validator exception.']
(B/'outputs/validation_report.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print('\n'.join(report))
sys.exit(1 if fails else 0)
