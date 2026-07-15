# Archivo climático de OS-MIN-001

El caso utiliza `ESP_MD_Madrid-Barajas-Suarez.AP.082210_TMYx.2009-2023.epw`, correspondiente a Madrid-Barajas-Suárez, estación WMO 082210.

El archivo procede de [Climate.OneBuilding.Org](https://climate.onebuilding.org/WMO_Region_6_Europe/ESP_Spain/) y representa un año meteorológico típico TMYx construido a partir del periodo 2009–2023. El encabezado EPW declara latitud 40,467°, longitud −3,556°, zona horaria UTC+1 y elevación 609,6 m.

Para descargarlo y verificarlo:

```powershell
./download_weather.ps1
```

Los archivos `.zip` y `.epw` están excluidos de Git. El script fija la URL y comprueba los hashes SHA-256 del paquete y del EPW antes de permitir su uso.

| Artefacto | SHA-256 |
|---|---|
| ZIP de distribución | `565aec437eefc483fb8d3c5aacb60d1128be79c5b8847e18bb69a4b9c4ec1385` |
| EPW | `2137be4961ebe634fe6f09f392ec3a320dfefcff34b4152c155334574bf8ba16` |

Este TMYx es adecuado para el caso de interoperabilidad, pero no sustituye la selección climática exigible para una justificación reglamentaria concreta.
