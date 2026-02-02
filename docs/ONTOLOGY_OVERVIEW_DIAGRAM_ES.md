# EDAAnOWL - Diagramas de Arquitectura

Diagramas simplificados para explicar la ontología EDAAnOWL.

---

## 1️⃣ Jerarquía de Clases: IDSA → EDAAnOWL

Este diagrama muestra **solo la herencia de clases** (subClassOf).

```mermaid
flowchart TD
    classDef idsa fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    classDef edaan fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px

    R["ids:Resource"]
    DR["ids:DataResource"]
    DA["ids:DataApp"]
    SDA["ids:SmartDataApp"]

    R --> DR
    R --> DA
    DA --> SDA

    DataAsset[":DataAsset"]
    STA[":SpatialTemporalAsset"]
    PA[":PredictionApp"]
    AA[":AnalyzerApp"]
    VA[":VisualizationApp"]

    DR --> DataAsset
    DataAsset --> STA
    SDA --> PA
    SDA --> AA
    SDA --> VA

    class R,DR,DA,SDA idsa
    class DataAsset,STA,PA,AA,VA edaan
```

**Leyenda:**
- 🔵 Azul = IDSA Information Model
- 🟢 Verde = EDAAnOWL (nuestras clases)
- Todas las flechas = `rdfs:subClassOf`

---

## 2️⃣ El Matchmaking Semántico

Cómo **DataAsset** (oferta) y **SmartDataApp** (demanda) se conectan mediante **ObservableProperty**.

```mermaid
flowchart LR
    classDef supply fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef demand fill:#bbdefb,stroke:#1976d2,stroke-width:2px
    classDef bridge fill:#fff9c4,stroke:#f9a825,stroke-width:2px

    DA["📦 DataAsset<br/>(Oferta)"]
    OP["🎯 ObservableProperty<br/>(ej: NDVI, Temperatura)"]
    APP["⚙️ SmartDataApp<br/>(Demanda)"]

    DA -- "servesObservableProperty" --> OP
    APP -- "requiresObservableProperty" --> OP
    APP -- "producesObservableProperty" --> OP

    class DA supply
    class APP demand
    class OP bridge
```

---

## 3️⃣ El Matchmaking Estructural

Cómo los **DataProfiles** describen la estructura de datos.

```mermaid
flowchart TD
    classDef data fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef profile fill:#fff9c4,stroke:#f9a825,stroke-width:2px
    classDef app fill:#bbdefb,stroke:#1976d2,stroke-width:2px

    DA["📦 DataAsset"]
    DIST["dcat:Distribution"]
    DP["📋 DataProfile"]
    APP["⚙️ DataApp"]

    DA -- "ids:representation" --> DIST
    DIST -- "conformsToProfile" --> DP
    APP -- "requiresProfile" --> DP
    APP -- "producesProfile" --> DP

    class DA data
    class DIST data
    class DP profile
    class APP app
```

---

## 4️⃣ Conexión con BIGOWL (Workflows)

Cómo las **DataApps** de IDSA se conectan con **Components** de BIGOWL.

```mermaid
flowchart LR
    classDef idsa fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    classDef bigowl fill:#fffde7,stroke:#fbc02d,stroke-width:2px
    classDef profile fill:#fff9c4,stroke:#f9a825,stroke-width:2px

    APP["ids:DataApp"]
    COMP["bigwf:Component"]
    WF["bigwf:Workflow"]
    
    DP["DataProfile"]
    DATA["bigdat:Data"]

    APP -- "implementsComponent" --> COMP
    COMP -- "bigwf:hasStep" --> WF
    DP -- "declaresDataClass" --> DATA

    class APP idsa
    class COMP,WF,DATA bigowl
    class DP profile
```

---

## 5️⃣ DataProfile: Contenido

Qué incluye un **DataProfile**.

```mermaid
flowchart TD
    classDef profile fill:#fff9c4,stroke:#f9a825,stroke-width:2px
    classDef content fill:#f5f5f5,stroke:#757575,stroke-width:1px

    DP["📋 DataProfile"]
    
    DC["bigdat:Data<br/>(Tipo: Tabular, Imagen...)"]
    OP["ObservableProperty<br/>(Variables semánticas)"]
    M["Metric<br/>(Métricas de calidad)"]
    CRS["skos:Concept<br/>(Sistema coordenadas)"]
    RES["xsd:decimal / xsd:duration<br/>(Resolución)"]

    DP -- "declaresDataClass" --> DC
    DP -- "declaresObservedProperty" --> OP
    DP -- "hasMetric" --> M
    DP -- "hasCRS" --> CRS
    DP -- "dcat:spatialResolutionInMeters" --> RES

    class DP profile
    class DC,OP,M,CRS,RES content
```

---

## 6️⃣ Diagrama Completo CON nombres de propiedades

Vista general con todas las propiedades etiquetadas.

```mermaid
flowchart TB
    classDef idsa fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    classDef edaan fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    classDef bigowl fill:#fffde7,stroke:#fbc02d,stroke-width:2px
    classDef external fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px

    subgraph IDSA ["IDSA Information Model"]
        DR["ids:DataResource"]
        DA["ids:DataApp"]
        SDA["ids:SmartDataApp"]
    end

    subgraph EDAAnOWL ["EDAAnOWL"]
        Asset[":DataAsset"]
        Profile[":DataProfile"]
        ObsProp[":ObservableProperty"]
        Metric[":Metric"]
        Apps[":PredictionApp"]
    end

    subgraph BIGOWL ["BIGOWL"]
        Comp["bigwf:Component"]
        Data["bigdat:Data"]
    end

    subgraph Standards ["Estándares W3C"]
        DCAT["dcat:Distribution"]
    end

    DR -.->|"subClassOf"| Asset
    SDA -.->|"subClassOf"| Apps
    
    Asset -->|"servesObservableProperty"| ObsProp
    Apps -->|"requiresObservableProperty"| ObsProp
    
    Asset -->|"ids:representation"| DCAT
    DCAT -->|"conformsToProfile"| Profile
    Apps -->|"requiresProfile"| Profile
    
    Profile -->|"declaresDataClass"| Data
    Profile -->|"hasMetric"| Metric
    
    DA -->|"implementsComponent"| Comp

    class DR,DA,SDA idsa
    class Asset,Profile,ObsProp,Metric,Apps edaan
    class Comp,Data bigowl
    class DCAT external
```

---

## 📋 Resumen de Propiedades Principales

| Desde | Hacia | Propiedad | Significado |
|-------|-------|-----------|-------------|
| DataAsset | ObservableProperty | `servesObservableProperty` | "Este dataset contiene..." |
| SmartDataApp | ObservableProperty | `requiresObservableProperty` | "Esta app necesita..." |
| SmartDataApp | ObservableProperty | `producesObservableProperty` | "Esta app genera..." |
| dcat:Distribution | DataProfile | `conformsToProfile` | "Esta distribución tiene este perfil" |
| DataApp | DataProfile | `requiresProfile` | "Esta app necesita este perfil" |
| DataApp | DataProfile | `producesProfile` | "Esta app genera este perfil" |
| DataApp | bigwf:Component | `implementsComponent` | "Esta app implementa este componente" |
| DataProfile | bigdat:Data | `declaresDataClass` | "Este perfil es de tipo..." |
| DataProfile | Metric | `hasMetric` | "Este perfil tiene esta métrica" |

---

## 🎯 Mensaje Clave

> **EDAAnOWL = Puente entre IDSA y BIGOWL**
> 
> - **IDSA** → Gobernanza (contratos, políticas, endpoints)
> - **BIGOWL** → Ejecución (workflows, algoritmos)
> - **EDAAnOWL** → Matchmaking (perfiles, propiedades observables)
