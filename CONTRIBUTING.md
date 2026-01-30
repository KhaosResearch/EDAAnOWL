# How to Contribute

Thank you for your interest in contributing to EDAAnOWL!

## Reporting Issues

If you find a bug, inconsistency, or have a feature request, please [open an Issue](https://github.com/KhaosResearch/EDAAnOWL/issues) in the repository.

## Submitting Changes (General Contributions)

For minor fixes or feature additions that don't constitute a new version:

1.  **Fork & Branch:** Fork the repository and create a descriptive branch from the `main` branch.

    ```bash
    # Make sure your main is up to date
    git checkout main
    git pull origin main

    # Create your new branch (e.g., feature/new-metrics)
    git checkout -b feature/new-metrics
    ```

2.  **Make Changes:** Modify the necessary `.ttl` files _within the latest version's folder_ (e.g., `src/0.5.0/`).
3.  **Run Validation:** Execute `python scripts/check_rdf.py && python scripts/validate_shacl.py`.
4.  **Commit & Push:** Commit your changes following [Conventional Commits](https://www.conventionalcommits.org/).
5.  **Open a Pull Request:** Submit a PR against the `main` branch.

---

## Automated Release Process (Release Please)

We use [Google Release Please](https://github.com/google-github-actions/release-please-action) to automate versioning and changelog generation.

### How it works

1.  **Commit Messages**: All commits must follow [Conventional Commits](https://www.conventionalcommits.org/).
    - `feat:` → Minor version bump (e.g., 0.5.0 → 0.6.0)
    - `fix:` → Patch version bump (e.g., 0.5.0 → 0.5.1)
    - `feat!:` or `BREAKING CHANGE:` → Major version bump
    - `docs:`, `chore:`, etc. → No release trigger (unless configured)

2.  **Release PR**: When changes are merged into the `main` branch, the **release-please** bot automatically checks commits since the last release.
    - If there are user-facing changes (`feat`, `fix`), it opens a **Release PR**.
    - This PR contains:
        - Updated `CHANGELOG.md`
        - Updated `.release-please-manifest.json` versions

3.  **Publishing**:
    - **Review** the Release PR created by the bot.
    - **Merge** the Release PR.
    - Only then will the bot:
        - Create a GitHub Release tag (`vX.Y.Z`).
        - Trigger the `release.yml` workflow to build/publish documentation.

### Developer Workflow

You do **NOT** need to manually update `CHANGELOG.md` or version numbers. Just write good commit messages!

```bash
git commit -m "feat: add support for new bigowl components"
git commit -m "fix: correct typo in owl:imports"
git commit -m "docs: update contributor guide"
```

---

## External Vocabulary Strategy (v0.5.0+)

> [!IMPORTANT]
> **EDAAnOWL does NOT import local vocabularies.** We use external standardized URIs directly.

### Why External Vocabularies?

1. **Maintenance burden**: Local vocabularies require constant updates
2. **Interoperability**: External URIs are recognized across data spaces
3. **Authority**: FAO, EU, OGC maintain authoritative vocabularies
4. **Alignment**: External vocabularies already have SKOS mappings

### Recommended Vocabularies

| Domain | Vocabulary | URI Pattern |
|--------|------------|-------------|
| Agriculture | AGROVOC | `http://aims.fao.org/aos/agrovoc/c_*` |
| Data Themes | EU Data Theme NAL | `http://publications.europa.eu/resource/authority/data-theme/*` |
| Data Types | BIGOWL Data | `https://w3id.org/BIGOWLData/*` |
| Quality | W3C DQV | `http://www.w3.org/ns/dqv#*` |
| CRS | OGC EPSG | `http://www.opengis.net/def/crs/EPSG/0/*` |

### What About Local Vocabulary Files?

Files in `vocabularies/` are **reference documents only**:
- `datatype-scheme.ttl` - Alignment with BIGOWL Data classes
- `metric-types.ttl` - DQV-aligned metric instances
- `data-theme.ttl` - EU NAL stubs for SHACL validation

They are NOT owl:imported by the main ontology.

### For Examples & SHACL Validation

Add stub definitions for external concepts:

```turtle
agrovoc:c_ce585e0d a skos:Concept ;
    skos:prefLabel "NDVI"@en .

bigdat:TabularDataSet a owl:Class ;
    rdfs:subClassOf bigdat:Data .
```

---

## Versioning Checklist (Quick Reference)

Use this checklist before every release:

```markdown
- [ ] New `src/X.Y.Z/` folder created
- [ ] `EDAAnOWL.ttl`: owl:versionIRI, owl:versionInfo, owl:priorVersion
- [ ] `EDAAnOWL.ttl`: All owl:imports point to X.Y.Z paths
- [ ] `vocabularies/*.ttl`: @base and owl:Ontology URIs updated
- [ ] `shapes/*.ttl`: Updated for new classes/properties
- [ ] `examples/*.ttl`: Valid against new ontology
- [ ] `src/X.Y.Z/README.md`: Updated
- [ ] `src/X.Y.Z/index.html`: Updated
- [ ] `CHANGELOG.md`: New version section added
- [ ] `CITATION.cff`: Version and date updated
- [ ] `README.md` (root): Latest version notes
- [ ] `SECURITY.md`: Supported versions updated
- [ ] `images/`: Diagrams consistent with ontology
- [ ] Validation passes: `check_rdf.py`, `validate_shacl.py`
```
