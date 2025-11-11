# EDAAnOWL

[![Deploy Ontology to GitHub Pages](https://github.com/KhaosResearch/EDAAnOWL/actions/workflows/release.yml/badge.svg)](https://github.com/KhaosResearch/EDAAnOWL/actions/workflows/release.yml)

[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-1f6feb)](https://khaosresearch.github.io/EDAAnOWL/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/KhaosResearch/EDAAnOWL?display_name=tag)](https://github.com/KhaosResearch/EDAAnOWL/releases)

A pilot ontology for the semantic exploitation of data assets in the Agri-food (EDAA) context, aligned with the IDSA Information Model and the BIGOWL ontology.

> [!NOTE]
> Latest stable: see `src/0.2.0/` (ontology, shapes, examples, vocabularies) and the rendered docs under GitHub Pages.

The purpose of `EDAAnOWL` is to serve as an annotation ontology that enriches the description of Data Space assets. It allows for modeling the functional profile (inputs, outputs, parameters) of `ids:DataApp` and `ids:DataResource`, facilitating their semantic discovery, composition into complex services, and compatibility validation.

---

## 📘 Background: IDSA and BIGOWL (what they are and why we align)

### IDSA Information Model (what/why/how)

- **What it is**: The International Data Spaces Association (IDSA) Information Model defines a common vocabulary for resources (data and apps), their representations, endpoints, usage contracts, participants, connectors, and security profiles. It provides a canonical taxonomy for `ids:Resource` and content/context views to describe how resources are exposed and governed.
- **How it works**: Key concepts include:
  - `ids:Resource` → specialized into `ids:DataResource` and `ids:DataApp`/`ids:SmartDataApp`.
  - `ids:Representation` capturing format/media type/language, linked from resources by `ids:representation` or `ids:defaultRepresentation`.
  - Usage control with contracts and rules (ODRL-based), endpoints for access, and participant/connector/security profiles.
- **Why we reuse it**: We want assets and apps to be discoverable and governable across Data Spaces without reinventing core notions (resource taxonomy, representation, policies, endpoints). Aligning with IDSA ensures compatibility with IDS-based tooling and documentation.
- **References**:
  - IDSA IM docs: [https://international-data-spaces-association.github.io/InformationModel/docs/index.html#Resource](https://international-data-spaces-association.github.io/InformationModel/docs/index.html#Resource)
  - Figures (examples): 
    - Resource taxonomy ([Fig. 3.15](https://international-data-spaces-association.github.io/InformationModel/images/Figure_3_15_Taxonomy_of_the_resource_concept.png))
    - Data App content view ([Fig. 3.32](https://international-data-spaces-association.github.io/InformationModel/images/Figure_3_32_Content_view_of_the_Data_App_resource.png))
    - Data App taxonomy ([Fig. 3.34](https://international-data-spaces-association.github.io/InformationModel/images/Figure_3_34_Data_App_taxonomy.png)).

### BIGOWL (what/why/how)

- **What it is**: A family of ontologies for analytical workflows, algorithms, problems, data, and components. It formalizes workflow elements (e.g., `bigwf:Component`), data types (`bigdat:Data`), and their relations.
- **How it works**: Workflows are composed of components with well-defined inputs/outputs. These can be linked to algorithms/problems, enabling reproducible compositions and reasoning about compatibility.
- **Why we reuse it**: We need to express the computational side (pipelines, components, inputs/outputs) and connect IDSA “apps” to executable workflow elements. BIGOWL gives us a neutral, modular way to do so, avoiding bespoke, ad-hoc workflow modeling.

---

## 🧭 Design Rationale: Why EDAAnOWL extends and aligns the way it does

EDAanOWL provides the “connective tissue” between IDSA’s resource/contract governance and BIGOWL’s workflow semantics:

- **Classes (why we created/extended them)**

  - `:DataAsset ⊑ ids:DataResource`: We specialize IDSA’s data resource to attach domain semantics (e.g., observable variables) needed for matchmaking and discovery.
  - `ids:SmartDataApp` specializations (`:PredictionApp`, `:AnalyzerApp`, `:VisualizationApp`): We align with IDSA’s app branch and provide a practical taxonomy reflecting functionality (prediction/analysis/visualization) inspired by IDSA’s Data App taxonomy.
  - `:DataProfile`: Encapsulates structural/semantic “signatures” of data (class, CRS, resolutions, observed properties). This lives alongside IDSA `ids:Representation` (format/media/language), not replacing it—complementary roles.
  - `:ObservableProperty ⊑ sosa:ObservableProperty`: We reuse SOSA/SSN for domain variables (e.g., NDVI, temperature), enabling semantic I/O specifications for apps and semantic descriptions for assets.

- **Object properties (motivations)**

  - `:conformsToProfile (ids:Resource → :DataProfile)`: A resource states it conforms to a profile (structural/semantic signature). Motivates profile-based compatibility checks.
  - `:requiresProfile` / `:producesProfile (ids:DataApp ↔ :DataProfile)`: Apps specify expected/produced data signatures to enable structural compatibility.
  - `:requiresObservableProperty` / `:producesObservableProperty (ids:SmartDataApp ↔ :ObservableProperty)`: Apps declare semantic I/O needs—enables simple, meaningful matchmaking (semantic compatibility).
  - `:servesObservableProperty (:DataAsset ↔ :ObservableProperty)`: Assets declare the variables they provide—completing the matchmaking triangle.
  - `:implementsComponent (ids:DataApp ↔ bigwf:Component)`: Bridges IDSA apps to BIGOWL components, grounding apps in executable workflow units.
  - `:realizesWorkflow (ids:DataApp ↔ opmw:WorkflowTemplate)`: Links apps to abstract workflows (OPMW) for documentation and reasoning.
  - `:hasDomainSector (⊑ dcat:theme)`: DCAT-aligned domain tagging using SKOS schemes, ensuring interoperable cataloguing and filtering across domains.

- **Data properties (motivations)**

  - `:profileCRS` and `:profileCRSRef`: Explicit CRS as string and IRI; we recommend the IRI form (`xsd:anyURI`) for unambiguous validation.
  - `:profileSpatialResolution`, `:profileTemporalResolution`: Required to capture EO and time-series constraints for practical matchmaking.
  - `:supportContact`: Operational contact—crucial in Data Spaces to support consumers.
  - Metrics (`:Metric` and subtypes with `:metricName`/`:metricValue`/`:metricUnit`/`:computedAt`): Allows publishing quality/performance indicators relevant to governance and selection.

- **Why both Profile-based and Direct Semantic models?**

  - Real-world data/app compatibility has two complementary facets:
    - Structural: “Does my dataset’s structure/CRS/resolution match the app’s expectations?” → `:DataProfile`.
    - Semantic: “Do I have NDVI/temperature that this app needs?” → `:ObservableProperty`.
  - Keeping both enables robust, explainable matchmaking and aligns with IDSA’s content view (representations) without conflating structure with format/serialization.

- **Why align with IDSA Representation instead of embedding formats in profiles?**

  - IDSA prescribes `ids:Representation` for format/media/language; we follow that and keep `:DataProfile` for data semantics/shape. This mirrors IDSA’s own separation of “content” vs. “context” and avoids duplication.

- **Why SKOS/DCAT/ODRL/PROV/LOCN/GeoSPARQL?**
  - We adopt standards recommended by IDSA and the Linked Data community. This maximizes interoperability and reduces custom modeling.
  - **[IDSA-IM (v4)](https://international-data-spaces-association.github.io/InformationModel/docs/index.html)**: Core model for resources, apps, and governance.
  - **[DCAT (v3)](https://www.w3.org/TR/vocab-dcat-3/)**: For cataloguing assets.
  - **[ODRL (v2.2)](https://www.w3.org/TR/odrl-model/)**: For usage control policies.
  - **[SOSA/SSN](https://www.w3.org/TR/vocab-ssn/)**: For observable properties, sensors, and observations.
  - **[GeoSPARQL (v1.1)](https://www.ogc.org/standard/geosparql/)**: For geospatial coverage.
  - **[OPMW/BIGOWL](https://w3id.org/BIGOWL)**: For workflow and component modeling.
  - **[SKOS](https://www.w3.org/TR/skos-reference/)**: For the modular vocabularies.

---

## 🚀 Features

- **Main Ontology**: A semantic "bridge" linking `ids:DataApp` to `bigwf:Component` (from BIGOWL).
- **Profile Model**: A `:DataProfile` class to describe the data "signatures" (inputs/outputs) of assets.
- **Modular Vocabularies**: Separate, resolvable SKOS vocabularies for domains, observed properties, etc., versioned alongside the main ontology.
- **Persistent Identifiers**: All ontology and vocabulary modules are resolvable via [https://w3id.org/EDAAnOWL/](https://w3id.org/EDAAnOWL/) for robust content negotiation.
- **Automated Documentation & CI/CD**: A GitHub Actions workflow (`release.yml`) that, upon creating a new release:
  - Generates a dynamic `catalog-v0.xml` to resolve all imports.
  - Builds comprehensive HTML documentation with **Widoco**.
  - Post-processes the HTML (`sed`) to ensure all vocabulary links are correctly versioned.
  - Publishes all artifacts (docs, vocabs, RDF serializations) to the `gh-pages` branch.
- **Versioning**: Supports a `latest` development version and immutable, versioned snapshots (e.g., `/0.0.1/`).

---

## 🏗 Architecture overview

![EDAAnOWL architecture — IDS ↔ BIGOWL (high-level)](images/eda-an-architecture-en.svg)

EDAAnOWL bridges three key layers:

- **Data Space Layer**: Real-world assets and applications
- **Semantic Layer**: IDSA model integration and semantic descriptions
- **Workflow Layer**: BIGOWL components and workflow definitions

> 📘 For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md)

---

## ✍️ How to Cite

If you use this ontology in your work, please cite it as:

```text
Martín Salvachúa. (2025). EDAAnOWL: A Pilot Ontology for the Semantic Exploitation of Data Assets
in the Agri-food (EDAA) Context [Computer software]. Version 0.2.0. Khaos Research Group,
University of Málaga. https://w3id.org/EDAAnOWL/
```

Or using BibTeX:

```bibtex
@software{edaanowl_2025,
  author       = {Martín Salvachúa},
  title        = {{EDAAnOWL}: A Pilot Ontology for the Semantic Exploitation of Data Assets in the {Agri-food} {(EDAA)} Context},
  year         = {2025},
  publisher    = {Khaos Research Group, University of Málaga},
  version      = {0.2.0},
  url          = {https://w3id.org/EDAAnOWL/},
  type         = {Ontology},
  keywords     = {semantic web, data spaces, IDSA, BIGOWL, agri-food},
  note         = {An ontology for semantic exploitation of data assets, aligned with IDSA Information Model and BIGOWL}
}
```
