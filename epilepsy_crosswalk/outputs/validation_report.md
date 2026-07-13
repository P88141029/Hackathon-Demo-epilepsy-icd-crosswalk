# Validation Report

Command: `python scripts/validate_outputs.py`

Exit status: 0

Passed checks: 38
Failed checks: 0

## Passed
- Required output files exist
- Input schema check
- Fixed scope exactly five
- All five codes represented
- No sixth source code
- Mapping IDs unique
- Mapping direction fixed
- Candidate completeness against frozen extract: extract=11, output=11
- Candidate row count: found 11
- Raw flags preserved
- Trace fields complete
- Cardinality matches candidates
- Multiple candidates class
- Approximate uncertainty retained
- Target exact lookup present
- All ambiguous mappings reviewed
- Medication limit
- Medication IDs represented
- Drug evidence row limit
- Drug evidence IDs unique
- Supported drug evidence complete
- Drug evidence enums
- No ICD fields in drug evidence
- No drug-to-code inference
- Source inventory categories
- Source inventory access enums
- Local source files hashed
- Audit summary coverage
- Audit does not claim final coding
- Eval cases synthetic
- Normal eval fixture
- Not-found eval fixture
- Conflicting eval fixture
- Eval result coverage
- Not-found safe failure
- Conflict escalated
- Human Review roles listed
- No patient-level diagnosis or recommendation

## Failed
- None

## Revision
- Revision count: 1
- Revision 1 corrected the scoped ICD-10 lookup label-field name after the first validator run raised a KeyError.
- Official CMS binary packages could not be retained in the runtime; the provenance limitation remains a Human Review item, not a hidden validator exception.
