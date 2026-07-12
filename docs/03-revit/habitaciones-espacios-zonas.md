---
title: Habitaciones, espacios y zonas térmicas en Revit 2026
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
software:
  nombre: Autodesk Revit
  version_base: "2026"
---

# Habitaciones, espacios y zonas térmicas en Revit 2026

Las habitaciones y los espacios permiten convertir la geometría arquitectónica en volúmenes identificables. En el flujo estudiado son la principal referencia para generar `IfcSpace`, reconstruir superficies analíticas y organizar posteriormente las zonas térmicas.

La estrategia debe garantizar que se representa todo el volumen relevante del edificio, no solo las estancias que aparecen en los planos arquitectónicos.

!!! warning "Habitación no equivale automáticamente a zona térmica"
    Una habitación de Revit es una unidad arquitectónica. Una zona térmica puede agrupar varias habitaciones o exigir dividir un recinto, según uso, horarios, orientación y sistema.

## 1. Habitaciones y espacios MEP

### 1.1 Habitaciones

Las habitaciones pertenecen al modelo arquitectónico y almacenan información como:

- Número.
- Nombre.
- Nivel.
- Área y perímetro.
- Volumen, cuando se activa su cálculo.
- Fase.
- Ocupación y departamento.
- Límites superior e inferior.

Son la referencia inicial recomendada cuando el modelo fuente es arquitectónico y se exporta desde ese mismo archivo.

### 1.2 Espacios MEP

Los espacios se utilizan en Revit MEP para análisis de sistemas, cargas y zonas. También se basan en elementos delimitadores y deben ocupar todo el volumen que interviene en el análisis.

Pueden resultar adecuados cuando:

- El modelo energético se gestiona en un archivo MEP independiente.
- La arquitectura está vinculada.
- Se necesitan propiedades específicas de sistemas.
- El flujo receptor está configurado para exportar espacios en lugar de habitaciones.

### 1.3 Elección de la fuente

Debe elegirse una fuente principal para evitar duplicidades:

| Situación | Fuente candidata |
|---|---|
| Arquitectura y exportación en el mismo archivo | Habitaciones |
| Modelo MEP separado con arquitectura vinculada | Espacios |
| Receptor exige una categoría concreta | La categoría verificada en ensayo |

No se exportarán habitaciones y espacios superpuestos sin confirmar cómo los interpreta el receptor.

## 2. Cobertura completa del edificio

Autodesk indica que un análisis eficaz requiere incluir todo el volumen del edificio. Además de las estancias habituales deben considerarse:

- Pasillos.
- Vestíbulos.
- Escaleras.
- Atrios.
- Patinillos.
- Cámaras.
- Áticos.
- Plénums.
- Espacios bajo cubierta.
- Aparcamientos.
- Cuartos técnicos.
- Espacios no habitables.

La ausencia de uno de estos volúmenes puede convertir sus cerramientos adyacentes en superficies exteriores o generar huecos en el modelo analítico.

## 3. Activación del cálculo de volúmenes

Revit no calcula por defecto los volúmenes de las habitaciones debido al impacto en el rendimiento.

Para preparar el modelo:

1. Activar el cálculo de áreas y volúmenes durante la revisión.
2. Regenerar tablas y vistas.
3. Comprobar que todas las habitaciones relevantes muestran volumen.
4. Mantenerlo activo durante las exportaciones de ensayo.

La activación no garantiza que el volumen sea correcto. Solo permite calcularlo según los límites existentes.

## 4. Estados de las habitaciones

La tabla de control debe distinguir:

- Colocada y cerrada.
- No colocada.
- No cerrada.
- Redundante.
- Área cero.
- Volumen no calculado.
- Volumen cero o anómalo.

### 4.1 No colocada

Existe en la tabla, pero no tiene posición en el modelo. No debe exportarse como recinto calculable.

### 4.2 No cerrada

Está colocada en una región sin cierre completo. Debe localizarse la discontinuidad, la fase incorrecta o el elemento que no delimita.

### 4.3 Redundante

Existen dos habitaciones en la misma región cerrada. Debe eliminarse o recolocarse la duplicada.

### 4.4 Regla de aceptación

No se aceptará ninguna habitación relevante con estado no colocado, no cerrado, redundante, área cero o volumen no calculado.

## 5. Límite inferior

El límite inferior depende de:

- Nivel base.
- Desfase de base.
- Elementos delimitadores existentes.

El desfase permite elevar o bajar el inicio del volumen respecto al nivel, pero debe utilizarse con una intención documentada.

Casos de revisión:

- Suelos elevados.
- Forjados con acabados independientes.
- Rampas.
- Plantas escalonadas.
- Recintos parcialmente enterrados.

## 6. Límite superior

El límite superior se define mediante:

- Nivel de límite superior.
- Desfase de límite.

La altura no delimitada es la máxima altura potencial derivada de estos parámetros. El volumen real puede quedar recortado por cubiertas, suelos o techos delimitadores intermedios.

### 6.1 Regla

El límite superior debe situarse por encima del cerramiento que realmente cierra el recinto cuando se desea que Revit utilice la geometría inclinada o irregular de dicho elemento.

Autodesk recomienda, por ejemplo, que una habitación bajo cubierta tenga un límite superior mayor que la cubierta para que esta recorte el volumen según su pendiente.

## 7. Altura de cálculo

La altura de cálculo del nivel determina la cota a la que Revit mide el perímetro para obtener el área. Puede afectar a:

- Muros inclinados.
- Espacios bajo escaleras.
- Cubiertas bajas.
- Cambios de sección.
- Nichos y huecos próximos al suelo.

Debe revisarse en sección antes de modificarla. Un ajuste que corrige una habitación puede alterar el perímetro de todas las habitaciones asociadas al nivel.

## 8. Elementos delimitadores

Pueden intervenir como límites:

- Muros.
- Suelos.
- Cubiertas.
- Techos.
- Columnas.
- Muros cortina.
- Líneas de separación.
- Elementos de vínculos cuando el vínculo se marca como delimitador.

La condición depende del parámetro `Room Bounding` y de la geometría efectiva.

## 9. Uso correcto de `Room Bounding`

### 9.1 Activar

Debe estar activo cuando el elemento representa una frontera real del volumen:

- Muro que separa recintos.
- Forjado entre plantas.
- Cubierta que cierra un espacio.
- Cerramiento exterior.
- Línea de separación que materializa una división analítica intencionada.

### 9.2 Desactivar o revisar

Debe revisarse en:

- Pilares interiores.
- Muros de altura parcial.
- Mobiliario fijo.
- Revestimientos independientes.
- Falsos techos.
- Elementos decorativos.
- Masas o familias auxiliares.
- Elementos exteriores que no deben crear recintos.

Autodesk documenta que una columna o muro parcial delimitador puede excluir del volumen el espacio situado sobre él.

### 9.3 No aplicar reglas ciegas

No se desactivará `Room Bounding` en toda una categoría sin comprobar casos particulares. Un techo puede ser irrelevante en una estancia y representar el límite real de un plénum en otra.

## 10. Líneas de separación

Las líneas de separación permiten dividir un área sin muro físico. Son útiles para:

- Separar usos dentro de un espacio abierto.
- Resolver límites virtuales.
- Dividir una geometría anular.
- Crear recintos analíticos simplificados.

Riesgos:

- Líneas duplicadas.
- Segmentos abiertos.
- Límites que atraviesan huecos o muros.
- Divisiones funcionales sin sentido térmico.
- Regiones estrechas o residuales.

Cada línea utilizada para el flujo energético debe tener una finalidad documentada.

## 11. Muros de altura parcial y pilares

Un elemento vertical que no alcanza el límite superior puede dividir el volumen de forma no deseada si actúa como delimitador.

Se comprobarán en sección:

- Altura real.
- Unión con techo o cubierta.
- Espacio situado sobre el elemento.
- Necesidad de separar térmicamente.

Los pilares interiores normalmente no deben fragmentar el espacio analítico.

## 12. Suelos y forjados

Los suelos pueden definir el límite inferior o superior de las habitaciones. Deben revisarse:

- Suelos de acabado independientes.
- Forjados estructurales.
- Suelos elevados.
- Elementos superpuestos.
- Desfases.

Autodesk advierte que un suelo situado por encima de la altura de cálculo puede interpretarse como límite superior en lugar de inferior y producir un volumen incorrecto.

## 13. Techos y plénums

### 13.1 Techo no delimitador

Si el plénum forma parte del mismo volumen térmico y no se calcula por separado, el falso techo puede dejar de delimitar la habitación para que el volumen alcance el forjado superior.

### 13.2 Plénum independiente

Si tiene comportamiento diferenciado, puede modelarse como espacio propio con:

- Límite inferior en el falso techo.
- Límite superior en el forjado.
- Condición de ventilación.
- Construcciones y adyacencias.

### 13.3 Decisión necesaria

No existe una regla única. Se decidirá según ventilación, sistemas, uso y capacidad del receptor.

## 14. Cubiertas y espacios bajo cubierta

Las habitaciones bajo cubierta deben:

- Extenderse por encima de la cubierta mediante el límite superior.
- Ser recortadas por una cubierta correctamente delimitadora.
- Evitar pequeños huecos en encuentros de muros y cubierta.
- Incluir cámaras o áticos según estrategia.

Se revisará el volumen en sección y 3D.

## 15. Dobles alturas

Opciones:

1. Una habitación continua desde la planta inferior.
2. Varias habitaciones vinculadas a una zona térmica común.
3. División analítica específica en el receptor.

Debe evitarse colocar una habitación en la planta superior dentro del vacío si se solapa con la habitación inferior.

Se comprobarán:

- Forjados parciales.
- Barandillas no delimitadoras.
- Volumen sobre pasarelas.
- Límites verticales.
- Colindancias con plantas adyacentes.

## 16. Escaleras

Las escaleras abiertas pueden conectar varias plantas. Estrategias posibles:

- Integrarlas en un espacio de circulación continuo.
- Separar espacios por planta y agruparlos térmicamente.
- Crear un espacio vertical específico.

La elección dependerá del movimiento de aire considerado, compartimentación y motor.

No deben utilizarse los peldaños y barandillas como límites térmicos detallados.

## 17. Patinillos y huecos verticales

Un patinillo puede:

- Formar parte de un espacio adyacente.
- Ser un espacio independiente.
- Representarse como un único volumen vertical.
- Simplificarse mediante una condición equivalente.

La documentación propia recomienda evitar un espacio independiente por planta cuando el hueco funciona como un volumen vertical continuo, salvo que el receptor o el análisis requieran segmentarlo.

## 18. Atrios

Los atrios combinan dobles alturas, cubiertas, pasarelas y fachadas interiores. Deben definirse:

- Volumen principal.
- Plantas conectadas.
- Espacios perimetrales.
- Superficies interiores.
- Sistema que los acondiciona.
- Estrategia de zonificación.

Un atrio es candidato a ensayo específico antes de generalizar reglas.

## 19. Patios interiores

Un patio abierto es exterior, aunque esté rodeado por el edificio. Las habitaciones o espacios del patio no deben exportarse como zonas interiores acondicionadas.

Debe verificarse:

- Apertura superior.
- Fachadas hacia el patio.
- Huecos.
- Sombras.
- Condición exterior.

Un patio cubierto puede requerir un espacio interior o semiacondicionado distinto.

## 20. Terrazas, balcones y galerías

Normalmente son espacios exteriores y no deben exportarse como `IfcSpace` interior. Sin embargo, sus elementos pueden influir como sombras.

Se utilizará un parámetro de exportación o una regla de selección para evitar convertirlos en recintos calculables sin eliminar su geometría relevante.

## 21. Espacios no habitables

Se incluirán cuando afecten a la envolvente:

- Trasteros.
- Aparcamientos.
- Cuartos técnicos.
- Cámaras sanitarias.
- Áticos.
- Zonas comunes no acondicionadas.

Cada uno debe clasificarse y relacionarse con las zonas habitables. Omitirlos puede transformar particiones interiores en cerramientos exteriores.

## 22. Geometrías anulares o tipo *donut*

Una habitación que rodea completamente a otra puede generar contornos complejos. Cuando el exportador o receptor presenta problemas, puede dividirse mediante líneas de separación en formas más simples.

La división debe:

- Mantener el área y volumen total.
- Evitar espacios residuales.
- Conservar una agrupación térmica común cuando corresponda.
- Ser estable en sucesivas exportaciones.

## 23. Modelos vinculados

Un vínculo Revit o IFC puede proporcionar límites si su propiedad `Room Bounding` está activada. Autodesk indica que esta propiedad está desactivada por defecto en los vínculos.

Riesgos:

- Vínculo descargado.
- Fase no compatible.
- Posición incorrecta.
- Cambio de geometría sin actualizar habitaciones.
- Elementos de vínculo duplicados en el anfitrión.
- Muros cortina IFC que no delimitan habitaciones en Revit.

Debe decidirse qué archivo contiene las habitaciones y cuál contiene la geometría delimitadora.

## 24. Fases

Las habitaciones son específicas de fase. Sus límites también se evalúan según la fase de la vista.

Se comprobará:

- Habitación y cerramientos en fase compatible.
- Estado existente, demolido o nuevo.
- Huecos creados o cerrados por fase.
- Copias de habitaciones entre fases.
- Tabla filtrada por la fase de exportación.

No debe exportarse una mezcla involuntaria de recintos de fases diferentes.

## 25. Opciones de diseño

Las habitaciones pueden variar entre opciones. Cada escenario debe exportarse por separado, con:

- Opción activa identificada.
- Habitaciones propias de la opción.
- Límites correspondientes.
- Nombre de escenario.

No se combinarán habitaciones solapadas de varias alternativas.

## 26. Nomenclatura

Se recomienda separar:

- Código estable.
- Nombre descriptivo.
- Uso energético.
- Unidad de uso.
- Estado habitable/no habitable.
- Zona térmica propuesta.

Ejemplo orientativo:

| Campo | Ejemplo |
|---|---|
| Número | `P01-023` |
| Nombre | `Dormitorio 2` |
| Uso energético | `Residencial privado` |
| Unidad de uso | `Vivienda 01` |
| Condición | `Habitable acondicionado` |
| Zona propuesta | `ZT-V01-DIA` |

Los valores reales deberán adaptarse al proyecto.

## 27. Agrupación mediante zonas

### 27.1 Zonas nativas de Revit

Revit 2026 ha cambiado las herramientas y flujos de zonas respecto a versiones anteriores. No se asumirá que las zonas MEP heredadas se exportan o funcionan igual que en Revit 2025.

### 27.2 `ZoneName`

Puede emplearse un parámetro controlado para transmitir una propuesta de agrupación, siempre que se compruebe el mapeado y el receptor.

### 27.3 Modelo analítico

Open BIM Analytical Model permite crear varias agrupaciones de espacios. Puede ser preferible mantener recintos elementales en IFC y realizar allí la agrupación térmica definitiva.

## 28. Criterios de zonificación térmica

Se considerarán:

- Uso.
- Horarios.
- Consignas.
- Sistema.
- Orientación.
- Relación con exterior.
- Unidad de uso.
- Requisitos reglamentarios.

La simplificación debe equilibrar precisión y número de zonas. No se agruparán espacios únicamente para reducir trabajo si presentan comportamientos claramente distintos.

## 29. Tabla de planificación de habitaciones

Campos mínimos:

- Número.
- Nombre.
- Nivel.
- Fase.
- Área.
- Volumen.
- Límite superior.
- Desfase de límite.
- Desfase de base.
- Altura no delimitada.
- Condición habitable.
- Unidad de uso.
- Zona propuesta.
- Exportable a IFC.

Debe mostrarse también lo no colocado o no cerrado durante el QA/QC.

## 30. Tabla de espacios MEP

Cuando se utilicen espacios:

- Número y nombre.
- Nivel y fase.
- Área y volumen.
- Tipo de espacio.
- Zona.
- Ocupación.
- Condiciones.
- Correspondencia con habitación arquitectónica.

La herramienta de nombres de espacios puede copiar nombres y números de habitaciones vinculadas, pero debe verificarse la unicidad y actualización.

## 31. Vistas de control

Se crearán:

- Plantas coloreadas por habitación.
- Secciones con relleno de volumen.
- Vista 3D de espacios, cuando sea posible.
- Filtros para no habitables.
- Filtros para no exportables.
- Vistas de dobles alturas y cubiertas.

La revisión en planta no basta para validar el volumen tridimensional.

## 32. Incidencias frecuentes

| Síntoma | Causa probable |
|---|---|
| No cerrada | Hueco, elemento no delimitador, fase o vínculo. |
| Volumen demasiado bajo | Falso techo, suelo o elemento parcial delimitador. |
| Volumen demasiado alto | Límite superior excesivo sin cubierta delimitadora. |
| Dos espacios en la misma región | Habitación redundante. |
| Superficie exterior inesperada | Falta el espacio adyacente. |
| Recinto dividido en fragmentos | Pilares, revestimientos o líneas separadoras. |
| Hueco vertical cerrado por planta | Forjado o límites superiores incorrectos. |

## 33. Matriz de decisiones

| Caso | Estrategia inicial |
|---|---|
| Estancia normal | Una habitación cerrada. |
| Pasillo | Habitación independiente o agrupada después. |
| Doble altura | Espacio continuo o varios espacios agrupados. |
| Plénum relevante | Espacio independiente. |
| Plénum irrelevante | Integrado en el recinto, techo no delimitador. |
| Patio abierto | Exterior, no exportar como recinto interior. |
| Patinillo continuo | Espacio vertical o simplificación documentada. |
| Terraza | No exportar como espacio interior; conservar sombras. |

## 34. Checklist previo a IFC

- [ ] Fuente elegida: habitaciones o espacios.
- [ ] Cálculo de volúmenes activado.
- [ ] Todos los volúmenes relevantes representados.
- [ ] Sin habitaciones no cerradas, redundantes o con área cero.
- [ ] Nivel base y límite superior revisados.
- [ ] Desfases documentados.
- [ ] `Room Bounding` revisado.
- [ ] Líneas separadoras justificadas.
- [ ] Dobles alturas comprobadas en sección.
- [ ] Plénums y falsos techos con estrategia definida.
- [ ] Espacios no habitables incluidos o representados.
- [ ] Patios y terrazas clasificados como exterior.
- [ ] Fase y opción de diseño verificadas.
- [ ] Vínculos delimitadores actualizados.
- [ ] Nombres y códigos únicos.
- [ ] Zona térmica propuesta documentada.
- [ ] Parámetro de exportación IFC comprobado.

## 35. Ensayo para Revit 2026

El modelo de prueba incluirá:

1. Habitación rectangular convencional.
2. Dos habitaciones adyacentes.
3. Línea de separación sin muro.
4. Pilar interior parcial.
5. Falso techo y plénum.
6. Cubierta inclinada.
7. Doble altura.
8. Escalera abierta.
9. Patinillo vertical.
10. Patio exterior.
11. Habitación en vínculo.
12. Dos fases.

Se comparará:

- Geometría y cantidades de `IfcSpace`.
- Nombres y números.
- Condición exterior.
- Límites espaciales.
- Resultado en Open BIM Analytical Model.
- Resultado de importación y vinculación en TeKton3D.

## 36. Fuentes principales

- Autodesk, *About Room Volume*, Revit 2026.
- Autodesk, *About Room Area*, Revit 2026.
- Autodesk, *About Ceilings and Floors in Room Volume Computations*, Revit 2026.
- Autodesk, *Use Room Boundaries in a Linked Model*, Revit 2026.
- Autodesk, *Spaces*, Revit MEP 2026.
- Autodesk, *Zones*, Revit MEP 2026.
- CYPE, *Guía de interoperabilidad CYPE-Revit v2.0* (`CYPE-REVIT-20`).

