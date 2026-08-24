# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

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
