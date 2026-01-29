# AGENTS.md

> Context file for AI coding agents working on EDAAnOWL.

## Project Overview

| Attribute | Value |
| :--- | :--- |
| **Purpose** | Bridge IDSA (Data Spaces with different domains) ↔ BIGOWL (Workflows) for semantic matchmaking |
| **Namespace** | `https://w3id.org/EDAAnOWL/` |
| **Version** | `0.5.0` (see `src/0.5.0/`) |
| **Language** | OWL/Turtle (`.ttl`) |

### Key Standards
- [IDSA Information Model](https://international-data-spaces-association.github.io/InformationModel/docs/index.html)
- [DCAT v3](https://www.w3.org/TR/vocab-dcat-3/) / [DCAT-AP 3.0](https://semiceu.github.io/DCAT-AP/releases/3.0.1/)
- [SHACL](https://www.w3.org/TR/shacl/), [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/), [PROV-O](https://www.w3.org/TR/prov-o/)

---

## Build & Validation

```bash
# Full validation (RDF syntax + SHACL + OWL consistency)
./scripts/local-validate.sh   # Linux/Mac
.\scripts\local-validate.bat  # Windows

# Individual checks
python scripts/check_rdf.py        # Syntax only
python scripts/validate_shacl.py   # SHACL shapes
```

**Expected output**: `✅ All SHACL validations passed!`

---

## External Vocabulary Strategy (v0.5.0+)

**EDAAnOWL provides structure, not content.** Use external standardized vocabularies for domain concepts:

| Domain | Vocabulary | Example URI |
| :--- | :--- | :--- |
| Agriculture | [AGROVOC](http://aims.fao.org/aos/agrovoc/) | `agrovoc:c_ce585e0d` (NDVI) |
| Data Quality | [DQV](http://www.w3.org/ns/dqv#) | `dqv:completeness` |
| Units | [QUDT](http://qudt.org/vocab/unit/) | `unit:DEG_C` |
| Geospatial | [EPSG](http://www.opengis.net/def/crs/EPSG/) | `EPSG/0/4326` |

**Find correct codes** in `vocabularies/observed-properties.ttl` and `vocabularies/agro-vocab.ttl` (look for `skos:exactMatch`).

**In examples**, add stub definitions for SHACL validation:
```turtle
agrovoc:c_ce585e0d a skos:Concept ;  # NDVI - verified from observed-properties.ttl
    skos:prefLabel "NDVI"@en .
```

---

## Code Patterns

### DataAsset + Representation (v0.5.0)
```turtle
ex:MyAsset a :DataAsset ;
    :servesObservableProperty agrovoc:c_ce585e0d ;  # NDVI (verified)
    ids:representation ex:MyAsset_Repr .

ex:MyAsset_Repr a :DataRepresentation ;
    dct:format "text/csv" ;
    dcat:accessURL <https://example.org/data.csv> ;
    dct:license <http://example.org/licenses/CC-BY-4.0> ;
    ids:instance [ a ids:Artifact ; ids:fileName "data.csv" ] ;
    :conformsToProfile ex:MyProfile .
```

---

## Critical Rules

| Rule | Reason |
| :--- | :--- |
| **UTF-8 encoding** | `rdflib` crashes on Latin-1 (Spanish chars). |
| **Use `dct:` not `dcterms:`** | Only `dct:` prefix is declared. |
| **Use `ids:instance`** | Local `:instance` was deprecated in v0.5.0. |
| **Profiles on Distribution** | `:conformsToProfile` domain is `dcat:Distribution`. |
| **Use external URIs** | Use AGROVOC, DQV, etc. instead of local concepts. |
| **Stub definitions in examples** | Add `skos:prefLabel` for external URIs. |
| **`ids:fileName` on Artifacts** | Required by SHACL. |

---

## Where to Edit

| Task | File |
| :--- | :--- |
| Add/modify Class or Property | `EDAAnOWL.ttl` |
| Add EDAAnOWL-specific data class | `vocabularies/datatype-scheme.ttl` |
| Add validation rule | `shapes/edaan-shapes.ttl` |
| Add/update examples | `examples/*.ttl` |

---

## References

- **Repo**: [github.com/KhaosResearch/EDAAnOWL](https://github.com/KhaosResearch/EDAAnOWL)
- **Docs**: [khaosresearch.github.io/EDAAnOWL/](https://khaosresearch.github.io/EDAAnOWL/)
- **PID**: [w3id.org/EDAAnOWL/](https://w3id.org/EDAAnOWL/)
