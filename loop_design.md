# Loop Design

1. **Plan**：凍結五碼、三藥、CMS 2018 GEMs 與 FY2026 April release。
2. **Act**：解析、lookup、建立 evidence rows。
3. **Observe**：檢查 row counts、raw flags、來源欄位與 target labels。
4. **Evaluate**：執行 deterministic validator 與 synthetic eval。
5. **Revise**：只修 parser、schema、lookup key、claim scope、status、conversion rule、reference；最多 2 輪。
6. **Stop**：全數通過或觸發缺來源、衝突、no progress、專業判斷。

No-progress：連續兩輪相同錯誤。Human Review：多候選、approximate/context flag、label mismatch、target release 疑義、drug normalization ambiguity、drug scope 與 subtype 需求不一致。
