# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
