# Schema Overview

This repository uses [LinkML](https://linkml.io) as the source-of-truth schema language. The
maintained schema is [`schemas/hrl_restoration_project.yaml`](https://github.com/lucy-dwr/hrl-restoration-schema/blob/main/schemas/hrl_restoration_project.yaml).

The schema has two main profiles:

- [`RestorationProjectSubmission`](reference/RestorationProjectSubmission.md) describes the attributes expected from
  submitting entities.
- [`RestorationProjectCanonicalRecord`](reference/RestorationProjectCanonicalRecord.md) describes standardized records after
  validation, ingestion, and assignment of program-managed fields.

Generated JSON Schema and other artifacts will be used by validation tools and
downstream systems. Those generated outputs should be reproducible from the
[LinkML](https://linkml.io) source.

Any Excel workbook or other tabular source used to develop the model is
historical reference. It is not the maintained source of truth.
