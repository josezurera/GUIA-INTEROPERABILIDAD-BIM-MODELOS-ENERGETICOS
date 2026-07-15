# OS-MIN-001

Caso mínimo de dos espacios adyacentes definido en la guía.

## Regeneración

Con OpenStudio CLI 3.11.0:

```powershell
openstudio create_model.rb
openstudio verify_model.rb
openstudio run -w workflow.osw
python extract_results.py
python validate_case.py --openstudio "C:/openstudioapplication-1.11.1/bin/openstudio.exe"
```

`create_model.rb` es la fuente reproducible del modelo y `verify_model.rb` comprueba sus magnitudes principales. `model.osm` se conserva como resultado de referencia. El directorio `run/` generado por el flujo se excluye del control de versiones porque contiene resultados derivados, entre ellos `in.idf`, `eplusout.err` y `eplusout.sql`.

## Estado

- Geometría y zonas: generadas y comprobadas mediante la API de OpenStudio 3.11.0.
- Traducción OSM–IDF: ejecutada con OpenStudio 3.11.0.
- Configuración: envolvente, cargas, horarios, infiltración, ventilación, termostatos y cargas ideales explícitos.
- Ejecución: días de diseño y periodo anual con EnergyPlus 25.2.0, 0 errores severos y 11 advertencias.
- Clima anual: TMYx 2009–2023 de Madrid-Barajas-Suárez, descargado y verificado mediante SHA-256.

Los días de diseño incorporados sirven únicamente para comprobar la integridad del flujo. Sus condiciones son valores de referencia y no sustituyen datos climáticos reglamentarios o estadísticos verificados.
