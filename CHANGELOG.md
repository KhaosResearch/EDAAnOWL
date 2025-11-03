# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- **Local validation tooling**:
  - Added a Docker-based validation environment (`Dockerfile`) to run ontology checks in a reproducible container.
  - Added `scripts/check_rdf.py` to perform RDF syntax validation over all `.ttl` files in the latest `src/<version>/` folder (vocabularies, examples, shapes).
  - Added cross-platform helper scripts:
    - `scripts/local-validate.bat` (Windows)
    - `scripts/local-validate.sh` (Linux/macOS)
  - The validation pipeline runs:
    - RDF syntax validation (`rdflib` via `check_rdf.py`)
    - SHACL validation (`pyshacl` with `edaan-shapes.ttl` and `test-consistency.ttl`)
    - OWL consistency checking (ROBOT `reason` with the ELK reasoner).

### Changed

- Documented the local validation workflow and Docker-based environment in `README.md`.

### Fixed

### Removed

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

[Unreleased]: https://github.com/KhaosResearch/EDAAnOWL/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/KhaosResearch/EDAAnOWL/releases/tag/v0.0.1
