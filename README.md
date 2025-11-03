# EDAAnOWL — (v0.0.1)

[![Deploy Ontology to GitHub Pages](https://github.com/KhaosResearch/EDAAnOWL/actions/workflows/release.yml/badge.svg)](https://github.com/KhaosResearch/EDAAnOWL/actions/workflows/release.yml)

A pilot ontology for the semantic exploitation of data assets in the Agri-food (EDAA) context, aligned with the IDSA Information Model and the BIGOWL ontology.

The purpose of `EDAAnOWL` is to serve as an annotation ontology that enriches the description of Data Space assets. It allows for modeling the functional profile (inputs, outputs, parameters) of `ids:DataApp` and `ids:DataResource`, facilitating their semantic discovery, composition into complex services, and compatibility validation.

## 🚀 Features

- **Main Ontology**: A semantic "bridge" linking `ids:DataApp` to `bigwf:Component` (from BIGOWL).
- **Profile Model**: A `:DataProfile` class to describe the data "signatures" (inputs/outputs) of assets.
- **Modular Vocabularies**: Separate, resolvable SKOS vocabularies for domains, observed properties, etc., versioned alongside the main ontology.
- **Persistent Identifiers**: All ontology and vocabulary modules are resolvable via `https://w3id.org/EDAAnOWL/` for robust content negotiation.
- **Automated Documentation & CI/CD**: A GitHub Actions workflow (`release.yml`) that, upon creating a new release:
  - Generates a dynamic `catalog-v0.xml` to resolve all imports.
  - Builds comprehensive HTML documentation with **Widoco**.
  - Post-processes the HTML (`sed`) to ensure all vocabulary links are correctly versioned.
  - Publishes all artifacts (docs, vocabs, RDF serializations) to the `gh-pages` branch.
- **Versioning**: Supports a `latest` development version and immutable, versioned snapshots (e.g., `/0.0.1/`).

## 📁 Repository Structure & Branching Model

This repository uses a `dev` -> `main` -> `gh-pages` git flow.

- **`main` branch**:

  - **Purpose**: This branch represents the most recent _stable, released_ version of the ontology.
  - **Do NOT commit directly here.** All changes must come from the `dev` branch via a Pull Request.
  - Creating a "Release" from this branch triggers the `gh-pages` deployment.
  - **Structure**:
    - `/src/`
      - `0.0.1/` (Ontology and vocabs for v0.0.1)
      - `0.0.2/` (Ontology and vocabs for v0.0.2)
    - `/.github/workflows/` (The CI/CD workflow)

- **`dev` branch**:

  - **Purpose**: This is the main **development branch**. All new features, fixes, and preparations for the _next_ version happen here.
  - All Pull Requests should be targeted at `dev`.
  - **Structure**:
    - Same as `main`, but may contain the _next_ unreleased version folder (e.g., `src/0.0.3/`) while it is in progress.

- **`gh-pages` branch**:

  - **Purpose**: **AUTO-GENERATED. DO NOT EDIT MANUALLY.**
  - This branch contains the static output of the `release.yml` workflow.
  - It hosts the public-facing documentation and RDF files served by GitHub Pages.
  - **Structure**:
    - `/latest/` (A mirror of the most recent version)
    - `/0.0.1/` (A snapshot of the v0.0.1 documentation and files)
    - `/0.0.2/` (A snapshot of the v0.0.2 documentation and files)
    - `.nojekyll` (Disables Jekyll on GitHub Pages)

- **Feature Branches (e.g., `feat/my-fix`)**:
  - **Purpose**: Temporary branches for new work. They should be based on `dev` and merged back into `dev` via a Pull Request.

## 🔗 Resolvability (PID)

This repository manages the _source code_. The Persistent Identifiers (PIDs) (e.g., `https://w3id.org/EDAAnOWL/...`) are resolved by the `.htaccess` file located in the [w3id.org repository](https://github.com/perma-id/w3id.org/tree/master/EDAAnOWL).

That `.htaccess` file points all requests to the documentation and files automatically built and published by our CI/CD workflow to the `gh-pages` branch, which is hosted at:

**`https://khaosresearch.github.io/EDAAnOWL/`**
