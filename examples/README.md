# Examples

Examples are executable attribute-contract fixtures and submitter-facing examples.
They contain no real project data, spatial package, or geometry dataset. The
`geometry` values are schema-required placeholders only; spatial package and
geometry validation belong in the `hrl-restoration-data-pipeline` repository.

`python scripts/validate_fixtures.py` validates every fixture with the
repository's LinkML validator.

## Valid fixtures

| Fixture | Target LinkML class/profile | Expected result |
| --- | --- | --- |
| `valid/restoration_project_submission_minimal.yaml` | `RestorationProjectSubmission` | Pass; smallest required submitted attribute set. |
| `valid/restoration_project_canonical_representative.yaml` | `RestorationProjectCanonicalRecord` | Pass; shared fields plus canonical provenance, funding-gap, and lifecycle fields. |
| `valid/restoration_project_public_representative.yaml` | `RestorationProjectPublicRecord` | Pass; public-export fields only. |

## Invalid fixtures

| Fixture | Target LinkML class/profile | Expected result and demonstrated rule |
| --- | --- | --- |
| `invalid/restoration_project_submission_missing_project_id.yaml` | `RestorationProjectSubmission` | Fail: required stable `project_id` is missing. |
| `invalid/restoration_project_submission_invalid_controlled_value.yaml` | `RestorationProjectSubmission` | Fail: `project_stage` is outside `ProjectStageEnum`. |
| `invalid/restoration_project_submission_malformed_contact_email.yaml` | `RestorationProjectSubmission` | Fail: `contact_email` does not match its email pattern. |
| `invalid/restoration_project_submission_missing_required_project_name.yaml` | `RestorationProjectSubmission` | Fail: required `project_name` is missing. |
| `invalid/restoration_project_submission_construction_start_year_below_minimum.yaml` | `RestorationProjectSubmission` | Fail: `construction_start_year` is below 2018. |
| `invalid/restoration_project_public_private_contact_email.yaml` | `RestorationProjectPublicRecord` | Fail: `contact_email` is an unexpected private field in the public contract. |

The schema does not define a pattern or other format constraint for
`project_id`, so there is intentionally no invalid-format `project_id` fixture.

- `examples/valid/` contains examples expected to pass attribute validation.
- `examples/invalid/` contains examples expected to fail specific checks.
- `examples/lead_entities/` contains a starter program-level key table for
  controlled lead entity IDs and their display names.

Detailed example CSVs or spatial files should be added only when the schema
fields and validation behavior are clear enough to represent safely. Draft
examples should be clearly marked as draft.
