# EDAAnOWL v0.0.1

Welcome to the documentation for version 0.0.1 of the EDAAnOWL ontology.

This ontology provides a semantic model for describing and annotating **Data Assets** and **Data Apps** (Applications/Services) within a Data Space, with a focus on the Agri-food domain.

Its primary goal is to enable **semantic compatibility discovery** between services and data, aligning the **IDSA** Information Model and the **BIGOWL** ontology framework.

## 🚀 Features in v0.0.1

* **Core Compatibility Model:** Introduces the `:DataProfile` class, which acts as a "semantic signature" to describe the inputs and outputs of assets.
* **Data App Extensions:** Provides specialized subclasses of `ids:SmartDataApp`, such as `:PredictionApp`, `:AnalyzerApp`, and `:VisualizationApp`.
* **BIGOWL Alignment:** Connects `ids:DataApp` instances to BIGOWL components (like `bigalg:Algorithm`) using the `:parameter` and `:implementsComponent` properties.
* **Modular Vocabularies:** Establishes separate, importable SKOS vocabularies for key concepts:
    * `sector-scheme.ttl`: For domain tagging (e.g., `:agriculture`).
    * `datatype-scheme.ttl`: For data types (e.g., `:tabular`, `:georaster`).
    * `observed-properties.ttl`: For semantic variables (e.g., `:ndvi`, `:yield`, `:temperature`).
    * `agro-vocab.ttl`: For domain-specific terms (e.g., `:agro_olive`).
* **Usage Examples:** Includes `instance-data.ttl` to demonstrate the `DataProfile` model in practice.

---

## 🧐 How v0.0.1 Fulfills Requirements

In this version, EDAAnOWL fulfills the project's requirements by using a **Profile-based Compatibility Model**.

This model is ideal for structured data (like tables or time-series) where the data's *shape* and *structure* are key to determining compatibility.

* An `ids:DataResource` (a data asset) declares that it **conforms to** a specific profile using the `:conformsToProfile` property.
* An `ids:DataApp` (a service) declares what it **requires** as input (`:requiresProfile`) and/or **produces** as output (`:producesProfile`).
* The `:DataProfile` class itself acts as the "semantic connector," describing the data's "signature" using properties like:
    * `:declaresDataClass` (e.g., `:tabular`)
    * `:declaresObservedProperty` (e.g., `:yield`)
    * `:profileCRS` (e.g., "EPSG:4326")
    * `:profileTemporalResolution` (e.g., "P1Y" - 1 year)


**Example (Use Case: "Repilo Service Composition"):**

This example from `instance-data.ttl` shows how two services could be chained together.

```turtle
# --- 1. The Application (Service) ---
# The "Repilo1.0.0" app is defined as a PredictionApp.
# It clearly states its semantic input and output needs.

ex:Repilo1.0.0 rdf:type :PredictionApp ;
    dct:title "Repilo" ;
    :hasDomainSector :agriculture ;
    # INPUT: It requires data matching the "Climate Input Profile"
    :requiresProfile ex:Profile_Repilo_Input_Climate ;
    
    # OUTPUT: It produces data matching the "Repilo Output Profile"
    :producesProfile ex:Profile_Repilo_Output_Incidence .

# --- 2. The Input Profile ---
# This profile describes the required climate data.
ex:Profile_Repilo_Input_Climate rdf:type :DataProfile ;
    dct:title "Climate Input Profile" ;
    :declaresDataClass :timeseries ,
                       :tabular ;
    :declaresObservedProperty :temperature ,
                              :precipitation .

# --- 3. The Output Profile ---
# This profile describes the resulting prediction data.
ex:Profile_Repilo_Output_Incidence rdf:type :DataProfile ;
    dct:title "Repilo Output Profile" ;
    :declaresDataClass :georaster ;
    :declaresObservedProperty :repiloIncidence .
```

**Result:** This model allows a Data Space orchestrator or search tool to function:
1. **Find Inputs:** It can search for any `ids:DataResource` that `:conformsToProfile` `ex:Profile_Repilo_Input_Climate` to feed the Repilo app.
2. **Chain Services:** It knows that the output of `ex:Repilo1.0.0` is compatible with any other Data App that `:requiresProfile` `ex:Profile_Repilo_Output_Incidence`.

This successfully achieves the goal of semantic discovery and service composition.

