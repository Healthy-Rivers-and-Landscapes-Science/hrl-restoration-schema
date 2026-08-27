# Submission Guidance

Submitted spatial files are expected to include required project attributes and
valid spatial geometry. Submit them through the HRL Azure Portal workflow in a
directory containing a `submission.json` manifest, one supported spatial file,
and a `_READY` marker uploaded last.

Submitting entities should provide the fields defined by
[`RestorationProjectSubmission`](reference/RestorationProjectSubmission.md).
Every submitted feature must include its program-assigned
[`project_id`](reference/project_id.md). It is a stable string identifier; do
not invent, reuse, or alter it. The pipeline rejects IDs that are absent from
the DWR-managed project-ID registry. System-assigned canonical fields, such as
[`update_date`](reference/update_date.md), must not be supplied by submitters.

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
