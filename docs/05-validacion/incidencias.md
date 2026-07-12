---
title: Registro de incidencias
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
---

# Registro de incidencias

El registro de incidencias permite aprender de los fallos, evitar reparaciones repetidas y determinar en qué aplicación debe corregirse cada problema.

## 1. Identificador

Formato propuesto:

```text
INC-<ETAPA>-<AAAA>-<NNNN>
```

Etapas:

- `RVT`: modelo Revit.
- `IFC`: archivo IFC.
- `ANA`: modelo analítico.
- `CAL`: modelo de cálculo.
- `SYNC`: actualización o sincronización.

Ejemplo: `INC-IFC-2026-0017`.

## 2. Campos obligatorios

| Campo | Descripción |
|---|---|
| Identificador | Código único |
| Título | Síntoma breve y específico |
| Fecha de alta | Fecha de detección |
| Proyecto | Proyecto o modelo de referencia |
| Severidad | S1, S2, S3 o S4 |
| Estado | Abierta, en análisis, corregida, validada, aceptada o descartada |
| Etapa de origen | Revit, IFC, analítico, cálculo o sincronización |
| Etapa de detección | Primera etapa donde se observó |
| Aplicación | Programa y módulo |
| Versión | Versión exacta |
| Archivo | Nombre y hash cuando corresponda |
| Elementos | Id Revit, GlobalId IFC y código EEM |
| Localización | Planta, zona, espacio o coordenadas |
| Síntoma | Comportamiento observado |
| Resultado esperado | Comportamiento correcto |
| Impacto | Magnitudes o procesos afectados |
| Reproducción | Pasos mínimos para repetirlo |
| Evidencia | Capturas, tablas, logs o archivos |
| Causa | Confirmada o hipótesis |
| Acción | Corrección o solución temporal |
| Responsable | Persona o rol asignado |
| Validación | Prueba realizada después de corregir |
| Revisión de cierre | Versión donde se comprobó |

## 3. Estados

| Estado | Uso |
|---|---|
| `ABIERTA` | Registrada, pendiente de análisis |
| `EN_ANALISIS` | Causa en investigación |
| `CORREGIDA` | Se ha aplicado una modificación |
| `VALIDADA` | La corrección supera la prueba |
| `ACEPTADA` | Limitación conocida aceptada |
| `DESCARTADA` | No reproducible o no constituye defecto |
| `REABIERTA` | El problema vuelve a aparecer |

Solo `VALIDADA`, `ACEPTADA` y `DESCARTADA` permiten cerrar una incidencia.

## 4. Causa frente a síntoma

Ejemplo:

- Síntoma: una superficie aparece como exterior.
- Causa posible: falta el espacio adyacente.
- Causa alternativa: el límite espacial no se exportó.
- Causa alternativa: el receptor no reconstruyó la adyacencia.

No se cerrará la incidencia describiendo únicamente el síntoma.

## 5. Evidencias mínimas

Según la etapa:

### Revit

- Vista con elemento seleccionado.
- Id o UniqueId.
- Propiedades relevantes.
- Planta o sección.

### IFC

- GlobalId.
- Entidad y Psets.
- Captura en visor.
- Fragmento de informe o validador.

### Modelo analítico

- Espacio o superficie.
- Área, tipo y adyacencias.
- Captura antes y después.

### Cálculo

- Entrada afectada.
- Resultado antes y después.
- Condiciones del ensayo.

## 6. Soluciones temporales

Una solución manual en el receptor se marcará como temporal cuando deba repetirse tras actualizar. Debe incluir:

- Instrucción exacta.
- Elementos afectados.
- Tiempo estimado.
- Riesgo de omisión.
- Responsable.
- Prueba de repetición.

## 7. Validación del cierre

Cerrar requiere:

1. Reproducir el fallo con la versión anterior.
2. Aplicar la corrección.
3. Repetir el mismo ensayo.
4. Confirmar que no aparecen efectos secundarios.
5. Registrar versión y evidencia.
6. Incorporar el caso al modelo de regresión si es generalizable.

## 8. Plantilla reutilizable

```text
ID:
Título:
Severidad:
Estado:
Proyecto:
Fecha:

Origen:
Detección:
Aplicación y versión:
Archivo y hash:
Elementos:
Localización:

Síntoma:
Resultado esperado:
Impacto:
Pasos para reproducir:

Causa:
Acción aplicada:
Solución temporal:
Responsable:

Prueba de validación:
Resultado:
Revisión de cierre:
Evidencias:
```

## 9. Indicadores del registro

Se revisarán periódicamente:

- Incidencias por etapa.
- Incidencias por receptor.
- Incidencias reabiertas.
- Tiempo medio de cierre.
- Reparaciones manuales recurrentes.
- Errores asociados a una versión.
- Tipos geométricos más problemáticos.

Estos indicadores orientarán nuevas normas de modelado y pruebas de regresión.

