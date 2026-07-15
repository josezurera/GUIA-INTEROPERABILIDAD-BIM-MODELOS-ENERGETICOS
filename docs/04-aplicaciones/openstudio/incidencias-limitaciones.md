# Incidencias y limitaciones de OpenStudio

El registro distingue entre errores bloqueantes ya corregidos, advertencias pendientes y limitaciones deliberadas del caso. La fuente estructurada es `data/incidencias-openstudio.yml`; esta página ofrece su lectura técnica.

## Resumen

| ID | Incidencia | Severidad | Estado |
|---|---|---|---|
| `OS-INC-001` | EPW no disponible durante la ejecución | Bloqueante | Validada |
| `OS-INC-002` | Carga People sin nivel de actividad | Bloqueante | Validada |
| `OS-INC-003` | Modelo opaco sin masa térmica | Advertencia | Abierta |
| `OS-INC-004` | Temperaturas del terreno no definidas | Advertencia | Abierta |
| `OS-INC-005` | Medidores no aplicables | Advertencia | Abierta |
| `OS-INC-006` | Variables mensuales no disponibles | Advertencia | Abierta |
| `OS-INC-007` | Escalados económicos sin tarifa | Advertencia | Abierta |

## Correcciones verificadas

### EPW ausente

La ejecución anual fallaba si `workflow.osw` no podía resolver el archivo climático. La corrección fija la ruta relativa, proporciona `weather/download_weather.ps1` y valida hashes SHA-256 antes de ejecutar. Se considera validada porque el periodo anual termina con 0 errores severos.

### Nivel de actividad de ocupantes

EnergyPlus exige un horario de potencia metabólica para cada objeto `People`. La primera configuración de cargas omitía `activity_level_schedule_name` y produjo un error fatal. `create_model.rb` asigna ahora `SCH-ACTIVITY-120-W-PERSON` a ambos espacios; la traducción y la ejecución posteriores son correctas.

## Advertencias abiertas

Las 11 advertencias de la ejecución anual se agrupan en cinco incidencias. No bloquean el ensayo de interoperabilidad, pero las dos primeras afectan a la interpretación física:

1. **Masa térmica:** el cerramiento opaco se representa mediante resistencia sin capacidad térmica.
2. **Terreno:** no se han fijado temperaturas mensuales verificadas.
3. **Medidores:** la plantilla general solicita salidas energéticas que el sistema ideal no utiliza.
4. **Informes mensuales:** algunas variables solicitadas no existen en el modelo.
5. **Economía:** las escaladas estadounidenses predeterminadas carecen de tarifas asociadas y no son aplicables al caso español.

## Reglas de mantenimiento

Cada nueva incidencia debe registrar:

- identificador estable `OS-INC-NNN`;
- versiones exactas afectadas;
- severidad y origen;
- síntoma observable y evidencia;
- acción aplicada o propuesta;
- estado `abierta`, `validada` o `descartada`;
- tarjeta Jira responsable.

Una incidencia solo pasa a `validada` después de repetir el caso y conservar evidencia del resultado. Las rutas dentro de `run/` son regenerables y no sustituyen el registro YAML versionado.

## Limitaciones de alcance

- El sistema de cargas ideales calcula necesidades, no el consumo de un sistema HVAC real.
- Los resultados no constituyen una certificación energética.
- El modelo Revit, el gbXML y la prueba mediante SketchUp todavía no existen.
- La conformidad geométrica entre aplicaciones permanece pendiente en BEM-59.
- Las advertencias abiertas deben resolverse antes de usar el caso como referencia física calibrada.
