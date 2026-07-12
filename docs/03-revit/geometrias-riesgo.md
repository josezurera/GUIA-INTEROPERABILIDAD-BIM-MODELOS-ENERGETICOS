---
title: Geometrías de riesgo en Revit 2026
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
software:
  nombre: Autodesk Revit
  version_base: "2026"
---

# Geometrías de riesgo en Revit 2026

Se consideran geometrías de riesgo aquellas que pueden verse correctamente en Revit, pero producir espacios incompletos, superficies degeneradas, huecos perdidos, adyacencias falsas o una fragmentación excesiva al generar el modelo analítico o exportar a IFC.

El propósito no es prohibir la arquitectura compleja, sino establecer cuándo debe simplificarse, dividirse, ensayarse o reconstruirse en la aplicación receptora.

!!! warning "Complejidad geométrica no equivale a precisión energética"
    Añadir caras, aristas y detalles puede reducir la interoperabilidad sin mejorar el cálculo. La representación adecuada es la más sencilla que conserva volumen, área, orientación, adyacencia y efecto solar dentro de las tolerancias del proyecto.

## 1. Principio de evaluación

Cada geometría se valorará mediante cuatro preguntas:

1. ¿Cambia una magnitud relevante para el análisis?
2. ¿Puede representarse mediante superficies planas y recintos válidos?
3. ¿Se conserva al pasar por IFC y por el receptor?
4. ¿Permanece estable después de actualizar el modelo?

Si alguna respuesta es negativa, debe definirse una representación analítica alternativa.

## 2. Indicadores de riesgo

Una zona requiere revisión especial cuando contiene:

- Aristas muy cortas.
- Ángulos muy agudos.
- Caras casi coplanares.
- Elementos duplicados o solapados.
- Superficies curvas o de doble curvatura.
- Muros inclinados o elípticos.
- Perfiles editados complejos.
- Recintos muy pequeños o estrechos.
- Dobles pieles y cámaras delgadas.
- Cubiertas con muchos faldones.
- Encuentros de más de tres elementos.
- Huecos tangentes a bordes.
- Mallas importadas.
- Coordenadas excesivamente alejadas del origen interno.

## 3. Matriz de severidad

| Nivel | Descripción | Actuación |
|---|---|---|
| Bajo | Diferencia visual sin efecto medible | Documentar o aceptar |
| Medio | Fragmentación o pequeña diferencia de área | Simplificar y comparar |
| Alto | Pérdida de superficie, hueco o adyacencia | Corregir antes de exportar |
| Crítico | No se genera el modelo o aparece un recinto inválido | Aislar el caso y sustituir la geometría |

La severidad depende del efecto, no solo de la rareza de la forma.

## 4. Tolerancias: qué significan y qué no

La resolución espacial y superficial de Revit controla la detección de espacios y caras. Autodesk indica que la resolución superficial debe ser menor que la dimensión mínima de la superficie que se desea conservar.

Estas configuraciones:

- No son tolerancias universales del proyecto.
- No determinan el comportamiento del exportador IFC.
- No garantizan la aceptación en CYPE o TeKton3D.
- No deben utilizarse para ocultar errores grandes.

El protocolo registrará por separado:

- Resolución espacial de Revit.
- Resolución superficial de Revit.
- Tolerancias del exportador o receptor, si se conocen.
- Tolerancias de comparación de área y volumen.

## 5. Pequeños huecos y bordes dentados

Autodesk documenta que el modelo analítico puede presentar pequeños huecos, solapes y bordes dentados como resultado de la aproximación geométrica. No siempre requieren corrección.

Se aceptarán únicamente cuando:

- No falte una superficie completa.
- El área total permanezca dentro de tolerancia.
- Las adyacencias sean correctas.
- No creen comunicación entre espacios que deban estar separados.
- No alteren huecos o sombras relevantes.
- El motor acepte la geometría sin reparación manual.

La inspección visual se acompañará de tablas de áreas y volúmenes.

## 6. Aristas cortas

Las aristas cortas aparecen por capturas imprecisas, uniones, perfiles editados o intersecciones. Pueden generar polígonos degenerados o superficies demasiado pequeñas para la resolución analítica.

Procedimiento:

1. Localizar segmentos muy pequeños en plantas y secciones.
2. Determinar si representan una forma real relevante.
3. Alinear o simplificar el contorno.
4. Evitar vértices casi coincidentes.
5. Regenerar el modelo y comparar áreas.

No se establece una longitud mínima fija para todos los flujos; se obtendrá mediante el modelo de ensayo.

## 7. Ángulos agudos y entrantes estrechos

Los ángulos próximos a cero pueden producir caras en forma de cuña, difíciles de teselar o emparejar con la superficie adyacente.

Opciones:

- Sustituir el vértice por un pequeño tramo recto controlado.
- Unificar caras con la misma construcción y orientación aproximada.
- Dividir el recinto en una zona geométricamente estable.
- Reconstruir la superficie en el receptor.

La simplificación debe conservar área y orientación solar de forma suficiente.

## 8. Caras coplanares y casi coplanares

Dos elementos ocupando el mismo plano pueden competir como límite del espacio. Una separación mínima no intencionada puede crear una cámara estrecha.

Casos frecuentes:

- Revestimiento modelado como muro independiente sobre el cerramiento.
- Duplicado entre archivo anfitrión y vínculo.
- Estado existente y reformado visibles simultáneamente.
- Panel opaco superpuesto a un muro cortina.
- Forjado estructural y arquitectónico duplicados.

Debe conservarse un único límite analítico o documentarse expresamente la cámara.

## 9. Solapes entre elementos

Pequeños solapes constructivos pueden ser admisibles, pero los grandes solapes pueden crear superficies interiores, sombras o volúmenes residuales.

Se revisarán:

- Muro con muro.
- Muro con pilar.
- Muro con suelo.
- Muro con cubierta.
- Cubierta con cubierta.
- Hueco con borde de anfitrión.

La herramienta **Unir geometría** puede mejorar la representación física, pero su efecto sobre IFC y límites espaciales debe comprobarse. No es una reparación universal.

## 10. Elementos duplicados

Los duplicados son de riesgo alto porque pueden producir áreas dobles sin ser evidentes en una vista sombreada.

Orígenes habituales:

- Copia accidental.
- Dos disciplinas modelando el mismo cerramiento.
- Vínculo y copia local.
- Grupos superpuestos.
- Opciones de diseño visibles a la vez.
- Fases mal filtradas.

Controles:

- Advertencias de Revit.
- Tablas por posición, tipo y área.
- Selección mediante filtros.
- Revisión de identificadores IFC.
- Comparación del recuento antes y después de exportar.

## 11. Muros inclinados

Autodesk advierte de posibles resultados analíticos inexactos con muros inclinados. Deben ensayarse por separado.

Comprobar:

- Volumen del espacio.
- Área interior y exterior.
- Unión con suelo y cubierta.
- Posición de huecos.
- Teselado IFC.
- Clasificación de sombras exteriores.

Si el receptor no conserva la geometría, puede utilizarse una superficie plana equivalente con inclinación y área correctas.

## 12. Muros curvos y elípticos

Los motores suelen representar superficies curvas mediante facetas planas. El número de facetas afecta al área, orientación solar, tamaño del archivo y estabilidad.

Se registrará:

- Radio o ejes de la curva.
- Longitud y altura.
- Número de facetas en IFC y receptor.
- Diferencia de área.
- Distribución de orientaciones.
- Tratamiento de ventanas.

Las paredes elípticas requieren especial cautela por la advertencia de Autodesk. Una aproximación poligonal controlada puede ser más estable que una curva exportada automáticamente.

## 13. Superficies de doble curvatura

Las superficies alabeadas, regladas o libres no pueden representarse como una única cara plana analítica.

Estrategias:

- Facetado con tamaño máximo controlado.
- Sustitución por varios planos dominantes.
- Modelo de masas simplificado.
- Reconstrucción manual en el receptor.

El facetado se aprobará mediante un estudio de convergencia: aumentar el número de caras hasta que área y efecto solar dejen de variar materialmente.

## 14. Cubiertas complejas

Son de riesgo:

- Cubiertas con numerosos faldones pequeños.
- Limahoyas muy próximas.
- Cambios de pendiente mínimos.
- Buhardillas y huecos tangentes.
- Cubiertas por cara sobre masas complejas.
- Varias cubiertas solapadas.

Se simplificarán faldones que compartan construcción y una orientación casi idéntica, siempre que no cambien volumen, sombra o drenaje relevante para el análisis.

La comprobación debe incluir el volumen bajo cubierta y las uniones con todos los muros.

## 15. Perfiles editados

Los perfiles editados pueden dejar contornos abiertos desde el punto de vista analítico. Autodesk distingue su comportamiento del de las herramientas nativas de abertura.

Riesgos:

- Hueco no identificado como abertura.
- Cara de espacio abierta.
- Segmentos residuales.
- Pérdida de anfitrión.
- Forma diferente tras exportar.

Se preferirán huecos o familias anfitrionadas para aberturas funcionales, reservando el perfil editado para el contorno exterior real del elemento.

## 16. Huecos tangentes o próximos a bordes

Una ventana que toca una esquina, un forjado u otro hueco puede dividir el cerramiento en fragmentos mínimos.

Debe verificarse:

- Distancia a cada borde.
- Franja opaca residual.
- Unión entre huecos contiguos.
- Área neta del cerramiento.
- Entidad de abertura IFC.

Cuando la franja no existe constructivamente, conviene remodelar el conjunto como sistema continuo en lugar de mantener una pieza residual artificial.

## 17. Recintos pequeños y estrechos

Armarios, patinillos, cámaras y conductos pueden estar por debajo de los umbrales analíticos o generar una gran cantidad de superficies.

Para cada recinto se decidirá:

- Integrarlo en el espacio adyacente.
- Mantenerlo como espacio no acondicionado.
- Representarlo como hueco o paso.
- Excluirlo del modelo energético.

La decisión dependerá de su efecto en volumen, transmisión y sistemas, no de que tenga nombre en los planos.

## 18. Volúmenes de altura reducida

Plénums, suelos técnicos y cámaras horizontales pueden convertirse en espacios analíticos independientes según su profundidad, configuración delimitadora y resolución.

Riesgos:

- Multiplicación de zonas innecesarias.
- Superficies paralelas muy próximas.
- Volumen asignado como acondicionado por error.
- Pérdida de la cámara al cambiar resolución.

Se definirá una estrategia común para todo el proyecto y se comprobará con las tablas de espacios analíticos.

## 19. Patinillos y huecos verticales

Un patinillo puede ser:

- Volumen no acondicionado.
- Abertura continua entre plantas.
- Conjunto de espacios separados por forjados.
- Conducto fuera del alcance geométrico.

No deben superponerse una habitación, una abertura de caja y varios huecos de forjado sin una decisión explícita. Se revisarán continuidad vertical, coronación, base y comunicación entre plantas.

## 20. Escaleras y rampas

Escaleras y rampas generan encuentros inclinados, huecos y volúmenes de forma irregular. Pueden producir bordes dentados en las superficies analíticas.

La geometría energética suele requerir:

- Definir el volumen del recinto de escalera.
- Controlar los huecos entre plantas.
- Decidir si la rampa o losa separa espacios.
- Simplificar peldaños y barandillas.
- Revisar caras inclinadas y adyacencias.

Los peldaños individuales no deben fragmentar el volumen analítico.

## 21. Atrios y dobles alturas

Los atrios combinan grandes volúmenes, huecos verticales, fachadas interiores y cubiertas complejas.

Se comprobará:

- Continuidad del espacio en altura.
- Plantas intermedias que invaden el volumen.
- Barandillas y pasarelas que no deben delimitarlo.
- Huecos de forjado.
- Cubierta o lucernarios.
- División térmica por alturas, si procede.

Una sola habitación arquitectónica puede no ser la zonificación térmica adecuada.

## 22. Dobles pieles y fachadas ventiladas

Las dobles pieles crean dos superficies próximas y una cámara intermedia. Son de riesgo alto porque pueden confundirse con elementos duplicados o desaparecer por la resolución.

Antes de modelarlas geométricamente debe decidirse si el motor las representa como:

- Construcción multicapa equivalente.
- Cámara no ventilada dentro del cerramiento.
- Cámara ventilada mediante propiedad específica.
- Zona térmica independiente.
- Dos cerramientos y flujo de aire modelado.

No se debe crear una zona estrecha únicamente porque existe espacio geométrico entre dos pieles.

## 23. Pilares y elementos embebidos

Pilares, vigas y nichos dentro de cerramientos pueden fragmentar caras. Se conservarán explícitamente solo si cambian de forma relevante:

- Área útil o volumen.
- Construcción térmica.
- Sombra.
- Continuidad de la envolvente.

En otros casos se integrarán en una construcción equivalente o se impedirán límites espaciales innecesarios.

## 24. Piezas, ensamblajes y capas separadas

Dividir un anfitrión en piezas puede exportar varias caras coincidentes. Modelar cada capa como elemento separado puede crear cámaras y duplicidades.

Se preferirá la estructura compuesta nativa mientras el receptor no demuestre una interpretación fiable de piezas y capas independientes.

Si se utilizan:

- Exportar un caso mínimo.
- Contar entidades.
- Revisar superficies de límite.
- Verificar que el receptor no suma espesores o áreas dos veces.
- Documentar la configuración de exportación.

## 25. Familias in situ y modelos genéricos

Autodesk identifica como posible causa de fallo que elementos arquitectónicos importados desde IFC se conviertan en familias in situ no utilizadas para generar el modelo energético.

Por tanto, una categoría visualmente apropiada no garantiza participación analítica. Las familias in situ deben:

- Tener una función justificada.
- Cortar o delimitar de forma comprobada.
- Exportarse con entidad IFC controlada.
- Superar el ensayo en los receptores.

Si representan envolvente principal, se recomienda sustituirlas por anfitriones nativos cuando sea viable.

## 26. Geometría importada y mallas

Las mallas de levantamientos, conversiones IFC, SAT o 3DM pueden contener:

- Caras no manifold.
- Normales invertidas.
- Autointersecciones.
- Triángulos degenerados.
- Huecos.
- Duplicados.
- Cantidad excesiva de polígonos.

No se utilizarán directamente como envolvente analítica sin reparación y prueba. Se reconstruirá una geometría nativa o simplificada cuando sea posible.

## 27. Coordenadas alejadas y precisión numérica

Una geometría situada muy lejos del origen interno puede sufrir problemas de visualización, precisión o teselado.

Se mantendrá la geometría de trabajo cerca del origen interno, utilizando coordenadas compartidas para georreferenciación. Se comprobarán:

- Distancias al origen interno.
- Unidades del vínculo o importación.
- Transformaciones acumuladas.
- Posición del IFC en el visor y receptor.

No se moverá el edificio de forma improvisada para corregir una exportación sin documentar el sistema de coordenadas.

## 28. Fases, opciones, grupos y vínculos

La complejidad lógica puede convertirse en duplicidad geométrica.

Revisar:

- Fase de creación y demolición.
- Opción primaria.
- Instancias de grupo coincidentes.
- Vínculos cargados varias veces.
- Copias para alternativas fuera de opciones.
- Elementos monitorizados y duplicados localmente.

El archivo de exportación debe representar un único estado físico coherente.

## 29. Señales en el modelo analítico

Autodesk recomienda revisar vistas y tablas de espacios y superficies analíticas. Son señales de incidencia:

- Espacio inesperadamente grande o pequeño.
- Área o volumen distintos de lo previsto.
- Superficie extremadamente pequeña.
- Tipo de superficie incorrecto.
- Sombra situada dentro del edificio.
- Hueco sin superficie anfitriona.
- Superficie exterior donde debe existir adyacencia.
- Ausencia de un cerramiento completo.

Los pequeños bordes dentados aislados no deben confundirse con estos fallos funcionales.

## 30. Método de aislamiento de errores

Cuando falle la generación o importación:

1. Guardar una copia de diagnóstico.
2. Confirmar fase, modo y elementos delimitadores.
3. Aislar el edificio por sectores mediante vistas o copias parciales.
4. Identificar el sector mínimo que reproduce el fallo.
5. Ocultar o sustituir categorías por grupos.
6. Localizar el elemento o encuentro causante.
7. Crear una versión geométrica simplificada.
8. Regenerar y comparar.
9. Registrar causa, solución y alcance.

No deben realizarse correcciones masivas sin identificar qué condición resolvió el problema.

## 31. Ensayo de convergencia geométrica

Para curvas, fachadas facetadas o sombras complejas se crearán varios niveles:

- Modelo simplificado.
- Modelo intermedio.
- Modelo detallado.

Se compararán:

- Área y volumen.
- Número de superficies.
- Tamaño del IFC.
- Tiempo de generación e importación.
- Resultados energéticos sensibles.

Se elegirá el nivel a partir del cual aumentar el detalle deja de producir una mejora significativa.

## 32. Registro de incidencias

Cada geometría de riesgo dispondrá de:

- Código de incidencia.
- Captura o localización.
- Elementos Revit implicados.
- Síntoma en Revit.
- Síntoma en IFC.
- Síntoma en cada receptor.
- Causa confirmada o hipótesis.
- Solución aplicada.
- Diferencia antes y después.
- Versión de software.
- Estado de cierre.

Este registro alimentará posteriormente el árbol de diagnóstico general.

## 33. Vistas y tablas de control

Se prepararán:

- Vista 3D de aristas y encuentros.
- Vista de elementos duplicados o solapados.
- Secciones de cubiertas, cámaras y dobles pieles.
- Vista aislada de curvas y muros inclinados.
- Tabla de espacios analíticos ordenada por área y volumen.
- Tabla de superficies analíticas ordenada por área.
- Vista de sombras inesperadas.
- Vista de vínculos, fases y opciones.

Ordenar las tablas de menor a mayor ayuda a localizar superficies degeneradas y espacios residuales.

## 34. Comparaciones cuantitativas

Como mínimo se compararán:

| Magnitud | Revit físico | Revit analítico | IFC | Receptor |
|---|---:|---:|---:|---:|
| Número de espacios | Sí | Sí | Sí | Sí |
| Área útil total | Sí | Sí | Si está disponible | Sí |
| Volumen total | Sí | Sí | Si está disponible | Sí |
| Área de envolvente | Sí | Sí | Sí | Sí |
| Área de huecos | Sí | Sí | Sí | Sí |
| Número de superficies | No siempre | Sí | Sí | Sí |

Las diferencias se analizarán por planta, orientación, tipo de cerramiento y espacio, no solo mediante totales globales.

## 35. Criterios de aceptación

Una geometría de riesgo podrá incorporarse cuando:

- Su función energética esté definida.
- Genere espacios y superficies válidos.
- No introduzca duplicidades ni adyacencias falsas.
- Sus áreas y volúmenes cumplan la tolerancia.
- El facetado o simplificación esté controlado.
- El IFC sea válido y manejable.
- Los receptores produzcan una interpretación coherente.
- El resultado sea estable al actualizar.
- Las limitaciones estén documentadas.

Si no cumple estas condiciones, se utilizará una representación analítica alternativa.

## 36. Checklist de entrega

- [ ] Se han identificado zonas con aristas cortas o ángulos agudos.
- [ ] No existen elementos duplicados ni grandes solapes.
- [ ] Las caras casi coplanares tienen una estrategia explícita.
- [ ] Muros inclinados, curvos y elípticos han sido ensayados.
- [ ] Las superficies de doble curvatura están facetadas o simplificadas.
- [ ] Las cubiertas complejas conservan volumen y continuidad.
- [ ] Los perfiles editados no sustituyen aberturas funcionales.
- [ ] Los huecos próximos a bordes no generan fragmentos residuales.
- [ ] Recintos pequeños, plénums y patinillos siguen criterios comunes.
- [ ] Escaleras, rampas y atrios están revisados en sección.
- [ ] Dobles pieles y cámaras responden al modelo térmico previsto.
- [ ] Piezas, capas separadas y familias in situ han superado pruebas.
- [ ] Mallas e importaciones no se usan sin simplificación validada.
- [ ] Coordenadas y unidades son estables.
- [ ] Fases, opciones, grupos y vínculos no duplican geometría.
- [ ] Las tablas analíticas no contienen valores anómalos sin justificar.
- [ ] El IFC y los receptores cumplen los criterios de aceptación.

## 37. Modelo de ensayo para Revit 2026

El banco de pruebas incluirá:

- Muro con arista corta y ángulo agudo.
- Dos muros casi coplanares.
- Elemento duplicado.
- Muro inclinado.
- Muro circular y elíptico.
- Superficie de doble curvatura facetada.
- Cubierta con múltiples faldones.
- Hueco tangente a una esquina.
- Patinillo estrecho.
- Plénum de poca altura.
- Escalera y rampa.
- Atrio de varias plantas.
- Doble piel con cámara.
- Familia in situ de cerramiento.
- Malla importada simplificada.
- Copia situada lejos del origen para ensayo de precisión.

Cada caso tendrá una variante original y otra corregida o simplificada. Se documentará el comportamiento en Revit, IFC, Open BIM Analytical Model, CYPETHERM HE Plus y TK-IFC/TK-CEEP.

## 38. Fuentes principales

- Autodesk, *Energy Analytical Model Contains Gaps and Jagged Edges*, Revit 2026.
- Autodesk, *Energy Analytical Model Creation Failure*, Revit 2026.
- Autodesk, *Analytical Space Resolution*, Revit 2026.
- Autodesk, *Analytical Surface Resolution*.
- Autodesk, *Understanding the Energy Analytical Model*.
- Autodesk, *About Surfaces in the Energy Analytical Model*.
- Autodesk, *About Creating Energy Analytical Models from Architectural Elements*, Revit 2026.
