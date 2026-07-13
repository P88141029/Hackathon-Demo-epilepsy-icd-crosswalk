# CMS GEM user guide notes

- File positions: source code, target code, five mapping flags.
- Flag order: approximate, no-map, combination, scenario, choice-list.
- `10000` therefore means approximate=1, no-map=0, combination=0, scenario=0, choice-list=0.
- Project classification precedence: no-map -> context-required -> multiple-candidates -> approximate-candidate -> direct-candidate.
- Because each scoped source code has more than one unique target, all five source-level mappings are classified `multiple_candidates`; every candidate also retains the approximate raw flag in `raw_mapping_flags` and limitation text.
- Official guide: https://www.cms.gov/files/document/diagnosis-code-set-general-equivalence-mappings-icd-10-cm-icd-9-cm-and-icd-9-cm-icd-10-cm.pdf
- Runtime provenance: rows were transcribed from a public mirror of the CMS 2018 file because the execution sandbox could not download ZIP binaries. The mirror blob SHA was `d6d6c065e788b12ff4fb8ef701e0f9b720e3405d`. Operational use requires comparison with the official CMS ZIP.
