# Resultados de la simulación de referencia

Esta página registra la primera ejecución anual reproducible de `OS-MIN-001`. Los resultados pertenecen a un caso sintético de interoperabilidad y no deben interpretarse como una certificación energética ni como prestaciones de un edificio real.

## Configuración ejecutada

| Campo | Valor |
|---|---|
| OpenStudio | 3.11.0+241b8abb4d |
| EnergyPlus | 25.2.0-cf7368216c |
| Modelo | `OS-MIN-001/model.osm` |
| Flujo | `OS-MIN-001/workflow.osw` |
| Clima | Madrid-Barajas-Suárez AP, WMO 082210 |
| Archivo | TMYx 2009–2023 |
| Periodos | Días de diseño y año completo |
| Superficie acondicionada | 80,00 m² |
| Sistema | Cargas ideales de aire |

## Ejecución reproducible

Desde `examples/openstudio/OS-MIN-001`:

```powershell
./weather/download_weather.ps1
openstudio create_model.rb
openstudio verify_model.rb
openstudio run -w workflow.osw
python extract_results.py
```

El flujo genera `run/in.idf`, `run/eplusout.err`, `run/eplusout.sql` y `run/eplustbl.htm`. La carpeta `run/` contiene resultados derivados y no se almacena en Git.

## Resultado anual

| Uso final | Vector energético | Resultado | Intensidad |
|---|---|---:|---:|
| Calefacción | District Heating Water | 20,13 GJ | 69,90 kWh/m²·a |
| Refrigeración | District Cooling | 30,39 GJ | 105,52 kWh/m²·a |
| Iluminación interior | Electricidad | 8,41 GJ | 29,20 kWh/m²·a |
| Equipos interiores | Electricidad | 10,51 GJ | 36,49 kWh/m²·a |
| **Total** | Todos | **69,44 GJ** | **241,11 kWh/m²·a** |

Las denominaciones *District Heating Water* y *District Cooling* son la representación contable utilizada por el sistema ideal de EnergyPlus. No describen una instalación real ni sus rendimientos.

Las consignas se cumplieron durante las horas ocupadas: 0,00 h fuera de consigna en calefacción y 0,00 h en refrigeración. El indicador simplificado ASHRAE 55 informa 2.116,17 h no confortables, pero no es concluyente porque el modelo no define vestimenta, velocidad de aire ni un estudio de confort completo.

## Diagnóstico

EnergyPlus terminó correctamente en 1,20 s con **0 errores severos y 11 advertencias**.

| Grupo | Cantidad | Clasificación | Tratamiento |
|---|---:|---|---|
| Modelo sin masa térmica | 1 | Limitación conocida | Sustituir el material sin masa en un caso físico posterior |
| Temperatura del terreno no definida | 1 | Supuesto incompleto | Incorporar temperaturas mensuales verificadas |
| Medidores de gas inexistentes o duplicados | 3 | Salida no aplicable | Eliminar solicitudes de medidores no usados |
| Variables mensuales no disponibles | 1 | Informe parcial | Ajustar la plantilla de informes |
| Escalados económicos de EE. UU. sin coste asociado | 5 | Informe no aplicable | Excluir análisis económico predeterminado |

Ninguna advertencia impide comprobar el flujo geométrico y energético. Antes de emplear el caso para evaluación física deben resolverse la masa térmica y la temperatura del terreno.

## Criterios de cierre

- [x] Ejecución mediante OSW versionado.
- [x] Archivo climático identificado y verificado.
- [x] Traducción OSM–IDF completada.
- [x] Cero errores severos.
- [x] Advertencias inventariadas y clasificadas.
- [x] Resultados principales extraídos de `eplusout.sql`.
- [x] Pasos y artefactos de salida documentados.
