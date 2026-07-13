from pathlib import Path
import csv,sys
B=Path(__file__).resolve().parents[1]
valid={r['target_code']:r for r in csv.DictReader(open(B/'sources/icd10/icd10cm_2026_april_scoped_codes.csv',encoding='utf-8-sig'))}
rows=list(csv.DictReader(open(B/'outputs/icd_crosswalk.csv',encoding='utf-8-sig')))
missing=[r['target_code'] for r in rows if r['target_code'] and r['target_code'] not in valid]
print({'checked':len(rows),'missing':missing})
sys.exit(1 if missing else 0)
