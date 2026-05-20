# HRL Restoration Schema

This repository contains the machine-readable schema and controlled
vocabularies for Healthy Rivers and Landscapes (HRL) restoration spatial data
submissions.

The maintained source of truth is
`schemas/hrl_restoration_project.yaml`. Generated files should be derived from
that LinkML schema rather than edited directly.

## Schema docs site

To view the schema docs site, visit https://lucy-dwr.github.io/hrl-restoration-schema/.

To see the GitHub repository that hosts the schema, visit https://github.com/lucy-dwr/hrl-restoration-schema.

## What this repository contains

- LinkML schema for HRL restoration spatial data submissions with inline
  controlled vocabularies/enums.
- Generated artifacts for downstream validation and documentation.
- Documentation for geometry policy, business rules, and validation interfaces.
- Example valid and invalid submissions.

## What this repository does not contain

- Spatial file validation code
- Azure pipeline infrastructure
- PostGIS database migrations
- API or map application code

## Schema profiles

`RestorationProjectSubmission` describes fields expected from submitting
entities. Program-assigned or system-assigned fields, such as `project_id` and
`update_date`, are not required in this profile and should not be supplied by
submitters.

`RestorationProjectCanonicalRecord` describes standardized records stored after
validation and ingestion. This profile includes program-assigned, derived, and
system-maintained fields.

## Intended workflow

If the schema needs to be updated, the process is:

1. Edit the LinkML schema
2. Lint and validate the schema
3. Regenerate generated artifacts
4. Validate examples
5. Open a pull request

## Namespace

The schema namespace currently uses the anticipated GitHub Pages URL:

`https://lucy-dwr.github.io/hrl-restoration-schema/`

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

## Status

This is an initial draft schema repository.
