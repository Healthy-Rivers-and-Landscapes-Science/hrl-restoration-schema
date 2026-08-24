# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Initial LinkML schema for HRL restoration spatial data submissions.
- Initial repository documentation structure.
- Placeholder directories for generated artifacts and examples.

### Changed

- Made `project_id` a required stable string field for submission, canonical,
  and public records.
- Added multi-valued controlled `lead_entity`, canonical provenance and
  lifecycle fields, `RecordStatusEnum`, and `RestorationProjectPublicRecord`.
- Restricted derived `funding_gap` to canonical records and documented
  pipeline-owned conditional validation and publication approval rules.
