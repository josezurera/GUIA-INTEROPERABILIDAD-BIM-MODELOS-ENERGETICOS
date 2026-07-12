---
title: QA/QC de Revit e IFC para análisis energético
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
---

# QA/QC de Revit e IFC para análisis energético

El control de calidad debe demostrar que el modelo energético representa la intención del proyecto y que puede reproducirse. La ausencia de errores de software no constituye una validación: un archivo puede abrir correctamente y contener espacios, áreas, orientaciones o construcciones equivocadas.

El procedimiento se organiza en cuatro puertas de control:

1. Modelo Revit.
2. Archivo IFC.
3. Modelo analítico receptor.
4. Modelo energético de cálculo.

!!! warning "Corregir en el nivel de origen"
    Una incidencia debe resolverse en la fuente más temprana que la produce. Las reparaciones manuales en el receptor solo se aceptarán cuando la limitación de intercambio esté demostrada y exista un procedimiento para repetirlas después de cada actualización.

## 1. Objetivos del QA/QC

- Detectar omisiones, duplicidades y clasificaciones erróneas.
- Comparar geometría entre etapas.
- Verificar espacios, superficies, huecos y sombras.
- Confirmar coordenadas, orientación y niveles.
- Comprobar propiedades y construcciones.
- Mantener identificadores entre revisiones.
- Registrar excepciones y limitaciones.
- Evitar que una actualización invalide correcciones previas.
- Proporcionar evidencia suficiente para aprobar o rechazar una entrega.

## 2. Diferencia entre QA y QC

### 2.1 Aseguramiento de calidad — QA

Define cómo debe prepararse el trabajo:

- Normas de modelado.
- Plantillas y parámetros.
- Configuraciones IFC.
- Responsabilidades.
- Criterios de aceptación.
- Modelos de prueba.
- Versionado.

### 2.2 Control de calidad — QC

Comprueba una entrega concreta:

- Inspecciones.
- Tablas y recuentos.
- Comparaciones geométricas.
- Validaciones IFC.
- Importaciones de ensayo.
- Resultados y evidencias.

Un buen QC no compensa un proceso de modelado sin QA; solo detecta sus consecuencias.

## 3. Estados de una entrega

| Estado | Significado |
|---|---|
| `BORRADOR` | Modelo en preparación, no apto para intercambio |
| `REVISION_INTERNA` | En controles de Revit |
| `IFC_CANDIDATO` | Exportado y pendiente de validación IFC |
| `ANALITICO_CANDIDATO` | Importado y pendiente de revisión analítica |
| `ACEPTADO_CON_LIMITACIONES` | Utilizable con excepciones documentadas |
| `ACEPTADO` | Cumple todos los criterios aplicables |
| `RECHAZADO` | Contiene incidencias bloqueantes |

No se enviará al siguiente nivel una entrega rechazada.

## 4. Responsabilidades mínimas

| Rol | Responsabilidad |
|---|---|
| Autor del modelo | Corregir geometría, parámetros y clasificación en Revit |
| Responsable IFC | Mantener configuración, exportar y validar el archivo |
| Responsable analítico | Revisar espacios, superficies, sombras y adyacencias |
| Responsable de cálculo | Confirmar construcciones, zonas, sistemas y resultados |
| Revisor | Verificar evidencias y aprobar o rechazar |

Una persona puede asumir varios roles en proyectos pequeños, pero las revisiones deben quedar registradas.

## 5. Elementos de una entrega controlada

- Modelo RVT o referencia a su revisión.
- IFC original sin modificar.
- Registro de exportación.
- Configuración IFC utilizada.
- Archivos de mapeado y Psets.
- Informe de validación.
- Matriz de comparación.
- Registro de incidencias.
- Capturas o vistas de evidencia.
- Modelo analítico receptor.
- Modelo de cálculo y resultados de control.

## 6. Identificación de archivos

Cada archivo tendrá:

- Proyecto.
- Disciplina.
- Destino.
- Estado.
- Revisión.
- Fecha.
- Hash SHA-256.

El hash permite demostrar que el archivo revisado es el mismo que se entrega.

## 7. Severidad de incidencias

| Severidad | Criterio | Efecto en la entrega |
|---|---|---|
| S1 — Bloqueante | Impide generar, importar o calcular | Rechazo inmediato |
| S2 — Mayor | Altera espacios, áreas, orientación, adyacencias o construcciones | Rechazo hasta corregir |
| S3 — Menor | Diferencia localizada dentro de límites controlables | Aceptación condicionada |
| S4 — Observación | Mejora documental sin efecto actual | No bloquea |

La severidad se asigna por impacto demostrado o razonablemente probable.

## 8. Tipos de comprobación

### 8.1 Automática

- Campos obligatorios.
- Enumeraciones.
- Duplicados.
- Recuentos.
- Rangos numéricos.
- Estructura IFC.

### 8.2 Semiautomática

- Comparación de áreas y volúmenes.
- Correspondencia de identificadores.
- Clasificación por orientación.
- Diferencias entre revisiones.

### 8.3 Visual

- Continuidad de envolvente.
- Sombras.
- Geometrías complejas.
- Adyacencias.
- Resultados inesperados.

### 8.4 Funcional

- Importación.
- Actualización.
- Conservación de asignaciones.
- Ejecución del cálculo.
- Sensibilidad de resultados.

Ningún tipo sustituye completamente a los demás.

# Puerta 0. Preparación del control

## 9. Definir el alcance

Antes de revisar se fijarán:

- Edificio y zonas incluidas.
- Estado o fase.
- Receptor y versión.
- Configuración IFC.
- Magnitudes de control.
- Tolerancias.
- Excepciones conocidas.
- Responsable y fecha límite.

## 10. Congelar referencias

Se registrarán las versiones de:

- Revit.
- Exportador IFC.
- Open BIM Analytical Model.
- CYPETHERM HE Plus.
- TeKton3D y módulos utilizados.
- Archivos de parámetros y mapeado.

Una actualización durante el control crea una nueva combinación de ensayo.

## 11. Tolerancias del proyecto

No se adoptará un único porcentaje para todas las magnitudes. Se definirán por:

- Área útil.
- Volumen.
- Área de envolvente.
- Área de huecos.
- Orientación.
- Número de espacios.
- Número de superficies.
- Coordenadas.

Debe existir tolerancia absoluta y relativa. Una diferencia porcentual pequeña puede ocultar un error grande en un elemento repetitivo, y una diferencia porcentual grande puede proceder de una superficie irrelevante muy pequeña.

## 12. Modelo de referencia

El banco de ensayo de la guía se utilizará como regresión antes de aprobar nuevas versiones o configuraciones. Debe contener casos simples y geometrías de riesgo con resultados esperados conocidos.

# Puerta 1. Control del modelo Revit

## 13. Identidad y estado

Comprobar:

- Archivo y revisión correctos.
- Modelo central/local según procedimiento.
- Fase y opción de diseño.
- Vínculos cargados y posicionados.
- Advertencias relevantes.
- Ausencia de elementos de prueba.

## 14. Coordenadas y orientación

- Ubicación geográfica.
- Norte verdadero.
- Punto base y punto topográfico.
- Coordenadas compartidas.
- Distancia al origen interno.
- Cotas de control.

Se verificará una fachada y un punto conocidos, no solo los símbolos de coordenadas.

## 15. Niveles

- Nombres únicos.
- Cotas y orden.
- Plantas de edificio.
- Restricciones de elementos.
- Niveles auxiliares excluidos como plantas IFC.
- Correspondencia con espacios.

## 16. Habitaciones, espacios y zonas

- Fuente única seleccionada.
- Todos los volúmenes relevantes representados.
- Sin colocar, no cerrados o redundantes identificados.
- Área y volumen calculados.
- Límites verticales correctos.
- Patinillos, plénums, atrios y espacios no acondicionados resueltos.
- Códigos de zona completos.

## 17. Envolvente

- Muros, suelos, cubiertas y techos continuos.
- Sin grandes huecos o duplicados.
- Restricciones y uniones correctas.
- Contactos con exterior, terreno y espacios adyacentes clasificados.
- Cerramientos parcialmente enterrados identificados.
- Elementos auxiliares sin función delimitadora.

## 18. Huecos

- Familias anfitrionadas y categorías correctas.
- Corte efectivo del anfitrión.
- Dimensiones y cotas.
- Área bruta, vidrio y marco documentados.
- Lucernarios y puertas mixtas ensayados.
- Paneles opacos y transparentes diferenciados.

## 19. Sombras

- Elementos relevantes clasificados.
- Contexto innecesario excluido.
- Voladizos, lamas y edificios vecinos simplificados.
- Protecciones móviles mediante escenario.
- Estudios solares de control coherentes.

## 20. Geometrías de riesgo

- Aristas cortas y ángulos agudos.
- Solapes y duplicados.
- Muros inclinados, curvos y elípticos.
- Cubiertas complejas.
- Dobles pieles y cámaras.
- Mallas y familias in situ.
- Coordenadas alejadas.

Cada caso aceptado debe tener evidencia de ensayo.

## 21. Parámetros

- Archivo de parámetros compartidos correcto.
- GUID, nombre y tipo de dato.
- Campos obligatorios completos.
- Enumeraciones válidas.
- Códigos únicos donde corresponda.
- Construcciones existentes en el catálogo.
- Valores de prueba eliminados.

## 22. Vista de exportación

- Vista 3D dedicada.
- Plantilla aplicada.
- Categorías y filtros.
- Fase y opción.
- Vínculos.
- Caja de sección.
- Sin ocultación temporal.

## 23. Modelo analítico nativo como diagnóstico

Generar y revisar:

- Espacios analíticos.
- Superficies.
- Aberturas.
- Sombras.
- Tabla de áreas y volúmenes.
- Valores inesperadamente grandes o pequeños.

Un modelo analítico nativo correcto no aprueba automáticamente el IFC, pero ayuda a localizar errores del RVT.

## 24. Salida de la Puerta 1

Evidencias mínimas:

- Checklist Revit firmado.
- Tablas de espacios y elementos.
- Capturas 3D y secciones de control.
- Registro de advertencias relevantes.
- Lista de excepciones.

Resultado: `APROBADO_P1` o `RECHAZADO_P1`.

# Puerta 2. Control del archivo IFC

## 25. Integridad del archivo

- El archivo existe y su tamaño es razonable.
- Hash calculado.
- Abre en visor independiente.
- Encabezado y esquema correctos.
- Aplicación y versión de origen registradas.
- No está modificado después de exportar.

## 26. Estructura espacial

- `IfcProject`.
- `IfcSite`.
- `IfcBuilding`.
- `IfcBuildingStorey`.
- `IfcSpace`.
- Contención correcta.
- Niveles auxiliares no convertidos en plantas.

## 27. Coordenadas IFC

- Punto de control X, Y, Z.
- Elevación del sitio.
- Rotación y norte.
- Coincidencia con otros modelos.
- Ausencia de desplazamientos manuales del visor.

## 28. Entidades

Contar y comparar:

- Espacios.
- Muros.
- Suelos.
- Cubiertas.
- Ventanas.
- Puertas.
- Muros cortina y paneles.
- Sombras u obstáculos.

Las diferencias deben explicarse por descomposición conocida, no aceptarse solo porque la geometría parece similar.

## 29. Geometría

- Cerramiento completo.
- Huecos insertados.
- Espacios con volumen.
- Curvas y pendientes.
- Sin duplicados.
- Sin elementos lejos del edificio.
- Sin triangulación desproporcionada.
- Sin contenido exterior irrelevante.

## 30. Relaciones

- Hueco y elemento de relleno.
- Tipo y ejemplar.
- Materiales y capas.
- Contención espacial.
- Límites de espacios, cuando se exportan.
- Zonas o grupos, cuando proceda.

## 31. Propiedades y cantidades

- Psets comunes.
- `EEM_EnergyExchange`.
- Valores y tipos de dato.
- Unidades.
- Cantidades base.
- Valores vacíos.
- Ausencia de propiedades duplicadas.

Se comprobarán con valores inequívocos del modelo de referencia.

La comprobación automática de entidades, atributos y propiedades se realizará mediante las especificaciones IDS versionadas descritas en [Validación automática de IFC mediante IDS](validacion-ids.md).

## 32. Identificadores

- GlobalIds válidos y únicos.
- Correspondencia con elementos Revit.
- Persistencia respecto a revisión anterior.
- Efecto de división por niveles.
- Nuevos, modificados y eliminados identificables.

## 33. Comparación cuantitativa P1–P2

| Magnitud | Revit | IFC | Diferencia | Tolerancia | Estado |
|---|---:|---:|---:|---:|---|
| Espacios |  |  |  |  |  |
| Área útil |  |  |  |  |  |
| Volumen |  |  |  |  |  |
| Área de envolvente |  |  |  |  |  |
| Área de huecos por orientación |  |  |  |  |  |

Los totales se desglosarán por planta, espacio, orientación y construcción cuando exista una diferencia.

## 34. Salida de la Puerta 2

Evidencias mínimas:

- Informe de estructura y entidades.
- Capturas de coordenadas y geometría.
- Matriz de propiedades.
- Comparación cuantitativa.
- Lista de incidencias IFC.

Resultado: `APROBADO_P2` o `RECHAZADO_P2`.

# Puerta 3. Control del modelo analítico receptor

## 35. Importación

Registrar:

- Aplicación y versión.
- Método: importar, vincular o generar.
- Opciones utilizadas.
- Tiempo de proceso.
- Mensajes y reparaciones automáticas.
- Elementos omitidos.

## 36. Espacios analíticos

- Número y códigos.
- Área y volumen.
- Espacios perdidos o fusionados.
- Recintos pequeños inesperados.
- Acondicionamiento.
- Asignación a zonas.

## 37. Superficies

- Tipo: exterior, terreno, interior, adiabática o sombra.
- Espacio principal y adyacente.
- Área y orientación.
- Construcción asignada.
- Fragmentación.
- Aristas y contornos.

Una superficie exterior donde debe existir un espacio adyacente es incidencia mayor.

## 38. Huecos

- Anfitrión analítico.
- Área.
- Orientación e inclinación.
- Marco y vidrio.
- Construcción.
- Huecos interiores.
- Puertas mixtas y muros cortina.

## 39. Sombras

- Presencia.
- Posición.
- Huecos afectados.
- Elementos propios y remotos.
- Protección móvil o escenario.
- Ausencia de falsos cerramientos.

## 40. Construcciones

- Códigos transferidos.
- Soluciones reconocidas.
- Propiedades que requieren reasignación.
- U, factor solar y permeabilidad.
- Contacto con terreno.
- Medianerías y adiabáticas.

## 41. Comparación P2–P3

Se compararán:

- Espacios.
- Superficies por tipo.
- Área de envolvente.
- Área de huecos por orientación.
- Sombras.
- Construcciones asignadas.
- Elementos no interpretados.

La geometría analítica puede simplificarse respecto al IFC, pero la diferencia debe ser coherente y estar dentro de tolerancia.

## 42. Actualización

Si el flujo es iterativo:

1. Actualizar con una revisión controlada.
2. Comprobar elementos añadidos y eliminados.
3. Verificar asignaciones conservadas.
4. Revisar superficies regeneradas.
5. Identificar reparaciones manuales perdidas.

Una actualización no controlada invalida la aprobación anterior.

## 43. Salida de la Puerta 3

Evidencias mínimas:

- Modelo analítico guardado.
- Tablas de espacios y superficies.
- Capturas de incidencias.
- Matriz de construcciones.
- Resultado del ensayo de actualización.

Resultado: `APROBADO_P3` o `RECHAZADO_P3`.

# Puerta 4. Control del modelo energético

## 44. Datos generales

- Ubicación y clima.
- Orientación.
- Zonificación.
- Uso y horarios.
- Condiciones operacionales.
- Sistemas, si forman parte del alcance.
- Procedimiento reglamentario.

## 45. Cerramientos y huecos

- Construcciones definitivas.
- U y masa térmica.
- Factor solar y marco.
- Permeabilidad.
- Puentes térmicos, si corresponden al motor.
- Condiciones de contorno.

## 46. Coherencia de resultados

Antes de aceptar se revisarán órdenes de magnitud y distribución:

- Demanda de calefacción y refrigeración.
- Cargas máximas.
- Ganancias solares.
- Pérdidas por transmisión.
- Ventilación e infiltración.
- Resultados por zona.

Un cálculo finalizado sin error puede ser físicamente incoherente.

## 47. Ensayos de sensibilidad

Modificar de forma controlada una variable relevante:

- Retirar una sombra.
- Cambiar U de un cerramiento.
- Reducir área de vidrio.
- Cambiar orientación.
- Desactivar una zona.

El resultado debe responder con el signo y magnitud razonables. Una ausencia total de sensibilidad puede revelar que el dato no se está utilizando.

## 48. Comparación entre motores

Cuando se comparen CYPE y TeKton3D, se igualarán primero:

- Geometría.
- Clima.
- Construcciones.
- Horarios.
- Zonificación.
- Ventilación e infiltración.
- Sistemas y consignas.

Las diferencias de resultados no deben atribuirse a motores distintos antes de eliminar diferencias de entrada.

## 49. Salida de la Puerta 4

Evidencias mínimas:

- Resumen de entradas.
- Listado de construcciones.
- Resultados principales por zona.
- Ensayos de sensibilidad.
- Incidencias y limitaciones.

Resultado: `ACEPTADO`, `ACEPTADO_CON_LIMITACIONES` o `RECHAZADO`.

# Gestión transversal

## 50. Matriz maestra de comparación

| Control | Revit | IFC | Analítico | Cálculo |
|---|---|---|---|---|
| Coordenadas | Sí | Sí | Sí | Orientación/clima |
| Espacios | Habitación/espacio | `IfcSpace` | Recinto analítico | Zona |
| Cerramientos | Anfitriones | Entidades IFC | Superficies | Construcciones |
| Huecos | Familias | `IfcWindow`/`IfcDoor` | Aberturas | Propiedades térmicas |
| Sombras | Geometría | Objeto exportado | Superficie de sombra | Efecto solar |
| Identidad | UniqueId | GlobalId | Id receptor | Referencia de cálculo |

## 51. Regla de trazabilidad

Toda incidencia debe señalar:

- Primera etapa donde aparece.
- Etapa donde se detecta.
- Aplicación y versión.
- Elementos afectados.
- Corrección aplicada.
- Evidencia antes y después.

## 52. Excepciones

Una excepción se acepta únicamente si:

- La limitación está demostrada.
- El impacto está cuantificado.
- Existe una solución repetible.
- Tiene responsable.
- Se revisa después de cada actualización.
- No incumple un requisito reglamentario.

## 53. Muestreo

Los controles automáticos se aplicarán al 100 % cuando sea posible. La inspección visual puede utilizar muestreo, pero incluirá siempre:

- Cada tipología geométrica.
- Cada construcción.
- Cada orientación.
- Cada planta.
- Todas las geometrías de riesgo.
- Todos los casos con incidencias previas.

## 54. Regresión

Debe repetirse el modelo de referencia cuando cambie:

- Revit.
- Exportador IFC.
- Esquema.
- Configuración.
- Mapeado.
- Aplicación receptora.
- Procedimiento de actualización.

## 55. Criterios globales de aceptación

La entrega se acepta cuando:

- Las cuatro puertas aplicables están aprobadas.
- No existen incidencias S1 o S2 abiertas.
- Las S3 están cuantificadas y aceptadas.
- Los archivos revisados coinciden con sus hashes.
- Las diferencias geométricas cumplen tolerancias.
- Las propiedades críticas llegan o se reasignan de forma controlada.
- La actualización ha sido probada si el flujo es iterativo.
- Los resultados responden de forma coherente a ensayos de sensibilidad.
- El informe permite reproducir el proceso.

## 56. Informe final

El informe de QA/QC contendrá:

1. Identificación y alcance.
2. Versiones de software.
3. Archivos y hashes.
4. Configuración IFC.
5. Tolerancias.
6. Resultado de cada puerta.
7. Comparaciones cuantitativas.
8. Incidencias abiertas y cerradas.
9. Limitaciones.
10. Aprobación, fecha y responsable.

## 57. Fuentes metodológicas

Este procedimiento consolida los criterios documentados en los capítulos de Revit, IFC, espacios, envolvente, huecos, sombras, geometrías de riesgo, parámetros y exportación. Las fuentes oficiales se mantienen en el registro estructurado y en la bibliografía del proyecto.
