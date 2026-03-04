# EDAAnOWL v0.8.0

This is a **minor release** that adds full alignment with **CRED recommendations** (UNE 0087:2025) for annotating data space assets, including DCAT-AP 3.0 cataloguing, ODRL 2.2 policy model, FOAF agents, and ADMS metadata.

## v0.8.0 Highlights

| Change | Impact | Justification |
|--------|--------|---------------|
| **DCAT-AP 3.0 Catalog** | New classes: `dcat:Catalog`, `dcat:DataService` | Enables complete cataloguing of data space resources following the CRED model. |
| **ODRL 2.2 Policy Model** | New classes: `odrl:Policy`, `odrl:Offer`, `odrl:Rule`, `odrl:Constraint` + properties: `odrl:hasPolicy`, `odrl:target`, `odrl:prohibition`, `odrl:obligation`, `odrl:assigner` | Full ODRL policy model for expressing usage conditions on assets as recommended by CRED. |
| **FOAF Agent** | New class: `foaf:Agent` + property: `foaf:name` | Enables representing publishers and creators as structured entities (DCAT-AP 3.0 mandatory). |
| **DCAT-AP Properties** | `dcat:dataset`, `dcat:distribution`, `dcat:accessURL`, `dcat:endpointURL`, `dcat:servesDataset`, `dcat:landingPage`, `dcat:mediaType`, `dcat:keyword`, `dcat:byteSize`, `dcat:service` | Complete DCAT-AP 3.0 property coverage for datasets, distributions, and services. |
| **Dublin Core Extensions** | `dct:publisher`, `dct:spatial`, `dct:accessRights`, `dct:rights`, `dct:language`, `dct:type`, `dct:accrualPeriodicity`, `dct:format`, `dct:identifier`, `dct:issued` | Full Dublin Core metadata coverage as required by DCAT-AP 3.0. |
| **ADMS / DCATAP** | `adms:status`, `adms:versionNotes`, `dcatap:applicableLegislation` | Vocabulary lifecycle metadata and applicable legislation support. |
| **Supporting Classes** | `dct:Location`, `dct:RightsStatement`, `dct:LicenseDocument`, `dct:Frequency`, `dct:LinguisticSystem`, `dct:MediaTypeOrExtent`, `time:DurationDescription` | Required range classes for properly typed DCAT-AP metadata. |

---

## New: CRED-Compliant Asset Annotation

EDAAnOWL v0.8.0 includes a complete example (`examples/cred-asset-example.ttl`) demonstrating how to annotate a data space asset following [CRED recommendations](https://espaciosdedatos.gob.es/), covering all 9 entity types:

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

This release is **fully backward-compatible** with v0.7.0. All new additions are external URI declarations (lightweight bridges) — no existing classes or properties are modified or deprecated.

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
| **Vocabulary Strategy** | External Normative Vocabs | Removed all local vocabularies in favor of global standards. |
| **Validation** | IDSA & DCAT-AP SHACL | Integrated authoritative SHACL shapes for deeper semantic compliance. |

---

## Vocabulary Strategy

EDAAnOWL **does not bundle local SKOS vocabularies** for domain concepts. Instead, we recommend using **established external vocabularies** directly:

| Domain | Recommended Vocabulary | URI Pattern |
|--------|------------------------|-------------|
| Agriculture (Global) | [AGROVOC](http://aims.fao.org/aos/agrovoc/) | `http://aims.fao.org/aos/agrovoc/c_*` |
| Agriculture (Spain) | [SIEX (local)](vocabularies/siex.ttl) | `https://w3id.org/EDAAnOWL/siex/kos/*` |
| Units of Measure | [QUDT](http://qudt.org/vocab/unit/) | `http://qudt.org/vocab/unit/*` |
| Data Quality | [DQV](http://www.w3.org/ns/dqv#) | `http://www.w3.org/ns/dqv#*` |
| General Science | [EuroSciVoc](http://data.europa.eu/8mn/) | `http://data.europa.eu/8mn/*` |
| Geospatial | [EPSG](http://www.opengis.net/def/crs/EPSG/) | `http://www.opengis.net/def/crs/EPSG/0/*` |
| Data Themes | [EU NAL](http://publications.europa.eu/resource/authority/data-theme/) | `http://publications.europa.eu/resource/authority/data-theme/*` |
| Languages | [EU NAL](http://publications.europa.eu/resource/authority/language/) | `http://publications.europa.eu/resource/authority/language/*` |
| File Types | [EU NAL](http://publications.europa.eu/resource/authority/file-type/) | `http://publications.europa.eu/resource/authority/file-type/*` |

> [!IMPORTANT]
> **Why this approach?** EDAAnOWL provides *structure* (classes, properties) for semantic interoperability. Domain *content* (concepts, terms) should come from globally recognized vocabularies to maximize cross-domain compatibility.

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
