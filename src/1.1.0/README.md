# AgoraOWL v1.1.0

This release achieves **Full DCAT-AP-ES 1.0.0 Compliance**, verified by official Spanish Government validation tools. It refines the v1.0.0 architecture introduced in the previous release with stricter metadata and surgical SHACL constraints.

## v1.1.0 Highlights (Full Compliance)

| Change                        | Impact                        | Justification                                                                                              |
| ----------------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **DCAT-AP-ES Compliance**     | 100% Green Validation         | Verified against official Spanish Government SHACL shapes using Dockerized validation.                     |
| **Surgical SHACL Targets**    | Prevents technical leakage    | Renamed distribution shapes and calibrated targets to only affect technical representations, not Catalogs. |
| **Standardized Metadata**     | Authoritative Agents/Contacts | Integrated DIR3-compliant IRIs and mandatory vCard recommended fields for Spanish data portals.            |
| **Atomic DataSpecifications** | Semantic variables refined    | Maintains the v1.0.0 decoupling while adding explicit Agrovoc types for broader interoperability.          |

---

## v1.1.0 Architecture

The previous monolithic profile approach has been evolved into a modular, three-layer model:

1. **Semantic Layer (`DataSpecification`)**: Atomic units defining the domain logic (e.g., "Olive Temperature", "Soil Moisture"). These contain NO technical details, units, or column names.
2. **Binding Layer (`FieldMapping`)**: Connects the atomic specification to a physical distribution, specifying the field name (`mapsField`), units (`qudt:Unit`), data type and metrics.
3. **Technical Layer (`Distribution`)**: Centralizes all physical properties (format, temporal/spatial resolution, CRS) following DCAT-AP 3.0.

### Why this change?

- **Massive Reuse**: A single `DataSpecification` for "NDVI" can be reused by thousands of different datasets regardless of their internal column naming or units.
- **High-Performance Matchmaking**: Discovery can be performed by simple URI comparison of specifications, while quality-aware matchmaking handles mission-critical constraints (via `DataConstraint`).
- **Standard Compliance**: Better alignment with DCAT-AP 3.0, QUDT, and SOSA.

---

---

<details>
<summary><b>v0.7.0 Highlights (Semantic Data Matching)</b></summary>

| Feature                    | Description                                              |
| :------------------------- | :------------------------------------------------------- |
| **DataProfile class**      | New structure for grouping multiple semantic variables.  |
| **hasMetricStandard**      | Formal link to QUDT units and statistical metrics.       |
| **measuresProperty**       | Direct link between a profile and its observed property. |
| **Unit-Aware Matchmaking** | Compatibility logic based on unit normalization.         |

</details>

<details>
<summary><b>v0.6.0 Highlights (IDSA & BIGOWL Alignment)</b></summary>

| Feature                        | Description                                      |
| :----------------------------- | :----------------------------------------------- |
| **ids:Resource Alignment**     | Native support for IDSA core conceptual model.   |
| **bigwf:Workflow Integration** | Linking DataApps to BIGOWL analytical pipelines. |
| **Technical Resolution**       | Properties for spatial and temporal granularity. |

</details>

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
