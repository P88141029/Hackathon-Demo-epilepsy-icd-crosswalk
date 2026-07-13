from pathlib import Path
import csv
BASE=Path(__file__).resolve().parents[1]

def undot(x): return x.replace('.','')
def dot_target(x):
    return x[:3]+'.'+x[3:] if len(x)>3 else x
scope={r['source_code']:r for r in csv.DictReader(open(BASE/'data/icd9_scope.csv',encoding='utf-8-sig'))}
labels={r['source_code']:r['source_label_verified'] for r in csv.DictReader(open(BASE/'sources/mapping/icd9_verified_labels_scoped.csv',encoding='utf-8-sig'))}
targets={r['target_code']:r for r in csv.DictReader(open(BASE/'sources/icd10/icd10cm_2026_april_scoped_codes.csv',encoding='utf-8-sig'))}
rows=[]
for n,line in enumerate(open(BASE/'sources/mapping/2018_I9gem_scoped_extract.txt',encoding='utf-8'),1):
    src,tgt,flags=line.split()
    sc=next(k for k in scope if undot(k)==src)
    tc=dot_target(tgt)
    rows.append((n,sc,tc,flags))
counts={s:len(set(t for _,ss,t,_ in rows if ss==s)) for s in scope}
fieldnames=['mapping_id','source_code_system','source_version','source_code','source_label_raw','source_label_verified','target_code_system','target_release','target_code','target_label_verified','mapping_direction','raw_mapping_flags','mapping_cardinality','mapping_class','target_code_status','mapping_source_name','mapping_source_version','mapping_source_row_reference','source_url_or_file','retrieval_date','status','limitation','needs_human_review']
out=[]
for i,(line_no,s,t,flags) in enumerate(rows,1):
    approximate=flags[0]=='1'; no_map=flags[1]=='1'; combination=flags[2]=='1'
    cls='no_map' if no_map else 'context_required' if combination else 'multiple_candidates' if counts[s]>1 else 'approximate_candidate' if approximate else 'direct_candidate'
    mismatch=scope[s]['source_label_raw'].rstrip('.').lower()!=labels[s].rstrip('.').lower()
    out.append({'mapping_id':f'MAP{i:03d}','source_code_system':'ICD-9-CM','source_version':'ICD-9-CM diagnosis code set used by 2018 GEMs','source_code':s,'source_label_raw':scope[s]['source_label_raw'],'source_label_verified':labels[s],'target_code_system':'ICD-10-CM','target_release':'FY 2026 ICD-10-CM April 1, 2026 release','target_code':t,'target_label_verified':targets[t]['target_label'],'mapping_direction':'ICD-9-CM_to_ICD-10-CM','raw_mapping_flags':flags,'mapping_cardinality':'one_to_many' if counts[s]>1 else 'one_to_one_candidate','mapping_class':cls,'target_code_status':targets[t]['lookup_status'],'mapping_source_name':'CMS 2018 ICD-9-CM to ICD-10-CM General Equivalence Mappings (GEMs)','mapping_source_version':'2018 final GEMs','mapping_source_row_reference':f'scoped extract line {line_no}','source_url_or_file':'sources/mapping/2018_I9gem_scoped_extract.txt','retrieval_date':'2026-07-12','status':'needs_review','limitation':('Multiple candidates; all candidate rows carry approximate=1. ' + ('Raw and verified source labels differ in wording. ' if mismatch else '') + 'Runtime used a scoped mirror-derived extract; compare with official CMS ZIP before operational use.'),'needs_human_review':'TRUE'})
with open(BASE/'outputs/icd_crosswalk.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=fieldnames); w.writeheader(); w.writerows(out)
print(f'wrote {len(out)} mapping rows')
