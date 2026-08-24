# Geometry Policy

This draft policy documents geometry expectations for HRL restoration spatial
data submissions. It is not a final enforcement specification.

Restoration areas are expected to be polygons or multipolygons. Fish passage
and fish screen installation or improvement project types may be represented as
points or multipoints, if that remains consistent with the schema.

Each standardized record represents one `project_id` and one geometry. The
pipeline standardizes polygonal outputs to `MULTIPOLYGON` and point outputs to
`MULTIPOINT`; it is responsible for approved consolidation of source parts and
for deterministic geometry repair.

Actual geometry checks will be performed by validation code using geospatial
libraries, not solely by [LinkML](https://linkml.io). Validation code should check:

- CRS is present
- CRS can be transformed to the target CRS
- Target CRS for standardization is [EPSG:3310](https://epsg.io/3310), unless the schema says
  otherwise
- Geometries are non-empty
- Geometries are valid
- Geometries fall within the expected extent
- Slivers are detected according to program thresholds
- Duplicate geometries are detected
- Geometry type is consistent with project type

The schema documents geometry-related expectations so downstream validation
code can apply them consistently.
