# HRL Restoration Schema

This repository contains the machine-readable schema and controlled
vocabularies for Healthy Rivers and Landscapes (HRL) restoration spatial data
submissions. The schema is created using [LinkML](https://linkml.io).

The maintained source of truth is
`schemas/hrl_restoration_project.yaml`. Generated files should be derived from
that LinkML schema rather than edited directly.

## Schema docs site

To view the schema docs site, visit https://healthy-rivers-and-landscapes-science.github.io/hrl-restoration-schema/.

To see the GitHub repository that hosts the schema, visit https://github.com/Healthy-Rivers-and-Landscapes-Science/hrl-restoration-schema.

## What this repository contains

- LinkML schema for HRL restoration spatial data submissions with inline
  controlled vocabularies/enums.
- Generated artifacts for downstream validation and documentation.
- Documentation for geometry policy, business rules, and validation interfaces.
- Example valid and invalid submissions.

## What this repository does not contain

- Spatial file validation code
- Azure pipeline infrastructure
- API or map application code

## Schema profiles

`RestorationProjectSubmission` describes fields expected from submitting
entities. The HRL program assigns the stable string `project_id` before
submission, and submitters must include that assigned ID on every submitted
record. The pipeline validates the ID against the DWR-managed project-ID
registry and never creates project IDs automatically. Submission-manifest
metadata and other system-assigned canonical fields do not belong in submitted
records.

`RestorationProjectCanonicalRecord` describes standardized records stored after
validation and ingestion. This profile includes program-assigned, derived, and
system-maintained fields, including provenance and lifecycle status.

`RestorationProjectPublicRecord` is the separate public-export contract. It is
produced from approved active canonical records and intentionally excludes
lifecycle, contact, contractor, non-public funding, and canonical provenance
fields.

## Intended workflow

If the schema needs to be updated, the process is:

1. Edit the LinkML schema
2. Lint and validate the schema
3. Regenerate generated artifacts
4. Validate examples
5. Open a pull request
6. Tag a new release

## Namespace

The schema namespace currently uses a GitHub Pages URL:

`https://healthy-rivers-and-landscapes-science.github.io/hrl-restoration-schema/`

The project may later migrate to a persistent identifier such as `w3id.org`,
but it does not use that namespace yet.

## Documentation site

This repository includes `mkdocs.yml` for GitHub Pages publishing. The Pages
workflow generates LinkML schema reference Markdown with `gen-doc`, builds the
MkDocs site, and deploys the static site artifact.

To preview the documentation locally:

```bash
python -m pip install -r requirements.txt
rm -rf docs/reference
gen-doc --no-mergeimports --no-render-imports --truncate-descriptions false \
  --directory docs/reference schemas/hrl_restoration_project.yaml
python scripts/generate_data_dictionary.py \
  --schema schemas/hrl_restoration_project.yaml \
  --output docs/data_dictionary.md
mkdocs serve
```

The generated `docs/reference/` directory and `docs/data_dictionary.md` file are
build artifacts and should not be hand-edited.

## Release and schema sync

When a new release is published in this repository, a GitHub Actions workflow
automatically copies `schemas/hrl_restoration_project.yaml` from the released
tag into `lucy-dwr/dwr-restoration-spatial-data` at
`schemas/hrl_restoration_project.yaml` and opens a pull request there.

The file is copied from the tagged release, not from `main`. If the schema file
is already identical in the target repository, no pull request is created.

The workflow requires a repository secret named `TARGET_REPO_TOKEN`: a
fine-grained personal access token scoped to `lucy-dwr/dwr-restoration-spatial-data`
with Contents (read and write) and Pull requests (read and write) permissions.

### v1.2.0 migration note

`v1.2.0` accepts an optional integer legacy `funding_gap` on submissions while
excluding it from public records. The data pipeline must import the immutable
schema snapshot, recalculate the canonical value from
`estimated_budget - funding_secured` when possible, and issue the documented
warnings for differing or pass-through legacy values. `v1.3.1` also permits a
canonical record to omit `funding_gap` while the underlying financial inputs
are unavailable. No change is expected in `hrl-restoration-map` because
`funding_gap` remains non-public.

### v1.3.0 migration note

`v1.3.0` permits submissions without `project_description` or
`target_species`; a public record still requires a description, while target
species remains optional when a project has no identified species target.
Submission `lead_entity` values may use cataloged organization names,
abbreviations, or aliases, which the data pipeline must resolve to stable
`LeadEntityEnum` IDs before canonicalization. The pipeline must export only
approved active canonical records and must not include `record_status` in the
public record output. Downstream consumers should import the immutable
`v1.3.0` schema snapshot and update their configured schema version before
adopting these contract changes.

## Status

This is an initial draft schema repository.
