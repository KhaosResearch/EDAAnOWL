# EDAAnOWL

[![Deploy Ontology to GitHub Pages](https://github.com/KhaosResearch/EDAAnOWL/actions/workflows/release.yml/badge.svg)](https://github.com/KhaosResearch/EDAAnOWL/actions/workflows/release.yml)

[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-1f6feb)](https://khaosresearch.github.io/EDAAnOWL/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/KhaosResearch/EDAAnOWL?display_name=tag)](https://github.com/KhaosResearch/EDAAnOWL/releases)
[![PURL](https://img.shields.io/badge/purl-w3id.org-blue)](https://w3id.org/EDAAnOWL/)
[![SHACL Validation](https://img.shields.io/badge/SHACL-Conformant-success)](src/0.3.2/shapes/edaan-shapes.ttl)
[![GitHub stars](https://img.shields.io/github/stars/KhaosResearch/EDAAnOWL?style=social)](https://github.com/KhaosResearch/EDAAnOWL/stargazers)

A pilot ontology for the semantic exploitation of data assets in the Agri-food (EDAA) context, aligned with the [IDSA Information Model](https://github.com/International-Data-Spaces-Association/InformationModel) and the [BIGOWL ontology](https://github.com/KhaosResearch/BIGOWL-DS/).
- :book: [IDSA ontology documentation](https://w3id.org/idsa/core)
- :book: [BIGOWL ontology documentation](https://w3id.org/BIGOWL/)

> [!NOTE]
> Latest stable: see `src/0.3.2/` (ontology, shapes, examples, vocabularies) and the rendered docs under GitHub Pages.
> Check out the `demo/` folder for a practical example of transforming a DCAT catalog to EDAAnOWL RDF.

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
  - `:hasCRS`: Links to a formal Coordinate Reference System (e.g., EPSG URI).
  - `:supportContact`: Standard contact point for support, using vCard (fn, email, telephone, URL).
  - `:legalContact`: A specific contact point for legal inquiries about the resource.


- **Data properties (motivations)**

  - `dcat:spatialResolutionInMeters`, `dcat:temporalResolution`, `dcat:spatialResolutionInDegrees`: Adopted from DCAT 3 to capture EO and time-series constraints for practical matchmaking.
  - Metrics (`:Metric` and subtypes with `:metricName`/`:metricValue`/`:metricUnit`/`:computedAt`): Allows publishing quality/performance indicators relevant to governance and selection.
  - `:metricType`: Links a metric to a standardized `:MetricType` from the controlled vocabulary (`metric-types.ttl`), enabling interoperable metric names across data spaces.
  - `:accessType`: Indicates the primary access mode for the resource (e.g., download, compute, ...).
  - `:alternativeName`: Alternative title or name for a resource.
  - `:auditLogAvailable`: Indicates if audit logs for the resource usage are available.
  - `:isAlive`: Indicates if the dataset is actively maintained and expects future updates.
  - `:knownLimitations`: Human-readable description of any known limitations, biases, or quality issues of the resource.
  - `:paymentModelDescription`: A human-readable description of the pricing or payment model (e.g., 'Monthly Subscription', 'Pay-per-use').
  - `:qualityReportURI`: Link to full quality report.
  - `:qualityScore`: A quantitative quality score (e.g., 0-100) assigned by the external quality report.
  - `:recommendedUse`: Human-readable description of the intended or recommended use cases for the resource.
  - `:refundPolicy`: A text description of the refund policy applicable to the resource.
  - `schema:thumbnailUrl`: A URL pointing to a thumbnail image for the resource.

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
  - **[PROV-O](https://www.w3.org/TR/prov-o/)**: For provenance and lineage tracking (`prov:wasGeneratedBy`, `prov:wasDerivedFrom`).
  - **[SKOS](https://www.w3.org/TR/skos-reference/)**: For the modular vocabularies.

---

## 🚀 Features

- **Main Ontology**: A semantic "bridge" linking `ids:DataApp` to `bigwf:Component` (from BIGOWL).
- **Profile Model**: A `:DataProfile` class to describe the data "signatures" (inputs/outputs) of assets.
- **Data Lineage & Provenance**: Support for tracking dataset generation (`prov:wasGeneratedBy`) and derivation chains (`prov:wasDerivedFrom`) using PROV-O properties.
- **Modular Vocabularies**: Separate, resolvable SKOS vocabularies for domains, observed properties, etc., versioned alongside the main ontology.
- **Persistent Identifiers**: All ontology and vocabulary modules are resolvable via [https://w3id.org/EDAAnOWL/](https://w3id.org/EDAAnOWL/) for robust content negotiation.
- **Automated Documentation & CI/CD**: A GitHub Actions workflow (`release.yml`) that, upon creating a new release:
  - Builds comprehensive HTML documentation with **Widoco**.
  - Post-processes the HTML (`sed`) to ensure all vocabulary links are correctly versioned.
  - Publishes all artifacts (docs, vocabs, RDF serializations) to the `gh-pages` branch.
- **Versioning**: Supports a `latest` development version and immutable, versioned snapshots (e.g., `/0.0.1/`).
- **Practical Examples**: See [USE_CASES.md](USE_CASES.md) for real-world examples of semantic matchmaking and provenance tracking.

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

Use the **“Cite this repository”** button on the right (GitHub sidebar), which is generated from our `CITATION.cff`. It provides BibTeX, APA, and more.
