# Informe de revision de EDAAnOWL v1.1.0

Fecha: 2026-03-16

## Resumen ejecutivo

EDAAnOWL v1.1.0 tiene una base conceptual buena para el objetivo principal de descubrimiento y matchmaking semantico entre datasets y data apps en espacios de datos. La separacion entre `DataSpecification`, `FieldMapping` y `Distribution` es la decision mas fuerte del modelo y es la que mejor posiciona la ontologia para reutilizacion entre dominios.

La principal conclusion de esta revision es que el modelo esta mas maduro que su capa de presentacion y publicacion. Lo que mas limita hoy su adopcion amplia no es la idea central, sino:

- la inconsistencia de versionado y narrativa entre `1.1.0` y `1.0.0`
- un quickstart que no era copiable directamente
- la falta de una demostracion visible de neutralidad sectorial
- algunas decisiones semanticas de alto impacto sobre vocabularios estandar

## Fortalezas

- Arquitectura de tres capas clara y util para matchmaking semantico.
- Buen encaje con DCAT, IDSA, BIGOWL, SOSA/SSN, QUDT, PROV y DQV.
- Ejemplos propios de `1.1.0` con buena cobertura funcional.
- Estrategia external-first razonable para favorecer interoperabilidad.
- Alineamiento practico con DCAT-AP-ES y ecosistema publico espanol.

## Riesgos prioritarios

### Prioridad alta

1. Quickstart y onboarding
   - El ejemplo rapido debe ser copiable, minimo y valido sin pasos ocultos.
   - Recomendacion: mantener un quickstart neutro y enlazar aparte al ejemplo agricola completo.

2. Coherencia de release
   - Ontologia, README, Widoco, changelog, ejemplos y shapes deben contar la misma historia de version.
   - Recomendacion: revisar cada release con una checklist de metadatos y referencias.

3. Reinterpretacion de DCAT
   - La declaracion `dcat:Catalog rdfs:subClassOf dcat:Dataset` introduce friccion con validadores y con la semantica esperada de DCAT.
   - Recomendacion para `1.1.0`: documentar esta decision como excepcional y dependiente del perfil CRED, o aislarla mejor en shapes y documentacion para que no se interprete como una redefinicion general de DCAT.
   - Recomendacion posterior: estudiar su retirada del core o moverla a un perfil especifico.

### Prioridad media

4. Matchmaking formalizado
   - El repositorio explica bien la intuicion, pero todavia no fija una especificacion clara de compatibilidad.
   - Recomendacion: definir niveles de match: exacto, compatible por unidad, compatible por transformacion, parcial y no compatible.

5. Neutralidad sectorial visible
   - El core parece generalista, pero la experiencia visible sigue demasiado centrada en agricultura.
   - Recomendacion: publicar ejemplos equivalentes en energia, movilidad o salud.

6. Operadores y restricciones
   - `constraintOperator` como texto libre es util para arrancar, pero debil para interoperabilidad fuerte.
   - Recomendacion: crear un pequeno vocabulario controlado de operadores o alinearlo con una representacion estandar.

### Prioridad baja

7. Mejora editorial
   - Hay restos de texto heredado en la documentacion.
   - Recomendacion: unificar el lenguaje de "introduced in v1.0.0" frente a "current in v1.1.0".

## Propuesta de cierre reforzado para la version 1.1.0

### Cambios recomendados que si pueden entrar en 1.1.0

- Corregir versionado y metadatos de publicacion.
- Dejar el quickstart minimo y valido.
- Hacer robustos los scripts de validacion en Windows.
- Separar en la tooling local la validacion de ejemplos propios frente a ejemplos oficiales externos.
- Mantener `DataSpecification` como unidad semantica pura y `FieldMapping` como borde tecnico.
- Consolidar `:hasConstraint` como propiedad canonica y dejar `:hasDataConstraint` como legado o alias documentado.
- Limpiar `widoco:introduction` para que no embeba imagenes remotas y no mezcle responsabilidades del modelo.
- Añadir al menos un ejemplo corto no agricola en la documentacion principal o en `examples/`.
- Añadir una seccion explicita de "semantic matchmaking" con reglas minimas:
  - coincidencia por `DataSpecification`
  - comprobacion de unidad
  - comprobacion de calidad
  - compatibilidad por esquema fisico a traves de `FieldMapping`
- Publicar una tabla breve de alineamiento del core:
  - `DataAsset`
  - `DataApp`
  - `DataSpecification`
  - `FieldMapping`
  - `InputProfile`
  - `DataConstraint`
- Revisar y limpiar el texto residual con referencias antiguas a `v1.0.0`.

### Cambios que podrian entrar en 1.1.0 solo si quieres asumir algo mas de riesgo

- Revisar la modelizacion de `dcat:Catalog` sin romper la compatibilidad de tus ejemplos actuales.
- Declarar explicitamente un perfil `core` y otro `compliance` dentro de la propia documentacion de `1.1.0`.
- Afinar `hasMetricStandard` para dejar totalmente claro que no describe el nucleo semantico del `DataSpecification`.
- Introducir un vocabulario controlado minimo para `constraintOperator`.

### Cambios que yo dejaria fuera de 1.1.0 si quieres una release estable

- Incorporar una especificacion de compatibilidad consumible por agentes.
- Anadir tests de matchmaking, no solo de sintaxis y SHACL.
- Publicar tabla normativa de alineamientos termino a termino.
- Reestructurar en profundidad la jerarquia DCAT del core.
- Cambiar de forma amplia la modularizacion del repositorio o separar fisicamente la ontologia en varios ficheros principales.

## Recomendaciones para adopcion amplia

- Mantener agricultura como caso tractor, pero no como cara principal del core.
- Presentar EDAAnOWL como capa semantica transversal para espacios de datos, con perfiles sectoriales encima.
- Evitar redefinir clases nucleares de estandares internacionales salvo en perfiles claramente etiquetados.
- Priorizar ejemplos que muestren reutilizacion real de la misma `DataSpecification` en varios dominios o esquemas tecnicos.

## Alcance recomendado para cerrar 1.1.0

Mi recomendacion practica es cerrar `1.1.0` con este alcance:

- modelo semantico interno consistente
- quickstart y documentacion coherentes
- validacion local robusta
- narrativa claramente generalista aunque el caso tractor siga siendo agricola
- matchmaking descrito de forma minima pero util

Y evitar en `1.1.0` cualquier cambio que obligue a rehacer por completo la alineacion DCAT o la estructura principal del repositorio.

## Estado tras esta revision

En esta iteracion se han corregido mejoras de bajo riesgo y alto impacto:

- quickstart principal actualizado y copiable
- referencias de version alineadas a `1.1.0` en documentacion principal y metadata de ontologia
- scripts de validacion adaptados para no fallar por la codificacion de consola en Windows
- validacion SHACL local separada por defecto de los ejemplos RDF oficiales externos

## Conclusion

La direccion es buena y el nucleo del modelo merece seguir evolucionando. Si quieres posicionarla para adopcion amplia, el siguiente salto no es anadir muchas mas clases, sino estabilizar el core, modularizar perfiles y publicar una especificacion de matchmaking realmente normativa.
