# EDAAnOWL v0.8.1

This is a **patch release** focused on semantic consistency, validation quality, and discoverability of observable properties.

## v0.8.1 Highlights

| Change | Impact | Justification |
|--------|--------|---------------|
| **DQV Refinement** | Clarifies metric definition vs. metric measurement | Aligns `:Metric`, `:MetricType`, and `:QualityMetric` more cleanly with `dqv:QualityMeasurement` and `dqv:Metric`. |
| **ODRL/DCT Usage Fixes** | Properties used operationally are modeled consistently | Reduces ambiguity between annotation properties and object/data properties used in examples and reasoning. |
| **Validation Consistency** | SHACL accepts the preferred `:conformsToProfile` pattern and validates DQV bridges | Brings shapes, examples, and ontology documentation into alignment. |
| **Observed Properties Bridge Vocabulary** | New `vocabularies/observed-properties.ttl` | Improves discoverability for acronyms like `NDVI`, `NDWI`, `EVI`, etc., while preserving external-first interoperability. |
| **Example Cleanup** | CRED and EO examples updated | Removes literal/IRI mismatches and ensures syntax, SHACL, and OWL reasoning consistency. |

---

## CRED and Validation

EDAAnOWL v0.8.1 includes a complete example (`examples/cred-asset-example.ttl`) demonstrating how to annotate a data space asset following [CRED recommendations](https://espaciosdedatos.gob.es/), covering all 9 entity types:

1. **Catalog** — `dcat:Catalog` aggregating data space resources
2. **Agent** — `foaf:Agent` for publishers and creators
3. **Dataset** — `dcat:Dataset` + `:DataAsset` with full DCAT-AP 3.0 metadata
4. **Distribution** — `dcat:Distribution` with access URL, format, license
5. **DataProfile** — EDAAnOWL semantic profile with metrics
6. **ODRL Policy** — `odrl:Offer` with permissions, prohibitions, and constraints
7. **DataService** — `dcat:DataService` with endpoint and served datasets
8. **Vocabulary-as-Dataset** — Ontology catalogued using CRED library model
9. **Rights & License** — `dct:RightsStatement` and `dct:LicenseDocument` instances

> [!TIP]
> The CRED example demonstrates how EDAAnOWL's unique DataProfile semantics (metrics, observable properties, CRS) complement the standard DCAT-AP cataloguing metadata.

---

## No Breaking Changes

This release is **backward-compatible** with v0.8.0. The changes focus on consistency fixes, bridge vocabulary support, and validation improvements.

---

## Previous v0.7.0 Highlights

v0.7.0 introduced explicit support for measurement units via [QUDT](https://qudt.org/) and SIEX vocabulary rebranding.

| Change | Impact | Justification |
|--------|--------|---------------|
| **Semantic Standards** | `metricUnit` → `edaan:hasMetricStandard` | Enables referencing standardized QUDT URIs or SKOS ConceptSchemes natively. |
| **Operational Meaning** | New Property: `edaan:measuresProperty` | Explicitly links metrics to the `ObservableProperty` they measure. |
| **SIEX Rebranding** | New Namespace: `w3id.org/EDAAnOWL/siex/` | Official URI persistence for SIEX vocabularies. |

---

## Previous v0.6.0 Highlights (Core Semantic Update)

| Change | Impact | Justification |
|--------|--------|---------------|
| **DQV Alignment** | `:metricType` → `dqv:isMeasurementOf`, `:metricValue` → `dqv:value` | Enables DQV-aware tools to interpret EDAAnOWL metrics natively. |
| **PROV Alignment** | `:computedAt` → `prov:generatedAtTime` | Establishes lineage tracking for metric measurements. |
| **Vocabulary Strategy** | External-First + Bridge Vocabs | Use external normative IRIs by default, plus minimal local bridge vocabularies when they improve discoverability or provide missing concepts. |
| **Validation** | IDSA & DCAT-AP SHACL | Integrated authoritative SHACL shapes for deeper semantic compliance. |

---

## Vocabulary Strategy

EDAAnOWL follows an **external-first vocabulary strategy**. We recommend using **established external vocabularies** directly whenever they are sufficient, while allowing **minimal local bridge vocabularies** for cases such as acronyms, aliases, curated alignments, or missing concepts:

| Domain | Recommended Vocabulary | URI Pattern |
|--------|------------------------|-------------|
| Agriculture (Global) | [AGROVOC](http://aims.fao.org/aos/agrovoc/) | `http://aims.fao.org/aos/agrovoc/c_*` |
| Agriculture (Spain) | [SIEX (local)](vocabularies/siex.ttl) | `https://w3id.org/EDAAnOWL/siex/kos/*` |
| Observable Properties (bridge) | [Observed Properties (local)](vocabularies/observed-properties.ttl) | `https://w3id.org/EDAAnOWL/*` |
| Units of Measure | [QUDT](http://qudt.org/vocab/unit/) | `http://qudt.org/vocab/unit/*` |
| Data Quality | [DQV](http://www.w3.org/ns/dqv#) | `http://www.w3.org/ns/dqv#*` |
| General Science | [EuroSciVoc](http://data.europa.eu/8mn/) | `http://data.europa.eu/8mn/*` |
| Geospatial | [EPSG](http://www.opengis.net/def/crs/EPSG/) | `http://www.opengis.net/def/crs/EPSG/0/*` |
| Data Themes | [EU NAL](http://publications.europa.eu/resource/authority/data-theme/) | `http://publications.europa.eu/resource/authority/data-theme/*` |
| Languages | [EU NAL](http://publications.europa.eu/resource/authority/language/) | `http://publications.europa.eu/resource/authority/language/*` |
| File Types | [EU NAL](http://publications.europa.eu/resource/authority/file-type/) | `http://publications.europa.eu/resource/authority/file-type/*` |

> [!IMPORTANT]
> **Why this approach?** EDAAnOWL provides *structure* (classes, properties) for semantic interoperability. Domain *content* should come primarily from globally recognized vocabularies. Local bridge vocabularies are used only when they add practical value, such as stable acronyms (`NDVI`), lexical normalization, or explicit mappings to external terms.

---

## Validation

1. **IDSA Official Shapes**: [idsa-shapes.ttl](shapes/idsa-shapes.ttl) for core Information Model compliance.
2. **DCAT-AP Alignment**: [dcat-ap-alignment.ttl](shapes/dcat-ap-alignment.ttl) for European data portal compatibility.
3. **Internal EDAAnOWL Shapes**: [edaan-shapes.ttl](shapes/edaan-shapes.ttl) for domain-specific rules.
4. **CRED Alignment Shapes**: [cred-alignment-shapes.ttl](shapes/cred-alignment-shapes.ttl) for Spanish Data Office (CRED) compliance.

Run the local validation script to verify compliance:

```powershell
.\scripts\local-validate.bat
```

Or on Linux/macOS:

```bash
./scripts/local-validate.sh
```

