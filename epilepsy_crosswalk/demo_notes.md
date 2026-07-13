# Five-Minute Demo Notes

## 0:00-0:40 Problem
ICD-9-CM to ICD-10-CM is not assumed one-to-one. Drug evidence is not coding evidence. This is an evidence audit, not automatic decision-making.

## 0:40-1:20 Scope and Sources
Show the five fixed codes, CMS 2018 GEMs, FY2026 April target release, and the three scoped ingredients.

## 1:20-2:30 Crosswalk
Use 345.10 as the example: three candidates are retained. Show `10000`, one-to-many cardinality, target exact lookup, and `needs_review`.

## 2:30-3:20 Drug Evidence
Show separate focal/generalized rows for carbamazepine and the conservative broad row for valproic acid. Emphasize that no medication row selects an ICD code.

## 3:20-4:15 Harness
Show normal, INVALID_ICD9_TEST/UNKNOWN_MEDICATION, and conflicting synthetic cases. Show validator checks for fixed scope, candidate completeness, trace fields, row limits, and separation.

## 4:15-5:00 Limits and Handoff
No diagnosis, final coding, prescribing, dose, prognosis, or patient advice. All ambiguous mappings go to a coder/neurologist; source ZIP extracts require independent verification.
