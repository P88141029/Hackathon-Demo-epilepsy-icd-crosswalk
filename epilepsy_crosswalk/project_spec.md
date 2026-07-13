# Project Specification

## 問題定義
針對固定五個 ICD-9-CM 癲癇細項，保存 CMS 2018 GEMs 的全部 ICD-10-CM 候選、原始旗標、版本與來源，並以 FY 2026 ICD-10-CM April 1 release 做 exact code lookup。另對最多三種指定藥物整理可回查的疾病範圍證據。

## 使用者情境
醫療資料工程與 evidence audit 展示；不是病人診斷、自動編碼或處方工具。

## 固定範圍
345.00、345.10、345.40、345.90、345.91；藥物為 Phenytoin、Carbamazepine、Valproic acid。

## 系統與方向
ICD-9-CM -> ICD-10-CM；CMS 2018 final GEMs；target release 為 FY 2026 April 1, 2026。

## In scope
候選擷取、raw flags、cardinality、target existence、藥物名稱正規化、窄範圍 evidence、validator、synthetic eval、human-review handoff。

## Out of scope
病人層級診斷、最終 coding、申報決策、用藥推薦、劑量、安全性評估、基因證據、反向 mapping。

## 安全與 Human Review
任何多候選、approximate flag、label wording mismatch、版本疑義或可影響照護/申報的結論一律交由 medical coder/health information manager；藥物範圍由 pharmacist/neurologist 複核。

## 完成條件
五碼與三藥均處理；所有輸出 schema 完整；validator 與 normal/not-found/conflicting eval 通過；來源限制明示。
