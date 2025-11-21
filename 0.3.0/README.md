# EDAAnOWL v0.3.0

Welcome to the documentation for version 0.3.0 of the EDAAnOWL ontology.

This ontology provides a semantic model for describing and annotating **Data Assets** and **Data Apps** (Applications/Services) within a Data Space, aligning the **IDSA** Information Model and the **BIGOWL** ontology framework.

## 🚀 Key Changes in v0.3.0: Quality & Provenance

This version enriches the ontology with standard vocabularies for **Data Quality** and **Provenance**, and simplifies the architecture.

### 1. Data Quality (DQV Alignment)
- **`edaan:Metric`** is now a subclass of `dqv:Metric`.
- **`edaan:QualityMetric`** is now a subclass of `dqv:QualityMetric`.
- This enables interoperability with tools that consume W3C Data Quality Vocabulary.

### 2. Provenance (PROV-O Alignment)
- Added support for **`prov:wasGeneratedBy`** in `:DataAsset`.
- Allows tracing the lineage of a data asset back to the `:DataApp` (or `:PredictionApp`) that generated it.

### 3. Architecture Simplification
- Removed the deprecated `:AnalyticalService` class (fully replaced by `ids:SmartDataApp` subclasses).
- See the updated [Architecture Diagram](../../ARCHITECTURE.md).

### 4. Demo & Transformation
- Added a `demo/` folder with a **DCAT-to-RDF transformation script** (`transform_catalog.py`).
- Demonstrates how to convert a standard `catalog.json` into EDAAnOWL RDF, automatically mapping keywords to algorithms and generating data profiles.

### 5. Fixes & Improvements
- **SHACL Shapes**: Split `:DataAssetShape` into `:SpatialTemporalAssetShape` (strict) and `:DataAssetShape` (flexible) to allow generic assets without mandatory spatial/temporal coverage.
- **Validation**: Fixed syntax errors in shape files and ensured full compliance with the new profile/semantic models.

## 🛠 Key changes in v0.2.1 (Previous)
(Kept for history)
This was a small maintenance/packaging release...

---

## 🧐 How the Ontology Fulfills Requirements (v0.3.0 Model)

EDAAnOWL v0.3.0 provides **two complementary compatibility models** that can now be used together.

### Model 1: Profile-based Compatibility (from v0.0.1)

This model is ideal for structured data where _shape_ and _structure_ are key.

- An `ids:DataResource` **conforms to** (`:conformsToProfile`) a `:DataProfile`.
- An `ids:SmartDataApp` (like `:PredictionApp`) **requires** (`:requiresProfile`) a `:DataProfile`.
- The `:DataProfile` describes the data's "signature":
  - `:declaresDataClass` (e.g., `:tabular`, `:georaster`)
  - `:declaresObservedProperty` (e.g., `:yield`, `:precipitation`)

### Model 2: Direct Semantic Compatibility (Refined in v0.2.0)

This model is ideal for simple, direct semantic "matchmaking" based on business concepts.

- A `:DataAsset` (subclass of `ids:DataResource`) **serves** a variable (e.g., `:servesObservableProperty :ndvi`).
- An `ids:SmartDataApp` (like `:PredictionApp`) **requires** a variable (e.g., `:requiresObservableProperty :ndvi`).

### Example (Using BOTH models together)

An application can now be described with full precision, combining both models in a single instance:

```turtle
# The APPLICATION is a standard, deployable IDSA App
ex:CropPredictorApp a :PredictionApp ;
    dct:title "Crop Yield Predictor" ;
    :hasDomainSector :agriculture ;

    # 1. STRUCTURAL Requirement (Profile Model)
    # "I need data shaped like this (columns, CRS, etc.)"
    :requiresProfile ex:AgriInputProfile ;

    # 2. SEMANTIC Requirement (Direct Model)
    # "Specifically, that data must contain NDVI and Temperature."
    :requiresObservableProperty :ndvi, :temperature ;

    # 3. SEMANTIC Output (Direct Model)
    # "And I produce 'Crop Yield'."
    :producesObservableProperty :yield .

# The DATASET satisfies both requirements
ex:MySentinelData a :SpatialTemporalAsset ;
    dct:title "Sentinel-2 Data for Jaen" ;

    # 1. It MATCHES the structure
    :conformsToProfile ex:AgriInputProfile ;

    # 2. It PROVIDES the semantics
    :servesObservableProperty :ndvi, :temperature .
```

### 🎨 Visualizing the Matchmaking Flow

The following diagram illustrates how an App and an Asset "meet" through their shared Profile and Observable Properties:

```mermaid
graph LR
    subgraph "Data App (Demand)"
    App[Crop Yield Predictor]
    end

    subgraph "Shared Semantics (The Match)"
    Profile[Agri Input Profile]
    NDVI((NDVI))
    Temp((Temperature))
    end

    subgraph "Data Asset (Supply)"
    Asset[Sentinel-2 Data]
    end

    %% Relationships
    App -- requiresProfile<br/>(Structure) --> Profile
    App -- requiresObservable<br/>(Meaning) --> NDVI
    App -- requiresObservable<br/>(Meaning) --> Temp

    Asset -- conformsToProfile<br/>(Structure) --> Profile
    Asset -- servesObservable<br/>(Meaning) --> NDVI
    Asset -- servesObservable<br/>(Meaning) --> Temp

    %% Styling
    style App fill:#f9f,stroke:#333,stroke-width:2px
    style Asset fill:#bbf,stroke:#333,stroke-width:2px
    style Profile fill:#dfd,stroke:#333,stroke-width:2px
    style NDVI fill:#ff9,stroke:#333,stroke-width:1px
    style Temp fill:#ff9,stroke:#333,stroke-width:1px
```

---

## ✅ Requirement Coverage (A3.2 / A4.1)

- R1 (IDSA Extension): Extends `ids:DataResource` as `:DataAsset` and leverages `ids:SmartDataApp` for apps; adds domain alignment via `:hasDomainSector`, support contacts, profiles, and semantic signatures.
- R2 (Atomic Services/Assets): Enables decomposition via `DataProfile` features and semantic I/O (`requires/producesObservableProperty`), and aligns with BIGOWL `Component`.
- R3 (Validation and Suggestion): Model includes all hooks to write SHACL shapes for matchmaking between assets and apps (profile-based and semantic-based). See section “Validation” in repository guidelines.
- R4 (Domain Alignment): Uses SOSA/SSN for `ObservableProperty`, SKOS concept schemes (sector, datatypes, observed properties) to align with external vocabularies.
- R5 (Workflow Generation): Bridges to BIGOWL `Component` and OPMW `WorkflowTemplate` through `:implementsComponent` and `:realizesWorkflow`.

---

## 🧩 Key Classes and Properties (Quick Reference)

| Class | Origin | Role in EDAAnOWL | Key Object Properties | Key Data Properties | Example |
| :-------------------------------------------- | :------------ | :--------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------ | :------------------------------------------------------ |
| ids:Resource | IDSA | Base for any asset/service | `:hasDomainSector`, `:topic`, `:spatialGranularityConcept` | `:supportContact` | `ex:r a ids:Resource` |
| :DataAsset ⊑ ids:DataResource | EDAAnOWL | Data asset with domain semantics | `:servesObservableProperty` | — | `ex:d a :DataAsset ; :servesObservableProperty :ndvi` |
| ids:SmartDataApp | IDSA | Data processing app/service | `:requiresProfile`, `:producesProfile`, `:requiresObservableProperty`, `:producesObservableProperty`, `:implementsComponent`, `:realizesWorkflow`, `:parameter` | — | `ex:a a ids:SmartDataApp ; :requiresProfile ex:p` |
| :PredictionApp ⊑ ids:SmartDataApp | EDAAnOWL | Predictive app specialization | inherits above | — | `ex:pred a :PredictionApp` |
| :AnalyzerApp ⊑ ids:SmartDataApp | EDAAnOWL | Descriptive/diagnostic app | inherits above | — | `ex:ana a :AnalyzerApp` |
| :VisualizationApp ⊑ ids:SmartDataApp | EDAAnOWL | Visualization/reporting app | inherits above | — | `ex:viz a :VisualizationApp` |
| :DataProfile | EDAAnOWL | Data “signature” (structure/semantics) | `:declaresDataClass`, `:declaresObservedProperty`, `:hasCRS` | `dcat:temporalResolution`, `dcat:spatialResolutionInMeters` | `ex:p a :DataProfile ; :declaresObservedProperty :ndvi` |
| :ObservableProperty ⊑ sosa:ObservableProperty | EDAAnOWL/SOSA | Semantic variable used by assets and apps | — | — | `:ndvi a :ObservableProperty` |
| bigwf:Component | BIGOWL | Workflow component implemented by apps | `:producesResource`, `:consumesResource` | — | `ex:c a bigwf:Component` |
| ids:Representation | IDSA | Representation consumed/produced in components | — | — | `ex:r a ids:Representation` |
| opmw:WorkflowTemplate | OPMW | Abstract workflow realized by apps | — | — | `ex:w a opmw:WorkflowTemplate` |

Notes:

- Prefer `:spatialGranularityConcept` (SKOS) over `:spatialGranularity` (string).
- `:hasCRS` should point to an IRI (e.g., EPSG).

---

## 📚 Mini Use Cases (Annotation Patterns)

1. Matchmaking (Semantic)

```turtle
ex:NDVIseries a :DataAsset ; :servesObservableProperty :ndvi .
ex:YieldPredictor a :PredictionApp ; :requiresObservableProperty :ndvi .
# A reasoner/SHACL can suggest: NDVIseries is a valid input for YieldPredictor
```

2. Matchmaking (Profile)

```turtle
ex:AgriProfile a :DataProfile ;
  :declaresDataClass bigdat:Data ;
  :declaresObservedProperty :temperature ;
  :hasCRS <http://www.opengis.net/def/crs/EPSG/0/4326> .

ex:WeatherApp a ids:SmartDataApp ; :requiresProfile ex:AgriProfile .
ex:WeatherDataset a :DataAsset ; :conformsToProfile ex:AgriProfile .
```

---

## 🔎 Validation (SHACL hints)

- Ensure an `ids:SmartDataApp` requiring an observable is linked to at least one `:ObservableProperty`.
- Ensure an asset that claims `:conformsToProfile` has consistent CRS/resolution datatypes.
- Suggest candidate assets for apps where `requiresObservableProperty` ⊆ assets’ `servesObservableProperty`.

---

## 🔗 IDSA alignment (Recommended usage)

This ontology follows the IDSA taxonomy and views:

- Resource taxonomy: `ids:Resource` → `ids:DataResource` (used by `:DataAsset`) and `ids:DataApp`/`ids:SmartDataApp` (used by app specializations). See IDSA docs and figures (Resource taxonomy, Data App taxonomy/content view).
- 3C views: Concept (what it is), Content (what it contains → `ids:Representation`), Context (conditions of use → contract/policies).

Minimal Content view example (Representation on a Data Asset):

```turtle
ex:MyRaster a :DataAsset ;
  dct:title "Example Raster" ;
  ids:representation ex:GeoTIFFRepr ;
  :servesObservableProperty :ndvi .

ex:GeoTIFFRepr a ids:Representation ;
  dct:format "GeoTIFF" ;
  ids:mediaType <https://www.iana.org/assignments/media-types/image/tiff> ;
  dct:language "en" .
```

Notes:

- Use `ids:representation` (or `ids:defaultRepresentation`) to link resources to `ids:Representation`.
- Put format/media type/language at the `ids:Representation` node. Keep structural/semantic constraints in `:DataProfile`.
- Policies/contracts: use ODRL/IDSA contracts linked to the resource/app when needed.

References:

- IDSA IM (Resource): https://international-data-spaces-association.github.io/InformationModel/docs/index.html#Resource
- Figures: Resource taxonomy, 3C views, Representation, Data App content view/taxonomy (see the linked figures in IDSA docs).

---

## 🧪 Optional patterns (Context view)

Endpoints (IDs Resource Endpoint):

```turtle
# Minimal endpoint node (extend with IDSA endpoint properties as needed)
ex:MyEndpoint a ids:ResourceEndpoint ;
  dct:description "HTTPS endpoint for raster download" .

ex:MyRaster ids:resourceEndpoint ex:MyEndpoint .
```

Contracts/Policies (ODRL/IDSA):

```turtle
ex:BasicUsePolicy a odrl:Policy , ids:ContractOffer ;
  odrl:permission [
    a odrl:Permission ;
    odrl:action odrl:use
  ] .

ex:MyRaster ids:contractOffer ex:BasicUsePolicy .
```

Notes:

- Attach `ids:resourceEndpoint` and `ids:contractOffer` to resources/apps to complete the IDSA Context view.
- Use additional ODRL constraints/duties (e.g., attribution) as required by your governance model.
