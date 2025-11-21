# EDAAnOWL Demo: DCAT to RDF Transformation

This folder contains a practical demonstration of how to transform a standard **DCAT Catalog** (in JSON-LD format) into **EDAAnOWL RDF** that complies with the ontology's SHACL shapes.

## 📂 Contents

- **`catalog.json`**: A sample DCAT catalog containing datasets (Data Assets) and services (Data Apps).
- **`transform_catalog.py`**: A Python script that performs the transformation.
- **`output.ttl`**: The resulting RDF file (Turtle format).

## 🚀 How to Run

1.  Ensure you have Python installed and the required dependencies:
    ```bash
    pip install rdflib pyshacl
    ```
2.  Run the transformation script:
    ```bash
    python transform_catalog.py
    ```
3.  The script will:
    - Read `catalog.json`.
    - Map DCAT datasets to `edaan:DataAsset` or `ids:SmartDataApp` based on keywords.
    - Enrich the data with **Data Profiles**, **Quality Metrics** (DQV), and **Provenance** (PROV-O).
    - Validate the output against the SHACL shapes (`../src/0.3.0/shapes/edaan-shapes.ttl`).
    - Save the result to `output.ttl`.

## 🧩 Transformation Logic

The script applies the following heuristics to map DCAT concepts to EDAAnOWL:

| DCAT Concept | Keyword/Type | EDAAnOWL Class | Added Features |
| :--- | :--- | :--- | :--- |
| `dcat:Dataset` | "algorithm", "model" | `ids:SmartDataApp` (specifically `:PredictionApp`) | `:requiresProfile`, `:producesObservableProperty` |
| `dcat:Dataset` | (default) | `edaan:DataAsset` | `:conformsToProfile`, `:servesObservableProperty`, `prov:wasGeneratedBy` |

It also automatically generates:
- **Data Profiles**: With `dcat:temporalResolution` and `:declaresDataClass`.
- **Quality Metrics**: `dqv:QualityMetric` instances (e.g., completeness).
- **Provenance**: Links assets to the apps that generated them.
