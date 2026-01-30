# How to Contribute

Thank you for your interest in contributing to EDAAnOWL!

## Reporting Issues

If you find a bug, inconsistency, or have a feature request, please [open an Issue](https://github.com/KhaosResearch/EDAAnOWL/issues) in the repository.

## Submitting Changes (General Contributions)

For minor fixes or feature additions that don't constitute a new version:

1.  **Fork & Branch:** Fork the repository and create a descriptive branch from the `dev` branch.

    ```bash
    # Make sure your dev is up to date
    git checkout dev
    git pull origin dev

    # Create your new branch
    git checkout -b fix/correct-typo-in-profile
    ```

2.  **Make Changes:** Modify the necessary `.ttl` files _within the latest version's folder_ (e.g., `src/0.5.0/`).
3.  **Run Validation:** Execute `python scripts/check_rdf.py && python scripts/validate_shacl.py`.
4.  **Commit & Push:** Commit your changes following [Conventional Commits](https://www.conventionalcommits.org/) and push to your fork.
5.  **Open a Pull Request:** Submit a PR against the `dev` branch using the [PR template](.github/pull_request_template.md).

---

## How to Publish a New Version (Core Maintainer Process)

Publishing a new version is a semi-automated process. It requires preparing all files in the `dev` branch, merging them into `main`, and then creating a GitHub Release.

### Version Numbering (Semantic Versioning)

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (X.0.0): Breaking changes (removed classes, changed property domains)
- **MINOR** (0.X.0): New features (new classes, properties, vocabularies)
- **PATCH** (0.0.X): Bug fixes, documentation updates

For breaking changes in commits, use:
```
feat!: description

BREAKING CHANGE: details of what breaks
```

---

### Step 1: Prepare the New Version on the `dev` Branch

All new development happens on the `dev` branch (or feature branches merged into it).

#### 1.1 Duplicate the Version Folder

```bash
cp -r src/0.4.0/ src/0.5.0/
```

#### 1.2 Update Version Metadata

Update these files with the new version number:

| File | What to Update |
|------|----------------|
| `src/X.Y.Z/EDAAnOWL.ttl` | `owl:versionIRI`, `owl:versionInfo`, `owl:priorVersion`, `dct:modified` |
| `src/X.Y.Z/README.md` | Version references, changelog summary |
| `src/X.Y.Z/index.html` | Version number in page |
| `src/X.Y.Z/vocabularies/*.ttl` | `@base` URI, `owl:Ontology` URI |
| `CHANGELOG.md` | Add new version section |
| `CITATION.cff` | `version` field, `date-released` |
| `README.md` (root) | Latest version badge, notes |
| `SECURITY.md` | Supported versions table |

#### 1.3 Update owl:imports in Main Ontology

```turtle
owl:imports <https://w3id.org/EDAAnOWL/0.5.0/vocabularies/datatype-scheme> ;
```

#### 1.4 Review and Update Content

- [ ] **Shapes** (`shapes/edaan-shapes.ttl`): Add/update validation rules
- [ ] **Examples** (`examples/*.ttl`): Update to use new patterns
- [ ] **Vocabularies** (`vocabularies/*.ttl`): Update alignments if needed
- [ ] **Images** (`images/`): Ensure diagrams reflect current ontology structure

#### 1.5 Run Validation

```bash
# Full validation
python scripts/check_rdf.py
python scripts/validate_shacl.py

# Or use Docker:
./scripts/local-validate.sh
```

#### 1.6 Commit to dev

```bash
git add .
git commit -m "feat: Prepare files for v0.5.0"
git push origin dev
```

---

### Step 2: Merge `dev` into `main`

1. Open a Pull Request from `dev` to `main`.
2. Title: "Release v0.5.0".
3. Use the [PR template](.github/pull_request_template.md).
4. Have the PR reviewed and approved.
5. **Merge the Pull Request.**

---

### Step 3: Create the GitHub Release (Triggers Automation)

1. Go to **Releases** → **Draft a new release**.
2. Create tag: `v0.5.0` (with `v` prefix).
3. Target: `main` branch.
4. Copy changelog notes into the release description.
5. Click **Publish release**.

---

### Step 4: What Happens Automatically

The `release.yml` workflow:
- Detects the tag `v0.5.0`
- Runs Widoco to generate HTML documentation
- Post-processes HTML for correct vocabulary links
- Copies files to `deploy/0.5.0/` and `deploy/latest/`
- Pushes to `gh-pages` branch

Wait ~5 minutes, then verify:
- https://w3id.org/EDAAnOWL/latest/
- https://w3id.org/EDAAnOWL/0.5.0/

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
