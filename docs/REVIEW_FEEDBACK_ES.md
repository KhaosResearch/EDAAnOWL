# Hallazgos de Revisión (EDAAnOWL v0.5.0)

## 1) Hallazgos priorizados

1. **[Crítico] Inconsistencia semántica de métricas respecto a DQV**  
Evidencia: `src/0.5.0/README.md:46` afirma que `:Metric` es una *measurement*, pero en ontología `:Metric` es `dqv:Metric` en `src/0.5.0/EDAAnOWL.ttl:1143` (en DQV eso es definición de métrica).  
Evidencia: `:metricType` apunta a `:MetricType` en `src/0.5.0/EDAAnOWL.ttl:451` y `src/0.5.0/EDAAnOWL.ttl:455`, pero `:MetricType` no es `dqv:Metric` en `src/0.5.0/EDAAnOWL.ttl:1161`.  
Recomendación: separar definición y medición (modelo DQV completo), o ajustar naming/clases para que no contradigan DQV.

2. **[Alto] `PerformanceMetric` no queda correctamente conectado a `DataApp`**  
Evidencia: `:hasMetric` tiene dominio `:DataProfile` en `src/0.5.0/EDAAnOWL.ttl:401`, pero `:PerformanceMetric` se describe para DataApp/servicio en `src/0.5.0/EDAAnOWL.ttl:1181`.  
Recomendación: crear `:hasPerformanceMetric` (dominio `ids:DataApp`) o ampliar dominio de `:hasMetric` con `owl:unionOf`.

3. **[Alto] Inconsistencia de clases BIGOWL entre ontología, SHACL y docs**  
Evidencia: se usa `bigdat:TabularData` en texto de ontología (`src/0.5.0/EDAAnOWL.ttl:74`, `src/0.5.0/EDAAnOWL.ttl:104`) y `bigdat:TabularDataSet` en otros sitios (`src/0.5.0/EDAAnOWL.ttl:334`).  
Evidencia: SHACL usa `bigdat:TabularData` y `bigdat:StructuredData` en `src/0.5.0/shapes/edaan-shapes.ttl:294` y `src/0.5.0/shapes/edaan-shapes.ttl:296`, pero esos términos no están en el stub local (`src/0.5.0/vocabularies/datatype-scheme.ttl:32`).  
Recomendación: unificar en un único set de clases BIGOWL en ontología, SHACL y documentación.

4. **[Alto] Estrategia de vocabularios contradictoria en documentación**  
Evidencia: “no local SKOS vocabularies” en `src/0.5.0/README.md:110`, pero “Modular Vocabularies” locales en `README.md:185`.  
Evidencia: `src/0.5.0/README.md:125` dice que se retiene `datatype-scheme` por falta de equivalentes, pero ahí mismo `:georaster`, `:tabular`, `:timeseries` están deprecados (`src/0.5.0/vocabularies/datatype-scheme.ttl:63`).  
Recomendación: fijar una narrativa única (vocabularios externos normativos + stubs de referencia, por ejemplo).

5. **[Medio] Dominio de `:hasDomainSector` potencialmente problemático**  
Evidencia: doble dominio `ids:DataApp` y `ids:Resource` en `src/0.5.0/EDAAnOWL.ttl:373`; en RDF eso implica intersección.  
Evidencia: en este fichero `ids:DataApp` no está declarado como subclase de `ids:Resource` (`src/0.5.0/EDAAnOWL.ttl:1263`).  
Recomendación: usar dominio con `owl:unionOf` o declarar jerarquía IDSA completa.

6. **[Medio] `VerifiableDataProfile` mezcla conceptos distintos**  
Evidencia: `:VerifiableDataProfile` es subclase de `:DataProfile` y de `VerifiableCredential` en `src/0.5.0/EDAAnOWL.ttl:1323`, pero también existe `:hasCredential` en `src/0.5.0/EDAAnOWL.ttl:670`.  
Recomendación: modelar VC como recurso separado enlazado desde `DataProfile` con `:hasCredential`.

7. **[Medio] Referencias internas desactualizadas a propiedades deprecadas**  
Evidencia: comentarios de `DataProfile` siguen citando `:profileCRSRef` (`src/0.5.0/EDAAnOWL.ttl:1107`, `src/0.5.0/EDAAnOWL.ttl:1117`) aunque está deprecada en `src/0.5.0/EDAAnOWL.ttl:850` y reemplazada por `:hasCRS` en `src/0.5.0/EDAAnOWL.ttl:360`.  
Recomendación: actualizar comentarios internos para evitar guiar a implementaciones legacy.

8. **[Medio] Recomendación de sector en docs no alineada con ontología**  
Evidencia: `README.md:150` recomienda AGROVOC para `:hasDomainSector`, pero ontología recomienda EU Data Theme NAL para ese predicado en `src/0.5.0/EDAAnOWL.ttl:378`.  
Recomendación: usar EU Data Theme NAL para sector y AGROVOC para `:topic`.

9. **[Bajo] Detalles documentales desfasados**  
Evidencia: badge SHACL apunta a `src/0.4.0/...` en `README.md:9`.  
Evidencia: Mermaid con IDs no definidos en `ARCHITECTURE.md:38`, `ARCHITECTURE.md:42`, `ARCHITECTURE.md:68`.  
Evidencia: texto menciona v0.4.0 en `ARCHITECTURE.md:133`.  
Recomendación: limpieza documental para evitar confusión de adopción.

## 2) Estado de validación técnica actual

1. Se ejecutó validación completa con `bash scripts/local-validate.sh`.
2. Resultado: RDF OK, SHACL OK, OWL consistency OK (`Conforms: True`).

## 3) Alineaciones adicionales recomendadas

1. **QUDT** para unidades de métricas (sustituir `:metricUnit` como string por URI de unidad).
2. **CSVW** para estructura tabular fina (columnas, tipos, constraints) vía `ids:dataTypeSchema`.
3. **GeoSPARQL 1.1** para cobertura/geométricas espaciales interoperables.
4. **DPV** para privacidad/compliance (si se amplía ese eje).

## 4) Orden de cambios recomendado

1. Corregir modelo DQV de métricas (definición vs medición).
2. Resolver enlace de métricas de rendimiento para `DataApp`.
3. Unificar clases BIGOWL de tipo de dato en ontología + SHACL + docs.
4. Armonizar documentación sobre vocabularios y deprecaciones.
