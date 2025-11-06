# EDAAnOWL v0.1.0

Welcome to the documentation for version 0.1.0 of the EDAAnOWL ontology.

This ontology provides a semantic model for describing and annotating **Data Assets** and **Data Apps** (Applications/Services) within a Data Space, with a focus on the Agri-food domain.

Its primary goal is to enable **semantic compatibility discovery** between services and data, aligning the **IDSA** and **BIGOWL** models.

## 🚀 Key Changes in v0.1.0

This version introduces a new, direct semantic annotation model, which complements the existing `:DataProfile` model.

* **New Classes:**
    * `:DataAsset`: A subclass of `ids:DataResource` for semantically annotating *what* observable property a data resource provides.
    * `:SpatialTemporalAsset`: A subclass of `:DataAsset` for Earth Observation (EO) data that has specific spatial and temporal coverage.
    * `:AnalyticalService`: A subclass of `ids:AppResource` for describing services (like AI models or BIGOWL workflows) based on the semantic properties they require and produce.
    * `:ObservableProperty`: The central class (a subclass of `sosa:ObservableProperty`) representing a semantic variable (e.g., "NDVI", "Temperature").

* **New Object Properties:**
    * `:servesObservableProperty`: (Domain: `:DataAsset`) -> (Range: `:ObservableProperty`)
    * `:requiresObservableProperty`: (Domain: `:AnalyticalService`) -> (Range: `:ObservableProperty`)
    * `:producesObservableProperty`: (Domain: `:AnalyticalService`) -> (Range: `:ObservableProperty`)
    * `:hasSpatialCoverage`: (Domain: `:SpatialTemporalAsset`) -> (Range: `gsp:Geometry`)
    * `:hasTemporalCoverage`: (Domain: `:SpatialTemporalAsset`) -> (Range: `time:Interval`)

* **New Imports:**
    * `sosa` (Sensor, Observation, Sample, and Actuator) has been added for the `:ObservableProperty` class.
    * `time` (OWL-Time) has been added for the `:hasTemporalCoverage` property.
    * `geosparql` (GSP) has been added for the `:hasSpatialCoverage` property.

---

## 🧐 How the Ontology Fulfills Requirements

EDAAnOWL v0.1.0 now provides **two compatibility models** that can be used separately or together.

### Model 1: Profile-based Compatibility (`:DataProfile`)

This model is ideal for structured data (tabular, time-series) where the data's *shape* and *structure* are just as important as its semantics.

* An `ids:DataResource` **conforms to** (`:conformsToProfile`) a `:DataProfile`.
* An `ids:DataApp` **requires** (`:requiresProfile`) and/or **produces** (`:producesProfile`) a `:DataProfile`.
* The `:DataProfile` describes the data's "signature":
    * `:declaresDataClass` (e.g., `:tabular`, `:georaster`)
    * `:declaresObservedProperty` (e.g., `:yield`, `:precipitation`)
    * `:profileCRS` (e.g., "EPSG:4326")
    * `:profileTemporalResolution` (e.g., "P1Y" - 1 year)



**Example (Use Case: "Crop Yield Prediction"):**

```turtle
# The APPLICATION defines what it needs:
ex:CropPredictorApp a :PredictionApp ;
    :requiresProfile ex:AgriYieldProfile .

# The PROFILE defines the data "signature":
ex:AgriYieldProfile a :DataProfile ;
    :declaresDataClass :tabular ;
    :declaresObservedProperty :yield ;
    :profileTemporalResolution "P1Y"^^xsd:duration .

# The RESOURCE declares it matches that signature:
ex:AndalusiaCropYield2024 a ids:DataResource ;
    :conformsToProfile ex:AgriYieldProfile .