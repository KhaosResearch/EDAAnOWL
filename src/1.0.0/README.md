# AgoraOWL v1.0.0

This is a **major release** introducing a refactored architecture for data asset description, focused on extreme reusability, schema-agnostic semantic profiles, and high-precision matchmaking.

## v1.0.0 Highlights (Structural Evolution)

| Change                           | Impact                                   | Justification                                                                                                                       |
| -------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Atomic DataSpecifications**    | Semantic variables are now pure          | Decouples "What is being measured" from "How it is stored", enabling a reusable Library of semantic variables.                      |
| **FieldMapping**                 | New bridge class for mapping             | Links atomic specifications to specific physical fields (`mapsField`) within a distribution.                                        |
| **InputProfile / OutputProfile** | Advanced DataApp profiles                | Allows Apps to define complex inputs/outputs as a group of specifications.                                                          |
| **DataConstraints**              | Granular data thresholds                 | Enables matchmaking based on technical or quality metrics (e.g., requiresUnit, requiresMetric).                                     |
| **DCAT-AP 3.0 Alignment**        | Technical metadata moved to Distribution | Adheres to standard practices by placing resolutions and CRS at the distribution level, keeping specifications semantically "pure". |

---

## The New v1.0.0 Architecture

The previous monolithic profile approach has been evolved into a modular, three-layer model:

1. **Semantic Layer (`DataSpecification`)**: Atomic units defining the domain logic (e.g., "Olive Temperature", "Soil Moisture"). These contain NO technical details, units, or column names.
2. **Binding Layer (`FieldMapping`)**: Connects the atomic specification to a physical distribution, specifying the field name (`mapsField`), units (`qudt:Unit`), data type and metrics.
3. **Technical Layer (`Distribution`)**: Centralizes all physical properties (format, temporal/spatial resolution, CRS) following DCAT-AP 3.0.

### Why this change?

- **Massive Reuse**: A single `DataSpecification` for "NDVI" can be reused by thousands of different datasets regardless of their internal column naming or units.
- **High-Performance Matchmaking**: Discovery can be performed by simple URI comparison of specifications, while quality-aware matchmaking handles mission-critical constraints (via `DataConstraint`).
- **Standard Compliance**: Better alignment with DCAT-AP 3.0, QUDT, and SOSA.

---

## CRED and Validation

1. **Catalog** — `dcat:Catalog` aggregating data space resources
2. **Agent** — `foaf:Agent` for publishers and creators
3. **Dataset** — `dcat:Dataset` + `:DataAsset` with full DCAT-AP 3.0 metadata
4. **Distribution** — `dcat:Distribution` with access URL, format, license
5. **DataProfile & DataSpecification** — AgoraOWL semantic profiles referencing specific variables
6. **ODRL Policy** — `odrl:Offer` with permissions, prohibitions, and constraints
7. **DataService** — `dcat:DataService` with endpoint and served datasets
8. **Vocabulary-as-Dataset** — Ontology catalogued using CRED library model
9. **Rights & License** — `dct:RightsStatement` and `dct:LicenseDocument` instances

> [!TIP]
> The CRED example demonstrates how AgoraOWL's unique DataSpecification semantics (metrics, properties, CRS) complement the standard DCAT-AP cataloguing metadata.

---

## Breaking Changes (Cleanup)

Version 1.0.0 is a **major release** that streamlines the ontology by removing 8 redundant properties that previously bypassed the modular architecture. This ensures a single, clear path for semantic discovery and matchmaking.

| Removed Property              | Replacement / Strategy                               |
| ----------------------------- | ---------------------------------------------------- |
| `:requiresObservableProperty` | Use `hasInputProfile → hasDataSpecification`.        |
| `:requiresFeatureOfInterest`  | Use `hasInputProfile → hasDataSpecification`.        |
| `:producesObservableProperty` | Use `producesProfile → OutputProfile`.               |
| `:producesFeatureOfInterest`  | Use `producesProfile → OutputProfile`.               |
| `:servesObservableProperty`   | Inherited from Bound Specification via Distribution. |
| `:declaresObservedProperty`   | Use `:hasObservableProperty`.                        |
| `:declaresFeatureOfInterest`  | Use `:hasFeatureOfInterest`.                         |
| `:conformsToProfile`          | Use `hasFieldMapping → mapsToSpecification`.         |

---

## Previous v0.7.0 Highlights

v0.7.0 introduced explicit support for measurement units via [QUDT](https://qudt.org/) and SIEX vocabulary rebranding.

| Change                  | Impact                                      | Justification                                                               |
| ----------------------- | ------------------------------------------- | --------------------------------------------------------------------------- |
| **Semantic Standards**  | `metricUnit` → `agoraowl:hasMetricStandard` | Enables referencing standardized QUDT URIs or SKOS ConceptSchemes natively. |
| **Operational Meaning** | New Property: `agoraowl:measuresProperty`   | Explicitly links metrics to the `ObservableProperty` they measure.          |
| **SIEX Rebranding**     | New Namespace: `w3id.org/AgoraOWL/siex/`    | Official URI persistence for SIEX vocabularies.                             |

---

## Previous v0.6.0 Highlights (Core Semantic Update)

| Change                  | Impact                                                              | Justification                                                                                                                                 |
| ----------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **DQV Alignment**       | `:metricType` → `dqv:isMeasurementOf`, `:metricValue` → `dqv:value` | Enables DQV-aware tools to interpret AgoraOWL metrics natively.                                                                               |
| **PROV Alignment**      | `:computedAt` → `prov:generatedAtTime`                              | Establishes lineage tracking for metric measurements.                                                                                         |
| **Vocabulary Strategy** | External-First + Bridge Vocabs                                      | Use external normative IRIs by default, plus minimal local bridge vocabularies when they improve discoverability or provide missing concepts. |
| **Validation**          | IDSA & DCAT-AP SHACL                                                | Integrated authoritative SHACL shapes for deeper semantic compliance.                                                                         |

---

## Vocabulary Strategy

AgoraOWL follows an **external-first vocabulary strategy**. We recommend using **established external vocabularies** directly whenever they are sufficient, while allowing **minimal local bridge vocabularies** for cases such as acronyms, aliases, curated alignments, or missing concepts:

| Domain                         | Recommended Vocabulary                                                 | URI Pattern                                                     |
| ------------------------------ | ---------------------------------------------------------------------- | --------------------------------------------------------------- |
| Agriculture (Global)           | [AGROVOC](http://aims.fao.org/aos/agrovoc/)                            | `http://aims.fao.org/aos/agrovoc/c_*`                           |
| Agriculture (Spain)            | [SIEX (local)](vocabularies/siex.ttl)                                  | `https://w3id.org/AgoraOWL/siex/kos/*`                          |
| Observable Properties (bridge) | [Observed Properties (local)](vocabularies/observed-properties.ttl)    | `https://w3id.org/AgoraOWL/*`                                   |
| Units of Measure               | [QUDT](http://qudt.org/vocab/unit/)                                    | `http://qudt.org/vocab/unit/*`                                  |
| Data Quality                   | [DQV](http://www.w3.org/ns/dqv#)                                       | `http://www.w3.org/ns/dqv#*`                                    |
| General Science                | [EuroSciVoc](http://data.europa.eu/8mn/)                               | `http://data.europa.eu/8mn/*`                                   |
| Geospatial                     | [EPSG](http://www.opengis.net/def/crs/EPSG/)                           | `http://www.opengis.net/def/crs/EPSG/0/*`                       |
| Data Themes                    | [EU NAL](http://publications.europa.eu/resource/authority/data-theme/) | `http://publications.europa.eu/resource/authority/data-theme/*` |
| Languages                      | [EU NAL](http://publications.europa.eu/resource/authority/language/)   | `http://publications.europa.eu/resource/authority/language/*`   |
| File Types                     | [EU NAL](http://publications.europa.eu/resource/authority/file-type/)  | `http://publications.europa.eu/resource/authority/file-type/*`  |

> [!IMPORTANT]
> **Why this approach?** AgoraOWL provides _structure_ (classes, properties) for semantic interoperability. Domain _content_ should come primarily from globally recognized vocabularies. Local bridge vocabularies are used only when they add practical value, such as stable acronyms (`NDVI`), lexical normalization, or explicit mappings to external terms.

---

## Validation

1. **IDSA Official Shapes**: [idsa-shapes.ttl](shapes/idsa-shapes.ttl) for core Information Model compliance.
2. **DCAT-AP Alignment**: [dcat-ap-alignment.ttl](shapes/dcat-ap-alignment.ttl) for European data portal compatibility.
3. **Internal AgoraOWL Shapes**: [agoraowl-shapes.ttl](shapes/agoraowl-shapes.ttl) for domain-specific rules.
4. **CRED Alignment Shapes**: [cred-alignment-shapes.ttl](shapes/cred-alignment-shapes.ttl) for Spanish Data Office (CRED) compliance.

Run the local validation script to verify compliance:

```powershell
.\scripts\local-validate.bat
```

Or on Linux/macOS:

```bash
./scripts/local-validate.sh
```
