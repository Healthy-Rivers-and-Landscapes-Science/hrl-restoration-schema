# HRL Restoration Schema

This repository contains the machine-readable schema and controlled
vocabularies for Healthy Rivers and Landscapes (HRL) restoration spatial data
submissions. The schema is created using [LinkML](https://linkml.io).

The maintained source of truth is
`schemas/hrl_restoration_project.yaml`. Generated files should be derived from
that LinkML schema rather than edited directly.

Cross-repository workflow reference:
[`hrl-azure-infrastructure/PIPELINE_INFRA.md`](https://github.com/Healthy-Rivers-and-Landscapes-Science/hrl-azure-infrastructure/blob/main/PIPELINE_INFRA.md).
Roles and ownership:
[`hrl-azure-infrastructure/DIVISION_OF_RESPONSIBILITIES.md`](https://github.com/Healthy-Rivers-and-Landscapes-Science/hrl-azure-infrastructure/blob/main/DIVISION_OF_RESPONSIBILITIES.md).
How to cut a release: [`CONTRIBUTING.md`](CONTRIBUTING.md).

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
record. The pipeline validates the ID against `project-id-registry.csv` in
[`hrl-project-registry`](https://github.com/Healthy-Rivers-and-Landscapes-Science/hrl-project-registry) and
never creates project IDs automatically. Submission-manifest metadata and other
system-assigned canonical fields do not belong in submitted records.

`RestorationProjectCanonicalRecord` describes standardized records stored after
validation and ingestion. This profile includes program-assigned, derived, and
system-maintained fields, including provenance and lifecycle status.

`RestorationProjectPublicRecord` is the separate public-export contract. It is
produced from approved active canonical records and intentionally excludes
lifecycle, contact, contractor, non-public funding, and canonical provenance
fields.

## Intended workflow

If the schema needs to be updated, the outline is:

1. Edit the LinkML schema
2. Lint and validate the schema
3. Regenerate generated artifacts
4. Validate examples
5. Open a pull request
6. Tag a new release, update the changelog, and write a migration note
7. Let the downstream pin catch up (the data pipeline imports the new snapshot)

The full step-by-step, including the downstream coordination, is in
[`CONTRIBUTING.md` &rarr; "Cutting a release"](CONTRIBUTING.md#cutting-a-release).

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

## Provider data-model spreadsheet

External data providers do not use Azure, Git, or a submission website. They
prepare a conforming GeoPackage and email it to HRL. The fill-in spreadsheet
they work from (field names, types, requiredness, and controlled-vocabulary
values for `RestorationProjectSubmission`) is a view of this schema: keep it in
sync with `docs/data_dictionary.md`, which is regenerated from the LinkML
source. Do not maintain an independent field list.

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
warnings for differing or pass-through legacy values. No change is expected in
`hrl-restoration-map` because `funding_gap` remains non-public. (See the v1.3.1
note below for the later relaxation of the canonical requirement.)

### v1.3.1 migration note

`v1.3.1` lets a `RestorationProjectCanonicalRecord` omit `funding_gap` when
`estimated_budget` and `funding_secured` are both unavailable and no legacy
value was supplied. The data pipeline imports the immutable `v1.3.1` snapshot
and no longer treats an absent canonical `funding_gap` as an error in that case.
`funding_gap` stays non-public, so `hrl-restoration-map` is unaffected. This is
the snapshot the pipeline currently pins.

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

In production use. The current release is **v1.3.1**, which the
`hrl-restoration-data-pipeline` pins by immutable commit and checksum and
validates every restoration submission against. Changes are made through pull
requests and tagged releases; see [`CONTRIBUTING.md`](CONTRIBUTING.md).
