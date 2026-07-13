# Task Specification

## Problem
建立可追溯的固定範圍 ICD crosswalk 與獨立藥物證據 audit。
## Input
`data/icd9_scope.csv`、`data/medication_scope.csv`、config、scoped source extracts。
## Output
crosswalk、drug evidence、source inventory、audit summary、review note、validation report 與 logs。
## Rules
不增加 codes/medications；不丟棄候選；不以藥物選 code；不捏造來源；所有 approximate/multiple cases 需 review。
## Check
執行 `python scripts/validate_outputs.py` 與三種 synthetic eval。
## Stop
輸入缺漏、來源版本未知、scope 超限、敏感資料、同一錯誤兩輪未改善、或需專業判斷時停止並 handoff。
