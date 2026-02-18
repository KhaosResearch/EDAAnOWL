# EDAAnOWL

[![Deploy Ontology to GitHub Pages](https://github.com/KhaosResearch/EDAAnOWL/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/KhaosResearch/EDAAnOWL/actions/workflows/deploy-docs.yml)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-1f6feb)](https://khaosresearch.github.io/EDAAnOWL/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/KhaosResearch/EDAAnOWL?display_name=tag)](https://github.com/KhaosResearch/EDAAnOWL/releases)
[![PURL](https://img.shields.io/badge/purl-w3id.org-blue)](https://w3id.org/EDAAnOWL/)
[![SHACL Validation](https://img.shields.io/badge/SHACL-Conformant-success)](src/0.6.0/shapes/edaan-shapes.ttl)

> **Semantic Bridge for Data Spaces**: Linking IDSA governance with BIGOWL workflows.

## 🚀 Overview

**EDAAnOWL** is a lightweight ontology designed to operationalize Data Spaces. It bridges the gap between the **IDSA Information Model** (governance, contracts) and **BIGOWL** (analytics, workflows), enabling:

1.  **Deep Semantic Matchmaking**: Discovery of assets based on *what they mean* (Observable Properties) not just metadata.
2.  **Structural Compatibility**: Automated validation of data shapes (Data Profiles) for smart application composition.
3.  **Performance & Quality Tracking**: Explicit support for DQV-aligned quality metrics and performance benchmarks.
4.  **Cross-Domain Interoperability**: Enabling data exchange between different sectors (e.g., Agri-food ↔ Mobility) by providing a unified functional meta-model, breaking vertical silos.

---

## 📘 Background & Design Rationale

### Why IDSA and BIGOWL?

- **[IDSA Information Model](https://github.com/International-Data-Spaces-Association/InformationModel)**: We use it for **Governance**. It provides the canonical taxonomy for resources (`ids:Resource`, `ids:DataApp`), usage control (ODRL), and security profiles. We align with it to ensure assets are governable across Data Spaces.
- **[BIGOWL](https://w3id.org/BIGOWL)**: We use it for **Workflows**. It formalizes analytical pipelines and components. We align with it (`:implementsComponent`) to connect abstract "Apps" to executable algorithms.

### Why Reuse Standard Vocabularies?

We adopt standards recommended by IDSA and the Linked Data community to maximize interoperability:

- **[SKOS](https://www.w3.org/TR/skos-reference/)**: For modular controlled vocabularies.
- **[DCAT (v3)](https://www.w3.org/TR/vocab-dcat-3/)**: For cataloguing assets (EDAAnOWL assets are also `dcat:Dataset`s).
- **[ODRL (v2.2)](https://www.w3.org/TR/odrl-model/)**: For usage control policies.
- **[SOSA/SSN](https://www.w3.org/TR/vocab-ssn/)**: For observable properties (`:ObservableProperty` aligns with `sosa:ObservableProperty`).
- **[GeoSPARQL (v1.1)](https://www.ogc.org/standard/geosparql/)**: For geospatial coverage.
- **[PROV-O](https://www.w3.org/TR/prov-o/)**: For provenance and lineage tracking.

---

## 🇪🇺 Strategic Alignment

EDAAnOWL is designed to work **in conjunction** with European interoperability standards, addressing the "Deep Semantic Gap" in current cataloging.

#### 🇪🇺 Alignment with Interoperable Europe
EDAAnOWL follows the guidelines of the **Interoperable Europe** initiative.
*   **The Goal**: Prevent "Data Silos" regarding technical reuse.
*   **Our Contribution**: While **DCAT-AP** acts as the "Map" for human discovery across portals, **EDAAnOWL** acts as the "Motor" for automated service composition, providing the functional semantics (inputs, outputs, variables) agents need to *execute* tasks.

#### 🇪🇸 Alignment with Spanish Framework (ENI & MIT)
We align with the **[Esquema Nacional de Interoperabilidad (ENI)](https://cred.digital.gob.es/content/dam/cred/img/docs/MarcoInteroperabilidadTecnico.pdf)** and the Technical Interoperability Framework (MIT).

*   **Enhanced Reuse (ENI)**: The ENI mandates facilitating information reuse. EDAAnOWL takes this further by enabling **automated reuse** through detailed functional semantics, reducing integration costs.
*   **Sectoral Semantic Interoperability (MIT)**: The [Marco de Interoperabilidad Técnico](https://cred.digital.gob.es/content/dam/cred/img/docs/MarcoInteroperabilidadTecnico.pdf) (p. 59) highlights the need for organizations to share a "common meaning" to enable reuse across sectors.
    *   **EDAAnOWL's Solution**: We address this challenge by providing a **Cross-Domain Annotation Layer**. By decoupling the *technical profile* (`DataProfile`) from *domain semantics* (`ObservableProperty`), EDAAnOWL allows assets from diverse sectors (e.g., Agriculture, Mobility, Health) to be modeled with the same grammar, facilitating the creation of transverse Data Spaces.

---

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

- **📘 [Architecture](docs/ARCHITECTURE.md)**: High-level view of how IDSA, BIGOWL, and EDAAnOWL fit together.
- **🧩 [Ontology Overview](docs/ONTOLOGY_OVERVIEW_DIAGRAM_ES.md)**: Diagrams and tables explaining Classes (`DataAsset`, `SmartDataApp`) and Properties.
- **💡 [Examples](docs/INTEROPERABILITY_EXAMPLES_ES.md)**: Practical scenarios of semantic interoperability and matchmaking.

## 📦 Repository Structure

- `src/`: Contains the ontology versions (e.g., `0.6.0/`), vocabularies, and SHACL shapes.
- `docs/`: Supplementary documentation and diagrams.
- `scripts/`: Validation and utility scripts.

## ⚡ Quick Start

```turtle
@prefix edaan: <https://w3id.org/EDAAnOWL/> .
@prefix ids: <https://w3id.org/idsa/core/> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .

# A Data Asset (Supply)
:MyAsset a edaan:DataAsset ;
    edaan:servesObservableProperty <http://aims.fao.org/aos/agrovoc/c_3527> ; # Soil Temperature
    ids:representation [
        a dcat:Distribution ;
        edaan:conformsToProfile :MyTechnicalProfile 
    ] .

# A Smart App (Demand)
:MyApp a edaan:PredictionApp ;
    edaan:requiresObservableProperty <http://aims.fao.org/aos/agrovoc/c_3527> ;
    edaan:requiresProfile :MyTechnicalProfile .
```

## ✍️ Citation

Please reference this work using the metadata in [CITATION.cff](CITATION.cff).
