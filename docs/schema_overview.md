# Schema Overview

This repository uses LinkML as the source-of-truth schema language. The
maintained schema is `schemas/hrl_restoration_project.yaml`.

The schema has two main profiles:

- `RestorationProjectSubmission` describes the attributes expected from
  submitting entities.
- `RestorationProjectCanonicalRecord` describes standardized records after
  validation, ingestion, and assignment of program-managed fields.

Generated JSON Schema and other artifacts will be used by validation tools and
downstream systems. Those generated outputs should be reproducible from the
LinkML source.

Any Excel workbook or other tabular source used to develop the model is
historical reference. It is not the maintained source of truth.
