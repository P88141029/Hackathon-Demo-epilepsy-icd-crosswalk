from pathlib import Path
import csv,sys
B=Path(__file__).resolve().parents[1]
lookup={'phenytoin':('Phenytoin','UNII:6158TKW0C5'),'carbamazepine':('Carbamazepine','UNII:33CM23913M'),'valproic acid':('Valproic acid','UNII:614OI1Z5WI')}
rows=list(csv.DictReader(open(B/'data/medication_scope.csv',encoding='utf-8-sig')))
for r in rows:
    print(r['medication_id'],lookup.get(r['medication_raw'].lower(),('','not_found')))
sys.exit(0 if all(r['medication_raw'].lower() in lookup for r in rows if r['include_in_mvp'].upper()=='TRUE') else 1)
