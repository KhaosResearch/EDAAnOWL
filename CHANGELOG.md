# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.1](https://github.com/KhaosResearch/EDAAnOWL/compare/v0.7.0...v0.7.1) (2026-03-06)


### Added

* **ontology:** v0.8.0 release with CRED alignment, DCAT-AP 3.0 and ODRL 2.2 ([feac434](https://github.com/KhaosResearch/EDAAnOWL/commit/feac434074cb74b647d2d7899190bb3c517cd54e))
* **siex:** integrate additional FEGA catalogs and sanitize project paths ([df74826](https://github.com/KhaosResearch/EDAAnOWL/commit/df7482622cea32770eb85b4fc0e1ecf0f324b530))


### Fixed

* **siex-codes:** update uris with version 0.8.0 ([d038cbf](https://github.com/KhaosResearch/EDAAnOWL/commit/d038cbf6840ce3d4e61911fcb3ed77f7b6f1b271))


### Changed

* **matchmaking:** clarify measuresProperty usage and update CRED example for semantic matchmaking ([9da6e60](https://github.com/KhaosResearch/EDAAnOWL/commit/9da6e6009d3d58866215dc08d67170ae45d989b6))
* update changelog links, citation and security for v0.8.0 ([f4cc9bb](https://github.com/KhaosResearch/EDAAnOWL/commit/f4cc9bb7172ad27ff582147c1a39ccf6ef58cf9c))
* update changelog links, citation and security for v0.8.0 ([be7aa64](https://github.com/KhaosResearch/EDAAnOWL/commit/be7aa64f37daff078a7161fa1815dfee7db2aae7))

## [0.8.0] - 2026-03-04

### ⚠ BREAKING CHANGES
- **ontology:** major update for CRED (Spanish Data Office) and UNE 0087:2025 alignment.
- Added mandatory hierarchy: `dcat:Catalog` -> `dcat:Dataset` -> `dcat:Distribution`.
- Enforced `xsd:nonNegativeInteger` for `dcat:byteSize`.

### Added
- **ontology:** alignment with DCAT-AP 3.0, ODRL 2.2, and FOAF.
- **shapes:** created `src/0.8.0/shapes/cred-alignment-shapes.ttl` for SHACL validation of CRED entities (Catalogs, Services, Offers, Agents).
- **classes:** added `dcat:Catalog`, `dcat:DataService`, `dcat:Resource`, `odrl:Policy`, `odrl:Offer`, `odrl:Rule`, `odrl:Constraint`, `odrl:Asset`, `foaf:Agent`, `dct:Location`, `dct:RightsStatement`, `dct:LicenseDocument`, `dcatap:LegalResource`.
- **properties:** added 25 Object Properties and 6 Data Properties from CRED recommendation.
- **documentation:** updated `ARCHITECTURE.md` with CRED layer diagram and explanation.

### Changed
- **hierarchy:** established `dcat:Catalog subClassOf dcat:Dataset`, `dcat:Dataset subClassOf dcat:Resource`, `dcat:DataService subClassOf dcat:Resource`.
- **metadata:** updated ontology version to 0.8.0 with updated abstract and descriptions for CRED.
- **properties:** added strict `rdfs:domain` and `rdfs:range` to CRED-aligned properties to support automated reasoning and validation.

## [0.7.0] - 2026-02-24

### Added
- **ontology:** full integration with QUDT units (replacing `metricUnit` with `hasMetricStandard`).
- **ontology:** introduced `measuresProperty` to explicitly link metrics to the `ObservableProperty` they measure.
- **ontology:** added IDSA-aligned security properties for access control and confidentiality.
- **vocabularies:** integrated SIEX (Spain) agricultural catalogs as automated SKOS transformations.
- **documentation:** comprehensive rebranding of diagrams and Widoco documentation.
- **examples:** improved interoperability examples with real-world sector-specific cases.

### Fixed
- **ontology:** fixed inconsistent prefix mappings for QUDT and provenance.
- **vocabularies:** corrected encoding issues and SIEX URI resolution patterns.
- **metadata:** ensured all versioned files (0.7.0) point to the correct release IRIs.

## [0.6.1](https://github.com/KhaosResearch/EDAAnOWL/compare/v0.6.0...v0.6.1) (2026-02-18)


### Fixed

* **ontology:** refine metric definitions and cleanup vocabularies ([d7290d6](https://github.com/KhaosResearch/EDAAnOWL/commit/d7290d6eb5b106e68456c9c51ccca20b4ad347b1))
* **ontology:** refine metric definitions and cleanup vocabularies ([60cd1ad](https://github.com/KhaosResearch/EDAAnOWL/commit/60cd1adff2cace840432b24558d898dc1b79787b))

## [0.6.0] (2026-02-17)


### ⚠ BREAKING CHANGES

* **ontology:** force minor version bump to v0.6.0 for the new ontology structure.

### Added

* **ontology:** v0.6.0 release ([c0c60bb](https://github.com/KhaosResearch/EDAAnOWL/commit/c0c60bb652c0d588ab58954bfcc3aa3ca43ec10e))
* **ontology:** v0.6.0 release with Zero-Local policy, DQV alignment, and documentation refactor ([a2c365e](https://github.com/KhaosResearch/EDAAnOWL/commit/a2c365ec18e24b90e755e8c811abe2ceb356cf73))


### Changed

* add comprehensive matchmaking documentation with diagrams ([ae49139](https://github.com/KhaosResearch/EDAAnOWL/commit/ae49139a31f7db654c70b8e030a476c1f47245a1))
* Add Spanish ontology overview diagrams for the EDAAnOWL ontology. ([984c7b7](https://github.com/KhaosResearch/EDAAnOWL/commit/984c7b7c097a00d9932fac1df94d53f660521e6d))
* remove manual changelog entries to let release-please automate the process ([877094c](https://github.com/KhaosResearch/EDAAnOWL/commit/877094cdc6f989f5c5a706b8ddf66cfc1f982fc9))
* Rename GitHub Actions workflow `release.yml` to `deploy-docs.yml` across documentation files. ([25f12fa](https://github.com/KhaosResearch/EDAAnOWL/commit/25f12fabd96608d6ae43be224f9823b7f6ed824c))
* revert manual version header to [Unreleased] for release-please ([7fe519a](https://github.com/KhaosResearch/EDAAnOWL/commit/7fe519ae12f33b6a7a582fb7cb2fd7e08007f321))

## [0.5.0] (2026-01-30)

### ⚠ BREAKING CHANGES

* Align with BIGOWL and enforce external vocabularies.
    - Added release-please configuration
    - Renamed release workflow to deploy-docs
    - Updated CONTRIBUTING and AGENTS docs
* Deprecated local vocabularies in favor of external URIs. Deprecated :realizesWorkflow in favor of :implementsComponent. Moved vocabulary strategy to use AGROVOC, EU NALs, and BIGOWL directly. Updated documentation and examples to reflect these changes."
* **ontology:** remove local vocabulary imports in favor of external URIs

### Added

* **ontology:** release v0.5.0 with DQV alignment and Concept properties ([8f5913c](https://github.com/KhaosResearch/EDAAnOWL/commit/8f5913c77ada43f09efcd4e37860465fd1b966d3))
* **ontology:** remove local vocabulary imports in favor of external URIs ([2f78840](https://github.com/KhaosResearch/EDAAnOWL/commit/2f78840ed561a1a7eb0b413b58ca8711c08f6770))
* prepare v0.5.0 release and setup automated versioning ([36fed7c](https://github.com/KhaosResearch/EDAAnOWL/commit/36fed7c9d10459345758424d4e0daa2d777ebd38))
* v0.5.0 release - BIGOWL alignment and External Vocabularies ([e3ffda8](https://github.com/KhaosResearch/EDAAnOWL/commit/e3ffda86fb0bb17ed48cf52d21c6df9b63dae6c1))
* **validation:** add SHACL shapes for DCAT-AP and AGROVOC alignment ([9ea082d](https://github.com/KhaosResearch/EDAAnOWL/commit/9ea082df15bf0332e0f8114420450e604f04ae5b))


### Fixed

* **vocabularies:** convert to UTF-8 encoding ([c28ae35](https://github.com/KhaosResearch/EDAAnOWL/commit/c28ae351d51c1c1544927d502e5a0b44b9b279ab))


### Changed

* add AGENTS.md for AI coding agents context ([4164d47](https://github.com/KhaosResearch/EDAAnOWL/commit/4164d47aebbd818e515a910ee5287482b4cacc72))
* **changelog:** add v0.5.0 external vocabulary breaking change ([ccc6ede](https://github.com/KhaosResearch/EDAAnOWL/commit/ccc6edeb60e989982ae53cc98d4e2670ba6b7671))
* comprehensive alignment with DCAT-AP, ENI, and Interoperable Europe ([60a811d](https://github.com/KhaosResearch/EDAAnOWL/commit/60a811d4809650964c67596b3f08d570501a32cc))
* consolidate use cases and examples into demo/USE_CASES.md ([23baeb5](https://github.com/KhaosResearch/EDAAnOWL/commit/23baeb529d73ed6b5b1f64af1ad0b3f8955e61d1))
* **demo:** use AGROVOC URIs in demo files with inline comments ([fa805e7](https://github.com/KhaosResearch/EDAAnOWL/commit/fa805e72bb05415a599d73b05f679fc6f3349fa6))
* **examples:** use verified AGROVOC URIs instead of local concepts ([9671f87](https://github.com/KhaosResearch/EDAAnOWL/commit/9671f87debc1ee6b894d98e4bd115ea9aba4656e))
* expand USE_CASES.md with DataProfile reuse, matchmaking reference, and multi-dimensional compatibility ([fe8523f](https://github.com/KhaosResearch/EDAAnOWL/commit/fe8523fe112603a8f5bdd4ce15c8072c4ca03e2a))
* **main:** release 0.5.0 ([07e13c5](https://github.com/KhaosResearch/EDAAnOWL/commit/07e13c54060aa1ce9c39a56c73edcfcfdf6b34f1))
* **main:** release 0.5.0 ([cdbe14b](https://github.com/KhaosResearch/EDAAnOWL/commit/cdbe14b4248defa8052369a4cc5f727d5a0b7812))
* **main:** release EDAAnOWL 0.5.0 ([484a261](https://github.com/KhaosResearch/EDAAnOWL/commit/484a261e4ea5bce1243ed8dc623e687d8df80d2d))
* **main:** release EDAAnOWL 0.5.0 ([6b4515f](https://github.com/KhaosResearch/EDAAnOWL/commit/6b4515f40c93e1add2e479eeef8c12338bf0835b))
* **main:** release EDAAnOWL 0.6.0 ([601221e](https://github.com/KhaosResearch/EDAAnOWL/commit/601221e1259ee10ac6b0ef3de4dfb9765269e602))
* **main:** release EDAAnOWL 0.6.0 ([3936b91](https://github.com/KhaosResearch/EDAAnOWL/commit/3936b91f82e3a40b8f41bdc2ae0fd4c669d14c8a))
* **releas-please:** update GitHub Actions workflow. ([9bf143f](https://github.com/KhaosResearch/EDAAnOWL/commit/9bf143f3694101212544959238bc5f325a10048e))
* **releas-please:** update GitHub Actions workflow. ([00b61e8](https://github.com/KhaosResearch/EDAAnOWL/commit/00b61e84848b98c2169cb575edfe59de5c0a0ff3))
* removed line from Unreleased Changelog section ([54fdbfd](https://github.com/KhaosResearch/EDAAnOWL/commit/54fdbfd11e2e400368442b73e7625df1167d287e))
* update CHANGELOG with unreleased changes since v0.4.1 ([2e6c456](https://github.com/KhaosResearch/EDAAnOWL/commit/2e6c456b20b904f0061bc95160bdfe0b2b94a688))
* update demos, guides and metadata for v0.5.0 ([384c0cd](https://github.com/KhaosResearch/EDAAnOWL/commit/384c0cdacbcf0348fa1156e9c6153876fe2a901a))
* update root README references to v0.5.0 ([fb3d975](https://github.com/KhaosResearch/EDAAnOWL/commit/fb3d975d1aafaa58a1c8efd4c3a11d055d185a56))
* **v0.5.0:** document external vocabulary strategy ([1161ccc](https://github.com/KhaosResearch/EDAAnOWL/commit/1161ccc8513141800dfd4e4dc8d795e2bffb6545))

---

## [0.4.1] - 2026-01-12

### Added

- **Pull Request Template**: Added `.github/pull_request_template.md` to standardize PR descriptions and checks.

### Fixed

- **OWL Restriction Bug**: Removed incorrect `owl:minCardinality` restriction on `:DataAsset` for `:conformsToProfile`. In v0.4.0, `:conformsToProfile` domain changed to `dcat:Distribution`, making this restriction semantically invalid.
- **Test Examples**: Updated `test-consistency.ttl` to use the correct v0.4.0 pattern (profile on Distribution, not directly on Resource).
- **Demo Scripts**: Fixed `demo/olive-grove/transform_csv.py` and `demo/catalog/transform_catalog.py` to generate RDF following the v0.4.0 pattern with `:DataRepresentation` and `ids:representation`.
- **Documentation**: Corrected examples and descriptions in `src/0.4.0/README.md` to reflect the v0.4.0 pattern where profiles are linked via `ids:representation → dcat:Distribution → :conformsToProfile`.
- **Ontology Introduction**: Updated `widoco:introduction` in `EDAAnOWL.ttl` to clarify the v0.4.0 usage pattern for linking profiles to distributions.

### Changed

- **`:DataAsset` class**: Updated `rdfs:comment` to explicitly document that profiles are linked via Distribution in v0.4.0+, not directly on the DataAsset.

---

## [0.4.0] - 2025-12-22

### Added

- **IDSA Class Alignment**: Now using IDSA URIs directly (`ids:SmartDataApp`, `ids:DataResource`) instead of local classes.
- **`:DataRepresentation`**: New internal class for data distributions, subclass of `dcat:Distribution`. Replaces usage of ghost `ids:DataRepresentation`.
- **`:instance`**: New property for linking Distributions to `ids:Artifact`. Replaces usage of ghost `ids:instance`.
- **New IDSA external terms**: Declared minimal references to IDSA classes used in examples:
  - Classes: `ids:DataResource`, `ids:ContractOffer`, `ids:ResourceEndpoint`, `ids:Endpoint`, `ids:ConnectorEndpoint`, `ids:AppEndpoint`, `ids:Described`, `ids:DescribedSemantically`, `ids:DigitalContent`, `ids:ManagedEntity`, `ids:UsagePolicyClass`
  - Object Properties: `ids:representation`, `ids:contractOffer`, `ids:resourceEndpoint`, `ids:appEndpoint`, `ids:endpointArtifact`, `ids:dataAppInformation`, `ids:dataTypeSchema`, `ids:supportedUsagePolicies`
  - Data Properties: `ids:checkSum`, `ids:accessURL`, `ids:appDocumentation`, `ids:appEndpointPort`, `ids:appEndpointProtocol`, `ids:appEnvironmentVariables`, `ids:appStorageConfiguration`, `ids:endpointURI`, `ids:fileName`
- **Traceability**: Added `:consumesDataRepresentation` and `:producesDataRepresentation` to link BIGOWL Components with EDAAnOWL DataRepresentations.
- **AppRepresentation flow**: Added `:consumesAppRepresentation` and `:producesAppRepresentation` for workflow component modeling.
- **Artifact Validation**: Added SHACL shapes for `ids:Artifact`.
- **New examples**: Added Use Case 5b demonstrating `AppRepresentation` with Workflow Components.
- **New observable properties**: Added `reflectance_red` and `reflectance_nir` to vocabulary.

### Changed

- **Profile Conformance (BREAKING)**: `:conformsToProfile` property domain changed from `ids:Resource` to `dcat:Distribution`. Existing data using `:conformsToProfile` directly on resources must be updated.
- **SHACL shapes**: Updated `sh:targetClass` to use `ids:DataResource` and `ids:SmartDataApp` instead of local classes.
- **Namespace Cleanup**: Moved several classes and properties from `ids:` namespace to `:edaan:` namespace to avoid invalid "ghost" IDSA entities.
- **Annotation Cleanup**: Stripped annotations from external terms (DCAT, PROV, SKOS, DCTERMS) to avoid redundancy.
- **Media Type**: Switched to `dcat:mediaType` instead of local `ids:mediaType`.

### Deprecated

- `ids:DataRepresentation` (ghost class, now use `:DataRepresentation`)
- `ids:instance` (ghost property, now use `:instance`)
- `ids:mediaType` (now use `dcat:mediaType`)

---

## [0.3.2] - 2025-12-16

### Added

- **0.3.2 directory**: Added `0.3.2/` directory with updated documentation and resources.
- **GitHub Pages**: Added `style.css` and `main.js` to improve the visual appearance of the rendering of `README.md` files in `index.html` files.
- **`:MetricType` class**: New class for standardized metric type vocabulary. Enables controlled, interoperable metric names instead of free-text strings.
- **`:metricType` property**: New object property to link a `:Metric` to a `:MetricType` from the controlled vocabulary.
- **`metric-types.ttl` vocabulary**: New vocabulary with ~20 standardized metric types:
  - Quality metrics (aligned with DQV): `mt_completeness`, `mt_uniqueness`, `mt_accuracy`, `mt_consistency`, `mt_timeliness`
  - Profiling metrics: `mt_recordCount`, `mt_featureCount`, `mt_nullRatio`, `mt_duplicateRatio`
  - Earth Observation metrics: `mt_cloudCoverage`, `mt_noDataRatio`, `mt_spatialExtent`
  - Temporal metrics: `mt_temporalExtent`, `mt_updateFrequency`
  - Performance metrics: `mt_executionTime`, `mt_modelAccuracy`, `mt_f1Score`
- **Extended `observed-properties.ttl`**: Expanded from 6 to ~25 observable properties:
  - Vegetation indices: `ndvi`, `evi`, `lai`, `chlorophyllContent`
  - Meteorological: `temperature`, `precipitation`, `relativeHumidity`, `windSpeed`, `solarRadiation`, `evapotranspiration`
  - Soil properties: `soilMoisture`, `soilTemperature`, `soilPH`, `electricalConductivity`, `organicMatter`
  - Crop production: `yield`, `yieldForecast`, `biomass`
  - Water management: `waterStress`, `irrigationNeed`
  - Pest & disease: `pestIncidence`, `diseaseIncidence`, `repiloIncidence`
  - All with `skos:exactMatch` / `skos:closeMatch` alignment to AGROVOC
- **Extended `agro-vocab.ttl`**: Expanded from 6 to ~25 agricultural concepts:
  - Mediterranean crops: `agro_olive`, `agro_vine`, `agro_almond`, `agro_citrus`
  - Cereals: `agro_wheat`, `agro_maize`, `agro_barley`, `agro_rice`
  - Industrial crops: `agro_sunflower`, `agro_cotton`, `agro_sugarbeet`
  - Agricultural practices: `agro_irrigation`, `agro_fertilization`, `agro_harvest`, `agro_pruning`, `agro_pestControl`, `agro_soilManagement`
  - Diseases: `agro_repilo`, `agro_tuberculosis`, `agro_verticillium`
  - Production types: `agro_organic`, `agro_precisionAgriculture`
  - All with `skos:exactMatch` alignment to AGROVOC and extensibility documentation
- **SHACL shapes**: Added `:MetricTypeShape`, `:ObservablePropertyShape`, and updated `:MetricValidationShape` with optional `metricType` validation
- **Example instances**: Updated `eo-instances.ttl` with:
  - MetricType usage examples
  - Extended observable properties
  - AGROVOC direct references
  - Provenance chain examples
  - Soil data use case

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

### Fixed

- **GitHub Pages**: Fixed the visual appearance of the rendering of `README.md` files in `index.html` files.
- **Local validation**: Fixed local validation script to correctly handle vocabulary files and validate against the latest version.
- **Agrovoc codes**: Fixed Agrovoc codes used in `agro-vocab.ttl`.
- **Agrovoc codes**: Fixed Agrovoc codes used in `observed-properties.ttl`.

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

[Unreleased]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.8.0...HEAD
[0.8.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.6.1...v0.7.0
[0.6.1]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/KhaosResearch/EDAAnOWL/releases/tag/v0.0.1
