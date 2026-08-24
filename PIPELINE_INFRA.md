# HRL Data Pipeline — Cross-Repository Agent Instructions

## Purpose

These instructions define the shared architecture, repository boundaries, data contracts, and development rules for the Healthy Rivers and Landscapes (HRL) Azure data pipeline and its first public application, the HRL restoration map.

This file has been copied into each relevant repository so that an agent working in any one repository understands the whole system and knows both what belongs there and what does not.

The architecture is intentionally **general at the Azure infrastructure level** so that future HRL scientific data pipelines can use the same patterns. The **restoration-project pipeline is the first implemented data workflow**, and the **HRL restoration map is the first downstream public application**.

---

## Relevant Repositories

### 1. `hrl-restoration-schema`
**Role:** Authoritative data standard

**Code:** https://github.com/lucy-dwr/hrl-restoration-schema

Owns:

- The HRL restoration LinkML schema
- Controlled vocabularies and enums that are part of the data standard
- `RestorationProjectSubmission`
- `RestorationProjectCanonicalRecord`
- `RestorationProjectPublicRecord`
- Valid and invalid examples
- Schema documentation
- Tagged schema releases

Does **not** own:

- Azure infrastructure
- Submission ingestion
- Spatial file handling
- Production data
- Public map code
- Pipeline orchestration

The LinkML schema in this repository is the source of truth. Downstream repositories must consume a **released schema version**, not independently maintain a divergent copy.

---

## Funding-Gap Compatibility Contract

This contract affects the following repositories:

- `hrl-restoration-schema` defines the optional legacy submission field and
  retains the required canonical field.
- `hrl-restoration-data-pipeline` must implement the calculation, precedence,
  pass-through, and warning behavior below after importing the released
  immutable schema snapshot.
- `hrl-restoration-map` is not expected to change because `funding_gap`
  remains non-public and is excluded from `RestorationProjectPublicRecord`.

`funding_gap` is a calculated canonical field, normally derived as:

```text
estimated_budget - funding_secured
```

A submission may optionally include a numeric legacy `funding_gap` value. The
pipeline must treat it as compatibility input rather than as an authoritative
calculation:

1. When both source budget fields are present, recalculate `funding_gap` from
   them. If a supplied legacy value differs, retain the recalculated value and
   issue a prominent warning.
2. When the source budget fields are insufficient to calculate the value, a
   numeric supplied legacy `funding_gap` may be passed through into the
   canonical record with a prominent warning.
3. A canonical record still requires `funding_gap`; the pipeline must report
   an error if it can neither calculate nor validly pass through a numeric
   value.

`funding_gap` must never be included in `RestorationProjectPublicRecord` or a
public export.

---

### 2. `hrl-restoration-data-pipeline`
**Role:** Restoration data-specific ingestion, validation, repair, standardization, merging, reporting, and publication code

This is the primary executable data processing repository.

Owns:

- Python pipeline code
- GeoPackage, GeoJSON, and zipped shapefile ingestion
- Spatial validation
- LinkML validation
- Business rule validation
- Conservative automatic repairs
- Canonical data transformation
- Project ID registry validation
- Merge/upsert logic for the master canonical restoration dataset
- Public data transformation
- HTML and JSON quality reports
- Reference layer acquisition and transformation
- Publication candidate generation
- Publication promotion logic
- Dockerfile and runtime dependencies
- Automated tests

Does **not** own:

- Azure resource definitions
- The authoritative LinkML schema
- Public application UI code
- Production data files in Git

---

### 3. `hrl-azure-infrastructure`
**Role:** Terraform definitions for Azure infrastructure

Owns:

- ADLS Gen2 / Blob Storage
- Storage containers and paths
- Storage Queue resources
- Event Grid subscriptions
- Azure Container Registry
- Azure Container Apps Environment
- Azure Container Apps Jobs
- Managed identities and role assignments
- Log Analytics and diagnostics
- Azure Static Web Apps
- Azure Front Door
- Public data routing
- Terraform state configuration
- Environment-specific infrastructure configuration

Does **not** own:

- Python validation logic
- Schema definitions
- Data repair rules
- Public map application logic

The infrastructure should remain general enough to support future HRL data pipelines beyond restoration projects.

---

### 4. `hrl-restoration-map`
**Role:** Public visualization and download application

**Code:** https://github.com/lucy-dwr/hrl-restoration-map

Owns:

- React/Vite frontend
- MapLibre/deck.gl visualization
- Public data loading
- Filters, search, map interaction, accessibility, downloads, and display logic
- Public application tests
- Data contract compatibility tests

Does **not** own:

- Production restoration data validation
- LinkML schema authority
- Production data transformation
- Production ingestion
- Production merge/upsert logic
- Production reference layer acquisition

During migration, legacy conversion scripts or checked-in generated datasets may remain temporarily, but the end state is that this application consumes approved Azure-hosted public artifacts.

---

## Supporting / Producer Repositories

Repositories such as:

- `dwr-restoration-spatial-data`
- `misc-restoration-spatial-data`

may prepare or test source datasets, but they are **not runtime dependencies** of the Azure pipeline.

They may produce files that a program lead later uploads to Azure, but Azure ingestion must work regardless of which local repository, GIS project, agency, consultant, or other process produced the submission.

---

# System Architecture

## Submission Pipeline

```text
Authorized program lead
        |
        | uploads via Azure Portal
        v
ADLS Gen2: raw-submissions/
        |
        | upload submission files
        | upload _READY last
        v
Azure Event Grid
        |
        v
Azure Storage Queue
        |
        v
Azure Container Apps Job
        |
        |-- read spatial package
        |-- validate package
        |-- validate geometry
        |-- validate against current LinkML release
        |-- validate business rules
        |-- apply conservative deterministic repairs
        |-- create HTML + JSON report
        |-- create canonical candidate data
        |-- create public candidate data
        |
        +------------------------------+
        |                              |
      FAIL                           PASS
        |                              |
        v                              v
validation-reports/           publication-candidates/
status = NEEDS_CORRECTION     status = AWAITING_APPROVAL
                                       |
                                       | human review in Azure Portal
                                       | upload _APPROVE
                                       v
                               publication promotion job
                                       |
                                       | merge/upsert into master
                                       | canonical dataset
                                       | build public snapshot
                                       v
                              standardized/
                              public-exports/
                                       |
                                       v
                               Azure Front Door
                                       |
                                       v
                              downstream public apps
```

Validation and publication are deliberately separate stages.

A dataset that passes validation must **not automatically replace public production data**.

---

# Human Publication Gate

A passing submission becomes a **publication candidate**.

The pipeline must:

1. Write the validation report as both JSON and HTML
2. Write the normalized canonical candidate
3. Write the derived public candidate
4. Set submission status to `AWAITING_APPROVAL`
5. Stop

An authorized program lead reviews the candidate through the Azure Portal.

The reviewer should be able to inspect or download:

- `validation-report.html`
- `validation-report.json`
- canonical candidate output
- public candidate output
- submission metadata
- recorded automatic repairs
- all warnings

Warnings must be **prominent**, not buried. A publishable report with warnings must clearly say that the submission passed **with warnings**.

To advance the candidate, the reviewer uploads an empty marker file named:

```text
_APPROVE
```

to the candidate directory.

Event Grid detects `_APPROVE` and initiates the publication/promotion step.

No custom approval web application is required.

A candidate that is never approved remains unpublished.

---

# Submission Upload Contract

Program leads upload submissions through the Azure Portal.

Each submission should have its own directory.

Example:

```text
raw-submissions/
  dwr/
    2026-08-21_dwr_restoration-projects_v001/
      submission.json
      restoration-projects.gpkg
      _READY
```

Supported spatial inputs:

- `.gpkg`
- `.geojson`
- `.zip` containing a complete shapefile package

Do not require users to upload individual shapefile component files separately. Shapefile submissions must be zipped.

`_READY` is always uploaded last.

The ingestion Event Grid rule must react to `_READY`, not every individual data file.

---

## `submission.json`

The submission manifest records **submission-level provenance and processing context** that cannot be reliably derived from the spatial dataset itself. Keep the manifest intentionally small. Dataset attributes and metadata governed by the LinkML schema belong in the dataset, not in this file.

### Required fields

A submission manifest should include:

```json
{
  "submission_id": "2026-08-24_dwr_restoration-projects_v001",
  "organization": "California Department of Water Resources",
  "organization_code": "DWR",
  "dataset_name": "HRL Restoration Projects",
  "submission_type": "update",
  "submission_scope": "complete_organization_snapshot",
  "data_as_of": "2026-08-20",
  "primary_file": "restoration-projects.gpkg"
}
```

Required fields have the following meanings:

| Field | Purpose |
| --- | --- |
| `submission_id` | Stable identifier tying together the raw submission, validation reports, publication candidate, logs, and publication history. |
| `organization` | Human-readable name of the organization supplying the data. |
| `organization_code` | Short, stable organization identifier suitable for storage paths and machine processing, such as `DWR` or `CDFW`. |
| `dataset_name` | Human-readable name of the submitted dataset. |
| `submission_type` | Identifies whether the submission is a routine `update` or a `correction` to a previous submission. |
| `submission_scope` | Indicates whether the submission is a `complete_organization_snapshot` or a `partial_update`. |
| `data_as_of` | Date through which the submitter considers the data current. This is distinct from the upload or processing date. |
| `primary_file` | Name of the spatial file or archive the pipeline should process. |

### Submission types

Initially support:

```text
update
correction
```

An `update` contains new or updated records to be merged/upserted into the canonical dataset.

A `correction` revises a previous submission. When `submission_type` is `correction`, `supersedes_submission_id` must also be supplied.

### Submission scope

Initially support:

```text
complete_organization_snapshot
partial_update
```

A `complete_organization_snapshot` indicates that the submission represents the organization's complete applicable dataset as of `data_as_of`.

A `partial_update` contains only records being added or changed.

Submission scope provides important provenance but **does not change the default deletion rule**: absence of a record from a later submission must never be interpreted as deletion or retirement. Deletion or retirement requires an explicit future mechanism.

### Optional fields

Optional submission-level provenance may include:

```json
{
  "supersedes_submission_id": "2026-08-21_dwr_restoration-projects_v001",
  "submitted_by": {
    "name": "Jane Smith",
    "email": "jane.smith@water.ca.gov"
  },
  "notes": "Quarterly project status update.",
  "known_limitations": [
    "Two project boundaries are still under review."
  ]
}
```

`supersedes_submission_id` is required for a `correction` and otherwise optional.

`submitted_by`, `notes`, and `known_limitations` should remain optional. Do not require users to manually supply information that Azure or the pipeline can reliably determine automatically.

### Derived metadata

Do **not** require the uploader to provide metadata that the system can reliably derive, including:

- upload or processing timestamp
- file format
- CRS
- geometry type
- feature count
- expected fields
- validation status
- pipeline version
- schema version

The system validates each submission against the **current approved production schema release**. Uploaders do not select a schema version.

The validation report and downstream provenance metadata must record at minimum:

- schema name
- schema version
- pipeline version
- validation timestamp
- submission ID

As a general rule:

> **If the system can reliably determine a metadata value, derive and record it automatically rather than requiring the uploader to enter it.**
---

# Raw Data Is Immutable

Never overwrite or mutate a submitted source file.

The raw submission is the provenance record.

If a submitter needs to make corrections, create a new submission version.

Example:

```text
2026-08-21_dwr_restoration-projects_v001/
2026-08-22_dwr_restoration-projects_v002/
```

Automatic repairs must be applied to a working/candidate representation, never silently written back into the raw submission.

---

# Storage Model

The Azure data layer should distinguish at least these logical areas:

```text
raw-submissions/
standardized/
validation-reports/
publication-candidates/
schema-snapshots/
public-exports/
```

The infrastructure may implement these as containers or appropriately isolated paths, but security and lifecycle boundaries should remain clear.

---

## Raw Submissions

```text
raw-submissions/
```

Contains original uploaded files and manifests.

Properties:

- Private
- Immutable by pipeline convention
- Retained for provenance
- Never served to public applications

---

## Validation Reports

```text
validation-reports/
```

Contains:

- `validation-report.json`
- `validation-report.html`
- `validation-report.pdf`
- status metadata
- pipeline version
- schema version
- warnings
- errors
- repairs

JSON is the authoritative machine-readable report.

HTML and PDF are the human-readable representations.

---

## Publication Candidates

```text
publication-candidates/
```

Contains outputs that passed validation but have not yet been approved.

Example:

```text
publication-candidates/
  restoration-projects/
    <submission-id>/
      canonical.geojson
      public.geojson
      validation-report.json
      validation-report.html
      status.json
      _APPROVE
```

The `_APPROVE` marker is absent until a program lead approves promotion.

---

## Standardized Data

```text
standardized/
```

Contains the internal canonical HRL dataset.

This may contain fields not intended for public applications.

For restoration projects, this is the merged/upserted canonical master dataset conforming to `RestorationProjectCanonicalRecord`.

---

## Public Exports

```text
public-exports/
```

Contains approved, privacy-filtered, application-ready data.

Public exports must exclude fields that are not approved for public release, including internal or contact fields where applicable.

The public export is derived from canonical standardized data. Canonical and public data are not the same thing.

For restoration projects, the public export conforms to
`RestorationProjectPublicRecord`. It excludes contacts, contractors, funding
secured, funding gap, all comment fields, and canonical provenance fields.
Funding sources remain public.

---

# Validation Model

Validation should be staged.

## 1. Package Validation

Examples:

- unreadable file
- missing shapefile components
- unsupported format
- multiple ambiguous primary layers
- corrupt archive

Package failures are errors.

---

## 2. Spatial Validation

Examples:

- missing CRS
- invalid geometry
- unexpected geometry type
- empty geometry
- geometry outside allowed geographic extent, if such a rule is adopted
- reprojection requirements

Safe reprojection may be automatic.

Ambiguous spatial problems must fail.

---

## 3. LinkML Schema Validation

Validate against the **current production release** of the HRL restoration schema.

Use native LinkML tooling from Python.

Do not independently reproduce the LinkML schema as a second manually maintained validation system.

---

## 4. Controlled Vocabulary Validation

Controlled vocabularies come from the schema release.

Unknown or invalid values must be handled according to the repair rules below.

---

## 5. Business Rule Validation

Examples may include:

- invalid combinations of fields
- impossible numeric values
- inconsistent project state
- invalid date relationships
- missing program-required values that cannot be expressed directly in LinkML

Business rules belong in the pipeline repository unless they are genuinely part of the reusable schema standard.

For restoration projects, each submitted record must be a complete record, not
a field-level patch. Each submitted `project_id` is a stable, program-assigned
string and must exist in the central DWR-managed project ID registry. A new
project must be registered and
assigned an ID through the program's intake process before it can pass
validation; the ingestion job must not create IDs automatically.

The schema identifies the fields required on every project record. The
pipeline applies stage-dependent rules: missing contact details are warnings;
budget, secured funding, and construction years may be absent with warnings
through design, but are errors at construction and post-construction stages.
Total acreage is required except for projects that are exclusively fish passage
and/or fish screen work.

---

# Error, Warning, and Repair Semantics

The pipeline must distinguish:

## Error

An issue that prevents publication.

Examples:

- required field missing
- ambiguous controlled vocabulary value
- invalid required geometry
- incompatible field type

Result:

```text
NEEDS_CORRECTION
```

No candidate may be approved or published.

---

## Warning

An issue that does not prevent publication but must be prominent in the report.

Examples:

- potentially unusual but valid value
- non-critical metadata issue
- accepted geometry repair
- value that merits human attention

Warnings may proceed to `AWAITING_APPROVAL`.

Warnings must be visually obvious in the HTML and PDF reports and clearly counted in status metadata.

---

## Automatic Repair

Automatic repairs must be:

- deterministic
- conservative
- semantics-preserving
- fully recorded
- reproducible

Examples:

- trim whitespace
- normalize casing where the standard defines case insensitivity
- replace a known controlled vocabulary alias with the canonical value
- normalize date formatting
- reproject geometry to the required CRS
- repair geometry only where the repair is deterministic and does not materially alter meaning

Never guess an ambiguous value.

Never silently repair data.

Each repair record should include:

- feature or record identifier
- field or geometry affected
- original value
- repaired value
- repair rule
- pipeline version

---

# Canonical Master Dataset and Merge/Upsert Behavior

Passing submissions do not replace the entire restoration dataset.

They are merged/upserted into a canonical master dataset using stable `project_id` values.

The canonical record must preserve record-level provenance for the most recent
approved source, including the source project identifier, organization code,
submission ID, and source data-as-of date. The canonical model must also have
an explicit record status field so retirement or supersession is intentional,
never inferred from a record being absent from a later submission.

Conceptually:

```text
current canonical master
        +
approved submission candidate
        |
        v
deterministic merge/upsert
        |
        v
new canonical master snapshot
```

The pipeline must define explicit behavior for:

- new `project_id`
- existing `project_id`
- unchanged record
- changed record
- records absent from a later agency submission
- deliberate deletion or retirement
- conflicting submissions
- duplicate IDs
- invalid attempts to change program-assigned identifiers

Do **not** infer deletion merely because a record is absent from a later submission.

If record deletion/retirement is needed, represent that intentionally through an explicit field or future workflow.

The merge must be deterministic and testable.

---

# Publication Model

Publication must use immutable snapshots.

Do not repeatedly overwrite a single production GeoJSON as the only source of truth.

Example:

```text
public-exports/
  restoration-projects/
    2026-08-21T153422Z/
      projects.geojson
      projects.gpkg
      projects.csv
      metadata.json

    current.json
```

`current.json` points to the approved current snapshot.

Example:

```json
{
  "version": "2026-08-21T153422Z",
  "geojson": "2026-08-21T153422Z/projects.geojson",
  "gpkg": "2026-08-21T153422Z/projects.gpkg",
  "csv": "2026-08-21T153422Z/projects.csv",
  "schema_version": "1.1.0",
  "pipeline_version": "1.4.2"
}
```

Versioned artifacts should be effectively immutable.

`current.json` is the promotion pointer.

Rollback should be possible by repointing `current.json` to a previously approved snapshot.

---

# Public Application Contract

The HRL restoration map should eventually fetch:

```text
current.json
```

then fetch the versioned GeoJSON referenced by that manifest.

The application must not know how raw submissions are validated or merged.

The frontend's contract is:

> consume already-approved public artifacts.

Production application code should not depend on a checked-in production GeoJSON once migration is complete.

Small test fixtures may remain in Git for automated tests.

---

# Reference / Context Data Pipeline

Reference layers are not submission data.

Examples include:

- watershed boundaries
- Delta boundary
- bypass boundaries
- stream network
- future authoritative context layers

They follow a separate workflow:

```text
authoritative external source
        |
        v
retrieve
        |
        v
validate source response
        |
        v
transform / clip / dissolve / simplify
        |
        v
validate output
        |
        v
versioned publication candidate
        |
        v
publish successful snapshot
```

These workflows should live in `hrl-restoration-data-pipeline`, under a clearly separate reference-data module.

They may use the same container image but different entry points.

---

## Reference Layer Execution

Initially, reference layer jobs should be **manually triggered** Container Apps Jobs.

Add schedules later only when source update frequency and operational value justify them.

Different reference layers may eventually use different schedules.

---

## Reference Layer Failure Rule

A failed reference-layer refresh must never damage the currently published layer.

On failure:

- record the failure
- log diagnostic information
- leave the current production pointer unchanged
- do not overwrite the last successful artifact

Only a successfully processed and validated new snapshot may replace the current pointer.

---

## Reference Layer Versioning

Version reference layers too.

Example:

```text
public-exports/
  reference/
    watersheds/
      2026-08-21/
        watersheds.geojson
        metadata.json

    streams/
      nhdplus-v2-build-2026-08/
        streams.pmtiles
        metadata.json
```

For every published reference layer, preserve provenance metadata such as:

- authoritative source
- retrieval time
- source version if known
- source endpoint or dataset identifier
- pipeline version
- transformations applied
- relevant spatial parameters
- output checksum if useful

---

# Stream-Network Processing

The stream network may require tools such as `tippecanoe`.

Do not reimplement specialized tooling in Python merely to avoid a subprocess.

The pipeline container may include:

- Python
- GDAL / PROJ
- GeoPandas
- Shapely
- Pyogrio
- LinkML
- Azure SDK packages
- `tippecanoe`
- other justified geospatial CLI dependencies

Python remains the orchestration and application language.

---

# Schema Release Contract

`hrl-restoration-schema` owns schema releases.

The production pipeline must validate against the current approved production schema release.

The pipeline must record:

- schema name
- schema version
- pipeline version
- validation time

The validator must not dynamically use whatever happens to be on the schema repository's `main` branch.

Use a tagged release or otherwise immutable released artifact.

A schema update and a pipeline update are separate versioned changes and must remain independently traceable.

For the `v1.2.0` funding-gap compatibility release, the pipeline must import
the immutable `v1.2.0` schema snapshot, update its configured schema version,
and add tests for recalculation/discrepancy warnings and legacy pass-through
warnings. No `hrl-restoration-map` schema-version or UI change is expected,
because the public-record contract continues to exclude `funding_gap`.

---

# Container and Release Contract

`hrl-restoration-data-pipeline` builds the production container image.

GitHub Actions in that repository should:

1. install dependencies
2. run formatting/linting as adopted
3. run unit tests
4. run integration tests
5. run representative valid/invalid spatial fixtures
6. build the Docker image
7. tag the image with an immutable version or commit identifier
8. push the image to Azure Container Registry

Production must not depend on a mutable `latest` tag.

Terraform remains authoritative for which image version production executes.

A merge to the pipeline repository should not silently switch the production Container Apps Job to a newly built image.

---

# Azure Infrastructure Responsibilities

The `hrl-azure-infrastructure` repository should implement the shared runtime.

Expected production infrastructure includes:

```text
rg-hrl-data-prod-wus3
  ADLS Gen2 / Blob Storage

rg-hrl-pipelines-prod-wus3
  Azure Container Registry
  Container Apps Environment
  submission processing job
  publication promotion job
  reference-layer job(s)
  Storage Queue
  Event Grid subscriptions
  managed identity
  diagnostics

rg-hrl-apps-prod-wus3
  Azure Static Web Apps
  Azure Front Door
```

Exact resource grouping should remain aligned with the existing Terraform architecture.

Use managed identities and Azure RBAC rather than embedded secrets wherever supported.

Do not put credentials, storage keys, SAS tokens, Terraform state, or real `.tfvars` files in Git.

---

# Identity and Upload Model

Do not build custom uploader identity management at this stage.

Authorized program leads already have Azure access.

Uploads are performed directly through the Azure Portal.

The Azure access model should rely on existing Azure RBAC and program-controlled contributor/data roles.

Do not create:

- custom upload web application
- custom user database
- custom login flow
- upload API solely for this workflow
- email notification system

unless requirements later change.

---

# Status Model

Use explicit status values.

Recommended states:

```text
UPLOADING
READY
VALIDATING
NEEDS_CORRECTION
AWAITING_APPROVAL
APPROVED
PUBLISHING
PUBLISHED
FAILED
```

Reference workflows may use a simpler analogous status model.

Status transitions should be deterministic and recorded.

---

# Observability

Every job execution should log enough information to diagnose failures without inspecting source code.

Include at minimum:

- submission ID
- job/execution ID
- pipeline version
- schema version where applicable
- input path
- output path
- validation status
- error counts
- warning counts
- repair counts
- exception details
- publication snapshot version

Do not log sensitive submission contents unnecessarily.

---

# Testing Requirements

## Schema Repository

Test:

- schema validity
- generated artifacts
- valid examples
- invalid examples
- controlled vocabularies
- release reproducibility

---

## Pipeline Repository

Test:

- GPKG ingestion
- GeoJSON ingestion
- zipped shapefile ingestion
- corrupt package behavior
- CRS handling
- invalid geometry
- LinkML validation
- controlled vocabulary repair
- ambiguous vocabulary failure
- warning behavior
- canonical transformation
- public-field removal
- deterministic merge/upsert
- duplicate IDs
- publication candidate generation
- approval promotion
- snapshot generation
- rollback-safe pointer updates
- reference API failure
- malformed reference responses
- reference publication safety

Use small test fixtures committed to Git. Do not commit production datasets.

---

## Infrastructure Repository

Test:

- `terraform fmt`
- `terraform validate`
- plans in appropriate CI contexts
- Event Grid filters
- queue configuration
- Container Apps Job configuration
- managed identity role assignments
- storage access boundaries
- Front Door routing

Do not apply production infrastructure automatically from unreviewed pull requests.

---

## Map Repository

Test:

- `current.json` parsing
- versioned GeoJSON loading
- failure handling
- backward-compatible data contracts
- downloads
- expected fields
- accessibility
- deployment path behavior

The frontend should fail visibly and safely if a published manifest is malformed or unavailable.

---

# Cross-Repository Change Rules

Agents must consider whether a change modifies a contract consumed by another repository.

Examples:

### Schema field changes

May require changes in:

- pipeline validation
- canonical transformation
- public export logic
- map display logic
- test fixtures

---

### Public manifest changes

May require changes in:

- pipeline publisher
- map data loader
- infrastructure routing/caching
- tests

---

### Storage path changes

May require changes in:

- Terraform
- pipeline storage client
- documentation
- Event Grid filters

---

### Container command changes

May require changes in:

- pipeline repo
- Terraform Container Apps Job definitions

---

Before implementing a cross-repository contract change, identify all affected repositories and keep the contract explicit.

---

# Migration From Current Map-Bundled Data Processing

The existing restoration map currently includes data conversion and reference layer scripts.

Migrate production responsibilities gradually.

End state:

```text
hrl-restoration-map
  renders data

hrl-restoration-data-pipeline
  produces data
```

Do not delete legacy scripts until equivalent pipeline behavior is tested and the Azure-hosted path is proven.

During migration, keep clear documentation of which path is authoritative.

---

# Development Order

Recommended implementation sequence:

## Phase 1 — Schema Contract

1. Confirm the current LinkML release.
2. Confirm canonical record structure.
3. Confirm stable `project_id` behavior.
4. Add or improve valid and invalid fixtures.
5. Tag a production schema release.

---

## Phase 2 — Local Pipeline

1. Create `hrl-restoration-data-pipeline`.
2. Implement local file ingestion.
3. Implement staged validation.
4. Implement conservative repair rules.
5. Generate JSON and HTML reports.
6. Generate canonical candidate output.
7. Generate public candidate output.
8. Implement deterministic merge/upsert logic.
9. Implement immutable snapshot publication locally.
10. Add tests.

Do not begin with Azure orchestration. First make the pipeline deterministic and testable locally.

---

## Phase 3 — Containerization

1. Create Dockerfile.
2. Include geospatial system dependencies.
3. Include LinkML tooling.
4. Include `tippecanoe` if required.
5. Run the full test suite in the container.
6. Build and push immutable image tags to ACR.

---

## Phase 4 — Azure Pipeline Infrastructure

Implement `infra/environments/prod/pipelines`.

Provision:

- ACR
- Container Apps Environment
- Storage Queue
- Event Grid filters
- submission job
- approval/promotion job
- managed identity
- RBAC
- diagnostics

Wire `_READY` to validation.

Wire `_APPROVE` to publication promotion.

---

## Phase 5 — Azure Data Flow

Prove:

```text
Portal upload
  -> _READY
  -> validation
  -> report
  -> AWAITING_APPROVAL
  -> human review
  -> _APPROVE
  -> merge/upsert
  -> public snapshot
  -> current.json
```

Test both passing and failing submissions.

Test publication with warnings.

Test that failed publication leaves the previous public version intact.

---

## Phase 6 — Reference Layers

Move or reimplement production reference layer generation in the pipeline repository.

Start with:

- watersheds
- Delta boundary
- bypass boundaries
- stream network

Use manually triggered jobs initially.

Preserve source metadata and immutable snapshots.

---

## Phase 7 — Map Migration

Modify `hrl-restoration-map` to consume Azure-hosted manifests and versioned public artifacts.

Retain local test fixtures.

Remove production dependence on checked-in generated restoration data only after the Azure path is verified.

---

# General Rules

1. Keep repository boundaries strict.
2. Prefer explicit data contracts over implicit coupling.
3. Preserve raw data and provenance.
4. Never silently repair data.
5. Never publish a failed validation.
6. Make warnings prominent.
7. Never let a failed refresh replace a known-good public artifact.
8. Use immutable snapshots and mutable pointers/manifests.
9. Keep schema and pipeline versions independently traceable.
10. Do not use mutable container tags in production.
11. Do not introduce a database unless a concrete requirement justifies it.
12. Do not introduce Data Factory, Databricks, AKS, Service Bus, or other heavier services without a specific need.
13. Prefer the simplest PaaS component that satisfies the requirement.
14. Do not build custom identity or upload UI unless requirements change.
15. Keep Azure infrastructure generic enough to support future HRL pipelines.
16. Keep restoration-specific business logic out of generic Terraform modules.
17. Do not commit production data or secrets to Git.
18. Make local pipeline behavior testable without Azure.
19. Treat public data transformation as a deliberate release step, not an incidental file conversion.
20. When uncertain about a cross-repository contract, document the decision before coding around it.

---

# Target End State

```text
hrl-restoration-schema
        |
        | released LinkML schema
        v
hrl-restoration-data-pipeline
        |
        | tested immutable container image
        v
hrl-azure-infrastructure
        |
        | runs validation / approval / publication
        v
ADLS + versioned public exports
        |
        v
Azure Front Door
        |
        v
hrl-restoration-map
```

The architectural principle is:

> **GitHub governs schemas, code, and infrastructure. Azure receives and preserves data, executes released pipeline code, records validation and provenance, and publishes approved immutable data products. Public applications consume only approved published artifacts.**
