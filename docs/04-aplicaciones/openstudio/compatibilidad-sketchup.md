# Compatibilidad de SketchUp y OpenStudio

Esta página registra el inventario del equipo de ensayo. No constituye todavía una matriz oficial de compatibilidad: distingue lo comprobado mediante ejecutables de lo que requiere abrir SketchUp y revisar su Administrador de extensiones.

## Componentes confirmados

| Componente | Versión | Evidencia |
|---|---|---|
| SketchUp | 2025 / 25.0.575 | Propiedades de `SketchUp.exe` |
| OpenStudio Application | 1.11.1+b19f3a988b | Propiedades de `OpenStudioApp.exe` |
| OpenStudio CLI | 3.11.0+241b8abb4d | `openstudio --version` |
| OpenStudio Ruby API | Incluida con Application 1.11.1 | Registro de instalación y carpeta `Ruby/` |
| EnergyPlus | 25.2.0-cf7368216c | Distribución incluida en OpenStudio |

También constan componentes **OpenStudio CLI For Revit** para Revit 2024–2027. No deben confundirse con el complemento de SketchUp: son integraciones distintas y tienen ciclos de versión propios.

## Estado del complemento de SketchUp

La inspección de las carpetas de extensiones de SketchUp 2024, 2025 y 2026 no localiza archivos o carpetas cuyo nombre contenga `OpenStudio`. Por tanto, el complemento se registra como **no confirmado**, aunque el usuario recuerde haberlo instalado.

!!! warning "Comprobación manual necesaria"
    Abrir SketchUp 2025 y consultar **Ventana → Administrador de extensiones**. Registrar nombre exacto, versión, estado habilitado/deshabilitado y firma. Una captura permitirá cerrar BEM-61 sin inferencias.

La presencia de `Ruby/openstudio.rb` dentro de OpenStudio Application confirma la API Ruby para scripts y medidas, pero no demuestra que exista una extensión activa dentro de SketchUp.

## Inventario reproducible

Desde la raíz del repositorio:

```powershell
./scripts/inventario-openstudio-sketchup.ps1
```

El resultado debe contrastarse con `data/inventario-openstudio-sketchup.yml`. Las rutas son evidencia de este equipo y pueden cambiar en otra estación de trabajo.

## Matriz provisional

| Flujo | Estado | Observación |
|---|---|---|
| Ruby API → OSM | Verificado | Genera y valida `OS-MIN-001` |
| OpenStudio Application → OSM | Disponible | Aplicación instalada; edición gráfica pendiente de ensayo documentado |
| OSM → EnergyPlus | Verificado | Simulación anual completada |
| SketchUp → OSM | Pendiente | Complemento no confirmado en el Administrador de extensiones |
| Revit → gbXML → OpenStudio | Pendiente | Aún no existe el modelo RVT ni el gbXML del caso |

## Criterios para confirmar compatibilidad

1. Identificar el complemento y su versión exacta.
2. Confirmar que carga sin errores en SketchUp 2025.
3. Abrir o importar una copia de `OS-MIN-001` sin modificar el modelo de referencia.
4. Guardar un OSM nuevo y ejecutar `verify_model.rb` sobre una copia preparada para la prueba.
5. Registrar pérdidas, cambios de nombres y diferencias geométricas.

Hasta completar esos pasos no se declarará compatible la combinación SketchUp 2025–OpenStudio Application 1.11.1.
