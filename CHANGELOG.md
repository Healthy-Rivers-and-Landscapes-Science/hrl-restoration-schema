# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [v1.3.0] - 2026-08-27

### Added

- Lead entity catalog metadata for full organization names, abbreviations, and
  accepted aliases, including five additional program lead entities.
- Valid and invalid fixtures for optional descriptions and target species, the
  public description requirement, and exclusion of lifecycle status from public
  records.

### Changed

- Submission records may omit `project_description` and `target_species`.
  Public records still require a project description, while target species is
  optional when a project has no identified species target.
- Submission `lead_entity` values may use a cataloged full name, abbreviation,
  or alias. The validation pipeline must resolve them to stable
  `LeadEntityEnum` identifiers before canonicalization.
- Public exports contain approved active canonical records only and no longer
  expose `record_status`.
- Acreage is a warning before construction and an error at construction and
  post-construction monitoring for area-based project types, with the existing
  fish passage- and fish screen-only exemption.

## [v1.2.0] - 2026-08-24

### Added

- Optional integer `funding_gap` compatibility input on
  `RestorationProjectSubmission` for legacy submissions.
- Valid and invalid fixtures for numeric legacy submission values, non-numeric
  values, canonical requiredness, and public-record exclusion.

### Changed

- Documented that canonical `funding_gap` normally equals `estimated_budget -
  funding_secured`; a supplied legacy value is non-authoritative when the
  inputs are available, and may be passed through only when they are
  insufficient, with warnings in either applicable case.
- Documented the `hrl-restoration-data-pipeline` migration to the immutable
  `v1.2.0` schema snapshot and configured schema version. The
  `hrl-restoration-map` is unaffected because `funding_gap` remains
  non-public.

## [v1.1.1] - 2026-08-24

### Fixed

- Corrected submission-profile documentation to clarify that `project_id` is
  program-assigned before submission, required on every submitted record,
  validated against the DWR-managed project-ID registry, and never generated
  automatically by the pipeline.

## [v1.1.0] - 2026-08-24

### Added

- Stable, submitted string `project_id` behavior: every submission supplies
  its pre-assigned identifier, which the downstream data pipeline checks
  against the program registry.
- Expanded canonical provenance and lifecycle fields, including source,
  submission, date, funding-gap, and record-status information.
- A separate public-record contract that excludes private contact, contractor,
  non-public funding, and canonical provenance fields.
- Executable valid and invalid fixtures covering the three record profiles.

### Changed

- Prepared the schema contract on `main` for the `v1.1.0` release; no tag or
  GitHub release has been created.
