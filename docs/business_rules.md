# Business Rules

Some HRL restoration data rules are not fully expressible in LinkML and should
be enforced by validation or ingestion code.

| Rule | Likely enforcement location | Error/warning/derived value | Notes |
| --- | --- | --- | --- |
| Construction completion year should not be earlier than construction start year | Validation code | Error | Applies when both years are present |
| Funding gap is calculated from estimated budget and secured funding | Canonical transformation | Derived value | `funding_gap` is canonical-only; legacy submitted values are discrepancies |
| Submitted [`project_id`](reference/project_id.md) must exist in the DWR-managed registry | Pipeline validation | Error | The schema requires a stable string ID but does not own registry access or assignment |
| Missing contact name or email | Pipeline validation | Warning | Prominent warning, not a LinkML required field |
| Budget and secured funding by stage | Pipeline validation | Warning or error | Warnings for concept/feasibility through design; errors for construction and post-construction monitoring and science |
| Construction start and completion years by stage | Pipeline validation | Warning or error | Warnings before construction; errors for construction and post-construction monitoring and science |
| Acreage by project type | Pipeline validation | Error | Required unless project type contains only fish passage improvement and/or fish screen installation or improvement |
| Update timestamps should be system-assigned | Ingestion code | Derived value | [`update_date`](reference/update_date.md) belongs to the canonical record profile |
| Retirement and supersession | Canonical promotion | Explicit approved update | Absence from a later submission never changes `record_status` |
| Lead entity and contact fields may later be checked against program-level reference tables | Validation code | Error or warning | Reference data is outside this schema repository |
| Project type may determine allowable geometry type | Validation code | Error | For example, restoration areas are expected to be polygonal |
