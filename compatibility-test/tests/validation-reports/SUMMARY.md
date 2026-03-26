# Informe de Validación DCAT-AP-ES

**Generado:** 2026-03-16 13:52:12

## Visión General de las Fases de Validación

El proceso de validación de DCAT-AP-ES consta de tres fases complementarias:

### Fase 2: Validación semántica (Ejemplos RDF contra SHACL)
**Propósito:** Validar archivos de ejemplo RDF contra las restricciones de las formas SHACL

| Caso de Prueba | Esperado | Estado |
|----------------|----------|--------|
| EDAAnOWL Core Ontology | Conformidad completa | ✅ CORRECTO |
| EDAAnOWL Earth Observation Instances | Conformidad completa | ✅ CORRECTO |
| EDAAnOWL Consistency Suite | Conformidad completa | ✅ CORRECTO |
| EDAAnOWL Credentialed Asset Example | Conformidad completa | ✅ CORRECTO |

---

## Estadísticas

- **Fase 2 (Semántica):** Fallos en pruebas: 4

## Informes Detallados

>[!TIP]
> **GitHub Actions**: Informes detallados disponibles en los artefactos generados por el contenedor. Ver: **https://github.com/datosgobes/DCAT-AP-ES/actions/workflows/validate-shacl.yml**

**Fase 2 - Resultados de Validación SHACL (formato Turtle):**
- `edaanowl_core-report.ttl` - EDAAnOWL Core Ontology
- `edaanowl_eo-report.ttl` - EDAAnOWL Earth Observation Instances
- `edaanowl_consistency-report.ttl` - EDAAnOWL Consistency Suite
- `edaanowl_cred-report.ttl` - EDAAnOWL Credentialed Asset Example
