# Human Review Note

## ICD mapping
All five source codes require review because each has multiple target candidates and every retained GEM row has raw flag `10000` (approximate=1). No unique target was selected.

| Source | Candidates | Class | Main review reason | Suggested reviewer |
|---|---|---|---|---|
| 345.00 | G40.A01; G40.A09 | multiple_candidates | status epilepticus distinction and approximate flag | Medical coder / neurologist |
| 345.10 | G40.309; G40.401; G40.409 | multiple_candidates | generalized subtype and status distinction | Medical coder / neurologist |
| 345.40 | G40.201; G40.209 | multiple_candidates | status epilepticus distinction | Medical coder / neurologist |
| 345.90 | G40.901; G40.909 | multiple_candidates | status epilepticus distinction | Medical coder |
| 345.91 | G40.911; G40.919 | multiple_candidates | status epilepticus distinction | Medical coder |

The user-supplied source labels and verified ICD-9-CM wording are both preserved. Differences were not silently overwritten.

## Drug evidence
Phenytoin and carbamazepine labels support both focal/partial and generalized tonic-clonic categories in separate rows. Valproic acid was conservatively classified `broad_epilepsy` from the current opened MedlinePlus statement. None of these rows can determine an ICD candidate. Pharmacist/neurologist review is recommended if a more specific disease-scope claim is needed.

## Source-package handoff
The sandbox could open official CMS release metadata and the GEM user guide but could not retain ZIP binaries. Before operational, billing, or patient-care use, compare the scoped GEM rows and target-code extract with the official CMS packages.

## Recommended reviewer roles

- Health information manager / medical coder
- Neurologist
- Pharmacist
- Data steward
