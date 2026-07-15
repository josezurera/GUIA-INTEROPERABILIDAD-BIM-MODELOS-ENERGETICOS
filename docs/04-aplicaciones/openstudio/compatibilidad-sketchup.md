# Compatibilidad de SketchUp y OpenStudio

Esta página registra el inventario del equipo de ensayo. Distingue la instalación comprobada de la compatibilidad funcional, que requiere completar un ensayo con un modelo OSM.

## Componentes confirmados

| Componente | Versión | Evidencia |
|---|---|---|
| SketchUp | 2025 / 25.0.575 | Propiedades de `SketchUp.exe` |
| OpenStudio Application | 1.11.1+b19f3a988b | Propiedades de `OpenStudioApp.exe` |
| OpenStudio CLI | 3.11.0+241b8abb4d | `openstudio --version` |
| OpenStudio Ruby API | Incluida con Application 1.11.1 | Registro de instalación y carpeta `Ruby/` |
| OpenStudio SketchUp Plug-in | 1.11.0 | `openstudio.rb`, constante `SKETCHUPPLUGIN_VERSION` y carpeta `openstudio/` |
| EnergyPlus | 25.2.0-cf7368216c | Distribución incluida en OpenStudio |

También constan componentes **OpenStudio CLI For Revit** para Revit 2024–2027. No deben confundirse con el complemento de SketchUp: son integraciones distintas y tienen ciclos de versión propios.

## Estado del complemento de SketchUp

El complemento oficial OpenStudio SketchUp Plug-in 1.11.0 está instalado para SketchUp 2025 en el perfil `josez`. Se localizan tanto el cargador `openstudio.rb` como su carpeta de recursos `openstudio/`.

La instalación se realizó mediante el paquete RBZ oficial, separado de OpenStudio Application. La aplicación de escritorio instalada no añade automáticamente la extensión a todos los perfiles de Windows.

!!! note "Alcance de la confirmación"
    La presencia y versión del complemento están confirmadas. Todavía falta abrir un OSM de prueba, guardarlo y validarlo para declarar compatible el flujo completo SketchUp 2025–OpenStudio.

## Incidencia de arranque resuelta

SketchUp se cerraba durante la apertura de la ventana de bienvenida en el perfil `josez`, aunque funcionaba desde otra cuenta del mismo equipo. Esto permitió descartar la instalación general, la GPU y el controlador como causa inmediata y acotar el fallo al perfil de usuario.

Con SketchUp cerrado, se conservó una copia de `login_session.dat` y se dejó que la aplicación generase una sesión nueva. SketchUp volvió a iniciar correctamente. Este procedimiento no elimina modelos, extensiones ni preferencias; si no resolviese el problema, el siguiente nivel de diagnóstico sería aislar el perfil completo de SketchUp de forma reversible.

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
| SketchUp → OSM | Preparado | Complemento 1.11.0 instalado; falta el ensayo con un OSM |
| Revit → gbXML → OpenStudio | Pendiente | Aún no existe el modelo RVT ni el gbXML del caso |

## Criterios para confirmar compatibilidad

1. Confirmar visualmente que el menú y las barras de OpenStudio cargan sin errores en SketchUp 2025.
2. Abrir o importar una copia de `OS-MIN-001` sin modificar el modelo de referencia.
3. Guardar un OSM nuevo y ejecutar `verify_model.rb` sobre una copia preparada para la prueba.
4. Registrar pérdidas, cambios de nombres y diferencias geométricas.

Hasta completar esos pasos no se declarará compatible la combinación SketchUp 2025–OpenStudio Application 1.11.1.
