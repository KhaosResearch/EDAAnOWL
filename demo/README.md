# EDAAnOWL Demos

This folder contains practical demonstrations and use cases for EDAAnOWL.

## 📖 Use Cases & Examples

See **[USE_CASES.md](USE_CASES.md)** for comprehensive documentation including:

- Semantic matchmaking (Olive Yield Prediction)
- DataApp as supply/demand
- Provenance and traceability
- Cross-domain interoperability (Agriculture ↔ Energy)
- Weighted/probabilistic matching with metrics
- **DataProfile reuse & lifecycle** *(how profiles are created and shared)*
- **Matchmaking property reference** *(when to use which property)*
- **Multi-dimensional compatibility** *(80% compatible scenarios)*
- Vocabulary strategies (local vs. direct linking)

---

## 📂 Practical Demos

### 1. [catalog/](catalog/) — DCAT Catalog Transformation

Transforms a standard **DCAT Catalog** (JSON-LD) into EDAAnOWL RDF.

- **Input**: `catalog.json` (DCAT datasets with DataApps and services)
- **Output**: `output.ttl` (EDAAnOWL DataAssets and Profiles)

```bash
cd demo/catalog
python transform_catalog.py
```

---

### 2. [olive-grove/](olive-grove/) — CSV Data Transformation

Transforms olive grove monitoring **CSV data** into EDAAnOWL RDF with full matchmaking support.

- **Input**: `olive-grove-monitoring-2024.csv`
- **Output**: `output.ttl` with:
  - `:SpatialTemporalAsset` with computed spatial/temporal coverage
  - `:DataProfile` with quality metrics using `:MetricType`
  - Observable properties for semantic matchmaking

```bash
cd demo/olive-grove
python transform_csv.py
```

**Highlights**:
- Demonstrates Use Case 1 from `USE_CASES.md`
- Dataset is compatible with `OliveYieldPredictor` app
- Uses all v0.5.0+ features

---

## 🔧 Requirements

```bash
pip install rdflib
```

Optional (for SHACL validation):
```bash
pip install pyshacl
```

