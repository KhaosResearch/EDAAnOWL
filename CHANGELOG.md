# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0](https://github.com/KhaosResearch/EDAAnOWL/compare/v1.1.0...v1.2.0) (2026-03-26)


### Added

* **examples:** achieve 100% DCAT-AP-ES compliance with official UMA DIR3 and add energy demo ([f0f1cdf](https://github.com/KhaosResearch/EDAAnOWL/commit/f0f1cdfb08e4a818313d3fa871ec928baea34856))
* **ontology:** finalize metadata and formal constraint operators for v1.2.0 ([ee64ebd](https://github.com/KhaosResearch/EDAAnOWL/commit/ee64ebd079bd053dd4125844de05c259c5e47224))


### Changed

* **metadata:** update v1.2.0 description and publisher URI to Khaos Research Group ([990ccb0](https://github.com/KhaosResearch/EDAAnOWL/commit/990ccb0ff1e4028d28b21b2d32415dc9e45163b7))
* **ontology:** implement DataProfile superclass hierarchy (R12) ([36a71b2](https://github.com/KhaosResearch/EDAAnOWL/commit/36a71b26999a03d233c43efd0c1aded845abef47))
* **ontology:** nuance compliance language in description ([9beede2](https://github.com/KhaosResearch/EDAAnOWL/commit/9beede2f719ac04274bb11afb479ee41745dee91))
* **release:** update documentation, citation, and security policy for v1.2.0 ([ef15a4c](https://github.com/KhaosResearch/EDAAnOWL/commit/ef15a4ce54788b80bb8b8b47a176835338d37d49))

## [1.1.0](https://github.com/KhaosResearch/EDAAnOWL/compare/v1.0.0...v1.1.0) (2026-03-26)


### Added

* **ci:** add official DCAT-AP-ES 1.0.0 validation suite and docker environment ([048eafb](https://github.com/KhaosResearch/EDAAnOWL/commit/048eafb4a7c4649fb5eeb40171b6e6a9af96fc5a))
* **compliance:** achieve full DCAT-AP-ES 1.0.0 compliance and add official validation infrastructure ([67cda14](https://github.com/KhaosResearch/EDAAnOWL/commit/67cda14e6226f287f74c31b29c316ea041e40bf3))
* **v1.1.0:** achieve full DCAT-AP-ES 1.0.0 compliance and restructure codebase ([1fe3531](https://github.com/KhaosResearch/EDAAnOWL/commit/1fe3531dd45d7fc1b3c0d7d5d367b9166af50428))
* **v1.1.0:** align documentation and ontology with v1.1.0 standards and fix consistency ([7d00fe7](https://github.com/KhaosResearch/EDAAnOWL/commit/7d00fe70e279c574f3244b3a4776bb2bdadf3eb6))


### Fixed

* align v1.1.0 docs, ontology notes and release tooling ([edab072](https://github.com/KhaosResearch/EDAAnOWL/commit/edab072c63974ca84edc2dc6bf605d9c0b7dd350))

## [Unreleased]

## [1.2.0] - 2026-03-24

### Added
- **Ontology**: Added `:requiresDataType` to `DataConstraint` for formalizing technical data type requirements.
- **Ontology**: Symmetric profiling architecture for `DataApp` using `:hasInputProfile` and `:hasOutputProfile`.
- **Ontology**: Promotions of `:OutputProfile` to a proper class for balanced I/O modeling.
- **Ontology**: **DCAT 3 Compliance**: Added `dct:temporal` and `dcat:inSeries` object properties.
- **Ontology**: **DCAT 3 Compliance**: Added `dct:PeriodOfTime` and `dcat:DatasetSeries` classes.
- **Ontology**: **DCAT 3 Compliance**: Updated and standardized `dcat:spatialResolutionInDegrees`, `dcat:spatialResolutionInMeters`, and `dcat:temporalResolution` properties.

### Changed
- **Ontology**: Refactored `:OutputProfile` and `:InputProfile` to use `minCardinality 1` for `hasDataSpecification`, supporting both atomic and grouped (port-based) requirements.
- **Ontology**: Generalized administrative metadata domains (`hasCertification`, `hasDPIA`, `supportContact`, `legalContact`, `topic`, `auditLogAvailable`, `collectionMethod`, `isAlive`, `knownLimitations`, `paymentModelDescription`) to support both `ids:Resource` and `:DataApp`.
- **Ontology**: Updated `hasFieldMapping` labels to "field mapping" for consistency with the architectural terminology.
- **Ontology**: Enforced `FieldMapping` as the primary domain for `hasDataType`, ensuring schema-independence of the semantic `DataSpecification` layer.

### Deprecated
- **Ontology**: Deprecated legacy properties `requiresProfile` and `producesProfile` in favor of the new decoupled profile pattern.
- **Ontology**: Deprecated technical properties (`hasSchemaType`, `conformsToSchema`) on `DataSpecification`.

## [1.1.0] - 2026-03-17

### Added
- **Compliance**: Full DCAT-AP-ES 1.0.0 and DCAT 3.0 compliance.
- **Validation**: Integrated official Spanish Government validation tools (Docker + `validate-local.sh`).
- **Shapes**: New specialized SHACL shapes for Spanish Data Office (CRED) and official vocabularies.
- **Metadata**: Standardized DIR3-compliant URIs for Agents and vCard alignment for ContactPoints.

### Fixed
- **SHACL**: Resolved URI collisions and refined technical distribution targets to prevent semantic leakage on Catalogs.
- **Consistency**: Added mandatory spatial and temporal fields to test suites for full validation.

### Changed
- **Architecture**: Refactored DataSpecifications into atomic reusable units, decoupled from technical distribution details via FieldMappings.

## [1.0.0] - 2026-03-12

### Added
- **Architecture**: Decoupled DataSpecifications from technical distributions via FieldMappings.
- **Library Model**: Enabled "Profile Libraries" for schema-agnostic semantic definitions.

### Changed
- **Matchmaking**: Upgraded to Matchmaking 2.0 with unit-aware constraints.

## [0.9.0](https://github.com/KhaosResearch/EDAAnOWL/compare/v0.8.1...v0.9.0) (2026-03-13)
