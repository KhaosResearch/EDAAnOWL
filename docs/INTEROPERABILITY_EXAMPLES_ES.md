# Ejemplos de Interoperabilidad Semántica y Polimorfismo (v1.0.0)

Este documento ilustra cómo la arquitectura de 3 capas de EDAAnOWL v1.0.0 permite que un único activo de datos sirva a múltiples aplicaciones de distintos dominios de manera eficiente.

---

## Escenario: El Dataset "Polímata" Urban-Agri

Tenemos un fichero CSV físico (`malaga_smart_city_2026.csv`) que contiene datos de sensores instalados en una zona urbana cercana a huertos periurbanos.

**Columnas:** `[timestamp, station_id, air_temp, traffic_intensity, pollution_no2]`

Este ÚNICO activo sirve a dos tipos de aplicaciones totalmente distintas.

### 1. El Activo y su Representación Física

```turtle
@prefix ex: <https://example.org/> .
@prefix edaan: <https://w3id.org/EDAAnOWL/> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix theme: <http://publications.europa.eu/resource/authority/data-theme/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix qudt: <http://qudt.org/vocab/unit/> .

ex:AssetUrbanAgri a edaan:DataAsset, dcat:Dataset ;
    dct:title "Monitoreo Urbano-Agrícola Málaga 2026" ;
    dcat:theme theme:ENVI, theme:TRAN, theme:AGRI ;
    dcat:distribution ex:DistribucionCSV .

ex:DistribucionCSV a edaan:DataRepresentation, dcat:Distribution ;
    dct:format <http://publications.europa.eu/resource/authority/file-type/CSV> ;
    
    # POLIMORFISMO SEMÁNTICO: Múltiples mapeos en el mismo archivo
    edaan:hasFieldMapping [
        a edaan:FieldMapping ;
        edaan:mapsToSpecification ex:SpecAirTemp ;
        edaan:mapsField "air_temp" ;
        edaan:hasUnit qudt:DEG_C
    ] ,
    [
        a edaan:FieldMapping ;
        edaan:mapsToSpecification ex:SpecTrafficFlow ;
        edaan:mapsField "traffic_intensity" ;
        edaan:hasUnit qudt:VEHICLE-PER-HR
    ] ,
    [
        a edaan:FieldMapping ;
        edaan:mapsToSpecification ex:SpecNO2Concentration ;
        edaan:mapsField "pollution_no2" ;
        edaan:hasUnit qudt:MicroGM-PER-M3
    ] .
```

---

## 2. Los Consumidores (DataApps)

### Aplicación A: Optimización de Riego (SmartAgri)
A esta app solo le interesa la temperatura para calcular la evapotranspiración.

```turtle
ex:AppSmartIrrigation a edaan:DataApp ;
    edaan:hasInputProfile [
        a edaan:InputProfile ;
        edaan:hasDataSpecification ex:SpecAirTemp ;
        edaan:hasConstraint [
            a edaan:DataConstraint ;
            edaan:requiresUnit qudt:DEG_C 
        ]
    ] .
```
**Resultado:** ¡MATCH! El motor encuentra que `ex:AssetUrbanAgri` tiene un mapeo a `ex:SpecAirTemp` en grados Celsius.

### Aplicación B: Gestión de Tráfico (SmartCity)
A esta app le interesa el flujo de vehículos.

```turtle
ex:AppTrafficControl a edaan:DataApp ;
    edaan:hasInputProfile [
        a edaan:InputProfile ;
        edaan:hasDataSpecification ex:SpecTrafficFlow ;
        edaan:hasConstraint [
            a edaan:DataConstraint ;
            edaan:requiresUnit qudt:VEHICLE-PER-HR 
        ]
    ] .
```
**Resultado:** ¡MATCH! El MISMO activo sirve a esta aplicación mediante su segundo mapeo.

---

## 3. Beneficios de la Arquitectura v1.0.0

1.  **Sin Redundancia:** No hace falta crear perfiles específicos para cada combinación de columnas. El `FieldMapping` es granular (por columna).
2.  **Matchmaking Desacoplado:** Las aplicaciones no necesitan conocer el nombre de la columna (`air_temp` vs `temperature`). Solo buscan por la URI de la `DataSpecification`.
3.  **Seguridad en el Tipo de Dato:** Gracias a `hasUnit` y `hasDataType` en el mapeo, la App sabe exactamente cómo parsear el valor antes de procesarlo.

Este modelo permite crear un verdadero **Mercado de Datos Semántico** donde la oferta y la demanda se encuentran mediante definiciones abstractas de variables reales.
