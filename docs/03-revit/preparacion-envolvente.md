---
title: Preparación de la envolvente térmica en Revit 2026
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
software:
  nombre: Autodesk Revit
  version_base: "2026"
---

# Preparación de la envolvente térmica en Revit 2026

La envolvente térmica debe modelarse como un conjunto continuo de elementos que separan recintos con condiciones distintas: interior y exterior, acondicionado y no acondicionado, edificio y terreno, o dos zonas térmicas. Su misión en este flujo no es reproducir cada detalle constructivo, sino permitir que el receptor reconstruya superficies, adyacencias y construcciones sin ambigüedad.

Este capítulo se ocupa de la geometría opaca: muros, suelos, cubiertas, techos y sus encuentros. Los huecos, los elementos transparentes y los muros cortina se desarrollan en el capítulo siguiente.

!!! warning "La envolvente arquitectónica no equivale automáticamente a la térmica"
    Un cerramiento puede pertenecer a la fachada arquitectónica y no limitar un espacio acondicionado, o puede existir una frontera térmica interior que no se perciba como fachada. La clasificación debe responder al modelo energético, no solo a la apariencia del edificio.

## 1. Objetivos de preparación

El modelo debe permitir determinar, para cada superficie:

- Qué espacio limita a cada lado.
- Si la cara opuesta corresponde a exterior, terreno u otro espacio.
- Qué elemento constructivo la representa.
- Su orientación, inclinación y área.
- La continuidad de su perímetro.
- Las aberturas que contiene.
- La fase y alternativa de diseño a las que pertenece.

La comprobación debe realizarse sobre el resultado exportado y no únicamente sobre las vistas de Revit.

## 2. Dos interpretaciones que deben verificarse

### 2.1 Modelo analítico generado por Revit

Revit puede obtener espacios y superficies analíticas directamente de los elementos arquitectónicos. Autodesk indica que muros, suelos, cubiertas, techos y otros elementos delimitadores intervienen cuando corresponde su condición `Room Bounding`.

Este proceso admite pequeños solapes y discontinuidades en función de la resolución analítica. Esa tolerancia facilita la generación, pero no convierte una geometría deficiente en un modelo fiable.

### 2.2 Geometría IFC reconstruida por la aplicación receptora

Open BIM Analytical Model, CYPETHERM y TeKton3D pueden interpretar el IFC mediante reglas propias. La coincidencia con el modelo analítico nativo de Revit no debe suponerse.

Por ello se conservarán dos controles diferenciados:

1. Revisión de habitaciones, espacios y volúmenes en Revit.
2. Revisión de superficies y adyacencias después de la importación o generación en la aplicación receptora.

## 3. Definición previa de la envolvente térmica

Antes de corregir geometría debe prepararse un esquema por plantas y secciones que identifique:

- Recintos acondicionados.
- Recintos no acondicionados.
- Espacios exteriores.
- Cerramientos en contacto con el terreno.
- Medianerías.
- Particiones entre zonas térmicas.
- Elementos en contacto con otros edificios.
- Cámaras, plénums y espacios bajo cubierta.

Sin esta decisión previa no puede establecerse si un elemento debe actuar como límite espacial ni cómo clasificarlo posteriormente.

## 4. Principios generales de modelado

### 4.1 Un elemento anfitrión reconocible

Siempre que sea posible, cada cerramiento principal se representará mediante su categoría nativa:

| Función | Categoría recomendada en Revit |
|---|---|
| Cerramiento vertical | Muro |
| Forjado o solera | Suelo |
| Cerramiento superior | Cubierta |
| Falso techo delimitador | Techo |
| Terreno | Toposólido, con ensayo específico del receptor |

Los modelos genéricos, familias in situ y masas solo se emplearán cuando la geometría no pueda resolverse de forma estable con categorías nativas y se haya comprobado su exportación.

### 4.2 Continuidad analítica

Los elementos deben encontrarse de forma inequívoca en esquinas, cambios de nivel y encuentros muro-forjado-cubierta. Se evitarán:

- Huecos visibles entre anfitriones.
- Solapes de gran dimensión.
- Cerramientos duplicados.
- Caras casi coplanares que compitan entre sí.
- Fragmentos residuales después de reformas.
- Elementos de fases incompatibles ocupando el mismo lugar.

### 4.3 Sencillez proporcional al cálculo

Se modelará la forma que cambie áreas, orientación, volumen, sombras o adyacencias. Los detalles que no alteren estas magnitudes deben simplificarse.

No suelen requerir geometría energética independiente:

- Rodapiés y molduras.
- Juntas y perfiles menores.
- Capas de acabado modeladas como piezas independientes.
- Pequeños resaltos decorativos.
- Sellados, remates y fijaciones.

## 5. Muros exteriores

### 5.1 Trazado y ubicación

Los muros se dibujarán con una línea de ubicación coherente en todo el proyecto. Cambiar entre eje, cara de acabado y cara de núcleo sin criterio puede producir desfases en encuentros y alterar áreas netas.

La elección no tiene que ser idéntica en todos los proyectos, pero debe:

- Estar documentada.
- Facilitar la coordinación con estructura.
- Mantener la continuidad de la cara que limita el espacio.
- Evitar reajustes improvisados durante la exportación.

### 5.2 Restricciones verticales

Cada muro debe tener base y coronación controladas mediante niveles, desfases o unión a otros elementos. Se evitarán alturas libres arbitrarias cuando exista un nivel o una cubierta que represente el límite real.

Revisar para cada tipo de cerramiento:

- Restricción de base.
- Desfase de base.
- Restricción superior o altura no conectada.
- Desfase superior.
- Unión superior o inferior a cubierta, suelo o plano de referencia.

### 5.3 Unión a cubiertas y forjados

La herramienta **Unir parte superior/base** permite adaptar el muro a una cubierta, un suelo, un techo, un plano de referencia u otro muro compatible. Es preferible a editar manualmente el perfil cuando el límite debe responder a cambios posteriores.

Después de unir se comprobará en sección:

- Que no queda una franja abierta bajo la cubierta.
- Que el muro no atraviesa innecesariamente el volumen superior.
- Que la unión cubre toda la longitud prevista.
- Que los extremos del muro también quedan resueltos.

### 5.4 Muros inclinados y curvos

Autodesk advierte de posibles resultados inexactos con muros inclinados o elípticos en determinados procesos analíticos. No deben sustituirse automáticamente por muros verticales, pero sí ensayarse de forma explícita.

Para cada caso complejo se registrará:

- Área en Revit.
- Teselado o subdivisión en IFC.
- Superficies resultantes en el receptor.
- Diferencia de área aceptada.
- Efecto sobre huecos y sombras.

### 5.5 Perfiles editados

Un perfil editado puede representar correctamente una fachada escalonada o inclinada, pero su comportamiento analítico no es idéntico al de una abertura nativa. Autodesk señala que una abertura creada con herramientas de hueco puede generar una superficie analítica de apertura de aire, mientras que un perfil editado se interpreta como borde abierto.

Se preferirán herramientas semánticas de abertura cuando la discontinuidad tenga esa función. Los perfiles editados se reservarán para la forma real del contorno del elemento.

### 5.6 Muros apilados, piezas y capas independientes

Los muros apilados, las piezas y las capas modeladas por separado añaden relaciones que no todos los exportadores reconstruyen igual. Antes de incorporarlos al flujo estable se verificará:

- Categoría y tipo IFC de cada componente.
- Conservación del anfitrión.
- Ausencia de superficies térmicas duplicadas.
- Continuidad de los límites espaciales.
- Capacidad del receptor para reagrupar o simplificar.

Si no aportan una ventaja analítica demostrable, se preferirá un muro compuesto convencional.

## 6. Muros interiores y fronteras térmicas

No todos los tabiques necesitan convertirse en superficies de intercambio diferenciadas. Su tratamiento dependerá de la zonificación:

- Entre dos espacios de la misma zona térmica pueden simplificarse en el modelo energético, según el receptor.
- Entre zonas térmicas distintas deben conservar una adyacencia correcta.
- Entre un espacio acondicionado y otro no acondicionado forman parte de la envolvente térmica.
- Un tabique que no alcanza el límite superior puede no separar completamente los volúmenes.

El parámetro `Room Bounding` se desactivará únicamente cuando se haya decidido que el elemento no debe dividir el volumen. No se usará como reparación general de habitaciones mal cerradas.

## 7. Estructuras compuestas y materiales

### 7.1 Orden de capas

En Revit, las estructuras compuestas organizan las capas de exterior a interior en muros y de arriba abajo en suelos, cubiertas y techos. Cada capa dispone de material, espesor y función.

Se comprobará:

- Orden correcto de las capas.
- Espesores no nulos salvo membranas.
- Material específico en cada capa relevante.
- Límites del núcleo coherentes.
- Función adecuada: estructura, sustrato, aislamiento/cámara, membrana o acabado.

### 7.2 Función y prioridad

La función controla cómo se resuelven las uniones de capas. Una asignación incorrecta puede producir encuentros gráficos y geométricos incoherentes, aunque la suma de espesores sea correcta.

La función **Thermal/Air Layer** identifica capas de aislamiento o control de aire dentro de la estructura de Revit, pero no sustituye la comprobación de propiedades térmicas ni garantiza el mapeado en el motor receptor.

### 7.3 Propiedades térmicas de materiales

Los materiales pueden contener activos térmicos que intervienen en la resistencia y masa térmica calculadas por Revit. Deben diferenciarse tres niveles de información:

1. **Geometría:** espesor y posición de las capas.
2. **Información térmica en Revit:** conductividad, densidad, calor específico y propiedades derivadas.
3. **Construcción en el motor de cálculo:** solución constructiva finalmente asignada y validada según el procedimiento reglamentario.

No se asumirá que los niveles 2 y 3 son equivalentes. En los flujos CYPE y TeKton3D se documentará qué propiedades se transfieren realmente y cuáles deben reasignarse.

### 7.4 Nombres y códigos de tipo

Los tipos deben poder identificarse fuera de Revit. Se recomienda una codificación estable, por ejemplo:

- `ENV-MUR-EXT-01`: muro exterior principal.
- `ENV-CUB-EXT-01`: cubierta exterior.
- `ENV-SOL-TER-01`: solera en contacto con terreno.
- `ENV-PAR-NAC-01`: partición con espacio no acondicionado.

El nombre no debe ser la única fuente de clasificación; se acompañará de parámetros compartidos en el capítulo de mapeado IFC.

## 8. Suelos, forjados y soleras

### 8.1 Función energética

Antes de modelar un suelo debe identificarse si separa:

- Un recinto y el terreno.
- Un recinto y el exterior.
- Dos plantas acondicionadas.
- Un recinto acondicionado y otro no acondicionado.
- Dos zonas térmicas diferentes.

La clasificación no puede deducirse únicamente del tipo constructivo.

### 8.2 Perímetro y encuentros

El croquis del suelo debe coincidir de manera controlada con los cerramientos verticales. Se evitarán pequeños entrantes, segmentos duplicados y aristas muy cortas originadas por capturas imprecisas.

En sección se comprobará si la referencia se ha tomado a:

- Cara interior del muro.
- Cara exterior.
- Eje.
- Límite del núcleo.

La regla elegida debe producir una envolvente sin huecos ni solapes significativos y mantenerse en todas las plantas.

### 8.3 Forjados entre plantas

Un forjado puede separar dos espacios superpuestos. Deben revisarse simultáneamente:

- Límite superior del espacio inferior.
- Límite inferior del espacio superior.
- Espesor y cota del forjado.
- Falsos techos y cámaras intermedias.
- Huecos de escalera, ascensor e instalaciones.

No deben quedar volúmenes sin asignar por confundir la cara superior, la cara inferior o el nivel de referencia.

### 8.4 Soleras y terreno

El contacto con el terreno requiere una clasificación específica en el motor de cálculo. La presencia de un toposólido no garantiza que el receptor deduzca correctamente el contacto.

Se recomienda:

- Modelar la solera con geometría continua.
- Identificar su cota respecto al terreno.
- Evitar que el terreno atraviese el volumen interior.
- Registrar los tramos parcialmente enterrados.
- Comprobar y, si procede, reasignar la condición de contorno después de importar.

## 9. Cubiertas

### 9.1 Categoría y forma

Se utilizará una cubierta nativa siempre que sea posible. Tanto las cubiertas por perímetro como las creadas por extrusión deben someterse a una prueba de exportación cuando tengan geometría compleja.

Se comprobarán:

- Contorno exterior.
- Pendientes y limatesas.
- Encuentros entre faldones.
- Aleros.
- Huecos y buhardillas.
- Espesor y posición respecto a los muros.

### 9.2 Cubierta sobre espacio habitable

Si la cubierta limita directamente el recinto, la habitación o espacio debe alcanzar su intradós de forma correcta. La unión de los muros a la cubierta y el cálculo de volumen deben revisarse en varias secciones.

### 9.3 Cubierta con cámara o espacio bajo cubierta

Cuando existe un ático o una cámara significativa, debe decidirse si se modela como espacio independiente. La decisión depende de su tamaño, ventilación, uso y tratamiento en el motor.

No debe asignarse automáticamente la cubierta al recinto inferior si entre ambos existe un volumen térmicamente relevante.

### 9.4 Aleros y partes exteriores

La parte de la cubierta que sobresale del volumen acondicionado puede actuar como sombra. Debe conservarse si su efecto solar es relevante, pero sin convertir el volumen bajo el alero en un espacio interior.

La separación entre superficie de transmisión y elemento de sombra se comprobará en el modelo analítico receptor.

## 10. Techos, falsos techos y plénums

Los techos pueden intervenir como elementos delimitadores y generar cámaras analíticas. Autodesk relaciona su tratamiento con la condición `Room Bounding`, la profundidad del vacío y la resolución analítica.

Se adoptará una de estas estrategias de forma explícita:

| Situación | Estrategia candidata |
|---|---|
| Falso techo sin relevancia térmica propia | No dividir el volumen |
| Plénum relevante | Crear y controlar un espacio independiente |
| Techo que separa zonas con condiciones distintas | Mantenerlo como frontera |

No se dejará que una configuración accidental de `Room Bounding` decida la zonificación.

## 11. Encuentros críticos

### 11.1 Esquinas de muros

Revisar en planta y en 3D:

- Extremos coincidentes.
- Tipo de unión.
- Prioridades de capas.
- Ausencia de muros duplicados.
- Continuidad del espacio interior.

### 11.2 Muro-forjado

Comprobar si el forjado llega al eje, al núcleo o a una cara del muro. Un solape constructivo razonable puede ser admisible; una banda abierta o una duplicación de cerramientos no lo es.

### 11.3 Muro-cubierta

Verificar en al menos dos secciones por faldón y en los cambios de pendiente. Las vistas en planta no permiten detectar todos los huecos verticales.

### 11.4 Cambios de espesor

Cuando dos tipos de muro se suceden, sus caras analíticas deben mantener continuidad. Se evitarán pequeños escalones involuntarios debidos a líneas de ubicación diferentes.

### 11.5 Encuentros con pilares

Los pilares interiores pueden fragmentar límites o reducir volúmenes según su tamaño y configuración. Se decidirá si deben delimitar el espacio y se comprobará el resultado, en lugar de aplicar una regla general a toda la categoría.

## 12. Cerramientos parcialmente enterrados

En edificios sobre ladera, un mismo muro puede tener una parte exterior y otra en contacto con terreno. Esta condición suele requerir dividir la superficie en el modelo energético.

Opciones a ensayar:

- Dividir el muro en elementos por altura o tramo.
- Conservar un único muro y subdividir la superficie en la aplicación analítica.
- Asignar condiciones de contorno manualmente después de importar.

La opción elegida debe evitar geometría redundante y permitir conservar la trazabilidad entre Revit, IFC y cálculo.

## 13. Medianerías y contacto con otros edificios

Una medianería no se clasificará automáticamente como muro exterior. Debe identificarse si limita con:

- Otro edificio conocido.
- Un espacio no modelado.
- Exterior.
- Un recinto de condiciones equivalentes.

Cuando el edificio colindante no forme parte del modelo, se documentará la condición de contorno que debe aplicarse en el motor. No es necesario modelarlo por completo salvo que sea preciso para sombras o para la geometría del contacto.

## 14. Reformas, fases y demolición

La envolvente exportada debe pertenecer a una fase coherente. Antes de exportar se revisará:

- Fase de creación.
- Fase de demolición.
- Fase de habitaciones o espacios.
- Filtro de fase de la vista de exportación.
- Existencia simultánea de cerramientos nuevo y demolido.

En rehabilitación conviene conservar estados de cálculo independientes para situación inicial y reformada, con exportaciones y registros diferenciados.

## 15. Vínculos y modelos federados

Cuando la estructura o parte de la envolvente se encuentra en un vínculo:

- Activar `Room Bounding` en el vínculo solo si sus elementos deben delimitar espacios.
- Verificar coordenadas, fase y opción visibles.
- Evitar duplicar en el archivo anfitrión los elementos ya presentes en el vínculo.
- Comprobar si el exportador incluye el vínculo y cómo conserva los identificadores.
- Realizar una prueba mínima antes de adoptar el flujo para todo el proyecto.

Una envolvente repartida entre varios archivos aumenta el riesgo de huecos y duplicidades en los encuentros.

## 16. Elementos que no deben contaminar la envolvente

Debe revisarse la condición delimitadora de objetos que se modelan con categorías capaces de intervenir en el análisis pero no representan cerramientos térmicos:

- Muros de urbanización.
- Petos y pretiles.
- Pavimentos exteriores.
- Cubiertas decorativas.
- Marquesinas.
- Muretes interiores bajos.
- Piezas auxiliares y revestimientos.
- Elementos provisionales.

Estos objetos pueden mantenerse para coordinación o sombras, pero deben aislarse de la generación de volúmenes cuando corresponda.

## 17. Tolerancias y resolución analítica

La resolución espacial analítica de Revit define el tamaño mínimo de discontinuidad que el algoritmo puede ignorar. Autodesk documenta para 2026 un valor predeterminado de 457,2 mm, un mínimo de 152,4 mm y una zona intermedia de comportamiento no determinista hasta dos veces la resolución.

Estas cifras pertenecen al generador analítico de Revit y **no deben trasladarse como tolerancias universales a IFC, CYPE o TeKton3D**.

Reglas de uso:

1. Corregir primero omisiones y huecos evidentes.
2. Generar el modelo con valores de referencia.
3. Revisar espacios y superficies.
4. Reducir la resolución de forma gradual si faltan detalles relevantes.
5. Registrar el valor utilizado y el tiempo de proceso.
6. Repetir la comprobación en el receptor IFC.

Una resolución menor no garantiza por sí sola un resultado mejor y puede revelar discontinuidades antes ignoradas.

## 18. Clasificación geométrica mínima

Antes de exportar, cada tipo de elemento de envolvente debe poder asociarse con una función energética:

| Código funcional | Descripción |
|---|---|
| `EXT-AIR` | Cerramiento en contacto con aire exterior |
| `GROUND` | Cerramiento en contacto con terreno |
| `INT-ZONE` | Partición entre zonas térmicas |
| `INT-UNCOND` | Separación con recinto no acondicionado |
| `ADIABATIC` | Condición sin intercambio, cuando proceda |
| `PARTY` | Medianería o contacto con edificio colindante |
| `SHADE` | Elemento exterior considerado solo como sombra |

Esta tabla es una convención editorial inicial. Los nombres definitivos de parámetros y el mapeado IFC se establecerán en el capítulo correspondiente.

## 19. Vistas de control en Revit

Se recomienda crear un conjunto específico de vistas:

### 19.1 Vista 3D `QA_ENV_01_CIERRE`

Mostrar exclusivamente:

- Muros.
- Suelos.
- Cubiertas.
- Techos relevantes.
- Habitaciones o espacios.

Aplicar sección de caja y revisar el edificio desde exterior, interior, arriba y abajo.

### 19.2 Secciones `QA_ENV_SEC`

Crear secciones en:

- Cada tipología de cubierta.
- Cambios de nivel.
- Fachadas escalonadas.
- Plantas enterradas.
- Patios y atrios.
- Dobles alturas.

### 19.3 Plantas `QA_ENV_PLANTA`

Utilizar detalle medio o fino para comprobar capas, líneas de ubicación, encuentros y contornos de suelos.

### 19.4 Tabla de cerramientos

Incluir al menos:

- Identificador.
- Categoría y tipo.
- Nivel.
- Fase.
- `Room Bounding` cuando esté disponible.
- Área y volumen pertinentes.
- Código funcional energético.
- Estado de revisión.

## 20. Procedimiento de preparación

1. Delimitar recintos acondicionados y no acondicionados.
2. Dibujar la envolvente térmica prevista en plantas y secciones.
3. Identificar los elementos Revit que representan cada frontera.
4. Corregir categorías impropias y duplicidades.
5. Revisar restricciones, uniones y perfiles.
6. Comprobar capas, materiales y nomenclatura.
7. Revisar habitaciones o espacios con cálculo de volumen activo.
8. Inspeccionar vistas 3D, plantas y secciones de control.
9. Generar el modelo analítico de Revit como diagnóstico auxiliar.
10. Exportar un IFC de prueba.
11. Revisar superficies y adyacencias en el receptor.
12. Registrar incidencias y repetir hasta cumplir los criterios de aceptación.

## 21. Criterios de aceptación

La envolvente estará preparada cuando:

- Todos los volúmenes de cálculo estén delimitados.
- No falte ningún cerramiento principal.
- No existan elementos duplicados que generen caras concurrentes.
- Los encuentros críticos estén revisados en sección.
- Los espacios no acondicionados relevantes estén representados.
- Las fronteras con terreno, exterior y otros espacios sean identificables.
- Las superficies del receptor mantengan adyacencias coherentes.
- Las diferencias de área estén dentro de la tolerancia definida para el proyecto.
- Las simplificaciones estén registradas.
- El IFC de ensayo pueda reproducirse con la misma configuración.

## 22. Checklist de entrega

- [ ] Se ha definido gráficamente la envolvente térmica.
- [ ] Muros, suelos y cubiertas usan categorías nativas siempre que es viable.
- [ ] No existen cerramientos principales ausentes o duplicados.
- [ ] Los muros tienen restricciones verticales controladas.
- [ ] Las uniones muro-forjado y muro-cubierta están revisadas.
- [ ] Los perfiles editados y aberturas tienen una justificación.
- [ ] Los muros inclinados, curvos o elípticos se han ensayado.
- [ ] Las estructuras compuestas tienen capas, funciones y materiales coherentes.
- [ ] Se distinguen exterior, terreno, medianería y espacios no acondicionados.
- [ ] Falsos techos, cámaras y áticos siguen una estrategia explícita.
- [ ] Los elementos exteriores no deseados no delimitan espacios.
- [ ] Las fases y vínculos corresponden al estado de cálculo.
- [ ] Se ha revisado el modelo analítico de Revit.
- [ ] Se ha comprobado el IFC en la aplicación receptora.
- [ ] Se han registrado configuración, incidencias y tolerancias.

## 23. Ensayo de referencia para Revit 2026

El modelo de prueba de la guía incorporará:

- Un recinto rectangular con cerramiento convencional.
- Una cubierta inclinada con muros unidos.
- Un forjado entre dos plantas.
- Una solera en contacto con terreno.
- Un muro parcialmente enterrado.
- Un espacio no acondicionado bajo cubierta.
- Un falso techo con plénum.
- Un muro inclinado y otro curvo.
- Un elemento exterior que solo produzca sombra.
- Un hueco vertical entre plantas.

Para cada caso se compararán:

- Volumen y área en Revit.
- Entidades y geometría IFC.
- Superficies generadas en Open BIM Analytical Model.
- Interpretación en CYPETHERM HE Plus.
- Interpretación mediante TK-IFC/TK-CEEP.

## 24. Fuentes principales

- Autodesk, *About Creating Energy Analytical Models from Architectural Elements*, Revit 2026.
- Autodesk, *Prepare a Model for Analysis*, Revit 2026.
- Autodesk, *Analytical Space Resolution*, Revit 2026.
- Autodesk, *Attach Walls to Other Elements*, Revit 2026.
- Autodesk, *About Applying a Function and a Priority to a Layer of a Compound Structure*, Revit 2026.
- Autodesk, *Video: Editing Compound Structures*, Revit 2026.
- Autodesk, *Energy Settings*, Revit 2026.
