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
   - `:DataProfile` with quality metrics using `:MetricType`
   - `:servesObservableProperty` for matchmaking

## 🔗 Matchmaking Compatibility

The generated dataset **matches the requirements** of `OliveYieldPredictor` from [USE_CASES.md](../USE_CASES.md):

| App Requires | Dataset Serves |
|--------------|----------------|
| `:ndvi` | ✅ `ndvi` column |
| `:temperature` | ✅ `temperature_celsius` column |
| `:precipitation` | ✅ `precipitation_mm` column |

**Result**: A semantic broker can automatically discover this dataset as compatible input for the yield prediction app.

## 📋 Data Columns

| Column | Observable Property | Description |
|--------|---------------------|-------------|
| `ndvi` | `:ndvi` | Vegetation index (0-1) |
| `temperature_celsius` | `:temperature` | Air temperature (°C) |
| `precipitation_mm` | `:precipitation` | Precipitation (mm) |
| `soil_moisture_percent` | `:soilMoisture` | Soil moisture (%) |
| `yield_kg_ha` | `:yield` | Olive yield (kg/ha) |
