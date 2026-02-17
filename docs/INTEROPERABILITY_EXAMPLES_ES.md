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

ex:AssetMalagaMultiuso a edaan:DataAsset ;
    dct:title "Datos Urbanos Integrados Málaga" ;
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
        edaan:metricName "completeness" ;
        edaan:metricValue 0.95 ; # Exige alta completitud
        edaan:appliesToFeatureConcept <http://purl.obolibrary.org/obo/ENVO_01000203> 
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
    # Esta App busca datos de temperatura
    edaan:requiresProfile [
        a edaan:DataProfile ;
        edaan:declaresObservedProperty <http://purl.obolibrary.org/obo/ENVO_01000203> 
    ] .
```
**Resultado:** ¡MATCH! `AssetMalagaMultiuso` tiene `ProfileMeteo` que declara esa propiedad.

### Caso 2: DataApp de Tráfico (SmartCity)

```turtle
ex:AppSemaforosInteligentes a ids:SmartDataApp ;
    # Esta App busca datos de tráfico
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
