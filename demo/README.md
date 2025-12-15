# EDAAnOWL Demos

This folder contains practical demonstrations of EDAAnOWL transformations.

## 📂 Available Demos

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
- Uses all v0.3.2 features: `MetricType`, `ObservableProperty`, AGROVOC alignment

---

## 🔧 Requirements

```bash
pip install rdflib
```

Optional (for SHACL validation):
```bash
pip install pyshacl
```
