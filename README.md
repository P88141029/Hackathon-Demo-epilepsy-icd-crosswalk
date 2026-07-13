# Hackathon-Demo-epilepsy-icd-crosswalk

## Epilepsy ICD-9-CM → ICD-10-CM Crosswalk & Medication Evidence Audit

> 一個固定範圍、可重跑、可追溯且具 Human Review 邊界的 Hackathon 專案。
>
> 本專案保留 CMS GEMs 提供的所有 ICD-10-CM 候選，並將藥物疾病範圍證據與 ICD 選碼邏輯分離。它是 **evidence audit package**，不是自動診斷、處方或最終編碼工具。

## 專案狀態

| 項目 | 結果 |
|---|---:|
| Completion status | `completed_with_review_required` |
| 固定 ICD-9-CM codes | 5 |
| ICD-10-CM candidate rows | 11 |
| 處理藥物 | 3 |
| Drug evidence rows | 5 |
| Validator checks | 38 passed / 0 failed |
| Revision count | 1 |

---

## 1. 專案背景

### ICD-9-CM 與 ICD-10-CM

**ICD-9-CM** 與 **ICD-10-CM** 都是疾病與診斷編碼系統，但兩者的結構與細緻程度不同：

| 比較項目 | ICD-9-CM | ICD-10-CM |
|---|---|---|
| 角色 | 較早期的臨床診斷編碼系統 | 較新、較細緻的臨床診斷編碼系統 |
| 代碼形式 | 以數字為主 | 英文字母與數字混合 |
| 臨床細節 | 相對較少 | 可表達更多疾病 subtype、嚴重度與臨床情境 |
| Crosswalk 特性 | 一個來源碼可能對應多個目標碼 | 需依原始病歷情境選擇合適代碼 |

ICD-9-CM 到 ICD-10-CM 的轉換通常不是單純的一對一替換。來源碼可能缺少 ICD-10-CM 所需要的細節，例如：

- seizure / epilepsy subtype；
- 是否為 intractable；
- 是否伴隨 status epilepticus；
- 是否需要多個候選或額外臨床情境。

因此，本專案的目標不是強制產生唯一答案，而是：

1. 保存所有可回查的候選 mapping；
2. 保留來源、版本與 GEM raw flags；
3. 驗證目標 ICD-10-CM code 是否存在於指定 release；
4. 將不確定或需專業判斷的結果標記為 `needs_review`。

---

## 2. 專案問題

本專案回答以下問題：

> 對五個固定的癲癇 ICD-9-CM 細項，CMS crosswalk 提供哪些 ICD-10-CM 候選？這些候選是否為一對多、近似對應或需要額外臨床資訊？三種指定抗癲癇藥物的公開證據可以支持哪些疾病範圍？哪些結果必須交由醫療編碼或臨床專業人員複核？

---

## 3. 固定分析範圍

### 3.1 ICD-9-CM scope

本次 MVP 僅處理以下五個來源碼：

| ICD-9-CM | 原始標籤 | 保留的 ICD-10-CM candidates |
|---|---|---|
| `345.00` | Generalized nonconvulsive epilepsy, not intractable. | `G40.A01`, `G40.A09` |
| `345.10` | Generalized convulsive epilepsy, not intractable. | `G40.309`, `G40.401`, `G40.409` |
| `345.40` | Localization-related (focal) epilepsy with complex partial seizures. | `G40.201`, `G40.209` |
| `345.90` | Epilepsy unspecified, not intractable. | `G40.901`, `G40.909` |
| `345.91` | Epilepsy unspecified, with intractable epilepsy. | `G40.911`, `G40.919` |

規則：

- 不自動新增其他 ICD-9-CM codes；
- 不只選取第一個 GEM candidate；
- 不將正向 mapping 假設為可逆 mapping；
- 不把候選 mapping 宣稱為最終 coding decision。

### 3.2 Medication scope

| Medication ID | 藥物 | 正規化識別碼 | 本次 evidence scope |
|---|---|---|---|
| `MED001` | Phenytoin | `UNII:6158TKW0C5` | `generalized_seizure`, `focal_seizure` |
| `MED002` | Carbamazepine | `UNII:33CM23913M` | `focal_seizure`, `generalized_seizure` |
| `MED003` | Valproic acid | `UNII:614OI1Z5WI` | `broad_epilepsy` |

藥物 evidence 僅用來描述疾病範圍，**不會用來選擇、補寫或確認 ICD-10-CM code**。

---

## 4. 輸入檔案

### 4.1 `AGENT.md`

`AGENT.md` 是本專案的主要操作規格，定義：

- Agent role 與任務邊界；
- 固定 ICD 與 medication scope；
- 允許使用的來源；
- mapping 與 drug evidence 的輸出 schema；
- `not_found`、`conflicting` 與 Human Review 規則；
- deterministic validator 與停止條件；
- 不得執行的診斷、處方或最終編碼行為。

### 4.2 Scope files

| 檔案 | 用途 |
|---|---|
| `data/icd9_scope.csv` | 定義固定五個 ICD-9-CM source codes 與原始標籤 |
| `data/medication_scope.csv` | 定義最多三個要正規化與查找 evidence 的藥物 |
| `data/eval_cases.csv` | 定義 normal、not-found、conflicting 三種 synthetic fixtures |

### 4.3 Configuration

`config/project_config.yaml` 凍結以下設定：

- source code system：ICD-9-CM；
- mapping direction：ICD-9-CM → ICD-10-CM；
- mapping source：CMS 2018 final GEMs；
- target release：FY 2026 ICD-10-CM April 1, 2026 release；
- medication 與 evidence row 上限；
- revision 上限。

### 4.4 Scoped source extracts

| 路徑 | 用途 |
|---|---|
| `sources/mapping/2018_I9gem_scoped_extract.txt` | 五個 source codes 的 GEM rows |
| `sources/mapping/icd9_verified_labels_scoped.csv` | ICD-9-CM verified wording |
| `sources/mapping/CMS_GEM_user_guide_notes.md` | GEM flag 與使用規則摘要 |
| `sources/icd10/icd10cm_2026_april_scoped_codes.csv` | 11 個候選 ICD-10-CM code 的 exact lookup |
| `sources/drug/evidence_excerpts.md` | 藥物來源與 evidence 摘要 |

---

## 5. Workflow

```text
Fixed ICD-9-CM and medication scope
                ↓
Freeze mapping source and target release
                ↓
Validate ICD-9-CM source codes and labels
                ↓
Extract all ICD-10-CM GEM candidates
                ↓
Preserve raw flags, source version and row references
                ↓
Validate candidates against the configured ICD-10-CM release
                ↓
Classify cardinality, mapping class and review status
                ↓
Normalize scoped medication ingredients
                ↓
Retrieve and separate drug disease-scope evidence
                ↓
Run normal / not-found / conflicting synthetic fixtures
                ↓
Run deterministic output validator
                ↓
Human Review and package handoff
```

Agent loop：

1. **Plan**：凍結五碼、三藥、CMS 2018 GEMs 與 FY2026 April release。
2. **Act**：解析來源、執行 lookup、建立 mapping 與 evidence rows。
3. **Observe**：檢查 row count、raw flags、來源欄位及 target labels。
4. **Evaluate**：執行 deterministic validator 與 synthetic eval。
5. **Revise**：僅修正 parser、schema、lookup key、claim scope、status 或 reference；最多兩輪。
6. **Stop**：全數通過，或遇到缺來源、衝突、無進展及需專業判斷的情形。

---

## 6. 執行方式

### 環境需求

- Python 3；
- scripts 僅使用 Python standard library；
- 請從 repository 根目錄執行。

### 執行順序

```bash
python scripts/build_crosswalk.py
python scripts/validate_icd10_codes.py
python scripts/normalize_medications.py
python scripts/validate_outputs.py
```

### 預期 validator 結果

```text
Exit status: 0
Passed checks: 38
Failed checks: 0
```

完整紀錄位於：

```text
outputs/validation_report.md
```

---

## 7. 預期產出

| 檔案 | 說明 |
|---|---|
| `outputs/icd_crosswalk.csv` | ICD-9-CM → ICD-10-CM 的逐列候選 mapping、raw flags、來源與 review status |
| `outputs/drug_evidence.csv` | 藥物正規化、disease scope、證據來源、限制與 Human Review 狀態 |
| `outputs/audit_summary.csv` | 將 ICD mapping 與 medication evidence 濃縮為 item-level 摘要 |
| `outputs/source_inventory.csv` | 來源名稱、版本、URL／本地檔案、hash 與使用範圍 |
| `outputs/eval_results.csv` | synthetic normal、not-found、conflicting cases 的執行結果 |
| `outputs/review_note.md` | 人工複核原因、建議 reviewer 與 source-package handoff |
| `outputs/validation_report.md` | deterministic validator 的通過與失敗項目 |
| `logs/run_log.md` | 執行過程、凍結來源、runtime 限制與 planned commands |
| `logs/search_log.csv` | 每次查找的目標、query、結果與使用來源 |
| `logs/issue_log.csv` | 已知限制、嚴重度及 resolution／handoff |
| `MANIFEST.csv` | 專案檔案大小與 SHA-256 hash |
| `completion_summary.md` | 本次執行的整體完成摘要 |

---

## 8. 本次結果摘要

### ICD mapping

- 5 個 ICD-9-CM source codes 全數完成；
- 共保留 11 個 ICD-10-CM candidate rows；
- 5 個 source codes 全部屬於 `multiple_candidates`；
- 11 個 candidate rows 的 GEM raw flag 均為 `10000`；
- 沒有自動選出任何唯一 ICD-10-CM code；
- 所有正式 mappings 都標記為 `needs_review`。

### `approximate flag = 1` 的意義

本專案所有 GEM raw flags 都是：

```text
10000
```

五個位置依序表示：

```text
approximate | no_map | combination | scenario | choice_list
     1      |   0    |      0      |    0     |      0
```

`approximate = 1` 表示來源與目標概念並非完全等價，轉換時可能缺少 ICD-10-CM 所需的臨床細節。它：

- 不代表 mapping 一定錯誤；
- 不代表信心只有 1%；
- 不代表 target code 不存在；
- 也不表示可以直接選第一個候選。

因此需要依原始病歷內容，由 medical coder 或 neurologist 判斷。

### Drug evidence

- 3 種藥物全數完成 ingredient-level normalization；
- 共建立 5 筆 evidence rows；
- generalized seizure：2 rows；
- focal seizure：2 rows；
- broad epilepsy：1 row；
- Valproic acid 僅保守分類為 `broad_epilepsy`；
- 沒有任何 drug evidence 被用來決定 ICD code。

---

## 9. Synthetic evaluation cases

| Case | 輸入目的 | 預期安全行為 | 結果 |
|---|---|---|---|
| `normal` | 使用正式 scope 中的 code 與 medication | 保留全部候選並標記 review | Passed |
| `not_found` | 使用 `INVALID_ICD9_TEST` 與 `UNKNOWN_MEDICATION` | 不產生虛構 code、藥名或來源 | Passed |
| `conflicting` | 對 `345.90` 提供不相符的 `G40.A01` | 不接受或替換衝突值，升級 Human Review | Passed |

> `not_found` 是刻意設計的 synthetic fixture。正式的五個 ICD-9-CM codes 與三種 medication scope 均成功找到資料。

---

## 10. Human Review

所有正式 ICD mappings 都需要人工複核，主要原因包括：

- 一個 source code 對應多個 ICD-10-CM candidates；
- GEM `approximate flag = 1`；
- 是否伴隨 status epilepticus 需要原始病歷資訊；
- source label 與 verified wording 可能存在文字差異；
- scoped extracts 在正式使用前需與官方完整 package 再比對；
- Valproic acid 的 opened evidence 無法建立特定 seizure subtype。

建議 reviewer：

- Health information manager／medical coder；
- Neurologist；
- Pharmacist；
- Data steward。

---

## 11. Evidence sources

本專案沒有直接使用 PubMed PMID 論文作為主要證據來源，而是優先使用可回查的官方 mapping、code set 與藥品資訊：

| 來源 | 用途 |
|---|---|
| CMS 2018 ICD-9-CM to ICD-10-CM GEMs | ICD crosswalk candidates |
| CMS FY2026 ICD-10-CM April 1, 2026 release | target code exact lookup |
| FDA UNII Search | medication ingredient normalization |
| DailyMed DILANTIN label | Phenytoin disease-scope evidence |
| DailyMed TEGRETOL label | Carbamazepine disease-scope evidence |
| MedlinePlus Valproic Acid | broad seizure-use evidence |

完整來源與版本記錄請參閱：

```text
outputs/source_inventory.csv
```

---

## 12. epilepsy_crosswalk directory structure

```text
.
├── AGENT.md
├── MANIFEST.csv
├── completion_summary.md
├── project_spec.md
├── task_spec.md
├── loop_design.md
├── harness_checklist.md
├── tool_inventory.md
├── demo_notes.md
├── config/
│   └── project_config.yaml
├── data/
│   ├── icd9_scope.csv
│   ├── medication_scope.csv
│   └── eval_cases.csv
├── sources/
│   ├── mapping/
│   ├── icd10/
│   └── drug/
├── scripts/
│   ├── build_crosswalk.py
│   ├── validate_icd10_codes.py
│   ├── normalize_medications.py
│   └── validate_outputs.py
├── outputs/
│   ├── icd_crosswalk.csv
│   ├── drug_evidence.csv
│   ├── audit_summary.csv
│   ├── source_inventory.csv
│   ├── eval_results.csv
│   ├── review_note.md
│   └── validation_report.md
└── logs/
    ├── run_log.md
    ├── search_log.csv
    └── issue_log.csv
```

---

## 13. Known limitations

1. 本次 runtime 可以開啟 CMS release metadata 與 GEM user guide，但未能保留官方 CMS ZIP binaries。
2. 專案使用 scoped local extracts；正式營運、申報或病人照護用途前，必須與官方完整 packages 重新比對。
3. 所有正式 mapping 均為多候選且 `approximate = 1`，不可直接視為唯一或最終編碼。
4. 藥物 evidence 僅支持 disease scope，不可反推病人診斷或 ICD subtype。
5. 本專案沒有使用真實病人資料，也不處理任何可識別個人資訊。

---

## 14. Safety disclaimer

本 repository 僅供 Hackathon、醫療資料工程與 evidence-audit 展示使用。

不得將本專案輸出直接用於：

- 病人層級診斷；
- 自動或最終 ICD coding；
- 醫療申報決策；
- 藥物推薦、停藥、換藥或劑量判斷；
- 病人安全性或預後評估。

任何可能影響臨床照護或申報的結論，都必須由合格的醫療編碼與臨床專業人員複核。

---

## 15. Reproducibility and integrity

`MANIFEST.csv` 記錄專案主要檔案的：

- relative path；
- file size；
- SHA-256 hash。

可利用 manifest 檢查交付後的檔案是否被修改，並支援後續 audit 與 handoff。
