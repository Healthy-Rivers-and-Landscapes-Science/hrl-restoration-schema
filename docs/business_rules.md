# Business Rules

Some HRL restoration data rules are not fully expressible in LinkML and should
be enforced by validation or ingestion code.

| Rule | Likely enforcement location | Error/warning/derived value | Notes |
| --- | --- | --- | --- |
| Construction completion year should not be earlier than construction start year | Validation code | Error | Applies when both years are present |
| Funding gap may be calculated from estimated budget and secured funding | Validation or ingestion code | Derived value | Submitted value may be compared with the calculated value |
| Program-assigned fields such as `project_id` should be assigned after validation and ingestion | Ingestion code | Derived value | Submitters should not provide these fields in the submission profile |
| Update timestamps should be system-assigned | Ingestion code | Derived value | `update_date` belongs to the canonical record profile |
| Lead entity and contact fields may later be checked against program-level reference tables | Validation code | Error or warning | Reference data is outside this schema repository |
| Project type may determine allowable geometry type | Validation code | Error | For example, restoration areas are expected to be polygonal |
