# Submission Guidance

Submitted spatial files are expected to include required project attributes and
valid spatial geometry. To submit a spatial file, please email Lucy Andrews (DWR
HRL data engineer and data scientist).

Submitting entities should provide the fields defined by
`RestorationProjectSubmission`. Program-assigned fields, including
`project_id`, and system-assigned fields, including `update_date`, should not be
supplied by submitters.

Controlled vocabulary values must match the values defined in the schema enums.
The validation layer may normalize file formats and report clear errors when a
submitted value is outside the allowed vocabulary.

Some schema fields are modeled as multivalued fields. Runtime validation may
serialize those fields using semicolon-delimited strings or another documented
convention, but the schema meaning remains multivalued.

Is submitted files fail to pass schema or geometry validation, the submitted
will be notified via email and provided with an automatically generated report
documenting errors.