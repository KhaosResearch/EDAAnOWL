# EDAAnOWL v0.7.0

This is a **minor release** introducing explicit support for measurement units via the [QUDT](https://qudt.org/) ontology, giving EDAAnOWL robust, semantic units of measure rather than simple strings.

## v0.7.0 Highlights

| Change | Impact | Justification |
|--------|--------|---------------|
| **Semantic Standards** | `metricUnit` → `edaan:hasMetricStandard` | Enables referencing standardized QUDT URIs or SKOS ConceptSchemes natively, improving interoperability and machine reasoning for both numerical units and categorical data. [(resolves #35)](https://github.com/KhaosResearch/EDAAnOWL/issues/35) |
| **Operational Meaning** | New Property: `edaan:measuresProperty` | Explicitly links metrics to the `ObservableProperty` they measure (e.g., AGROVOC terms), ensuring type-safe measurements and better matchmaking. |
| **SIEX Rebranding** | New Namespace: `w3id.org/EDAAnOWL/siex/` | Official URI persistence for SIEX vocabularies, removing all legacy Agrixels dependencies. |

---

## Breaking Changes (Migration Required)

### Deprecated Properties

| Deprecated Property | Replacement | Notes |
|---------------------|-------------|-------|
| `:metricUnit` (string) | `:hasMetricStandard` (ObjectProperty → QUDT / SKOS) | Prefer QUDT URIs for units (e.g., `unit:PERCENT`) or SKOS for categorical codes. |
| `:hasMetricUnit` (Object) | `:hasMetricStandard` | Consolidated into standard-agnostic property. |
| `:accessType` (string) | `:accessTypeConcept` (ObjectProperty → `skos:Concept`) | Use a controlled vocabulary for access modes. |
| `:appliesToFeature` (string) | `:appliesToFeatureConcept` (ObjectProperty → `skos:Concept`) | Link to formal schema elements when available. |

> [!NOTE]
> The deprecated string properties are still functional for backward compatibility. However, new implementations should prefer the `*Concept` or URI-based object properties.

---

## Detailed Changes

### 1. Semantic Measurement Standards (QUDT & SKOS)

We have explicitly separated the concept of the phenomenon observed from the standard in which it is measured, using `hasMetricStandard` for both units and categorical vocabularies.

```diff
- :metricUnit rdf:type owl:DatatypeProperty ;
-             rdfs:range xsd:string .
+ :hasMetricStandard rdf:type owl:ObjectProperty .
+ :measuresProperty rdf:type owl:ObjectProperty .
```

**Why?** Previously, units were plain strings. Now, using `:hasMetricStandard`, you can link directly to a standardized URI (e.g., QUDT `unit:KiloGM-PER-HA`) or a SKOS ConceptScheme. The new `:measuresProperty` provides the semantic "bridge" to the phenomenon (e.g., AGROVOC yield) being measured.

---

## Previous v0.6.0 Highlights (Core Semantic Update)

v0.6.0 introduced **deeper alignment with European standards** (DQV, DCAT, PROV) and **vocabulary standardization**.

| Change | Impact | Justification |
|--------|--------|---------------|
| **DQV Alignment** | `:metricType` → `dqv:isMeasurementOf`, `:metricValue` → `dqv:value` | Enables DQV-aware tools to interpret EDAAnOWL metrics natively. |
| **PROV Alignment** | `:computedAt` → `prov:generatedAtTime` | Establishes lineage tracking for metric measurements. |
| **Vocabulary Strategy** | External Normative Vocabs | Removed all local vocabularies (`/vocabularies/`) in favor of global standards. |
| **Validation** | IDSA & DCAT-AP SHACL | Integrated authoritative SHACL shapes for deeper semantic compliance. |

---

### Previous DQV Alignment

We align EDAAnOWL's metric properties with the W3C Data Quality Vocabulary (DQV):

```diff
-:metricType rdf:type owl:ObjectProperty .
+:metricType rdf:type owl:ObjectProperty ;
+            rdfs:subPropertyOf dqv:isMeasurementOf .

-:metricValue rdf:type owl:DatatypeProperty .
+:metricValue rdf:type owl:DatatypeProperty ;
+             rdfs:subPropertyOf dqv:value .
```

**Why?** A `:Metric` in EDAAnOWL is semantically a *measurement* (an observation of a quality dimension), not the *definition* of a metric. This aligns with DQV's distinction between `dqv:Metric` (the definition) and `dqv:QualityMeasurement` (the observation).

### 2. PROV Alignment

```diff
-:computedAt rdf:type owl:DatatypeProperty .
+:computedAt rdf:type owl:DatatypeProperty ;
+            rdfs:subPropertyOf prov:generatedAtTime .
```

**Why?** This allows any PROV-aware tool to trace *when* a quality assertion was made, connecting data quality to provenance chains.

### 3. DCAT-AP Compliance

```diff
 :DataProfile rdf:type owl:Class ;
              rdfs:subClassOf dcterms:Standard .

 :conformsToProfile rdf:type owl:ObjectProperty ;
                    rdfs:subPropertyOf dcterms:conformsTo .
```

**Why?** These alignments were already present in v0.4.x but are now *explicitly documented*. By declaring `:DataProfile` as a subclass of `dct:Standard`, DCAT-AP catalogs can interpret profile conformance without needing to understand EDAAnOWL-specific classes.

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
       └─ :DataRepresentation (EDAAnOWL specialization)
```

**Key Improvements:**
- **Inheritance**: `:DataRepresentation` now explicitly extends `ids:DataRepresentation` (instead of acting as a sibling or generic subclass).
- **Instance Management**: We now use `ids:instance` (range `ids:RepresentationInstance`) to link to artifacts (files) or values, removing the redundant `:instance` property.
- **Standards**: We recommend using `ids:representationStandard` (for technical standards like CSV W3C) alongside `:conformsToProfile` (for semantic/quality profiles).

---

## Vocabulary Strategy (BREAKING CHANGE)

Starting with v0.6.0, EDAAnOWL **no longer bundles local SKOS vocabularies** for domain concepts, observable properties, metrics, or sectors. Instead, we recommend using **established external vocabularies** directly:

| Domain | Recommended Vocabulary | URI Pattern |
|--------|------------------------|-------------|
| Agriculture | [AGROVOC](http://aims.fao.org/aos/agrovoc/) | `http://aims.fao.org/aos/agrovoc/c_*` |
| General Science | [EuroSciVoc](http://data.europa.eu/8mn/) | `http://data.europa.eu/8mn/*` |
| Data Quality | [DQV](http://www.w3.org/ns/dqv#) | `http://www.w3.org/ns/dqv#*` |
| Units | [QUDT](http://qudt.org/vocab/unit/) | `http://qudt.org/vocab/unit/*` |
| Geospatial | [EPSG](http://www.opengis.net/def/crs/EPSG/) | `http://www.opengis.net/def/crs/EPSG/0/*` |

> [!IMPORTANT]
> **Why this change?** EDAAnOWL's purpose is to provide *structure* (classes, properties) for semantic interoperability across data spaces. Domain *content* (concepts, terms) should come from globally recognized vocabularies to maximize cross-domain compatibility.

### Zero-Local Policy
As of v0.6.0, all local vocabulary files (previously in `vocabularies/`) have been removed. Semantic interoperability is now achieved by directly referencing external normative IRIs.

---

## Validation

Starting with v0.6.0, we prioritize authoritative validation:

1. **IDSA Official Shapes**: We include [idsa-shapes.ttl](shapes/idsa-shapes.ttl) for core Information Model compliance.
2. **DCAT-AP Alignment**: We use [dcat-ap-alignment.ttl](shapes/dcat-ap-alignment.ttl) for European data portal compatibility.
3. **Internal EDAAnOWL Shapes**: [edaan-shapes.ttl](shapes/edaan-shapes.ttl) remains as a complementary set for domain-specific rules (profiling, metrics, etc.).

Run the local validation script to verify compliance across all sets:

```powershell
.\scripts\local-validate.bat
```

Or on Linux/macOS:

```bash
./scripts/local-validate.sh
```
