# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed

### Removed

---

## [0.3.2] - 2025-12-09

### Added

- **0.3.2 directory**: Added `0.3.2/` directory with updated documentation and resources.

### Changed

- **Structural Refinement into `0.3.2/EDAAnOWL.ttl`**:
  - **`:ObservableProperty`** is now a subclass of both `sosa:ObservableProperty` and `skos:Concept`. This allows using SKOS concepts (like AGROVOC terms) directly as observable properties while maintaining SOSA semantics.
  - **`:declaresObservedProperty`** now has a range of `:ObservableProperty` (instead of generic `skos:Concept`), enforcing stricter typing and consistency.
  - updated `README.md` to reflect the changes.
  - updated `ARCHITECTURE.md` to reflect the changes.
  - updated `demo/README.md` to reflect the changes.
  - updated `demo/transform_catalog.py` to reflect the changes.
  - updated `CITATION.md` to reflect the changes.
  - updated `USE_CASES.md` to reflect the changes.

---

## [0.3.1] - 2025-11-28

### Added

- **[MULTILINGUAL]** Added Spanish translations (`@es`) for all labels (`rdfs:label`) and comments (`rdfs:comment`) in the main ontology file (`EDAAnOWL.ttl`).
  - Translated ontology metadata: `dcterms:abstract`, `dcterms:description`, `dcterms:title`, `widoco:introduction`.
  - Translated all Object Properties (24 properties).
  - Translated all Data Properties (23 properties).
  - Translated all Classes (11 classes).
- **[MULTILINGUAL]** The ontology now provides full bilingual support (English/Spanish) for better accessibility and international adoption.

### Changed

- Updated `owl:versionIRI` to `.../0.3.1` and `owl:priorVersion` to `.../0.3.0`.
- Updated all vocabulary `owl:imports` to point to the `.../0.3.1/` path.
- Updated `dct:modified` to `2025-11-28`.

---

## [0.3.0] - 2025-11-19

### Added

- Added `:hasMetric` (ObjectProperty) to link an `:DataProfile` to its `:Metric` instances.
- Added `:appliesToFeature` (DatatypeProperty) to allow metrics to reference specific columns, JSON paths, or attributes (e.g., "column_name" or "$.user.city").
- Added `:hasCRS` (ObjectProperty) to semantically link a DataProfile to a formal Coordinate Reference System (e.g., an EPSG URI).
- Added `rdfs:comment` annotations to all core classes and properties for better documentation.
- Added `owl:minCardinality` and `owl:qualifiedCardinality` restrictions to `:DataAsset` (must have `:conformsToProfile`), `:DataProfile` (must have `:hasMetric` and `:declaresDataClass`), and `:Metric` (must have `:metricName` and `:metricValue`) to enforce model integrity.
- **[PROVENANCE]** Added `prov:wasGeneratedBy` (ObjectProperty) to link a `:DataAsset` to the `ids:DataApp` that generated it, enabling lineage tracking.
- **[PROVENANCE]** Added `prov:wasDerivedFrom` (ObjectProperty) to link a derived `:DataAsset` to its source `:DataAsset`, supporting data derivation chains.
- **[DEMO]** Added `demo/` folder with `transform_catalog.py` to demonstrate the automated transformation of standard DCAT metadata into EDAAnOWL-compliant RDF assets and profiles.
- **[DOCUMENTATION]** Added `USE_CASES.md` with practical examples in English illustrating semantic matchmaking and provenance tracking using real vocabulary concepts.

### Fixed

- Split SHACL shapes into `:SpatialTemporalAssetShape` (strict) and `:DataAssetShape` (flexible) to fix validation for generic assets.
- Corrected syntax errors in `edaan-shapes.ttl`.

### Changed

- Changed the range (`rdfs:range`) of `:metricValue` from `xsd:decimal` to `rdfs:Literal`. This is a breaking change that enables storing boolean, string, or numeric metric values.
- Aligned `:ObservableProperty` with the W3C SOSA standard by adding `rdfs:subClassOf sosa:ObservableProperty`.
- Aligned `:DataProfile` with DCAT 3 by adding restrictions for `dcat:temporalResolution` and `dcat:spatialResolutionInMeters`.
- Cleaned up `:supportContact` to be a clear `rdfs:subPropertyOf dcat:contactPoint`.
- Updated `dct:abstract`, `dct:description`, and `widoco:introduction` to reflect the new focus on profiling and metrics.

### Deprecated

- Deprecated `:profileTemporalResolution` and `:profileSpatialResolution` in favor of the standardized DCAT 3 properties.
- Deprecated `:profileCRS` and `:profileCRSRef` in favor of the new `:hasCRS` object property.

---

## [0.2.1] - 2025-11-10

### Added

- Added bibliographic metadata: `dct:bibliographicCitation` was added to the ontology header.
- Added a `schema:image` annotation pointing at the architecture diagram hosted on GitHub (annotation triple using `<https://schema.org/image>`).

With this both annotations we help to widoco to generate a better documentation for EDAAnOWL ontology.

### Removed

- The `-includeImportedOntologies` parameter has been removed from the widoco command for generating ontology documentation in `release.yml`. Now widoco will only generate specific documentation based on our ontology and will not describe imported external ontologies.

---

## [0.2.0] - 2025-11-10

### Changed

- **Model Unification:** The domain (`rdfs:domain`) of the properties `:requiresObservableProperty` and `:producesObservableProperty` has been changed from the deprecated `:AnalyticalService` to `ids:SmartDataApp`.
- This change unifies the "Profile-based Model" (v0.0.1) and the "Direct Semantic Model" (v0.1.0), allowing any `ids:SmartDataApp` (or its subclasses, like `:PredictionApp`) to use both semantic description methods simultaneously.
- Updated `owl:versionIRI` to `.../0.2.0` and `owl:priorVersion` to `.../0.1.0`.
- Updated all vocabulary `owl:imports` to point to the `.../0.2.0/` path.
- Updated `dct:abstract` and `widoco:introduction` to reflect the unified model.
- **Documentation:** Split the root `README.md` into a user-facing overview (`README.md`) and a developer-facing `ARCHITECTURE.md`.

- Prefix consistency: replaced `ns1:` with `dcat:`; corrected GeoSPARQL prefix to `gsp#`.
- Datatypes: `dct:modified` typed as `xsd:date`; `:profileCRSRef` set to `xsd:anyURI`.
- Deprecated: Marked `:spatialGranularity` as deprecated in favor of `:spatialGranularityConcept` (SKOS).

### Added

- Documentation: “IDSA alignment” section in `src/0.2.0/README.md` with examples for `ids:Representation`, Resource taxonomy, 3C views, and optional Context view (endpoint + contract).
- Validation: New SHACL shape for `ids:Representation` ensuring `dct:format` or `ids:mediaType`.
- Examples: Extended `eo-instances.ttl` with `ids:representation`, `ids:contractOffer` (ODRL Permission), and `ids:resourceEndpoint`.
- Root README: Summaries of IDSA & BIGOWL and design rationale for classes/properties in EDAAnOWL.
- `ARCHITECTURE.md` file

### Removed

- Removed the redundant class `:AnalyticalService` (which was a subclass of `ids:AppResource`). All app/service functionality is now consolidated under the `ids:DataApp` -> `ids:SmartDataApp` hierarchy.
- Removed the class `:Model` and the object property `:implementsModel`, which were associated with the deprecated `:AnalyticalService` class.
- Removed redundant prefixes from shapes `edaan-shapes.ttl`

---

## [0.1.0] - 2025-11-05

### Added

- **New Ontology Model (v0.1.0):**
  - Added new classes for direct semantic description: `:DataAsset`, `:SpatialTemporalAsset`, and `:AnalyticalService`.
  - Added new properties to support this model: `:servesObservableProperty`, `:requiresObservableProperty`, `:producesObservableProperty`, `:hasSpatialCoverage`, and `:hasTemporalCoverage`.
  - Added new `owl:imports` for `sosa`, `geosparql`, and `owl-time` to support the new classes.
  - Added new example file `eo-instances.ttl` to demonstrate the `v0.1.0` model.
- **Validation:**
  - The workflow validates RDF Syntax (using `check_rdf.py`), SHACL conformance (using `pyshacl`), and OWL Consistency (using `ROBOT reason`).
- **Local Validation:**
  - Added a `Dockerfile` to create a self-contained validation environment with Python, Java, ROBOT, and pyshacl.
  - Added `local-validate.sh` and `local-validate.bat` scripts to run the full CI validation suite locally.
- **SHACL & Consistency Tests:**
  - Added `src/0.1.0/shapes/edaan-shapes.ttl` with rules for both `v0.0.1` (`:DataProfile`) and `v0.1.0` (`:DataAsset`) models.
  - Added `src/0.1.0/examples/test-consistency.ttl` to provide valid data for SHACL and ROBOT testing.
- **Documentation:**
  - Added version-specific `README.md` files (like `src/0.1.0/README.md`) intended for deployment to `gh-pages`.
  - Added `index.html` templates for the `gh-pages` root and versioned folders to provide navigation.

### Changed

- **Versioning:** Upgraded version from `0.0.1` to `0.1.0` (Minor release) due to the addition of new, backwards-compatible ontology features.
- **CI/CD (`release.yml`):** Updated the release workflow to find and copy the version-specific `README.md` from `src/X.Y.Z/` to the `gh-pages` branch during deployment.
- **Validation (`edaan-shapes.ttl`):** Updated SHACL shapes to be more "realistic", checking that properties point to `skos:Concept` where appropriate.
- **Vocabularies:** Ensured all vocabulary files in `src/0.1.0/` have their `@base` and `owl:imports` URIs correctly updated to point to the `.../0.1.0/...` path.

### Fixed

- **Validation Scripts:** Fixed a bug in `check_rdf.py` that caused duplicate file logging by simplifying the file search logic.
- **Example Files:** Corrected multiple syntax errors in `eo-instances.ttl` and `test-consistency.ttl` (missing prefixes) that were causing `rdflib` to fail.

---

## [0.0.1] - 2025-11-03

### Added

- **Initial Ontology**: First version (`0.0.1`) of the EDAAnOWL ontology, including the main module (`EDAAnOWL.ttl`) and its `DataProfile` model.
- **Modular Vocabularies**: Added versioned SKOS vocabularies for `agro-vocab`, `datatype-scheme`, `observed-properties`, and `sector-scheme`. All vocabs are versioned in sync with the main ontology.
- **Persistent Identifiers**: Configured `.htaccess` file at `w3id.org/EDAAnOWL` to provide PID resolution and content negotiation.
- **CI/CD (`release.yml`)**: Implemented a GitHub Actions workflow that triggers on new releases to:
  - Automatically generate a dynamic `catalog.xml` file to resolve all `owl:imports`.
  - Build HTML documentation using Widoco (v1.4.25 with JDK 17).
  - Post-process Widoco's HTML (`sed`) to enforce correct, versioned links for all imported vocabularies.
  - Standardize documentation output (flattening `doc/` folder).
  - Publish all artifacts (docs, RDF serializations, vocabularies) to versioned folders (e.g., `0.0.1/`) and the `latest/` folder on the `gh-pages` branch.
- **Project Documentation**: Added `CHANGELOG.md` to track project history.
- **Contribution Guidelines**: Added `CONTRIBUTING.md` detailing the `dev` -> `main` -> `release` workflow.

### Changed

- **Repository Documentation**: Updated `README.md` to describe the project, branching model, and CI/CD process.

[Unreleased]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.3.2...HEAD
[0.3.2]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/KhaosResearch/EDAAnOWL/releases/tag/v0.0.1
