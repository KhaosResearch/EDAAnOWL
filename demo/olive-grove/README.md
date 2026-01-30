# Olive Grove Monitoring Demo

This demo transforms real-world olive grove monitoring data (CSV) into EDAAnOWL RDF, demonstrating a **complete matchmaking scenario**.

## 📂 Contents

- **`olive-grove-monitoring-2024.csv`**: Sample dataset from olive plots in Jaén, Spain
- **`transform_csv.py`**: Python script that performs the transformation
- **`output.ttl`**: Generated RDF output

## 🚀 How to Run

```bash
cd demo/olive-grove
pip install rdflib
python transform_csv.py
```

## 📊 What the Script Does

1. **Reads the CSV** and extracts olive grove observations
2. **Computes metrics** from the actual data:
   - Record count
   - Completeness ratio
   - Feature count
   - Spatial/temporal extent
3. **Generates EDAAnOWL RDF** including:
   - `:SpatialTemporalAsset` with spatial/temporal coverage
   - `:DataProfile` with quality metrics
   - `:servesObservableProperty` for matchmaking (using AGROVOC URIs)

## 🔗 Matchmaking Compatibility

The generated dataset **matches the requirements** of `OliveYieldPredictor` from [USE_CASES.md](../USE_CASES.md):

| App Requires | Dataset Serves | AGROVOC URI |
|--------------|----------------|-------------|
| NDVI | ✅ `ndvi` column | `agrovoc:c_ce585e0d` |
| Temperature | ✅ `temperature_celsius` column | `agrovoc:c_7657` |
| Precipitation | ✅ `precipitation_mm` column | `agrovoc:c_6161` |

**Result**: A semantic broker can automatically discover this dataset as compatible input for the yield prediction app.

## 📋 Data Columns

| Column | Observable Property | AGROVOC Code | Description |
|--------|---------------------|--------------|-------------|
| `ndvi` | NDVI | `c_ce585e0d` | Vegetation index (0-1) |
| `temperature_celsius` | Temperature | `c_7657` | Air temperature (°C) |
| `precipitation_mm` | Precipitation | `c_6161` | Precipitation (mm) |
| `soil_moisture_percent` | Soil Moisture | `c_7208` | Soil moisture (%) |
| `yield_kg_ha` | Yield | `c_8488` | Olive yield (kg/ha) |
