# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0] - 2024-12-17

### Added
- **:DataRepresentation**: New internal class for data distributions, aligned with `dcat:Distribution`. Replaces usage of ghost `ids:DataRepresentation`.
- **:instance**: New property for linking Distributions to Artifacts. Replaces usage of ghost `ids:instance`.
- **:SmartDataApp**, **:DataResource**: Internal definitions replacing ghost IDSA classes.
- **Traceability**: Added `:consumesDataRepresentation` and `:producesDataRepresentation` to link BIGOWL Components with EDAAnOWL DataRepresentations.
- **Artifact Validation**: Added SHACL shapes for `ids:Artifact`.

### Changed
- **Profile Conformance**: `:conformsToProfile` property domain changed from `ids:Resource` to `dcat:Distribution`.
- **Namespace Cleanup**: Moved several classes and properties from `ids:` namespace to `:edaan:` namespace to avoid invalid "ghost" IDSA entities.
- **Annotation Cleanup**: Stripped annotations from external terms (DCAT, PROV, SKOS, DCTERMS) to avoid redundancy.
- **Media Type**: Switched to `dcat:mediaType` instead of local `ids:mediaType`.

### Deprecated
- `ids:DataRepresentation`, `ids:instance`, `ids:mediaType` (removed from ontology definition).

## [0.3.2] - 2024-12-11
- Added `MetricType` and `ObservationProperty` vocabularies using SKOS.
- Aligned `DataProfile` with `dcat:Distribution` semantics partially.
- Added SHACL shapes for `Metric` and `DataProfile`.

## [0.3.1] - 2024-11-20
- Added initial alignment with BIGOWL.
- Introduced `DataApp` and `SmartDataApp`.

## [0.3.0] - 2024-10-15
- Initial public release of EDAAnOWL.
