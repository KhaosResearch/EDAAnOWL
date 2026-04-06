# AgoraOWL v0.6.1

This is a **patch release** refining v0.6.0 with critical semantic fixes and documentation cleanup.

## Changelog vs v0.6.0

| Type         | Component    | Description                                                                                                   |
| ------------ | ------------ | ------------------------------------------------------------------------------------------------------------- |
| **Fix**      | Metrics      | Corrected `:metricType` range to `skos:Concept` (MetricType) and aligned `:metricValue` with `dqv:value`.     |
| **Fix**      | DataApps     | Added `:hasPerformanceMetric` to explicitly link DataApps to performance metrics (resolving domain mismatch). |
| **Fix**      | Semantics    | Cleaned up `:hasDomainSector` domain to properly cover both `ids:Resource` and `ids:DataApp`.                 |
| **Refactor** | Credentials  | Decoupled `:VerifiableDataProfile` from `VerifiableCredential` class (now linked via `:hasCredential`).       |
| **Cleanup**  | Vocabularies | Permanently removed legacy local vocabularies from catalog and documentation.                                 |

---

## v0.6.0 Highlights (Core Release)

v0.6.0 introduced **deeper alignment with European standards** (DQV, DCAT, PROV) and **vocabulary standardization**.

| Change                  | Impact                                                              | Justification                                                                   |
| ----------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **DQV Alignment**       | `:metricType` → `dqv:isMeasurementOf`, `:metricValue` → `dqv:value` | Enables DQV-aware tools to interpret AgoraOWL metrics natively.                 |
| **PROV Alignment**      | `:computedAt` → `prov:generatedAtTime`                              | Establishes lineage tracking for metric measurements.                           |
| **Vocabulary Strategy** | External Normative Vocabs                                           | Removed all local vocabularies (`/vocabularies/`) in favor of global standards. |
| **Validation**          | IDSA & DCAT-AP SHACL                                                | Integrated authoritative SHACL shapes for deeper semantic compliance.           |

---

## Breaking Changes (Migration Required)

### Deprecated Properties

| Deprecated Property          | Replacement                                                  | Notes                                          |
| ---------------------------- | ------------------------------------------------------------ | ---------------------------------------------- |
| `:accessType` (string)       | `:accessTypeConcept` (ObjectProperty → `skos:Concept`)       | Use a controlled vocabulary for access modes.  |
| `:appliesToFeature` (string) | `:appliesToFeatureConcept` (ObjectProperty → `skos:Concept`) | Link to formal schema elements when available. |

> [!NOTE]
> The deprecated string properties are still functional for backward compatibility. However, new implementations should prefer the `*Concept` versions.

---

## Detailed Changes

### 1. DQV Alignment

We align AgoraOWL's metric properties with the W3C Data Quality Vocabulary (DQV):

```diff
-:metricType rdf:type owl:ObjectProperty .
+:metricType rdf:type owl:ObjectProperty ;
+            rdfs:subPropertyOf dqv:isMeasurementOf .

-:metricValue rdf:type owl:DatatypeProperty .
+:metricValue rdf:type owl:DatatypeProperty ;
+             rdfs:subPropertyOf dqv:value .
```

**Why?** A `:Metric` in AgoraOWL is semantically a _measurement_ (an observation of a quality dimension), not the _definition_ of a metric. This aligns with DQV's distinction between `dqv:Metric` (the definition) and `dqv:QualityMeasurement` (the observation).

### 2. PROV Alignment

```diff
-:computedAt rdf:type owl:DatatypeProperty .
+:computedAt rdf:type owl:DatatypeProperty ;
+            rdfs:subPropertyOf prov:generatedAtTime .
```

**Why?** This allows any PROV-aware tool to trace _when_ a quality assertion was made, connecting data quality to provenance chains.

### 3. DCAT-AP Compliance

```diff
 :DataProfile rdf:type owl:Class ;
              rdfs:subClassOf dcterms:Standard .

 :conformsToProfile rdf:type owl:ObjectProperty ;
                    rdfs:subPropertyOf dcterms:conformsTo .
```

**Why?** These alignments were already present in v0.4.x but are now _explicitly documented_. By declaring `:DataProfile` as a subclass of `dct:Standard`, DCAT-AP catalogs can interpret profile conformance without needing to understand AgoraOWL-specific classes.

### 4. CRS Range Restriction

```diff
 :hasCRS rdf:type owl:ObjectProperty ;
-        rdfs:range owl:Thing .
+        rdfs:range skos:Concept .
```

**Why?** Using `skos:Concept` enforces the use of controlled vocabularies (like EPSG URIs) and enables better SHACL validation.

### 5. New `*Concept` Properties

Added to replace string-based properties:

- `:accessTypeConcept` (Domain: `ids:Resource`, Range: `skos:Concept`)
- `:appliesToFeatureConcept` (Domain: `:Metric`, Range: `skos:Concept`)

**Why?** Controlled vocabularies enable machine reasoning and interoperability, while string values are error-prone and ambiguous.

---

### 6. Data Representation Hierarchy & IDSA Alignment

We have refined the class hierarchy to strictly follow the IDSA 4.2.0 taxonomy:

```turtle
dcat:Distribution
  └─ ids:DataRepresentation (IDSA Taxonomy)
       └─ :DataRepresentation (AgoraOWL specialization)
```

**Key Improvements:**

- **Inheritance**: `:DataRepresentation` now explicitly extends `ids:DataRepresentation` (instead of acting as a sibling or generic subclass).
- **Instance Management**: We now use `ids:instance` (range `ids:RepresentationInstance`) to link to artifacts (files) or values, removing the redundant `:instance` property.
- **Standards**: We recommend using `ids:representationStandard` (for technical standards like CSV W3C) alongside `:conformsToProfile` (for semantic/quality profiles).

---

## Vocabulary Strategy (BREAKING CHANGE)

Starting with v0.6.0, AgoraOWL **no longer bundles local SKOS vocabularies** for domain concepts, observable properties, metrics, or sectors. Instead, we recommend using **established external vocabularies** directly:

| Domain          | Recommended Vocabulary                       | URI Pattern                               |
| --------------- | -------------------------------------------- | ----------------------------------------- |
| Agriculture     | [AGROVOC](http://aims.fao.org/aos/agrovoc/)  | `http://aims.fao.org/aos/agrovoc/c_*`     |
| General Science | [EuroSciVoc](http://data.europa.eu/8mn/)     | `http://data.europa.eu/8mn/*`             |
| Data Quality    | [DQV](http://www.w3.org/ns/dqv#)             | `http://www.w3.org/ns/dqv#*`              |
| Units           | [QUDT](http://qudt.org/vocab/unit/)          | `http://qudt.org/vocab/unit/*`            |
| Geospatial      | [EPSG](http://www.opengis.net/def/crs/EPSG/) | `http://www.opengis.net/def/crs/EPSG/0/*` |

> [!IMPORTANT]
> **Why this change?** AgoraOWL's purpose is to provide _structure_ (classes, properties) for semantic interoperability across data spaces. Domain _content_ (concepts, terms) should come from globally recognized vocabularies to maximize cross-domain compatibility.

### Zero-Local Policy

As of v0.6.0, all local vocabulary files (previously in `vocabularies/`) have been removed. Semantic interoperability is now achieved by directly referencing external normative IRIs.

---

## Validation

Starting with v0.6.0, we prioritize authoritative validation:

1. **IDSA Official Shapes**: We include [idsa-shapes.ttl](shapes/idsa-shapes.ttl) for core Information Model compliance.
2. **DCAT-AP Alignment**: We use [dcat-ap-alignment.ttl](shapes/dcat-ap-alignment.ttl) for European data portal compatibility.
3. **Internal AgoraOWL Shapes**: [agoraowl-shapes.ttl](shapes/agoraowl-shapes.ttl) remains as a complementary set for domain-specific rules (profiling, metrics, etc.).

Run the local validation script to verify compliance across all sets:

```powershell
.\scripts\local-validate.bat
```

Or on Linux/macOS:

```bash
./scripts/local-validate.sh
```
