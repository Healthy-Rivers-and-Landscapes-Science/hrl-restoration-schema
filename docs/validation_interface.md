# Validation interface

The validation implementation is
[`hrl-restoration-data-pipeline`](https://github.com/Healthy-Rivers-and-Landscapes-Science/hrl-restoration-data-pipeline).
It consumes this repository's released artifacts; it does not duplicate schema
logic. This page describes the boundary between the two.

## What the pipeline consumes from here

The pipeline pins one **immutable, tagged** release of
`schemas/hrl_restoration_project.yaml` (currently `v1.3.1`), stored by commit and
checksum. From it, using `linkml-runtime`, it derives:

- the induced slots and requiredness of each profile
  (`RestorationProjectSubmission`, `RestorationProjectCanonicalRecord`,
  `RestorationProjectPublicRecord`);
- the controlled-vocabulary (enum) values;
- the multivalued slots;
- the lead-entity catalog (full names, abbreviations, aliases).

It never follows `main`. Adopting a new release is an explicit, reviewed step
(see [`CONTRIBUTING.md` &rarr; "Cutting a release"](https://github.com/Healthy-Rivers-and-Landscapes-Science/hrl-restoration-schema/blob/main/CONTRIBUTING.md#cutting-a-release)).

## What the pipeline owns, not this repository

- Reading GeoPackage, GeoJSON, and zipped-shapefile inputs, and archive safety.
- Coordinate reference systems: reprojecting inputs to the working CRS,
  requiring an input CRS, range-checking geometry, and reprojecting the public
  GeoJSON to WGS84 lon/lat.
- Geometry validity checks with geospatial libraries.
- Conditional business rules that LinkML intentionally does not express
  (stage-dependent requiredness, acreage thresholds, funding-gap
  reconciliation) - documented in [`business_rules.md`](business_rules.md).
- The project-ID registry check against
  [`hrl-project-registry`](https://github.com/Healthy-Rivers-and-Landscapes-Science/hrl-project-registry).
- Conservative, deterministic repairs, recorded in the report.
- Producing the validation report and the standardized outputs, and holding a
  passing submission at an approval candidate until an `_APPROVE` marker is
  supplied.

## Validation report

The pipeline writes `validation-report.json` (authoritative),
`validation-report.html`, and, on request, `validation-report.pdf` (the standard
human-readable and provider-facing copy). Each finding carries a stage, a
severity (error / warning), a rule identifier, a human-readable message, and,
where applicable, the record identifier. The report records the schema version,
the registry commit, and the pipeline version for reproducibility.
