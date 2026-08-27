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
| Acreage by project type and stage | Pipeline validation | Warning or error | Warning before construction; error at construction and post-construction unless project type contains only fish passage improvement and/or fish screen installation or improvement |
| Update timestamps should be system-assigned | Ingestion code | Derived value | [`update_date`](reference/update_date.md) belongs to the canonical record profile |
| Retirement and supersession | Canonical promotion | Explicit approved update | Absence from a later submission never changes `record_status` |
| Submitted lead-entity names and aliases | Pipeline validation | Error | Resolve every value against the catalog metadata in `LeadEntityEnum`; reject unknown or ambiguous values and write stable IDs to canonical records |
| Public lifecycle filtering | Public-export transformation | Derived filter | Export only canonical records with `record_status = active`; do not expose lifecycle status in public records |
| Project type may determine allowable geometry type | Validation code | Error | For example, restoration areas are expected to be polygonal |
