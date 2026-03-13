# EDAAnOWL v0.9.0

This release introduces major semantic enhancements focused on the decoupling of subjects and properties, alignment with planetary-scale observation standards, and refined data space metadata.

## v0.9.0 Highlights

| Change | Impact | Justification |
|--------|--------|---------------|
| **Features of Interest** | New class: `:FeatureOfInterest` (SOSA aligned) | Decouples the subject of study (e.g., a "Crop Plot" or "Building") from the measured properties (e.g., "NDVI" or "Temperature"). |
| **SOSA/SSN Alignment** | Deep integration with W3C SOSA | Enables better interoperability with IoT and Earth Observation platforms by using standard patterns for observations and sampling. |
| **DQV/CRED Refinement** | Improved alignment with DQV and Spanish CRED | Ensures that quality metrics and data space annotations are strictly compliant with the latest interoperability guidelines. |
| **Validation Suite** | Enhanced SHACL shapes and consistency rules | Improved automated checks for profile completeness and semantic integrity across all modules. |
| **Vocabulary Updates** | Enriched bridge vocabularies | Added more precise alignments for agricultural and spectral concepts in `observed-properties.ttl`. |

---

## Decoupling with Features of Interest

In previous versions, properties were often implicitly tied to a measurement context. Version 0.9.0 introduces explicit support for `edaan:declaresFeatureOfInterest`:

*   **ObservableProperty**: What is being measured (e.g., Nitrogen content).
*   **FeatureOfInterest**: What the property belongs to (e.g., a specific Parcel or a Crop type).

This allows a single `DataProfile` to describe complex datasets where multiple characteristics of different features are reported together.

---

## CRED and Metadata Refinement

EDAAnOWL v0.9.0 continues to track the [CRED recommendations](https://espaciosdedatos.gob.es/) from the Spanish Data Office, ensuring that `dcat:Catalog`, `dcat:Dataset`, and `dcat:Distribution` metadata follow the UNE 0087:2025 standard.

> [!TIP]
> The updated validation shapes now strictly verify that every `DataAsset` is correctly catalogued and that its profile metrics are linked to the appropriate `ObservableProperty`.

---

## Evolution from v0.8.1

While v0.8.1 focused on patch consistency and labels, v0.9.0 is a **minor release** that expands the semantic expressiveness of the model without breaking backward compatibility for standard profile-conformance patterns.

---

## Vocabulary Strategy

EDAAnOWL remains **external-first**. Key normative vocabularies integrated in v0.9.0:

| Domain | Recommended Vocabulary | URI Pattern |
|--------|------------------------|-------------|
| Observations/IoT | [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/) | `http://www.w3.org/ns/sosa/*` |
| Agriculture | [AGROVOC](http://aims.fao.org/aos/agrovoc/) | `http://aims.fao.org/aos/agrovoc/c_*` |
| Data Quality | [DQV](http://www.w3.org/ns/dqv#) | `http://www.w3.org/ns/dqv#*` |
| Spanish Sector | [SIEX (local)](vocabularies/siex.ttl) | `https://w3id.org/EDAAnOWL/0.9.0/vocabularies/siex/*` |

---

## Validation

Run the updated validation suite:

```powershell
.\scripts\local-validate.bat
```

Or on Linux/macOS:

```bash
./scripts/local-validate.sh
```
