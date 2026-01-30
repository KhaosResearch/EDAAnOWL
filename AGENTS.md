# AGENTS.md

> Context file for AI coding agents working on EDAAnOWL.

## Project Overview

| Attribute | Value |
| :--- | :--- |
| **Purpose** | Bridge IDSA (Data Spaces) ↔ BIGOWL (Workflows) for semantic matchmaking |
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

> **EDAAnOWL provides structure, not content.** Use standardized EU/international vocabularies.
> See [CONTRIBUTING.md](CONTRIBUTING.md#external-vocabulary-strategy-v050) for full rationale.

| Domain | Vocabulary | Example URI |
| :--- | :--- | :--- |
| Domain Sectors | [EU Data Theme NAL](http://publications.europa.eu/resource/authority/data-theme) | `theme:AGRI` |
| Data Types | [BIGOWL Data](https://w3id.org/BIGOWLData) | `bigdat:TabularDataSet` |
| Workflows | [BIGOWL Workflows](https://w3id.org/BIGOWLWorkflows) | `bigwf:Component` |
| Agriculture | [AGROVOC](http://aims.fao.org/aos/agrovoc/) | `agrovoc:c_ce585e0d` (NDVI) |
| Data Quality | [DQV](http://www.w3.org/ns/dqv#) | `dqv:Completeness` |
| CRS | [OGC EPSG](http://www.opengis.net/def/crs/EPSG/0/) | `EPSG/0/4326` |
| Spatial Granularity | [EU NUTS](http://publications.europa.eu/resource/authority/nuts) | NUTS codes |
| Access Rights | [EU Access Rights NAL](http://publications.europa.eu/resource/authority/access-right) | `access-right:PUBLIC` |

**BIGOWL Integration:**
- `ids:DataApp` → implements `bigwf:Component` (single processing step)
- Use `:implementsComponent` to link DataApp to BIGOWL Component
- `:realizesWorkflow` is **DEPRECATED** (DataApp = Component, not Workflow)
- Use `bigdat:TabularDataSet`, `bigdat:Image` instead of local `:tabular`, `:georaster`

**Why NO local vocabularies?** (v0.5.0+)
- Local vocabularies require maintenance
- External URIs are interoperable across data spaces
- Authoritative sources (FAO, EU, OGC) already maintain these

---

## Code Patterns

### DataAsset + Representation (v0.5.0)
```turtle
ex:MyAsset a :DataAsset ;
    :servesObservableProperty agrovoc:c_ce585e0d ;  # NDVI (external)
    ids:representation ex:MyAsset_Repr .

ex:MyAsset_Repr a :DataRepresentation ;
    dct:format "text/csv" ;
    dcat:accessURL <https://example.org/data.csv> ;
    dct:license <http://example.org/licenses/CC-BY-4.0> ;
    ids:instance [ a ids:Artifact ; ids:fileName "data.csv" ] ;
    :conformsToProfile ex:MyProfile .

ex:MyProfile a :DataProfile ;
    :declaresDataClass bigdat:TabularDataSet ;  # BIGOWL class
    :declaresObservedProperty agrovoc:c_ce585e0d .
```

---

## Critical Rules

| Rule | Reason |
| :--- | :--- |
| **UTF-8 encoding** | `rdflib` crashes on Latin-1 (Spanish chars). |
| **Use `dct:` not `dcterms:`** | Only `dct:` prefix is declared. |
| **Use `ids:instance`** | Local `:instance` was deprecated in v0.5.0. |
| **Profiles on Distribution** | `:conformsToProfile` domain is `dcat:Distribution`. |
| **Use external URIs** | Use AGROVOC, DQV, BIGOWL etc. instead of local concepts. |
| **Stub definitions in examples** | Add `skos:prefLabel` for external URIs for SHACL. |
| **`ids:fileName` on Artifacts** | Required by SHACL. |

---

## Versioning Process

> **See [CONTRIBUTING.md](CONTRIBUTING.md#automated-release-process-release-please) for detailed guide.**

We use **Release Please** for automated versioning.

1.  **Development**: Work on `feat/` or `fix/` branches.
2.  **Commit**: Use [Conventional Commits](https://www.conventionalcommits.org/):
    - `feat: ...` for features
    - `fix: ...` for bugs
    - `feat!: ...` for breaking changes
3.  **Merge**: Merge to `main`.
4.  **Bot Action**: `release-please` creates a Release PR with updated CHANGELOG.
5.  **Release**: Merging the Release PR triggers the final release and documentation build.

### Manual Steps per Version (still required)
When starting a new version (e.g., 0.6.0), you must still create the folder structure manually *before* the release:
1. For example: `cp -r src/0.5.0/ src/0.6.0/` (being 0.5.0 the previous version).
2. Update `owl:versionIRI` and imports in the new files.
3. Commit these changes as `chore: prepare v0.6.0 folder hierarchy`.

---

## Where to Edit

| Task | File |
| :--- | :--- |
| Add/modify Class or Property | `EDAAnOWL.ttl` |
| Add BIGOWL Data class stubs | `vocabularies/datatype-scheme.ttl` |
| Add validation rule | `shapes/edaan-shapes.ttl` |
| Add/update examples | `examples/*.ttl` |
| Document changes | `CHANGELOG.md` |

---

## References

- **Repo**: [github.com/KhaosResearch/EDAAnOWL](https://github.com/KhaosResearch/EDAAnOWL)
- **Docs**: [khaosresearch.github.io/EDAAnOWL/](https://khaosresearch.github.io/EDAAnOWL/)
- **PID**: [w3id.org/EDAAnOWL/](https://w3id.org/EDAAnOWL/)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
