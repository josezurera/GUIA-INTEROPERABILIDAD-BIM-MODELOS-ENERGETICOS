---
title: Ensayo Revit 2026–IFC–MVD
status: experimental
fecha_ensayo: 2026-07-13
---

# Ensayo Revit 2026–IFC–MVD

## 1. Alcance y estado

Este ensayo comprueba de forma reproducible qué conserva el exportador IFC instalado con Revit 2026 al variar el esquema, la vista de definición y el nivel de límites espaciales.

El ensayo **cierra la matriz técnica del exportador para el modelo mínimo**, pero todavía no aprueba definitivamente los perfiles por aplicación receptora. Esa aprobación exige importar los archivos en Open BIM Analytical Model, TK-IFC/TeKton3D y la ruta elegida para OpenStudio.

## 2. Entorno probado

| Componente | Versión registrada |
|---|---|
| Revit | Autodesk Revit 2026.2 |
| Compilación | `26.2.0.20` |
| Subversión | `2026.2` |
| Exportador integrado | `Revit.IFC.Export.dll` `26.2.0.20` |
| Fecha | 13 de julio de 2026 |
| Validador | Herramienta IDS y QA/QC del repositorio |

La instalación comprobada también dispone de TeKton3D `1.8.50.8`, TK-IFC `1.1.0.8` y TK-CEEP `1.2.5.0`. Estas versiones se registran para el siguiente ensayo de receptor; su presencia no equivale todavía a una importación aprobada.

## 3. Modelo mínimo

El generador crea un RVT nuevo a partir de la plantilla española de Revit 2026. No abre ni modifica proyectos del usuario.

El caso contiene:

- una planta rectangular de 12 × 8 m;
- dos habitaciones contiguas con cálculo de volúmenes activado;
- cuatro muros exteriores y una partición interior;
- un suelo y una cubierta plana modelada como forjado superior;
- una puerta interior y una ventana exterior;
- un pilar con `Room Bounding` desactivado;
- funciones interior/exterior asignadas a los tipos;
- nombre de proyecto, edificio y espacios;
- Psets IFC comunes, Psets internos de Revit y cantidades base activados.

El código de reproducción se conserva en `tools/revit-2026-test-generator` y los IFC resultantes permanecen fuera de Git por su tamaño y carácter temporal.

## 4. Matriz exportada

Se generaron correctamente siete archivos:

| Caso | Esquema/MVD | Límites |
|---|---|---:|
| `ifc2x3-cv2-sb0` | IFC2x3 Coordination View 2.0 | 0 |
| `ifc2x3-cv2-sb1` | IFC2x3 Coordination View 2.0 | 1 |
| `ifc2x3-cv2-sb2` | IFC2x3 Coordination View 2.0 | 2 |
| `ifc4-rv-sb0` | IFC4 Reference View | 0 |
| `ifc4-rv-sb1` | IFC4 Reference View | 1 |
| `ifc4-rv-sb2` | IFC4 Reference View | 2 |
| `ifc4-dtv-sb2` | IFC4 Design Transfer View | 2 |

## 5. Resultados QA/QC

| Perfil | Incidencias de esquema | `IfcSpace` | `IfcRelSpaceBoundary` | Relaciones de material | Área de espacios | Volumen de espacios |
|---|---:|---:|---:|---:|---:|---:|
| IFC2x3 CV2 SB0 | 0 | 2 | 0 | 12 | 2/2 | 0/2 |
| IFC2x3 CV2 SB1 | 4 | 2 | 13 | 12 | 2/2 | 0/2 |
| IFC2x3 CV2 SB2 | 12 | 2 | 13 | 12 | 2/2 | 0/2 |
| IFC4 RV SB0 | 0 | 2 | 0 | 6 | 2/2 | 2/2 |
| IFC4 RV SB1 | 4 | 2 | 13 | 6 | 2/2 | 2/2 |
| IFC4 RV SB2 | 12 | 2 | 13 | 6 | 2/2 | 2/2 |
| IFC4 DTV SB2 | 12 | 2 | 15 | 14 | 2/2 | 2/2 |

En todos los perfiles:

- los dos espacios tienen geometría cerrada procesable;
- no se detectan intersecciones volumétricas entre espacios;
- el pilar no aparece como elemento delimitador cuando existen relaciones espaciales;
- los GlobalIds son válidos, únicos y completos;
- se exportan referencias de espacios y clasificaciones interior/exterior;
- los requisitos IDS de transmitancia de los muros exteriores no se cumplen todavía.

## 6. Incidencia de límites espaciales

Los archivos SB1 y SB2 contienen relaciones espaciales, pero el validador detecta instancias de `IfcCurveBoundedPlane` sin el atributo obligatorio `InnerBoundaries`. El número de incidencias fue:

- cuatro en SB1;
- doce en SB2;
- doce en IFC4 DTV SB2.

En este modelo, SB2 no añade relaciones respecto a SB1 en IFC2x3 CV2 ni IFC4 RV, pero triplica las incidencias de esquema. Por ello **SB2 no se adopta como valor general para Revit 2026.2 / exportador 26.2.0.20**.

La incidencia debe repetirse con un exportador 2026 más reciente. Autodesk publicó versiones posteriores del complemento IFC para Revit 2026, por lo que no debe extrapolarse este defecto sin volver a ejecutar la regresión.

## 7. Hallazgo sobre Psets y cantidades

En Revit 2026.2 no basta con añadir cadenas como `ExportIFCCommonPropertySets=true` a `IFCExportOptions`. La interfaz del exportador actualiza también su plantilla de parámetros en sesión. El ensayo solo obtuvo los Psets comunes y las cantidades esperadas después de reproducir esa configuración.

Consecuencias para el procedimiento manual:

1. utilizar una configuración guardada mediante la interfaz IFC de Revit;
2. activar **IFC common property sets** y **base quantities**;
3. no suponer que una automatización antigua reproduce todos los ajustes de la interfaz;
4. validar el IFC resultante, no únicamente la pantalla de configuración.

Con esta corrección:

- IFC4 exportó área y volumen de ambos espacios;
- IFC2x3 exportó el área, pero no una cantidad de volumen reconocida;
- la semántica interior/exterior pasó a los Psets comunes;
- quedó pendiente proporcionar o mapear la transmitancia térmica.

## 8. Decisión provisional por perfil

| Perfil del manual | Candidato para ensayo receptor | Estado |
|---|---|---|
| `EEM_CYPE_ANALYTICAL` | IFC4 RV SB1 | Candidato; falta importar en Open BIM Analytical Model |
| `EEM_TEKTON_IMPORT` | IFC2x3 CV2 SB0 y SB1 | Comparación necesaria en TK-IFC |
| `EEM_TEKTON_LINK` | IFC4 RV SB0; SB1 si consume relaciones | Comparación y actualización pendientes |
| `EEM_OPENSTUDIO` | IFC4 RV SB1 como fuente del conversor | No es una importación IFC directa aprobada |

IFC4 RV SB0 es el archivo mínimo conforme al esquema y conserva los volúmenes, pero no permite verificar relaciones de límite ni la regla de pilares no delimitadores. IFC4 RV SB1 añade las relaciones necesarias para QA espacial, aunque presenta cuatro incidencias de esquema. Ninguno debe declararse definitivo sin conocer la tolerancia y el resultado del receptor.

## 9. Criterios para aprobar un receptor

Cada aplicación deberá superar, como mínimo:

1. apertura o importación sin cierre ni pérdida silenciosa;
2. dos espacios reconocidos y con nombres estables;
3. áreas y volúmenes coherentes con el RVT;
4. partición interior y envolvente correctamente diferenciadas;
5. puerta y ventana asociadas a sus cerramientos;
6. ausencia de un contorno adicional debido al pilar;
7. materiales o construcciones trazables;
8. persistencia aceptable al actualizar el IFC;
9. registro de reparaciones manuales necesarias;
10. aprobación explícita de esquema, MVD y nivel de límites.

## 10. Siguiente ensayo

El siguiente frente prioritario es ejecutar los candidatos en este orden:

1. TK-IFC y TeKton3D, disponibles en el equipo;
2. Open BIM Analytical Model y transferencia a CYPETHERM HE Plus;
3. conversión del modelo analítico intermedio a OpenStudio;
4. repetición con una versión posterior del exportador IFC 2026 para comprobar `InnerBoundaries`.

## 11. Fuentes técnicas

- Autodesk, [repositorio oficial Revit IFC](https://github.com/Autodesk/revit-ifc).
- Autodesk, [versiones publicadas del exportador IFC](https://github.com/Autodesk/revit-ifc/releases).
- Autodesk, [`IFCExportConfiguration` de la rama Revit 2026](https://github.com/Autodesk/revit-ifc/blob/Release_26.x.x/Source/IFCExporterUIOverride/IFCExportConfiguration.cs).
