# Historial de cambios

Este proyecto sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y versionado semántico adaptado a documentación.

## [Sin publicar]

### BEM-57 — Configuración energética mínima

- Se hacen explícitas las construcciones, cargas internas, horarios, infiltración, ventilación y consignas de `OS-MIN-001`.
- Se mantiene el sistema de cargas ideales para aislar el comportamiento de la envolvente.
- Se documentan los valores y unidades en la guía y en el registro YAML.
- Se fija el EPW TMYx 2009–2023 de Madrid-Barajas-Suárez con descarga y verificación SHA-256 reproducibles.

### BEM-58 — Resultados EnergyPlus

- Se documenta la primera simulación anual de `OS-MIN-001`, sus resultados principales y los artefactos generados.
- Se inventarían y clasifican las 11 advertencias de EnergyPlus.

### BEM-59 — Línea base QA/QC

- Se automatiza la validación conjunta de geometría, nombres, adyacencia, diagnóstico y resultados.
- Se incorpora una matriz de comparación que identifica como pendientes los artefactos Revit/gbXML y SketchUp.

### Añadido

- Estructura inicial del manual.
- Separación entre reglas comunes y módulos por aplicación.
- Registro de fuentes, compatibilidad y requisitos.
- Configuración de MkDocs Material y GitHub Pages.
- Módulo de OpenStudio 3.11.0 y EnergyPlus 25.2.0 como flujo abierto de simulación.
- Arquitectura del flujo OpenStudio–EnergyPlus, incluidos artefactos, medidas y puntos de control.
- Ruta inicial Revit–OpenStudio mediante gbXML 7.03 y separación respecto a Systems Analysis.
- Especificación cuantificada del caso mínimo de referencia para OpenStudio.
- Modelo OSM reproducible, verificación geométrica y ejecución de control con EnergyPlus.

### Cambiado

- OpenStudio sustituye a DesignBuilder en el alcance y la navegación de la guía.

## [0.1.0] - 2026-07-11

### Añadido

- Inicio formal del repositorio documental.

