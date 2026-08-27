# Schema Overview

This repository uses [LinkML](https://linkml.io) as the source-of-truth schema language. The
maintained schema is [`schemas/hrl_restoration_project.yaml`](https://github.com/Healthy-Rivers-and-Landscapes-Science/hrl-restoration-schema/blob/main/schemas/hrl_restoration_project.yaml).

The schema has three record profiles:

- [`RestorationProjectSubmission`](reference/RestorationProjectSubmission.md) describes the attributes expected from
  submitting entities.
- [`RestorationProjectCanonicalRecord`](reference/RestorationProjectCanonicalRecord.md) describes standardized records after
  validation, ingestion, and assignment of program-managed fields.
- [`RestorationProjectPublicRecord`](reference/RestorationProjectPublicRecord.md) defines the deliberately restricted public-export
  contract produced from approved canonical records.

Every submission record includes a program-assigned, stable string
[`project_id`](reference/project_id.md). The data pipeline checks that ID against
the DWR-managed registry; registry assignment is not a LinkML function.

`lead_entity` supports joint responsibility. Submissions may provide one or
more cataloged organization names, abbreviations, or aliases (for example,
`Yuba Water Agency` or `YWA`). During validation, the pipeline resolves each
value through the program-level lead-entity catalog. Canonical and public
records retain the resulting stable IDs (for example, `yuba_water_agency`),
not the submitted display text.

The catalog metadata is carried with `LeadEntityEnum`: each permissible ID has
its full name and, where applicable, abbreviation and accepted aliases. The
separate lead-entity catalog example is a readable representation of the same
set of entities.

Generated JSON Schema and other artifacts will be used by validation tools and
downstream systems. Those generated outputs should be reproducible from the
[LinkML](https://linkml.io) source.

Any Excel workbook or other tabular source used to develop the model is
historical reference. It is not the maintained source of truth.
