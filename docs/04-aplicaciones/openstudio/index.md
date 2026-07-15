# OpenStudio y EnergyPlus

| Campo | Valor |
|---|---|
| Software | OpenStudio SDK |
| Versión base | 3.11.0 |
| Motor de simulación | EnergyPlus 25.2.0 |
| Fecha de revisión | 2026-07-15 |
| Estado | Confirmado para el alcance; flujo BIM pendiente de validación |
| Formato de intercambio BIM | Por determinar mediante ensayo |

## Función en la guía

[OpenStudio](https://openstudio.net/) es una plataforma abierta y multiplataforma para el modelado energético integral de edificios. Proporciona un SDK, una interfaz de línea de comandos y flujos automatizables sobre el motor de cálculo EnergyPlus.

La guía adopta como pareja de referencia **OpenStudio 3.11.0 y EnergyPlus 25.2.0**. Esta combinación está documentada por los proyectos oficiales y evita mezclar versiones cuya compatibilidad no se haya verificado.

!!! warning "EnergyPlus 26.1.0"
    EnergyPlus 26.1.0 es una versión estable posterior, pero no se incorpora todavía a la pareja de referencia. Se añadirá cuando exista una versión de OpenStudio adoptada por la guía que declare su compatibilidad y el flujo haya sido ensayado.

## Alcance inicial

El módulo documentará:

- la relación entre el modelo OpenStudio (`.osm`) y el modelo EnergyPlus;
- el intercambio de geometría y datos desde Revit;
- zonas térmicas, construcciones, cargas, horarios y sistemas;
- archivos climáticos y condiciones de simulación;
- ejecución, advertencias, errores y resultados;
- medidas de OpenStudio y automatización reproducible;
- controles QA/QC y comparación con los demás flujos de la guía.

La secuencia de componentes, archivos y transformaciones se desarrolla en [Arquitectura del flujo](arquitectura.md).

La ruta propuesta para obtener el primer modelo a partir de Revit se describe en [Intercambio desde Revit](intercambio-revit.md).

La geometría y los resultados esperados del ensayo común se definen en [Caso mínimo de referencia](caso-minimo.md).

## Fuera del alcance actual

- adoptar automáticamente la versión más reciente de EnergyPlus;
- considerar válido un flujo Revit–OpenStudio sin un ensayo reproducible;
- documentar DesignBuilder como aplicación objetivo;
- certificar resultados reglamentarios sin comprobar el procedimiento aplicable.

## Fuentes iniciales

- [Sitio oficial de OpenStudio](https://openstudio.net/).
- [Repositorio oficial de OpenStudio](https://github.com/NatLabRockies/OpenStudio).
- [Repositorio oficial de EnergyPlus](https://github.com/NatLabRockies/EnergyPlus).

## Limitaciones conocidas

El método de intercambio desde Revit, la conservación de espacios y superficies, y la transferencia de propiedades térmicas permanecen **pendientes de validación**. Se resolverán mediante un modelo mínimo común y pruebas versionadas.
