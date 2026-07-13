# Tool Inventory

| Tool | Purpose | Input | Output | Side effect | Permission |
|---|---|---|---|---|---|
| Python csv/text parser | 讀取 scope、GEM 與 code extract | CSV/TXT | rows | none | local read |
| Official crosswalk reader | 解析 GEM 固定欄位 | scoped GEM TXT | candidates/raw flags | none | local read |
| ICD-10-CM validator | exact code lookup | candidates + scoped release CSV | status/label | none | local read |
| Drug terminology lookup | ingredient normalization | medication raw | normalized name + UNII | none | public lookup |
| Drug evidence retriever | 讀取 DailyMed/MedlinePlus | ingredient | narrow claims | none | public read |
| Output validator | schema/enums/separation/eval | project files | report/exit code | report write | local execute |
| File writer | 建立 artifacts | structured rows | CSV/MD | file creation | project directory only |

ZIP binary下載在本次 sandbox 失敗，因此使用 scoped local extracts，並在 provenance 與 review note 明示需比對官方 ZIP。
