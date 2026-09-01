# Contributing

Schema changes are made through pull requests and tagged releases. This is the
**technical maintainer's** guide; for how this repository fits the wider
workflow and who decides a change is warranted, see
[`hrl-azure-infrastructure/DIVISION_OF_RESPONSIBILITIES.md`](https://github.com/Healthy-Rivers-and-Landscapes-Science/hrl-azure-infrastructure/blob/main/DIVISION_OF_RESPONSIBILITIES.md).

## Ground rules

- Edit the LinkML source, `schemas/hrl_restoration_project.yaml`. **Never edit
  generated files** &mdash; everything in `docs/reference/`, `docs/data_dictionary.md`,
  and `generated/` is derived from the source.
- Keep changes small and reviewable. Treat a controlled-vocabulary change as a
  schema change.
- Update documentation when the meaning of a field changes; add or update
  `examples/` fixtures when validation behaviour changes.
- Do not add validation code, infrastructure, database migrations, API code, or
  map application code to this repository.
- American spellings.

## Local setup

```sh
python -m pip install -r requirements.txt
```

Run what CI runs (`.github/workflows/validate-schema.yaml`):

```sh
linkml-lint --ignore-warnings schemas/hrl_restoration_project.yaml
python scripts/check_schema_contract.py --schema schemas/hrl_restoration_project.yaml
python scripts/validate_fixtures.py --schema schemas/hrl_restoration_project.yaml
```

Regenerate the derived docs and check the site builds:

```sh
rm -rf docs/reference
gen-doc --no-mergeimports --no-render-imports --truncate-descriptions false \
  --directory docs/reference schemas/hrl_restoration_project.yaml
python scripts/generate_data_dictionary.py \
  --schema schemas/hrl_restoration_project.yaml --output docs/data_dictionary.md
mkdocs build --strict
```

Preview locally with `mkdocs serve`.

## Cutting a release

Downstream repositories pin an **immutable, tagged** schema release &mdash; never
`main`. The order matters: release here first, let the pipeline adopt it, and
only then let any producer send data shaped for the new rules
([`PIPELINE_INFRA.md` &rarr; "Cross-repository change discipline"](https://github.com/Healthy-Rivers-and-Landscapes-Science/hrl-azure-infrastructure/blob/main/PIPELINE_INFRA.md#cross-repository-change-discipline)).

1. **Land the schema change** on `main` via a reviewed PR, with `docs/reference/`,
   `docs/data_dictionary.md`, and the `examples/` fixtures regenerated/updated in
   the same PR. CI (lint, contract check, fixtures, MkDocs `--strict`) must pass.
2. **Update `CHANGELOG.md`** &mdash; move `[Unreleased]` items under a new
   `[vX.Y.Z] - YYYY-MM-DD` heading.
3. **Write a migration note** in `README.md`, next to the existing `v1.2.0` /
   `v1.3.0` / `v1.3.1` notes: what changed in the contract, and what each
   downstream consumer must do (or that it is unaffected).
4. **Tag an annotated release.** `git tag -a vX.Y.Z -m "vX.Y.Z"` and push it, then
   create the GitHub release. The tag must be annotated &mdash; the pipeline's
   `import_schema_snapshot.py` resolves it with `git ls-remote --tags ... ^{}`
   and refuses a lightweight tag.
5. **Publishing the release fires two workflows:**
   - `publish-docs.yaml` deploys the docs site to GitHub Pages.
   - `sync-schema-to-spatial-data.yaml` copies the tagged schema file into
     `dwr-restoration-spatial-data` and opens a PR there. This needs the
     `TARGET_REPO_TOKEN` secret (a PAT scoped to that repo). If the sync does
     not appear, check the token has not expired
     ([`hrl-azure-infrastructure/docs/secrets-management.md`](https://github.com/Healthy-Rivers-and-Landscapes-Science/hrl-azure-infrastructure/blob/main/docs/secrets-management.md)).
6. **Adopt the release in the pipeline.** In `hrl-restoration-data-pipeline`, on
   a review branch: `python scripts/import_schema_snapshot.py vX.Y.Z`, update
   `_SNAPSHOT_RELATIVE_PATH` and the `pyproject.toml` `force-include`, adjust
   fixtures, `pytest`, merge. Only after this merge does the new schema take
   effect for submissions.

## Namespace

The schema namespace is the GitHub Pages URL
(`https://healthy-rivers-and-landscapes-science.github.io/hrl-restoration-schema/`).
A move to a persistent identifier such as `w3id.org` is possible later but not
done; do not reference `w3id.org` yet.
