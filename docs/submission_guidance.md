# Submission Guidance

Data providers prepare one GeoPackage (or GeoJSON, or a zipped shapefile
package) with the required project attributes and valid spatial geometry, using
the HRL data-model spreadsheet, and email it to HRL. Providers do not need
Azure, Git, or a submission website: the HRL data operator creates the Azure
submission package (`submission.json` manifest, the spatial file, and a
`_READY` marker uploaded last) and runs validation.

Submitting entities should provide the fields defined by
[`RestorationProjectSubmission`](reference/RestorationProjectSubmission.md).
Every submitted feature must include its program-assigned
[`project_id`](reference/project_id.md). It is a stable string identifier; do
not invent, reuse, or alter it. Validation rejects IDs that are absent from
`project-id-registry.csv` in `hrl-project-registry`. System-assigned canonical
fields, such as [`update_date`](reference/update_date.md), must not be supplied
by submitters.

Controlled vocabulary values must match the values defined in the schema enums.
The validation layer may normalize file formats and report clear errors when a
submitted value is outside the allowed vocabulary.

Some schema fields are modeled as multivalued fields. Runtime validation may
serialize those fields using semicolon-delimited strings or another documented
convention, but the schema meaning remains multivalued.

The pipeline applies conditional rules that LinkML intentionally does not
duplicate: contact fields are warned on when absent; construction dates and
funding values become errors at construction and post-construction monitoring
stages; and acreage is a warning before construction but an error at
construction and post-construction for area-based project types (with an
exemption for projects consisting solely of fish passage and/or fish screen
work). A passing submission becomes an approval
candidate, not public data. It is published only after an authorized reviewer
uploads the `_APPROVE` marker.
