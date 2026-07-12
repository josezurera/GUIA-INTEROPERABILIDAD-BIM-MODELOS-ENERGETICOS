---
title: Parámetros y mapeado IFC para análisis energético
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
software:
  nombre: Autodesk Revit
  version_base: "2026"
---

# Parámetros y mapeado IFC para análisis energético

La geometría permite reconstruir espacios y superficies, pero no explica por sí sola su función energética. Este capítulo define una estructura mínima de información para identificar elementos, clasificar fronteras, relacionar tipos constructivos y verificar qué datos llegan realmente a IFC y a las aplicaciones receptoras.

!!! warning "Exportado no significa utilizado"
    Un parámetro puede existir en el IFC y ser visible en un visor, pero Open BIM Analytical Model, CYPETHERM HE Plus o TeKton3D pueden ignorarlo. Deben comprobarse por separado la presencia del dato, su lectura y su aplicación efectiva al cálculo.

## 1. Objetivos

El sistema de parámetros debe permitir:

- Identificar elementos y tipos de forma estable.
- Distinguir la función energética de la categoría arquitectónica.
- Mantener trazabilidad entre Revit, IFC y cálculo.
- Filtrar y revisar el modelo antes de exportar.
- Comparar revisiones sin depender de nombres variables.
- Reducir la reasignación manual en los receptores.
- Documentar qué información no se transfiere.

## 2. Capas de información

Se distinguirán cinco capas:

| Capa | Contenido | Ejemplo |
|---|---|---|
| Identidad Revit | Id, familia, tipo, marca | Tipo de muro `ENV-MUR-EXT-01` |
| Semántica energética | Función y condición de contorno | `EXT_AIR`, `GROUND` |
| Semántica IFC | Entidad, tipo predefinido y Psets | `IfcWall`, `Pset_WallCommon` |
| Construcción | Código y prestaciones documentales | `CONS_MUR_01`, U = 0,25 |
| Asignación de cálculo | Solución efectiva del motor | Cerramiento seleccionado en CYPETHERM |

No se considerarán equivalentes hasta demostrar el mapeado entre capas.

## 3. Principios de diseño de parámetros

### 3.1 Estabilidad

El nombre, GUID, tipo de dato y alcance de un parámetro compartido no deben cambiar durante el proyecto. Si cambia su significado se crea una nueva versión, no se reutiliza el parámetro anterior.

### 3.2 Una propiedad, un significado

No se utilizará un mismo campo para almacenar alternativamente códigos, comentarios y valores numéricos.

### 3.3 Tipado correcto

- Booleano para sí/no.
- Longitud, área o volumen para magnitudes geométricas.
- Número para factores adimensionales.
- Coeficiente de transferencia térmica para U cuando esté disponible.
- Texto para códigos y enumeraciones controladas.

Los valores numéricos no se guardarán como texto salvo limitación comprobada del flujo.

### 3.4 Unidades explícitas

La definición indicará unidad y magnitud. El intercambio se verificará en unidades SI aunque Revit muestre unidades de proyecto diferentes.

### 3.5 Valores nulos

Vacío significa **no informado**. No se utilizará `0`, `N/A`, guiones o textos equivalentes en campos numéricos. Un cero real debe conservar su significado físico.

### 3.6 Enumeraciones controladas

Los códigos se elegirán de listas versionadas. Se evitarán variantes ortográficas, acentos y espacios en campos destinados a reglas automáticas.

## 4. Parámetros de tipo y de ejemplar

### 4.1 Parámetros de tipo

Se usarán cuando el valor sea común a todas las instancias del tipo:

- Código de construcción.
- Prestación térmica documental.
- Tipo de vidrio.
- Fracción de marco de una familia homologada.
- Función prevista del tipo, si no cambia por instancia.

### 4.2 Parámetros de ejemplar

Se usarán cuando el valor dependa de ubicación, fase o relación espacial:

- Estado de revisión.
- Condición de contorno confirmada.
- Código de zona o espacio.
- Función como sombra.
- Excepción de exportación.
- Comentario de incidencia.

### 4.3 Regla de prevalencia

Si existe un valor general de tipo y una excepción de ejemplar, el manual debe definir cuál prevalece. No se duplicará el mismo dato en ambos niveles sin una regla explícita.

## 5. Parámetros compartidos

Autodesk permite crear parámetros compartidos, aplicarlos a categorías y almacenarlos como tipo o ejemplar. Estos parámetros pueden planificarse, etiquetarse y mapearse con mayor control.

El repositorio mantendrá:

- Archivo maestro de parámetros compartidos.
- Diccionario legible en Markdown o CSV.
- GUID de cada parámetro.
- Tipo de dato.
- Categorías aplicables.
- Nivel tipo/ejemplar.
- Descripción y valores permitidos.
- Versión de alta, modificación o retirada.

El archivo no se editará manualmente sin conservar GUID y formato.

## 6. Convención de nombres

Se propone el prefijo `EEM_` —**Energy Exchange Model**— para parámetros propios de la guía.

Reglas:

- Mayúsculas y guion bajo.
- Sin espacios ni tildes.
- Nombre breve pero inequívoco.
- Sufijo de unidad solo cuando el tipo de dato no la expresa.
- No utilizar nombres reservados de IFC sin intención de mapeado.

Ejemplos:

- `EEM_ELEMENT_CODE`
- `EEM_CONSTRUCTION_CODE`
- `EEM_BOUNDARY_TYPE`
- `EEM_THERMAL_ZONE_CODE`
- `EEM_EXPORT_STATUS`

## 7. Diccionario mínimo común

| Parámetro | Nivel | Tipo | Categorías principales | Finalidad |
|---|---|---|---|---|
| `EEM_ELEMENT_CODE` | Ejemplar | Texto | Todas las relevantes | Código humano estable |
| `EEM_CONSTRUCTION_CODE` | Tipo | Texto | Muros, suelos, cubiertas, techos, puertas, ventanas, paneles | Relación con solución constructiva |
| `EEM_BOUNDARY_TYPE` | Ejemplar | Texto controlado | Cerramientos | Condición de contorno prevista |
| `EEM_ENERGY_ROLE` | Ejemplar | Texto controlado | Elementos y espacios | Función en el modelo energético |
| `EEM_THERMAL_ZONE_CODE` | Ejemplar | Texto | Habitaciones y espacios | Agrupación térmica prevista |
| `EEM_CONDITIONING` | Ejemplar | Texto controlado | Habitaciones y espacios | Acondicionado/no acondicionado |
| `EEM_EXPORT_STATUS` | Ejemplar | Texto controlado | Todas las relevantes | Incluir, excluir o revisar |
| `EEM_QA_STATUS` | Ejemplar | Texto controlado | Todas las relevantes | Estado de validación |
| `EEM_SOURCE_SYSTEM` | Ejemplar | Texto | Todas las relevantes | Autoridad del dato |
| `EEM_NOTES` | Ejemplar | Texto | Todas las relevantes | Excepción documentada |

Este diccionario es un núcleo editorial. Su archivo técnico se generará y probará antes de incorporarlo a la plantilla Revit.

## 8. Enumeraciones comunes

### 8.1 `EEM_BOUNDARY_TYPE`

- `EXT_AIR`: contacto con aire exterior.
- `GROUND`: contacto con terreno.
- `INT_ZONE`: separación entre zonas térmicas.
- `INT_UNCOND`: separación con espacio no acondicionado.
- `PARTY`: medianería o contacto con edificio colindante.
- `ADIABATIC`: condición adiabática justificada.
- `NOT_APPLICABLE`: no corresponde.
- `TO_REVIEW`: pendiente de confirmar.

### 8.2 `EEM_ENERGY_ROLE`

- `ENVELOPE`
- `OPENING`
- `SPACE`
- `SHADE_SELF`
- `SHADE_REMOTE`
- `CONTEXT_ONLY`
- `IGNORE`
- `TO_REVIEW`

### 8.3 `EEM_CONDITIONING`

- `CONDITIONED`
- `UNCONDITIONED`
- `SEMI_CONDITIONED`
- `EXTERIOR`
- `TO_REVIEW`

### 8.4 `EEM_EXPORT_STATUS`

- `INCLUDE`
- `EXCLUDE`
- `INCLUDE_TEST_ONLY`
- `TO_REVIEW`

### 8.5 `EEM_QA_STATUS`

- `NOT_REVIEWED`
- `IN_REVIEW`
- `ACCEPTED`
- `ACCEPTED_WITH_LIMITATION`
- `REJECTED`

## 9. Identidad y trazabilidad

Se conservarán varios identificadores porque cumplen funciones distintas:

| Identificador | Uso |
|---|---|
| Revit Element Id | Diagnóstico dentro de una versión del RVT |
| Revit UniqueId | Seguimiento más estable dentro del modelo |
| IFC GlobalId | Correspondencia entre entregas IFC cuando se conserva |
| `EEM_ELEMENT_CODE` | Lectura humana y registro de incidencias |
| Código de tipo | Relación con construcción o catálogo |

Autodesk permite almacenar el GUID IFC generado después de exportar. Esta opción se ensayará porque modifica el modelo y debe coordinarse con el procedimiento de publicación.

El GlobalId no debe regenerarse innecesariamente entre exportaciones si se pretende actualizar vínculos o comparar revisiones.

## 10. Datos de proyecto y edificio

El IFC debe identificar como mínimo:

- Nombre y código de proyecto.
- Estado o revisión.
- Autor u organización.
- Emplazamiento.
- Edificio.
- Fase de cálculo.
- Sistema de coordenadas.
- Fecha de exportación.
- Configuración IFC utilizada.
- Aplicación y versión de origen.

Los campos de cabecera y proyecto no sustituirán el registro externo de entrega, que conservará nombre de archivo, hash y responsable.

## 11. Espacios

### 11.1 Datos mínimos

| Dato | Fuente candidata |
|---|---|
| Código | Número de habitación/espacio o `EEM_ELEMENT_CODE` |
| Nombre | Nombre de habitación/espacio |
| Nivel | Nivel asociado |
| Zona térmica | `EEM_THERMAL_ZONE_CODE` |
| Acondicionamiento | `EEM_CONDITIONING` |
| Área y volumen | Cantidades geométricas verificadas |
| Ocupación/uso | Parámetro controlado del proyecto |
| Estado | `EEM_QA_STATUS` |

### 11.2 IFC

La entidad esperada es `IfcSpace`. buildingSMART indica que `Pset_SpaceCommon.IsExternal` es la propiedad preferida para distinguir espacios exteriores en IFC 4.3, frente a valores de tipo anteriores hoy desaconsejados.

Se comprobarán:

- Nombre y `LongName`, cuando proceda.
- Nivel o contenedor espacial.
- `Pset_SpaceCommon`.
- Cantidades base.
- Relaciones de límites espaciales, si se exportan.
- Código de zona térmica personalizado.

## 12. Zonas térmicas

Una zona puede agrupar varios espacios. No se confiará únicamente en el nombre de zona de Revit.

Se mantendrán:

- Código estable de zona.
- Nombre descriptivo.
- Tipo de acondicionamiento.
- Sistema o estrategia, si está definido.
- Lista de espacios miembros.
- Estado de revisión.

La representación como `IfcZone`, `IfcSpatialZone`, grupo o propiedad depende del esquema y exportador. Debe verificarse en el IFC real y en cada receptor.

## 13. Cerramientos opacos

### 13.1 Datos mínimos

- Código de elemento.
- Código de construcción.
- Función energética.
- Condición de contorno prevista.
- Exterior/interior.
- Estado de fase.
- Prestación U documental, cuando esté disponible.
- Fuente de la prestación.

### 13.2 Propiedades IFC comunes

buildingSMART define `ThermalTransmittance` e `IsExternal` en conjuntos comunes como `Pset_WallCommon`. La transmitancia se refiere al conjunto del elemento en la dirección del flujo, incluyendo sus materiales.

La propiedad `IsExternal` no sustituye `EEM_BOUNDARY_TYPE`: un cerramiento puede no ser exterior y, sin embargo, separar un espacio acondicionado de uno no acondicionado.

### 13.3 Cantidades

Se exportarán y comprobarán, cuando proceda:

- Longitud, anchura y altura.
- Área bruta y neta.
- Volumen bruto y neto.

Las cantidades IFC no se utilizarán sin confirmar la cara de medición y el tratamiento de huecos.

## 14. Ventanas y puertas

### 14.1 Datos mínimos

- Código de tipo.
- Construcción.
- Condición exterior/interior.
- Ancho y alto.
- Área de hueco.
- Fracción de vidrio.
- U del conjunto.
- Factor solar.
- Transmitancia visible.
- Infiltración o clase, cuando proceda.

### 14.2 IFC común

buildingSMART incluye en `Pset_WindowCommon` propiedades como `IsExternal`, `Infiltration`, `ThermalTransmittance` y `GlazingAreaFraction`. Para puertas existe un conjunto análogo.

`GlazingAreaFraction` expresa la fracción acristalada respecto al área total del elemento de relleno cuando el área de los paneles no se proporciona por separado.

La existencia de estas propiedades en el estándar no garantiza que Revit las complete ni que los receptores las consuman.

### 14.3 Prestaciones solares

Los datos detallados de acristalamiento pueden pertenecer a conjuntos específicos. Se evitará mapear un factor solar reglamentario a una propiedad IFC de significado diferente sin revisar su definición y unidad.

## 15. Sombras

Los elementos de sombra mantendrán:

- `EEM_ENERGY_ROLE`.
- Código de tipo.
- Fijo o móvil.
- Escenario de operación.
- Opacidad o factor equivalente, si procede.
- Aplicación receptora validada.

No se les asignará `IsExternal` como único criterio porque esa propiedad no distingue sombra de cerramiento exterior.

## 16. Construcciones y materiales

### 16.1 Código frente a nombre

El código de construcción será estable y breve; el nombre podrá evolucionar para ser más descriptivo.

Ejemplo:

`CONS_MUR_EXT_01` — fachada cerámica con aislamiento continuo.

### 16.2 Fuente de verdad

Debe definirse dónde se mantiene la construcción aprobada:

- Catálogo del motor.
- Base de datos normativa.
- Ficha técnica validada.
- Revit, solo si se ha acordado como fuente.

Revit no será automáticamente la autoridad de prestaciones térmicas por contener materiales.

### 16.3 Capas IFC

La composición de capas puede exportarse mediante materiales y conjuntos de capas. Se comprobarán orden, espesores, materiales y orientación.

Si el receptor ignora las capas, el código de construcción servirá para reasignar una solución equivalente.

## 17. Conjuntos de propiedades IFC

### 17.1 Conjuntos comunes

Se activarán cuando sean compatibles con el esquema y la finalidad del intercambio. Tienen prioridad para propiedades ya normalizadas.

### 17.2 Conjunto propio de intercambio

Para información no cubierta o no controlable mediante Psets comunes se propone un conjunto personalizado denominado:

`EEM_EnergyExchange`

No se utilizará el prefijo `Pset_` para evitar aparentar que el conjunto propio forma parte del estándar buildingSMART.

Propiedades candidatas:

- `ElementCode`
- `ConstructionCode`
- `BoundaryType`
- `EnergyRole`
- `ThermalZoneCode`
- `Conditioning`
- `ExportStatus`
- `QAStatus`
- `SourceSystem`
- `Notes`

### 17.3 Evitar duplicidades

Si una propiedad normalizada se exporta correctamente en un conjunto común, no se repetirá en el conjunto propio salvo necesidad transitoria documentada.

## 18. Vías de exportación desde Revit

Autodesk documenta varias opciones:

- Conjuntos de propiedades comunes IFC.
- Conjuntos de propiedades específicos de Revit.
- Cantidades base.
- Tablas de planificación como conjuntos personalizados.
- Conjuntos de propiedades definidos por el usuario.
- Tabla de mapeado de parámetros.

Cada vía tiene un objetivo diferente. Activarlas todas puede duplicar información y aumentar el archivo.

## 19. Tablas como conjuntos de propiedades

Revit puede exportar tablas como Psets; el nombre de la tabla se convierte en nombre del conjunto y las columnas en propiedades IFC.

Esta vía es útil para prototipos y control visible porque:

- El equipo puede revisar los mismos campos antes de exportar.
- Se filtran categorías y elementos.
- Se comprueban valores vacíos.

Riesgos:

- Nombres de columnas inestables.
- Campos calculados no exportados como se espera.
- Duplicidad con Psets comunes.
- Dependencia del idioma de la plantilla.

Las tablas destinadas a IFC tendrán un prefijo y no se utilizarán como documentación gráfica ordinaria.

## 20. Conjuntos definidos por el usuario

Para Revit 2026.0–2026.2 se mantendrá el flujo basado en archivo de texto cuando sea necesario. Autodesk indica que desde Revit 2026.3 existe una gestión mejorada de conjuntos personalizados y mapeo, con capacidad para importar archivos anteriores.

El procedimiento registrará:

- Versión exacta de Revit.
- Versión del complemento/exportador IFC.
- Archivo de Psets utilizado.
- Fecha y hash del archivo.
- Resultado de prueba.

No se sobrescribirá un archivo aprobado sin incrementar su versión.

## 21. Mapeado de categorías y entidades

El mapeado de categoría determina la clase IFC y, cuando corresponda, el tipo predefinido.

Se comprobará al menos:

| Revit | Entidad IFC esperada |
|---|---|
| Habitaciones/espacios | `IfcSpace` |
| Muros | `IfcWall` |
| Suelos/forjados | `IfcSlab` |
| Cubiertas | `IfcRoof` y/o elementos asociados |
| Ventanas | `IfcWindow` |
| Puertas | `IfcDoor` |
| Muros cortina | `IfcCurtainWall` y componentes |

Las entidades exactas dependerán del esquema y de la descomposición elegida. No se forzará una clase distinta solo para conseguir que un receptor la muestre sin evaluar consecuencias.

## 22. Parámetros IFC de control

Revit admite mecanismos como `IfcExportAs` para influir en la clase exportada, dentro de las clases compatibles. Su uso será excepcional y trazado.

Antes de forzar una entidad:

1. Corregir la categoría Revit si es incorrecta.
2. Revisar el mapeado general.
3. Confirmar el esquema IFC.
4. Ensayar la entidad en el receptor.
5. Documentar la excepción.

## 23. Esquema IFC y compatibilidad

El diccionario no debe ligarse a un único esquema sin pruebas. Se preparará una matriz para:

- IFC 2x3 Coordination View 2.0, cuando lo exija una aplicación.
- IFC 4 Reference View, cuando esté soportado.
- Otras variantes solo si existe requisito concreto.

Para cada esquema se verificará:

- Entidades.
- Psets.
- Cantidades.
- Relaciones espaciales.
- GlobalIds.
- Interpretación en las aplicaciones.

La presencia de una propiedad en IFC 4.3 no implica que esté disponible con idéntico nombre o semántica en IFC 2x3.

## 24. Reglas de cumplimentación

### 24.1 Obligatorio

Debe existir para que el elemento se admita en la entrega.

### 24.2 Condicional

Se exige solo cuando aplica, por ejemplo factor solar en elementos transparentes.

### 24.3 Informativo

Ayuda a revisión, pero no bloquea la entrega.

El diccionario técnico marcará cada campo con uno de estos niveles y una regla de validación.

## 25. Validación previa en Revit

Se crearán tablas por categoría con filtros para detectar:

- Códigos vacíos.
- Valores fuera de enumeración.
- Construcciones inexistentes.
- Zonas sin código.
- Elementos `TO_REVIEW`.
- Contradicciones entre función y categoría.
- Duplicidad de códigos de ejemplar.
- Tipos con prestaciones incompletas.

No se exportará una entrega formal con campos obligatorios pendientes.

## 26. Validación del IFC

La revisión se realizará en cuatro niveles:

1. **Sintaxis:** el archivo abre y cumple el esquema.
2. **Semántica:** las entidades y relaciones son adecuadas.
3. **Información:** Psets, propiedades y cantidades están presentes.
4. **Consumo:** el receptor utiliza o permite mapear la información.

Para cada parámetro se registrará:

| Campo | Revit | IFC | Open BIM Analytical Model | TeKton3D | CYPETHERM |
|---|---|---|---|---|---|
| Presente | Sí/No | Sí/No | Sí/No | Sí/No | Sí/No |
| Editable | Sí/No | No aplica | Sí/No | Sí/No | Sí/No |
| Aplicado | No aplica | No aplica | Sí/No | Sí/No | Sí/No |

## 27. Ensayo de persistencia

Para comprobar actualizaciones:

1. Exportar versión A.
2. Registrar GlobalIds y códigos.
3. Modificar posición de un elemento.
4. Cambiar una propiedad de otro.
5. Añadir y eliminar elementos de prueba.
6. Exportar versión B con la misma configuración.
7. Actualizar en cada receptor.
8. Comprobar elementos conservados, añadidos y retirados.

Una propiedad útil pero incapaz de mantenerse entre revisiones debe tratarse como dato de entrega, no como clave de sincronización.

## 28. Valores calculados y valores declarados

Se distinguirán:

- Valor geométrico calculado por Revit.
- Valor exportado como cantidad IFC.
- Valor declarado mediante parámetro.
- Valor recalculado por el receptor.

No se duplicará un área calculada como texto para forzar coincidencia. Las diferencias deben investigarse y documentarse.

## 29. Calidad y procedencia del dato

`EEM_SOURCE_SYSTEM` identificará la autoridad, por ejemplo:

- `REVIT_GEOMETRY`
- `PROJECT_SPECIFICATION`
- `MANUFACTURER`
- `CYPE_CATALOG`
- `TEKTON_LIBRARY`
- `MANUAL_VALIDATED`

Para propiedades críticas se conservarán también referencia documental, fecha y responsable en el registro externo o catálogo.

## 30. Datos que no deben incluirse sin necesidad

- Propiedades internas irrelevantes de Revit.
- Parámetros vacíos masivos.
- Textos duplicados en varios Psets.
- Información personal no necesaria.
- Rutas locales del equipo.
- Comentarios de trabajo no aprobados.
- Prestaciones no verificadas.
- Valores por defecto que aparenten validación.

Minimizar datos facilita la revisión y reduce ambigüedad.

## 31. Estructura versionada propuesta

El repositorio incorporará progresivamente:

```text
config/
  revit/
    shared-parameters/
    schedules/
  ifc/
    category-mapping/
    property-sets/
    parameter-mapping/
data/
  diccionario-parametros.yml
  enumeraciones.yml
```

Cada archivo incluirá versión compatible, fecha, responsable y estado de validación.

## 32. Procedimiento de implantación

1. Aprobar el diccionario mínimo.
2. Generar parámetros compartidos con GUID estables.
3. Incorporarlos a una plantilla de prueba.
4. Crear tablas de cumplimentación y QA.
5. Definir Psets y mapeados por esquema.
6. Preparar un modelo mínimo con valores inequívocos.
7. Exportar IFC.
8. Inspeccionar propiedades y cantidades.
9. Importar en Open BIM Analytical Model y TeKton3D.
10. Transferir a CYPETHERM HE Plus.
11. Completar la matriz de consumo.
12. Retirar campos no utilizados o corregir el mapeado.
13. Publicar una versión aprobada de la configuración.

## 33. Valores de prueba inequívocos

Durante el ensayo no se usarán valores reales repetitivos. Se introducirán marcas reconocibles:

- `TEST_SPACE_A01`
- `TEST_WALL_EXT_01`
- `TEST_CONS_023`
- U = 0,237 W/(m²·K)
- Fracción de vidrio = 0,613

Esto permite detectar redondeos, pérdidas, conversiones y cruces de campos.

Los valores de prueba se eliminarán antes de publicar el modelo de referencia definitivo.

## 34. Errores frecuentes

| Síntoma | Causa probable | Revisión inicial |
|---|---|---|
| El parámetro existe en Revit pero no en IFC | Pset o mapeado no activado | Configuración y archivo de mapeado |
| La propiedad aparece duplicada | Varias vías de exportación activas | Psets comunes, tablas y conjunto propio |
| El número llega como texto | Tipo de parámetro o mapeado incorrecto | Definición y tipo IFC |
| Cambian unidades o escala | Conversión no comprobada | Unidad IFC y valor de prueba |
| Se pierde al actualizar | GlobalId regenerado o receptor no sincroniza | Persistencia y configuración |
| `IsExternal` contradice la frontera | Clasificación arquitectónica insuficiente | Espacios adyacentes y `BoundaryType` |
| U de Revit no coincide con el motor | Diferente alcance o fuente | Vidrio/marco/conjunto y catálogo |
| Zona térmica no llega | Representación no soportada | Propiedad personalizada o recreación |
| Revit 2026 no muestra el gestor esperado | Función disponible desde 2026.3 | Versión exacta y flujo TXT |

## 35. Criterios de aceptación

El mapeado estará preparado cuando:

- El diccionario esté aprobado y versionado.
- Los GUID de parámetros sean estables.
- Los campos obligatorios estén completos.
- Las enumeraciones no contengan valores libres.
- Entidades y tipos IFC sean coherentes.
- Psets y cantidades necesarias estén presentes.
- No existan duplicidades de propiedades.
- Unidades y tipos de dato sean correctos.
- GlobalIds y códigos permitan comparar revisiones.
- La matriz de consumo de los receptores esté cumplimentada.
- Las propiedades aplicadas al cálculo se hayan comprobado mediante resultados o interfaz.

## 36. Checklist de entrega

- [ ] Se ha utilizado la versión aprobada del archivo de parámetros compartidos.
- [ ] Los parámetros conservan GUID, nombre y tipo de dato.
- [ ] Tipo y ejemplar se han asignado correctamente.
- [ ] Los códigos obligatorios están completos.
- [ ] `EEM_BOUNDARY_TYPE` utiliza valores admitidos.
- [ ] Espacios y zonas tienen identificadores estables.
- [ ] Cerramientos y huecos tienen código de construcción.
- [ ] Las prestaciones incluyen fuente y alcance.
- [ ] La configuración corresponde a la versión exacta de Revit.
- [ ] El esquema IFC está documentado.
- [ ] Se han activado solo los Psets y cantidades necesarios.
- [ ] El archivo de mapeado está versionado.
- [ ] Las propiedades se han inspeccionado en el IFC.
- [ ] Se ha comprobado su lectura en los receptores.
- [ ] Se ha realizado el ensayo de persistencia.
- [ ] No quedan valores de prueba en la entrega.

## 37. Ensayo de referencia

El modelo de prueba contendrá:

- Dos espacios en una zona y un espacio no acondicionado.
- Muro exterior, muro con terreno y partición interior.
- Ventana con U y fracción de vidrio inequívocas.
- Puerta parcialmente acristalada.
- Cubierta, suelo y sombra.
- Un elemento excluido.
- Un tipo con construcción común y una excepción de ejemplar.

Se exportará al menos en los esquemas realmente admitidos por los receptores. La matriz final indicará para cada propiedad si se exporta, se muestra, se conserva al actualizar y se aplica.

## 38. Fuentes principales

- Autodesk, *Customize the IFC Setup*, Revit 2026.
- Autodesk, *IFC Export Setup Options*.
- Autodesk, *Create Shared Project Parameters*, Revit 2026.
- Autodesk, *Export Shared Parameters to a Shared Parameter File*, Revit 2026.
- Autodesk, *Export User Defined Properties to IFC*.
- Autodesk, *Supported IFC Classes*, Revit 2026.
- buildingSMART, *IFC 4.3.2 Documentation: IfcSpace*.
- buildingSMART, *IFC 4.3.2 Documentation: Pset_WallCommon*.
- buildingSMART, *IFC 4.3.2 Documentation: IfcWindow*.
- buildingSMART, *IFC 4.3.2 Documentation: IfcDoor*.
