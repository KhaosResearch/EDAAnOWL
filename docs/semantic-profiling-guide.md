# Ejemplo Completo: Dataset Real y Diferencia entre DQV y QUDT

Es muy normal hacerse un lío con la diferencia entre la **Calidad del Dato (DQV)** y las **Unidades de Medida (QUDT)**, porque ambas forman la idea abstracta de una "Métrica". 

En la versión **v0.7.0** de EDAAnOWL, hemos clarificado esta separación. Aquí tienes la regla de oro:

- **DQV (Data Quality Vocabulary):** Define **QUÉ** estás midiendo y **CUÁL** es su valor. 
  Por ejemplo: *"Estoy midiendo la Completitud de la columna"* o *"Estoy calculando el Rendimiento Medio"*. (Usa `dqv:value`).
- **QUDT & SKOS (Estándares):** Define en **QUÉ REFERENCIA** está expresado ese valor. 
  Puede ser una **Unidad Física** (Kilos, Litros) o un **Vocabulario** (SIEX, AGROVOC). (Usa `edaan:hasMetricStandard`).

### ¿Cómo se asocian las Unidades a las Propiedades?

Una duda común es: *¿Por qué no ponemos la unidad directamente en la Propiedad Observable (ej. en el concepto de AGROVOC)?*
La respuesta es por **Interoperabilidad**: El fenómeno físico "Rendimiento" es universal, pero puede medirse en Kilos, Toneladas o Libras. Si fijamos la unidad en el concepto, rompemos el estándar.

La solución de EDAAnOWL v0.7.0 es el **vínculo a través de la Métrica** usando la nueva propiedad `edaan:measuresProperty` y fijando su sistema de referencia con `edaan:hasMetricStandard`. La métrica actúa como el "pegamento" que dice: *"Este valor (dqv:value), expresado en este estándar (hasMetricStandard), es una medición de esta propiedad (measuresProperty)"*.

A continuación, vamos a ver un caso real: un archivo `CSV` de una granja que registra las cosechas, el agua de riego aplicada y el abono empleado, columnas por columna.

---

## 1. El Dataset Real (Archivo CSV)

Imagina un fichero CSV llamado `registro-campo-2024.csv` con estas columnas:

| fecha      | parcela_id | rendimiento_kg | riego_litros | fertilizante_n_kg | notas |
|------------|------------|----------------|--------------|-------------------|-------|
| 2024-05-10 | P-01       | 4500.5         | 12000.0      | 50.2              | Ok    |
| 2024-05-12 | P-02       | 3800.0         | 11500.0      | 45.0              | ...   |

Este CSV ofrece datos sobre 3 cosas físicas reales (**Propiedades Observables - AGROVOC**):
1. **Rendimiento de cultivo** (`agrovoc:c_8488`): Medido en Kilogramos (`unit:KiloGM`).
2. **Riego / Agua** (`agrovoc:c_3954`): Medido en Litros (`unit:L`).
3. **Nitrógeno** (`agrovoc:c_5193`): Medido en Kilogramos (`unit:KiloGM`).

---

## 2. Modelando con EDAAnOWL v0.7.0 (Turtle)

Vamos a modelar el `DataAsset`, la `DataRepresentation` del CSV, y su `DataProfile`. 
Fíjate bien en el perfil (`Profile_RegistroCampo`): ahí es donde creamos las **Métricas**. Algunas métricas describen la *calidad* del CSV (ej. valores nulos) y otras describen un *resumen de los datos* (ej. la media total de rendimiento para la gente que busque por volumen).

```turtle
@prefix : <https://w3id.org/EDAAnOWL/> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix ids: <https://w3id.org/idsa/core/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix agrovoc: <http://aims.fao.org/aos/agrovoc/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix qudt: <http://qudt.org/schema/qudt/> .
@prefix unit: <http://qudt.org/vocab/unit/> .
@prefix bigdat: <https://w3id.org/BIGOWLData/> .
@prefix ex: <http://example.org/data/> .

# ------------------------------------------------------------------
# 1. El Dataset (Asset)
# Observa que declaramos QUÉ fenómenos físicos recoge el CSV en general
# ------------------------------------------------------------------
ex:Asset_RegistroCampo a :DataAsset, dcat:Dataset ;
    dct:title "Registro Agrícola de Campo 2024"@es ;
    :servesObservableProperty agrovoc:c_8488,   # Contiene datos de Rendimiento 
                              agrovoc:c_3954,   # Contiene datos de Riego
                              agrovoc:c_5193 ;  # Contiene datos de Nitrógeno
    ids:representation ex:Repr_CSV_Registro .

# ------------------------------------------------------------------
# 2. La Representación Física (El archivo CSV)
# ------------------------------------------------------------------
ex:Repr_CSV_Registro a :DataRepresentation ;
    dct:format "text/csv" ;
    dcat:accessURL <https://server.com/registro-campo-2024.csv> ;
    ids:instance [ a ids:Artifact ; ids:fileName "registro-campo-2024.csv" ] ;
    dct:conformsTo ex:Profile_RegistroCampo . # Aquí enlazamos nuestro perfil semántico

# ------------------------------------------------------------------
# 3. El Perfil de Datos (DataProfile)
# Es aquí donde vive la distinción DQV vs QUDT
# ------------------------------------------------------------------
ex:Profile_RegistroCampo a :DataProfile ;
    :declaresDataClass bigdat:TabularDataSet ;
    
    # ---------------------------
    # MÉTRICA DE CALIDAD (DQV) 
    # Mide la integridad del CSV
    # ---------------------------
    :hasMetric [
        a :Metric, :QualityMetric ;
        # -- Parte DQV (Qué mido y su valor) --
        :metricName "completitud_columna_riego" ;
        dqv:value "99.5"^^xsd:decimal ;
        
        # -- Parte Estándar (En qué unidad está el 99.5) --
        :hasMetricStandard unit:PERCENT ;       # La métrica está en Porcentaje (%)
        :appliesToFeature "riego_litros"    # Sobre la columna 'riego_litros'
    ] ,

    # ---------------------------
    # MÉTRICA DE PROFILING (AGREGACIÓN DE DATOS)
    # Resume el Rendimiento Total
    # ---------------------------
    [
        a :Metric ;
        # -- Parte DQV (Qué mido y su valor) --
        :metricName "rendimiento_total_acumulado" ;
        dqv:value "81000.5"^^xsd:decimal ;
        
        # -- SECCION CLAVE: El vínculo semántico --
        :measuresProperty agrovoc:c_8488 ;  # Decimos que esto mide el Rendimiento
        :hasMetricStandard unit:KiloGM ;        # Y que está en Kilogramos
        
        :appliesToFeature "rendimiento_kg"  # Calculado sobre la columna 'rendimiento_kg'
    ] ,

    # ---------------------------
    # MÉTRICA DE PROFILING (AGREGACIÓN DE DATOS)
    # Resume la Media de Agua Empleada
    # ---------------------------
    [
        a :Metric ;
        # -- Parte DQV (Qué mido y su valor) --
        :metricName "riego_medio_por_parcela" ;
        dqv:value "11750.0"^^xsd:decimal ;
        
        # -- SECCION CLAVE --
        :measuresProperty agrovoc:c_3954 ;  # Decimos que esto mide el Riego
        :hasMetricStandard unit:L ;             # Y que está en Litros (L)
        
        :appliesToFeature "riego_litros"
    ] .
```

## Resumen del Ejemplo

1. El Dataset indica mediante `servesObservableProperty` que sabe de *Rendimiento (agrovoc)* y *Riego (agrovoc)*.
2. Eso informa a un buscador de que ahí encontrará variables agrícolas.
3. El *Profile* va mucho más allá: inspecciona los datos `(DQV)` para ver que el CSV está completo al `99.5 (QUDT: Porcentaje)`.
4. El *Profile* también hace un resumen estadístico y expone que la media de riego aplicado fue `11750 (QUDT: Litros)`.

De este modo separar **el valor matemático y su definición lógica (DQV)** de **su magnitud física real (QUDT)**.

> [!IMPORTANT]
> **Profiling vs. Anotación: ¿Por qué solo un `dqv:value`?**
> Es vital entender que `DataProfile` sirve para describir el **fichero entero** (metadato), no para anotar cada fila individual. 
> - Si pones `dqv:value "Arcilloso"`, estás reportando una **métrica de resumen** (ej. la Moda o el valor más frecuente del dataset).
> - Si quisiéramos anotar cada fila, estaríamos haciendo **Anotación Semántica** (RDF), lo cual generaría millones de datos. El Catálogo solo necesita el "perfil" para que una App sepa si el dataset le sirve o no antes de comprarlo.

---

## 2.1 ¿Y qué pasa con los datos no numéricos (Categorías)?

No todo en un Data Space son kilos o litros. ¿Qué pasa si tu columna contiene etiquetas como "Abono Orgánico" o "Nitrato Amónico"?

Para estos casos, sustituimos la **Unidad de Medida** por un **Vocabulario Controlado (skos:ConceptScheme)**. 

### Reglas para Datos Categóricos:
1. **measuresProperty:** Sigue apuntando al fenómeno (ej. `agrovoc:Fertilizers`).
2. **hasMetricStandard:** Sigue siendo la misma propiedad, pero ahora apunta al tesauro oficial (ej. SIEX).

### Ejemplo Turtle (Columna Categórica):
```turtle
# Perfil para un dataset de tratamientos fitosanitarios
ex:Profile_Tratamientos a :DataProfile ;
    :hasMetric [
        a :Metric ;
        :metricName "fertilizante_utilizado" ;
        :appliesToFeature "tipo_abono" ;
        
        # El fenómeno es el Fertilizante
        :measuresProperty agrovoc:c_2862 ; 
        
        # Usamos la misma propiedad que para unidades, el sistema es idéntico
        :hasMetricStandard <https://w3id.org/SIEX/vocab/Fertilizantes> ;
        
        # Podemos indicar el valor más frecuente (Moda) como resumen
        dqv:value "Urea" ; 
        :metricType :TopCategory 
    ] .

### Ejemplo 2: Clasificación de Textura del Suelo (Variedad Categórica)
El mismo Asset puede reportar distintas métricas según el estándar que use el usuario final. Aquí vemos la variedad de valores permitidos:

```turtle
# Métrica 1: Valor predominante de Textura
ex:Metric_Textura_A a :Metric ;
    # Usamos URI externa de DDI (Data Documentation Initiative) para el concepto de "Moda"
    :metricType <http://rdf-vocabulary.ddialliance.org/cv/SummaryStatisticType/2.1.2/650be61> ; 
    :metricName "textura_predominante" ; # Etiqueta humana opcional
    :measuresProperty agrovoc:c_7181 ; 
    :hasMetricStandard <http://aims.fao.org/aos/agrovoc/c_7183> ; 
    dqv:value "Arcilloso" . 

# Métrica 2: Categoría de Drenaje (Cualitativo)
ex:Metric_Drenaje a :Metric ;
    :metricType <http://rdf-vocabulary.ddialliance.org/cv/SummaryStatisticType/2.1.2/650be61> ;
    :metricName "capacidad_drenaje" ;
    :measuresProperty agrovoc:c_2393 ; # Drenaje
    :hasMetricStandard ex:SoilDrainage_Scheme ;
    dqv:value "Moderadamente rápido" . 
```

## 2.2 El Nivel de Abstracción Total: Meta-Métricas (La Galería Meta)

¿Podemos medir cosas que no están en el fichero, sino que describen al Dataset en sí? **SÍ**. Esto permite que una App filtre por "Confianza" o "Madurez".

### Ejemplo 1: Nivel de Privacidad (GDPR/DPV)
```turtle
ex:Metric_Privacidad a :Metric ;
    :measuresProperty <https://w3id.org/dpv#DataClassification> ; 
    :hasMetricStandard ex:GDPR_Levels ; 
    dqv:value "Datos Seudonimizados" . # O "Datos Sensibles", "Privacidad Total"...
```

### Ejemplo 2: Madurez Tecnológica (TRL - Technical Readiness Level)
Útil para saber si un dataset viene de un experimento de laboratorio o de un entorno de producción real.
```turtle
ex:Metric_TRL a :Metric ;
    :metricName "nivel_madurez_datos" ;
    :measuresProperty <http://purl.org/npg/ontology/trl> ; # Estándar TRL
    :hasMetricStandard <https://w3id.org/standards/TRL_Scale> ;
    dqv:value "TRL 9" . # Sistema probado en entorno operativo
```

### Ejemplo 3: Puntuación de Confianza (Trust Score)
Un valor abstracto calculado por un tercero independiente.
```turtle
ex:Metric_Trust a :Metric ;
    :metricName "indice_confiabilidad" ;
    :measuresProperty <https://w3id.org/trust/Score> ;
    :hasMetricStandard unit:PERCENT ; # Las meta-métricas también pueden ser numéricas
    dqv:value "98" 
.
```

---

## 2.3 Soporte para Tipos Avanzados: Esquemas y Streaming

Para escenarios industriales o de tiempo real, el perfil semántico (`:DataProfile`) puede ahora vincularse con la estructura técnica exacta y definir el comportamiento del flujo.

### Ejemplo 1: Vinculación con JSON Schema (Estructura Técnica)
A diferencia de la semántica (que dice *qué* es el dato), el esquema técnico dice *cómo* está construido físicamente.

```turtle
ex:Profile_IoT_Avanzado a :DataProfile ;
    :declaresDataClass bigdat:NestedData ;
    
    # Vinculación técnica
    :conformsToSchema <https://schema.example.org/sensor-v2.json> ;
    :hasSchemaType <https://www.iana.org/assignments/media-types/application/schema+json> ;
    
    :hasMetric [
        a :Metric ;
        :metricName "avg_latency" ;
        :hasMetricStandard unit:MilliSEC ;
        dqv:value "120"
    ] .
```

### Ejemplo 2: Datos en Tiempo Real (Streaming)
Para activos que no son ficheros estáticos, sino flujos continuos (MQTT, Kafka).

```turtle
ex:Profile_RealTime_Weather a :DataProfile ;
    :isStreaming true ; # Indica que el dato es un flujo continuo
    dcat:temporalResolution "PT1S"^^xsd:duration ; # Resolución de 1 segundo
    :hasMetric [
        a :Metric ;
        :metricName "update_rate" ;
        :hasMetricStandard unit:HERZ ; # Hercios
        dqv:value "1"
    ] .
```

---

## 3. Compras Seguras: Matchmaking Semántico en el Espacio de Datos

El usuario ha planteado una pregunta clave: *"¿Para qué sirve todo esto si yo soy el creador de una App y quiero comprar datos?"*

En un **Data Space** (como el propuesto por IDSA), el pago por datos es un intercambio común, y comprar el dataset incorrecto puede ser un problema grave. Aquí es donde brilla la separación entre "Fenómeno Físico" y "Unidad de Medida" de EDAAnOWL v0.7.0.

### El Escenario de Matchmaking

Imagina que desarrollas una **DataApp** llamada "Calculadora de Renta Agrícola". Tu aplicación recibe datos de Rendimiento de Cultivo (Yield) para hacer proyecciones económicas, pero el algoritmo de tu App está programado única y exclusivamente para trabajar con **Toneladas por Hectárea**. 

Si compras un Dataset de "Rendimiento" expresado en "Libras por Acre", tu aplicación fallará estrepitosamente.

### La Solución: SHACL + QUDT

Con EDAAnOWL, cada Dataset (`DataAsset`) expone libre y públicamente su **DataProfile**. Este perfil es un metadato ligero que *no contiene la información jugosa y privada* por la que estás pagando, pero sí expone **cómo está estructurada**.

Tú, como dueño de la App, puedes publicar un "requisito" en forma de validación semántica (SHACL). Tu regla sería algo así:

> *"Para que un Asset sea compatible con mi App, DEBE declarar que sirve a la propiedad `agrovoc:c_8488` (Rendimiento) Y su Perfil DEBE tener una Métrica cuyo `hasMetricStandard` sea indiscutiblemente `unit:TON_Metric` (Toneladas)."*

### Modelando la DataApp (Turtle)

Para que el Espacio de Datos pueda leer tus requisitos, primero debes declarar tu aplicación formalmente. Observa cómo usamos `requiresObservableProperty` para decir lo que necesitamos, y cómo definimos un perfil de *Requisitos* para exigir la unidad de medida.

```turtle
# ------------------------------------------------------------------
# 4. La Aplicación (DataApp) que BUSCA datos
# ------------------------------------------------------------------
ex:App_CalculadoraRendimiento a ids:SmartDataApp ;
    dct:title "Calculadora de Renta Agrícola"@es ;
    
    # Decimos QUÉ propiedad física necesita la App para funcionar
    :requiresObservableProperty agrovoc:c_8488 ; # Necesita Rendimiento
    
    # Vinculamos un Perfil de Requisitos
    :requiresProfile ex:ProfileReq_Calculadora .

# ------------------------------------------------------------------
# 5. El Perfil de Requisitos de la App
# Aquí exigimos la unidad exacta
# ------------------------------------------------------------------
ex:ProfileReq_Calculadora a :DataProfile ;
    # Exigimos datos tabulares
    :declaresDataClass bigdat:TabularDataSet ;
    
    # Exigimos tener una métrica en TONELADAS para el RENDIMIENTO
    :hasMetric [
        a :Metric ;
        :measuresProperty agrovoc:c_8488 ; # Vínculo explícito
        :hasMetricStandard unit:TON_Metric
    ] .
```

### La Consulta de Matchmaking (SPARQL)

Una vez que el Data Space tiene registrados tanto los Datasets de los proveedores (como el CSV de la sección 2) como tu DataApp (sección 4), el motor semántico ejecuta la búsqueda.

Aquí tienes la consulta **SPARQL** que cruza la información. Esta consulta busca Datasets compatibles para nuestra `ex:App_CalculadoraRendimiento`:

```sparql
PREFIX edaan: <https://w3id.org/EDAAnOWL/>
PREFIX ids: <https://w3id.org/idsa/core/>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?appTitle ?datasetTitle ?dataset
WHERE {
  # 1. Seleccionamos nuestra App y la propiedad que requiere
  BIND(<http://example.org/data/App_CalculadoraRendimiento> AS ?app)
  ?app dct:title ?appTitle ;
       edaan:requiresObservableProperty ?requiredProp ;
       edaan:requiresProfile ?appProfile .
       
  # 2. Descubrimos el Estándar (Unidad o Vocabulario) que exige la App
  ?appProfile edaan:hasMetric ?appMetricReq .
  ?appMetricReq edaan:hasMetricStandard ?requiredStandard .

  # 3. Buscamos un Dataset en el catálogo que SIRVA esa misma propiedad
  ?dataset a edaan:DataAsset ;
           dct:title ?datasetTitle ;
           edaan:servesObservableProperty ?requiredProp ;
           ids:representation ?representation .
           
  # 4. Verificamos que el Dataset cumpla el requisito EXACTO del Estándar
  ?representation dct:conformsTo ?datasetProfile .
  ?datasetProfile edaan:hasMetric ?datasetMetric .
  ?datasetMetric edaan:hasMetricStandard ?requiredStandard .
}
```

### ¿Qué ocurriría al ejecutar esto?

1. **Si evaluamos contra el CSV del ejemplo de arriba (`ex:Asset_RegistroCampo`):**
   - Sirve `agrovoc:c_8488` (Rendimiento). **✅ Check 1: Propiedad correcta.**
   - Su perfil reporta `unit:KiloGM`.
   - Nuestra app exige `unit:TON_Metric`.
   - La consulta SPARQL **filtrará y descartará** este Dataset. ¡Te has ahorrado comprar un dataset inútil para tu App porque la unidad matemática es distinta!

2. **Si el proveedor sube un CSV en Toneladas (`unit:TON_Metric`):**
   - La consulta SPARQL detecta que las URIs `unit:TON_Metric` del requisito y de la oferta son **idénticas**.
   - El sistema devuelve un "Match Positivo" y te sugiere comprarlo con total seguridad operacional.

Esta es la potencia real de usar ontologías formales como QUDT sobre simples etiquetas de texto. Una etiqueta `"%"` o `"toneladas"` es subjetiva y puede escribirse de mil formas ("Ton", "Tons", "t"), lo cual rompe los JOIN de bases de datos. Sin embargo, `unit:TON_Metric` es una URI global inmutable que los motores de los Data Spaces (SPARQL, SHACL) pueden evaluar a la perfección.

### ¿Tiene Sentido una Exigencia Tan Estricta?

Es natural preguntarse: *"¿No es demasiado restrictivo que una App rechace un dataset solo porque está en Kilos en lugar de Toneladas?"*. En un Data Space corporativo o industrial, **esta rigidez no solo tiene sentido, es una necesidad comercial profunda**:

1. **La Fragilidad de los Algoritmos (IA / Machine Learning):** Las DataApps casi nunca son interfaces visuales para humanos; suelen ser pipelines de modelado algorítmico o IA. Estos modelos no tienen "sentido común". Si una red neuronal está entrenada asumiendo que el riego entra en `Milímetros (mm)`, e ingiere datos provenientes en `Litros por m2`, la matemática subyacente fallará de forma silenciosa, devolviendo predicciones catastróficas. Restringir la unidad a nivel semántico garantiza operaciones seguras.
2. **"Plug-and-Play" (Conectar y Listo):** Al pagar por datos, el comprador espera usarlos de inmediato (Plug-and-play). Si la App no exige unidades explícitas, obligamos al comprador a auditar los CSVs y crear *scripts* "pegamento" en Python para traducir Kilos a Toneladas antes de poder usarlos.
3. **El Santo Grial: Los Servicios de Transformación Automática:** Como el Data Space sabe que ambos (App y Dataset) hablan en "QUDT", sabe qué magnitud subyace. Un intermediario avanzado en la red podría decir: *"Estos datos están en Kilos, tu App pide Toneladas. Son compatibles porque miden Masa (*Mass*). Añadiré un nodo de microservicio de conversión automáticamente en el flujo"*. Esto solo es viable cuando las entidades y métricas operan con URIs formales indiscutibles en lugar de cadenas de texto libre.

---

## 4. Integración en el Frontend (UI de Publicación)

Para que toda esta potencia semántica sea usable, la interfaz gráfica del Data Space (el formulario de "Nuevo Recurso" en el panel de control) debe facilitar la captura de estos datos sin que el usuario necesite saber escribir código Turtle.

### Estructura sugerida para el bloque "Perfil Semántico"

Debajo de la selección de **Propiedad Observada** (ej. "Rendimiento de Cultivo (agrovoc:c_8488)"), el formulario debe incluir un área dinámica llamada **Métricas de Calidad y Resumen**.

Cada vez que el usuario añada una métrica, figurará una fila con 4 componentes clave que mapean directamente a la ontología:

1. **¿Qué estamos midiendo?**
   - *UI:* Input de texto o selector de catálogo.
   - *Ejemplo:* "completitud" o "rendimiento_medio".
   - *Mapeo Ontológico:* `edaan:metricName`

2. **Columna / Campo Objetivo (Opcional)**
   - *UI:* Input de texto.
   - *Ejemplo:* "riego_litros".
   - *Mapeo Ontológico:* `edaan:appliesToFeature` (o a futuro `appliesToFeatureConcept`).

3. **Valor Resultante**
   - *UI:* Input numérico.
   - *Ejemplo:* `99.5` o `12000`.
   - *Mapeo Ontológico:* `dqv:value`

4. **Estándar de Referencia**
   - *UI:* Dropdown restrictivo (No texto libre).
   - *Opciones amigables:* "Porcentaje (%)", "Kilogramos (kg)", "Tesauro SIEX Fertilizantes".
   - *Mapeo Ontológico:* `edaan:hasMetricStandard` apuntando a `unit:PERCENT`, `unit:KiloGM`, o la URI del vocabulario.

### Automatización (El escenario ideal)

En un Data Space avanzado, el usuario humano casi no debería rellenar este formulario. 
Lo óptimo es implementar un **Data Profiler** en el backend. Cuando el usuario sube su `registro-campo-2024.csv`, el sistema lo analiza, extrae las medias de las columnas numéricas, identifica vacíos (completitud) y **autopopula el formulario**. 

El usuario solo se encarga de confirmar la propuesta (por ejemplo, confirmando que la columna numérica *rendimiento* se midió en Kilos y no en Onzas).
