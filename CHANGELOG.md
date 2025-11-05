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

## [0.1.0] - 2025-11-05

### Added
- **New Ontology Model (v0.1.0):**
  - Added new classes for direct semantic description: `:DataAsset`, `:SpatialTemporalAsset`, and `:AnalyticalService`.
  - Added new properties to support this model: `:servesObservableProperty`, `:requiresObservableProperty`, `:producesObservableProperty`, `:hasSpatialCoverage`, and `:hasTemporalCoverage`.
  - Added new `owl:imports` for `sosa`, `geosparql`, and `owl-time` to support the new classes.
  - Added new example file `eo-instances.ttl` to demonstrate the `v0.1.0` model.
- **Validation CI (`validation.yml`):**
  - Added a new GitHub Actions workflow (`validation.yml`) that runs on every push/PR to `dev` and `main`.
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

[Unreleased]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/KhaosResearch/EDAAnOWL/releases/tag/v0.0.1
