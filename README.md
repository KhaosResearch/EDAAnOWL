# EDAAnOWL: An ontology for annotating data-space assets aligned with IDSA and BIGOWL

[![Deploy Ontology to GitHub Pages](https://github.com/KhaosResearch/EDAAnOWL/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/KhaosResearch/EDAAnOWL/actions/workflows/deploy-docs.yml)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-1f6feb)](https://khaosresearch.github.io/EDAAnOWL/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Ontology Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://w3id.org/EDAAnOWL/1.1.0)
[![Latest Stable Version](https://img.shields.io/badge/latest-1.1.0-green.svg)](https://w3id.org/EDAAnOWL/)
[![PURL](https://img.shields.io/badge/purl-w3id.org-blue)](https://w3id.org/EDAAnOWL/)
[![SHACL Validation](https://img.shields.io/badge/SHACL-Conformant-success)](src/1.0.0/shapes/edaan-shapes.ttl)
[![DCAT-AP-ES Compliance](https://img.shields.io/badge/DCAT--AP--ES-Full%20Compliance-brightgreen.svg)](https://github.com/datosgobes/DCAT-AP-ES)

> **Semantic Bridge for Data Spaces**: Linking IDSA governance with BIGOWL workflows.

## 🚀 Overview

**EDAAnOWL** is a lightweight ontology designed to operationalize Data Spaces. It bridges the gap between the **IDSA Information Model** (governance, contracts) and **BIGOWL** (analytics, workflows), enabling:

- **Full DCAT-AP-ES 1.0.0 Compliance**: Verified by official Spanish Government tools.
- **Atomic DataSpecifications**: Decoupled from technical distribution via `FieldMappings`.
- **Matchmaking 2.0**: Enhanced unit-aware constraints and semantic alignment.
- **Structural Compatibility**: Decoupled "Field Mappings" to link semantic concepts to physical schemas (CSV/Parquet/etc) adding units and types at the edge.
- **Performance & Quality Tracking**: Granular data constraints for DataApps with explicit technical thresholds.
- **Cross-Domain Interoperability**: Decentralized "Specification Libraries" that allow reusing the same semantic definition across different sectors and schemas.

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
    *   **EDAAnOWL's Solution**: We address this challenge by providing a **Cross-Domain Annotation Layer**. By decoupling the *technical mapping* (`FieldMapping`) from *domain semantics* (`DataSpecification`), EDAAnOWL allows assets from diverse sectors to reuse the same semantic library, facilitating the creation of transverse Data Spaces.
*   **Sector-Specific Alignment (SIEX & FEGA)**: To support the [EDAAn Data Space](https://edaan.agora-datalab.eu/), we provide explicit alignment with the **[SIEX (Spain)](https://www3.sede.fega.gob.es/bdcsixpor/catalogos)** catalogs from FEGA.
    *   **Rationale**: These codes are the *de facto* standard for the Spanish agricultural sector, used by participants to manage government aid (CAP/PAC). By transforming these official catalogs into SKOS concepts, we ensure that the data space is immediately operational and intuitive for Spanish users, bridging the gap between administrative requirements and semantic interoperability.

---

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

- **📘 [Architecture](docs/ARCHITECTURE.md)**: High-level view of how IDSA, BIGOWL, and EDAAnOWL fit together.
- **🧩 [Ontology Overview](docs/ONTOLOGY_OVERVIEW_DIAGRAM_ES.md)**: Diagrams and tables explaining Classes (`DataAsset`, `SmartDataApp`) and Properties.
- **💡 [Examples](docs/INTEROPERABILITY_EXAMPLES_ES.md)**: Practical scenarios of semantic interoperability and matchmaking.

## 📦 Repository Structure

- `src/`: Contains the ontology versions (e.g., `1.0.0/`), vocabularies, and SHACL shapes.
- `docs/`: Supplementary documentation and diagrams.
- `scripts/`: Validation and utility scripts.

## ⚡ Quick Start (v1.0.0 Architecture)

```turtle
@prefix edaan: <https://w3id.org/EDAAnOWL/> .
@prefix ids: <https://w3id.org/idsa/core/> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix qudt: <http://qudt.org/vocab/unit/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix theme: <http://publications.europa.eu/resource/authority/data-theme/> .

# 1. Define an Atomic Reusable Specification (e.g., in a Library)
:NDVISpec a edaan:DataSpecification ;
    edaan:hasFeatureOfInterest <http://aims.fao.org/aos/agrovoc/c_12926> ; # Olives
    edaan:hasObservableProperty <http://aims.fao.org/aos/agrovoc/c_ce585e0d> . # NDVI

# 2. A Data Asset (Supply) with a Distribution that MAPS to the spec
:MyAsset a edaan:DataAsset ;
    dcat:theme theme:AGRI ;
    ids:representation :MyDistribution .

:MyDistribution a dcat:Distribution ;
    dct:format <https://www.iana.org/assignments/media-types/text/csv> ;
    edaan:hasFieldMapping [
        a edaan:FieldMapping ;
        edaan:mapsToSpecification :NDVISpec ;
        edaan:mapsField "ndvi_val" ; # Column name in the CSV
        edaan:hasUnit <http://qudt.org/vocab/unit/UNITLESS> ;
        edaan:hasDataType xsd:float ;
        edaan:hasMetric [
            a edaan:Metric ;
            edaan:metricType edaan:Accuracy ;
            edaan:metricValue "0.98"^^xsd:decimal
        ]
    ] .

# 3. Define an App (Demand) with Input Profiles
:MyApp a edaan:DataApp ;
    dcat:theme theme:AGRI ;
    edaan:hasInputProfile [
        a edaan:InputProfile ;
        edaan:hasDataSpecification :NDVISpec ;
        edaan:hasConstraint [
            a edaan:DataConstraint ;
            edaan:requiresUnit <http://qudt.org/vocab/unit/UNITLESS> ;
            edaan:constraintMetricType edaan:Accuracy ;
            edaan:constraintOperator ">=" ;
            edaan:constraintValue "0.95"^^xsd:decimal
        ]
    ] .
```

## ✍️ Citation

Please reference this work using the metadata in [CITATION.cff](CITATION.cff).
