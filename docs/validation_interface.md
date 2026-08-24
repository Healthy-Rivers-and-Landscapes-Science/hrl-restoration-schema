# Validation Interface

A future validation repository should consume generated artifacts from this
schema repository rather than duplicating schema logic.

Expected generated artifacts include:

- JSON Schema for submission records
- JSON Schema for canonical records
- JSON Schema for public export records
- Controlled vocabulary JSON/CSV
- Human-readable data dictionary

Validation code should own:

- Reading GeoPackage and zipped shapefile inputs
- Extracting attributes
- Validating attributes against generated schema artifacts
- Validating geometry with geospatial libraries
- Producing validation reports
- Writing standardized outputs
- Applying conditional business rules, project-ID registry checks, and
  conservative deterministic repairs
- Creating JSON and HTML validation reports and stopping successful records at
  an approval candidate until a program lead supplies an `_APPROVE` marker

Proposed validation report fields:

| Field | Description |
| --- | --- |
| `file_name` | Name of the submitted file |
| `schema_version` | Schema version or release used for validation |
| `validation_timestamp` | Timestamp when validation ran |
| `severity` | Error, warning, or info |
| `check_category` | Attribute, vocabulary, geometry, business rule, or system check |
| `feature_identifier` | Feature identifier or row number |
| `field_name` | Field associated with the finding, if applicable |
| `message` | Human-readable validation message |
| `suggested_fix` | Suggested correction, when available |
