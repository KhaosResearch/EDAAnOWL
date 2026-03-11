# Ejemplos de Interoperabilidad Semántica y Polimorfismo

Este documento ilustra el concepto de **"Poly-conformance"**: cómo un único Dataset físico puede servir a múltiples DataApps de distintos dominios mediante el uso de múltiples DataProfiles.

---

## Escenario: El Dataset "Polímata"

Tenemos un fichero CSV físico (`meteo_trafico_malaga_2025.csv`) alojado en un conector IDS.
**Columnas:** `[Timestamp, Lat, Lon, Temp_C, Traffic_Flow, NO2_Level]`

Este ÚNICO asset tendrá **3 Perfiles Semánticos** asociados.

### 1. El Asset (Físico)

```turtle
@prefix ex: <https://example.org/> .
@prefix edaan: <https://w3id.org/EDAAnOWL/> .
@prefix bigdat: <https://w3id.org/BIGOWLData/> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix theme: <http://publications.europa.eu/resource/authority/data-theme/> .

ex:AssetMalagaMultiuso a edaan:DataAsset ;
    dct:title "Datos Urbanos Integrados Málaga" ;
    dcat:theme theme:ENVI, theme:TRAN ; # Medio Ambiente y Transporte
    ids:representation ex:ReprCSV .

ex:ReprCSV a edaan:DataRepresentation ;
    dcat:mediaType "text/csv" ;
    # CLAVE: Conforma a múltiples perfiles SIMULTÁNEAMENTE
    edaan:conformsToProfile ex:ProfileEstructural ;  # Perfil Técnico
    edaan:conformsToProfile ex:ProfileMeteo ;        # Perfil Dominio 1
    edaan:conformsToProfile ex:ProfileMovilidad .    # Perfil Dominio 2
```

---

## 2. Los Perfiles (Semántica)

### A. Perfil Técnico (Estructural)
Describe la realidad física del fichero. Usado por herramientas de ingestión o validación.

```turtle
ex:ProfileEstructural a bigdat:TabularDataSet, edaan:DataProfile ;
    rdfs:label "Perfil Técnico Completo" ;
    bigdat:hasHeader true ;
    bigdat:delimiter "," ;
    # Lista TODAS las columnas
    bigdat:hasColumn ex:ColTime, ex:ColLat, ex:ColLon, ex:ColTemp, ex:ColTraf, ex:ColNO2 .
```

### B. Perfil Meteorológico (Dominio 1)
Usado por una **App de Predicción Agrícola**. Solo le importa el clima.

```turtle
ex:ProfileMeteo a edaan:DataProfile ;
    rdfs:label "Perfil Climatológico Básico" ;
    # Declara semánticamente qué contiene (usando vocabulario ENVO/AGROVOC)
    edaan:declaresObservedProperty <http://purl.obolibrary.org/obo/ENVO_01000203> ; # Temperatura
    
    # Requisitos de Calidad específicos para Meteo
    edaan:hasMetric [
        a edaan:Metric ;
        edaan:metricType <https://w3id.org/EDAAnOWL/Completeness> ; # Definición estandarizada
        edaan:metricValue 0.95 ; # Exige alta completitud
        edaan:measuresProperty <http://purl.obolibrary.org/obo/ENVO_01000203> 
    ] .
```

### C. Perfil de Movilidad (Dominio 2)
Usado por una **App de Gestión de Tráfico**. Solo le importa el flujo vehicular.

```turtle
ex:ProfileMovilidad a edaan:DataProfile ;
    rdfs:label "Perfil de Flujo Vehicular" ;
    edaan:declaresObservedProperty <https://w3id.org/transport/TrafficFlow> ;
    
    # Puede tener restricciones legales distintas
    edaan:containsPersonalData false .
```

---

## 3. El Matchmaking (¡La Magia!)

### Caso 1: DataApp Agrícola (SmartAgri)

```turtle
ex:AppPrediccionCosecha a ids:SmartDataApp ;
    dcat:theme theme:AGRI ;
    # Descubrimiento de alto nivel (Matchmaking Semántico)
    edaan:requiresFeatureOfInterest <http://aims.fao.org/aos/agrovoc/c_5333> ; # Olivos
    edaan:requiresObservableProperty <http://purl.obolibrary.org/obo/ENVO_01000203> ; # Temperatura
    
    # Requisitos Técnicos (Validación de Payload)
    edaan:requiresProfile [
        a edaan:DataProfile ;
        edaan:hasMetric [
            a edaan:Metric ;
            edaan:measuresProperty <http://purl.obolibrary.org/obo/ENVO_01000203> ;
            edaan:hasMetricStandard <http://qudt.org/vocab/unit/DEG_C>
        ]
    ] .
```
**Resultado:** ¡MATCH! `AssetMalagaMultiuso` tiene `ProfileMeteo` que declara esa propiedad.

### Caso 2: DataApp de Tráfico (SmartCity)

```turtle
ex:AppSemaforosInteligentes a ids:SmartDataApp ;
    dcat:theme theme:TRAN ;
    edaan:requiresFeatureOfInterest <https://w3id.org/transport/Vehicle> ;
    edaan:requiresObservableProperty <https://w3id.org/transport/TrafficFlow> ;
    
    edaan:requiresProfile [
        a edaan:DataProfile ;
        edaan:declaresObservedProperty <https://w3id.org/transport/TrafficFlow> 
    ] .
```
**Resultado:** ¡MATCH! El MISMO `AssetMalagaMultiuso` también tiene `ProfileMovilidad`.

### Caso 3: DataApp de Salud (Gaia-X Certified)

Esta app requiere datos que sean gdpr-compliant y tengan certificación.

```turtle
ex:AppEpidemiologia a ids:SmartDataApp ;
    edaan:requiresProfile [
        a edaan:DataProfile ;
        # Requiere certificación Gaia-X
        edaan:hasCertification [
            a edaan:CertificationReport ;
            edaan:certificationLevel "Gaia-X Label 1"
        ] ;
        # Requiere que NO tenga datos personales
        edaan:containsPersonalData false
    ] .
```

---

## 4. Certificación y Alineación Gaia-X

Para soportar el Caso 3, el `ProfileMovilidad` podría incluir:

```turtle
ex:ProfileMovilidad 
    edaan:containsPersonalData false ;
    edaan:hasCertification [
        a edaan:CertificationReport ;
        rdfs:label "Gaia-X Label 1 Compliance" ;
        edaan:certificationLevel "Gaia-X Label 1" ;
        edaan:reportingEntity <https://gaia-x.eu/issuer> ;
        edaan:reportDate "2026-01-01"^^xsd:date
    ] .
```

Esto permite filtrar assets no solo por contenido, sino por **confianza y cumplimiento**, pilares de Gaia-X.

---

## 5. Métricas de Rendimiento

Las DataApps pueden declarar su rendimiento esperado para ayudar en la orquestación.

```turtle
ex:AppTiempoReal a edaan:VisualizationApp ;
    rdfs:label "Dashboard de Tráfico en Tiempo Real" ;
    
    # Métrica de rendimiento
    edaan:hasPerformanceMetric [
        a edaan:PerformanceMetric ;
        edaan:metricType <https://w3id.org/EDAAnOWL/Latency> ;
        edaan:metricValue 200 ;
        edaan:hasMetricStandard <http://qudt.org/vocab/unit/MilliSEC> ;
        edaan:computedAt "2025-06-01T12:00:00Z"^^xsd:dateTime
    ] .

---

## 6. Caso 4: Matchmaking por Sujeto (Feature of Interest)

Este escenario demuestra cómo encontrar datos sobre un **objeto específico** (ej: Olivos) independientemente de las propiedades medidas.

### A. El Perfil de Producción de Aceituna
Declara que el sujeto de estudio son los Olivos.

```turtle
ex:ProfileProduccionOlivar a edaan:DataProfile ;
    rdfs:label "Perfil de Producción Olivarera" ;
    # El sujeto de interés es el Olivo (AGROVOC)
    edaan:declaresFeatureOfInterest <http://aims.fao.org/aos/agrovoc/c_12926> .
```

### B. El Activo del Lote Experimental
Vincula el archivo físico a una parcela específica.

```turtle
ex:AssetParcelaJaen_001 a edaan:DataAsset ;
    dct:title "Sensores Parcela Jaen 001" ;
    # Este activo trata específicamente sobre esta parcela (individuo)
    edaan:hasFeatureOfInterest ex:ParcelaJaen_001 ;
    ids:representation [
        edaan:conformsToProfile ex:ProfileProduccionOlivar
    ] .
```

### C. La DataApp de Inventario Agrícola
Busca cualquier dataset que trate sobre Olivos para actualizar su inventario.

```turtle
ex:AppInventarioOlivares a ids:SmartDataApp ;
    dcat:theme theme:AGRI ;
    # La App declara directamente sobre qué objetos puede operar
    edaan:requiresFeatureOfInterest <http://aims.fao.org/aos/agrovoc/c_12926> ; # Olivo
    
    edaan:requiresProfile [
        a edaan:DataProfile ;
        edaan:declaresFeatureOfInterest <http://aims.fao.org/aos/agrovoc/c_12926> 
    ] .
```

**Resultado:** ¡MATCH! El motor semántico descubre que `ex:AssetParcelaJaen_001` es apto porque su perfil declara que el sujeto de estudio es el Olivo.
```
