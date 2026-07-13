---
title: Huecos y elementos transparentes en Revit 2026
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
software:
  nombre: Autodesk Revit
  version_base: "2026"
---

# Huecos y elementos transparentes en Revit 2026

Los huecos condicionan las pérdidas térmicas, las ganancias solares, la iluminación natural y la infiltración. Para que el intercambio sea fiable no basta con que una ventana se vea correctamente: el hueco debe estar contenido en un cerramiento, conservar dimensiones y orientación, identificarse como puerta o ventana y recibir la construcción térmica adecuada en el motor de cálculo.

Este capítulo trata ventanas, puertas, lucernarios, muros cortina y aberturas sin carpintería. Los dispositivos de sombra se desarrollarán con mayor detalle en el capítulo siguiente.

!!! warning "Dimensión nominal, hueco bruto y vidrio no son la misma magnitud"
    El ancho y alto de una familia pueden describir el hueco de obra, el marco o la hoja. El motor energético puede necesitar el área total del hueco y, además, la fracción de marco o el área transparente. Estas magnitudes deben identificarse y verificarse, no deducirse solo del nombre del tipo.

## 1. Objetivos de preparación

Para cada hueco debe poder determinarse:

- Cerramiento anfitrión.
- Espacio al que pertenece.
- Condición de contorno del cerramiento.
- Categoría: ventana, puerta, lucernario o abertura.
- Ancho, alto, antepecho y cota de dintel.
- Forma y área bruta.
- Área transparente y área de marco, si el receptor las distingue.
- Orientación e inclinación.
- Construcción térmica y propiedades solares.
- Elementos de sombra asociados.
- Identificador estable para revisar actualizaciones.

## 2. Clasificación funcional

Antes de exportar se asignará cada elemento a una función energética:

| Clase | Ejemplos | Tratamiento esperado |
|---|---|---|
| Ventana exterior | Ventana practicable o fija | Hueco transparente en cerramiento exterior |
| Puerta exterior opaca | Puerta de acceso | Hueco opaco con construcción propia |
| Puerta exterior acristalada | Puerta con vidrio | Solución mixta o transparente según el receptor |
| Ventana interior | Hueco entre zonas | Superficie interior, si es relevante |
| Lucernario | Ventana en cubierta | Hueco inclinado u horizontal |
| Muro cortina | Fachada ligera | Paneles transparentes y opacos diferenciados |
| Abertura de aire | Paso sin carpintería | Comunicación entre espacios, no ventana |
| Hueco no analítico | Nicho o rebaje | No debe atravesar completamente el cerramiento |

La categoría de Revit constituye una primera pista, pero la función energética depende también del anfitrión y de los espacios a ambos lados.

## 3. Uso de categorías nativas

### 3.1 Ventanas

Las ventanas se modelarán preferentemente con familias de categoría **Ventanas** alojadas en un muro o, cuando proceda, en una cubierta. Autodesk las define como componentes anfitrionados y permite documentar dimensiones, materiales, operación IFC y propiedades analíticas de tipo.

Ventajas:

- El hueco queda relacionado con su anfitrión.
- La categoría se exporta de forma reconocible.
- Puede planificarse en tablas.
- Se conservan cotas de antepecho y dintel.
- Es posible asociar parámetros térmicos y códigos de tipo.

### 3.2 Puertas

Las puertas deben utilizar la categoría **Puertas**, incluso cuando incorporen vidrio. El parámetro de función interior/exterior ayuda a filtrar y revisar, pero no sustituye la comprobación de la condición real del muro anfitrión.

Una puerta acristalada no debe reclasificarse automáticamente como ventana. Debe ensayarse cómo la interpreta cada receptor y si permite separar la parte opaca de la transparente.

### 3.3 Aberturas sin carpintería

Los pasos de aire se modelarán como aberturas cuando representen una comunicación real entre volúmenes. Autodesk indica que las herramientas de abertura de cara, muro, vertical o caja de ascensor pueden producir superficies analíticas de tipo **Air Opening**.

No deben emplearse para representar una ventana sin familia, porque se perderían su identidad y sus propiedades térmicas.

### 3.4 Modelos genéricos y familias in situ

Se evitará representar ventanas mediante modelos genéricos que simplemente se solapan con el muro. Una geometría visible que no corta al anfitrión puede no generar ningún hueco analítico.

Su uso solo será admisible si:

- La categoría y el mapeado IFC están controlados.
- El vacío corta realmente al anfitrión.
- Se conservan dimensiones y propiedades.
- El resultado se ha comprobado en los tres flujos previstos.

## 4. Requisitos de las familias

### 4.1 Corte del anfitrión

La familia debe contener un vacío o una abertura que corte completamente el cerramiento anfitrión en todas las variantes del tipo.

Comprobar:

- Espesor mínimo y máximo de muro admitido.
- Cambio de tamaño del hueco al modificar ancho y alto.
- Corte en planta, alzado, sección y 3D.
- Comportamiento en muros curvos o inclinados.
- Ausencia de sólidos que cierren accidentalmente el hueco.

### 4.2 Planos de referencia y restricciones

El ancho, el alto, el antepecho y la posición del vidrio deben gobernarse mediante planos de referencia estables. Las restricciones no deben fallar al generar tamaños extremos.

Se ensayarán como mínimo:

- Tipo más pequeño.
- Tipo más grande.
- Muro anfitrión más delgado.
- Muro anfitrión más grueso.
- Inversión de orientación.

### 4.3 Geometría 3D frente a representación 2D

Las líneas simbólicas sirven para la documentación, pero no forman parte de la geometría tridimensional. El contorno energético no puede depender de líneas de alzado o planta.

Los herrajes, juntas y perfiles menores se representarán de forma simplificada o solo en 2D cuando no afecten al área del hueco ni a las sombras relevantes.

### 4.4 Subfamilias anidadas

Las hojas, vidrios y marcos anidados pueden ser útiles para documentación, pero añaden riesgo de exportar varios objetos superpuestos.

Se revisará si las subfamilias:

- Se comparten o permanecen integradas.
- Se exportan como entidades independientes.
- Duplican el vidrio o el marco.
- Conservan materiales y parámetros.
- Son necesarias para el cálculo.

Si el receptor solo necesita una abertura con propiedades globales, una familia analíticamente sencilla será más robusta.

## 5. Dimensiones que deben distinguirse

### 5.1 Hueco bruto

Es el área del recorte practicado en el anfitrión. Puede corresponder a los parámetros `Rough Width` y `Rough Height`, pero esto depende de la construcción de la familia.

### 5.2 Dimensión nominal

Es el ancho y alto utilizado para identificar el tipo. No se asumirá que coincide con el hueco bruto hasta verificarlo.

### 5.3 Área de marco

Incluye perfiles opacos, montantes, travesaños y, según el sistema, cajones o paneles ciegos. Puede representarse mediante una fracción de marco o mediante geometría separada.

### 5.4 Área transparente

Es la superficie efectiva de vidrio. Para obtenerla puede ser necesario:

- Calcularla a partir de parámetros de la familia.
- Medir la geometría del panel acristalado.
- Aplicar una fracción de marco en el receptor.
- Dividir una carpintería compleja en varios paños.

### 5.5 Criterio documental

Cada familia homologada incluirá una ficha con:

- Parámetro que controla ancho nominal.
- Parámetro que controla alto nominal.
- Dimensiones del hueco bruto.
- Regla de cálculo del área transparente.
- Regla de cálculo del marco.
- Límites de uso de la familia.

## 6. Posición y orientación

### 6.1 Antepecho y dintel

Las ventanas deben mantener cotas coherentes respecto al nivel. Se controlarán:

- Nivel.
- Altura de antepecho.
- Altura de cabeza o dintel.
- Desfase del anfitrión.
- Restricciones internas de la familia.

Las incoherencias entre estos valores pueden situar el hueco fuera del volumen de la habitación aunque sea visible en fachada.

### 6.2 Cara interior y exterior

La orientación de la familia debe coincidir con la del cerramiento. Una ventana invertida puede alterar:

- Posición del vidrio.
- Retranqueo.
- Elementos de sombra.
- Operación IFC.
- Asignación interior/exterior de materiales.

Se incluirá una comprobación de flechas de giro y orientación en las vistas de control.

### 6.3 Retranqueo

La posición del vidrio dentro del espesor del muro afecta a las sombras del propio hueco. Si el motor receptor reproduce mochetas o retranqueos, debe compararse su posición con Revit.

Si el receptor simplifica el hueco sobre el plano del cerramiento, se documentará la pérdida geométrica y se decidirá si requiere un elemento de sombra equivalente.

## 7. Huecos rectangulares y formas especiales

Los huecos rectangulares son los más interoperables. Las formas arqueadas, circulares, triangulares o poligonales deben ensayarse porque pueden:

- Teselarse en varios polígonos.
- Convertirse en un rectángulo equivalente.
- Perder parte del contorno.
- Generar superficies no válidas.
- Separarse del cerramiento anfitrión.

Para cada forma especial se compararán área, perímetro, posición y número de superficies antes de aprobarla.

La simplificación a un rectángulo equivalente solo será aceptable si conserva el área, la orientación y el efecto solar dentro de la tolerancia del proyecto.

## 8. Ventanas múltiples y conjuntos

Una carpintería compuesta puede representarse como:

- Una sola ventana con varios paños.
- Varias ventanas contiguas.
- Un sistema de muro cortina.
- Una ventana con subfamilias anidadas.

La elección debe responder al nivel de cálculo necesario.

Se preferirá una única entidad cuando todos los paños compartan construcción y el receptor aplique propiedades globales. Se separarán paños cuando cambien:

- Tipo de vidrio.
- Fracción de marco.
- Inclinación u orientación.
- Condición de sombra.
- Operación o permeabilidad relevante.
- Construcción térmica.

No deben quedar separaciones opacas ficticias entre ventanas contiguas ni huecos solapados.

## 9. Puertas opacas y acristaladas

### 9.1 Puertas exteriores opacas

Se identificarán como cerramientos opacos con transmitancia propia. Debe comprobarse que el receptor no les asigna por defecto propiedades de ventana.

### 9.2 Puertas parcialmente acristaladas

Existen tres estrategias:

1. Construcción equivalente global.
2. Puerta opaca más hueco acristalado independiente.
3. Elemento compuesto interpretado por el receptor.

La opción 2 ofrece mayor detalle, pero puede producir solapes o dobles huecos si la familia y el IFC no están preparados. Se escogerá mediante ensayo.

### 9.3 Puertas interiores

Solo requieren propiedades térmicas diferenciadas cuando separan zonas o recintos con condiciones distintas. Su existencia arquitectónica no implica que el modelo energético necesite simularlas de forma independiente.

## 10. Lucernarios y huecos en cubierta

Los lucernarios deben alojarse en la cubierta y conservar su inclinación. Se comprobará:

- Corte completo de la cubierta.
- Correspondencia con el espacio inferior.
- Orientación del plano de vidrio.
- Área bruta y transparente.
- Encuentro con petos o zócalos.
- Sombras producidas por el propio hueco.

Las familias alojadas en cara pueden ser necesarias para geometrías complejas, pero deben mantener una clasificación IFC inequívoca.

Los huecos de cubierta creados solo mediante edición del perímetro no equivalen necesariamente a un lucernario ni a una abertura analítica identificable.

## 11. Muros cortina

### 11.1 Descomposición del sistema

Un muro cortina puede contener:

- Paneles acristalados.
- Paneles opacos.
- Montantes y travesaños.
- Puertas.
- Huecos o paneles vacíos.

El modelo energético debe distinguir al menos las partes transparentes y opacas. Tratar toda la fachada como vidrio suele sobreestimar ganancias solares y transmisión.

### 11.2 Rejillas y paneles

Las rejillas deben responder a la modulación necesaria para diferenciar construcciones, no a cada junta decorativa. Una subdivisión excesiva aumenta el número de superficies y dificulta las actualizaciones.

Se comprobará que:

- Todos los paños tienen panel asignado.
- Los paneles opacos no usan material transparente.
- Los paneles acristalados son reconocibles.
- No existen paneles solapados.
- Las puertas sustituyen realmente al panel correspondiente.

### 11.3 Montantes

El receptor puede representar los montantes explícitamente, integrarlos como fracción de marco o ignorarlos. La estrategia elegida debe evitar contabilizarlos dos veces.

Para sistemas repetitivos suele ser más robusto asignar una fracción de marco verificada que exportar geometría detallada de todos los perfiles, salvo que la aplicación receptora gestione correctamente esa geometría.

### 11.4 Agrupación analítica

Autodesk indica que los paneles de muro cortina adyacentes y del mismo tipo pueden agruparse en una superficie analítica en determinados modos. Por ello, el número de paneles físicos no garantiza el mismo número de huecos analíticos.

La revisión debe comparar áreas totales por orientación y construcción, además del recuento de objetos.

### 11.5 Muros cortina curvos o inclinados

Se registrará el teselado y la variación de orientación entre paños. Un único valor de orientación para toda una fachada curva puede no representar adecuadamente las ganancias solares.

## 12. Propiedades térmicas y solares

### 12.1 Propiedades disponibles en Revit

Autodesk documenta propiedades analíticas de tipo como:

- Construcción analítica.
- Coeficiente de transmisión térmica `U`.
- Resistencia térmica `R`, según la categoría.
- Factor solar o `SHGC`.
- Transmitancia visible.

Estas propiedades pueden servir para inventario y comprobación, pero su presencia no demuestra que el exportador IFC ni la aplicación receptora las utilicen.

### 12.2 Valor U

Debe aclararse si el valor corresponde a:

- Vidrio central.
- Vidrio completo.
- Marco.
- Hueco completo, incluyendo vidrio y marco.

El valor requerido por el procedimiento reglamentario y por cada motor puede diferir. La fuente y el alcance del dato deben registrarse.

### 12.3 Factor solar

El factor solar debe corresponder al conjunto de vidrio definido y a las condiciones de cálculo utilizadas. No debe confundirse con transmitancia visible ni con una propiedad gráfica del material.

### 12.4 Permeabilidad e infiltración

La permeabilidad al aire de la carpintería no suele deducirse de su geometría. Se incorporará como propiedad o dato del motor cuando el procedimiento lo requiera, manteniendo referencia al tipo Revit.

### 12.5 Protecciones solares móviles

Persianas, estores y lamas móviles requieren datos de operación y control que exceden la geometría estática. Se documentarán como propiedades del sistema o del motor, sin suponer que su posición visible en Revit representa el horario de funcionamiento.

## 13. Materiales de vidrio

El material asignado a un sólido transparente ayuda a identificar el vidrio, pero no garantiza una construcción energética completa.

Se recomienda:

- Usar materiales con nombres y códigos estables.
- Evitar un único material genérico para vidrios térmicamente diferentes.
- Distinguir vidrio de marco y panel opaco.
- No confiar en transparencia gráfica como propiedad térmica.
- Registrar composición y fuente de prestaciones fuera de la geometría.

Ejemplos de códigos:

- `GLZ-DV-LOWE-01`: doble vidrio bajo emisivo.
- `GLZ-TV-SOLAR-01`: triple vidrio con control solar.
- `FRM-ALU-RPT-01`: marco de aluminio con rotura de puente térmico.
- `DOR-OPA-INS-01`: puerta exterior opaca aislada.

## 14. Huecos interiores y adyacencias

Una ventana o puerta entre dos espacios debe conservar ambos recintos como adyacentes. Se revisará especialmente cuando:

- Los espacios pertenecen a archivos vinculados diferentes.
- El muro anfitrión no delimita habitaciones.
- Uno de los espacios no está colocado.
- Existen fases distintas.
- La abertura queda por encima o por debajo del volumen de uno de los espacios.

Si ambos recintos pertenecen a la misma zona térmica, el motor puede simplificar la partición; aun así, la geometría no debe generar una falsa superficie exterior.

## 15. Relación con elementos de sombra

El hueco y su protección deben ser objetos conceptualmente distintos. Pueden afectar al sombreado:

- Retranqueo del vidrio.
- Dintel y jambas profundas.
- Voladizos.
- Lamas fijas.
- Balcones.
- Cuerpos del propio edificio.
- Edificios próximos.

La geometría detallada solo se conservará cuando produzca una diferencia solar relevante y el receptor pueda interpretarla sin crear cerramientos o espacios falsos.

## 16. Fases, opciones y vínculos

### 16.1 Fases

En rehabilitación se distinguirán carpinterías existentes, demolidas y nuevas. No deben exportarse simultáneamente dos ventanas superpuestas en el mismo hueco.

### 16.2 Opciones de diseño

Cada alternativa debe generar un conjunto completo y coherente. Se evitará combinar el cerramiento de una opción con ventanas de otra.

### 16.3 Vínculos

Cuando los huecos están en el vínculo arquitectónico y los espacios en el anfitrión, se comprobará:

- Condición delimitadora del vínculo.
- Inclusión del vínculo en la exportación.
- Conservación de anfitrión y hueco.
- Coordenadas y fase.
- Ausencia de carpinterías duplicadas en el archivo MEP.

## 17. Identificación y nomenclatura

Cada tipo debe disponer de un código estable que no dependa exclusivamente del nombre comercial. Una convención inicial puede ser:

`WIN-EXT-01`, `WIN-INT-01`, `DOR-EXT-OPA-01`, `DOR-EXT-GLZ-01`, `SKY-01`, `CW-GLZ-01`.

Cada instancia conservará:

- Identificador Revit.
- Marca de ejemplar.
- Marca de tipo.
- Código energético.
- Nivel.
- Orientación calculada o verificable.
- Estado de revisión.

El mapeado de estos datos a IFC se definirá en el capítulo de parámetros.

## 18. Tablas de control

### 18.1 Tabla de ventanas

Campos recomendados:

- Familia y tipo.
- Marca de tipo y ejemplar.
- Ancho y alto nominal.
- Ancho y alto de hueco bruto.
- Antepecho y dintel.
- Nivel y fase.
- Anfitrión.
- Área bruta.
- Área transparente calculada.
- Código de vidrio y marco.
- `U`, factor solar y transmitancia visible documentales.
- Estado de revisión.

### 18.2 Tabla de puertas exteriores

Añadir:

- Función interior/exterior.
- Porcentaje acristalado.
- Construcción opaca o mixta.
- Permeabilidad o clase, cuando proceda.

### 18.3 Tabla de paneles de muro cortina

Agrupar por:

- Tipo de panel.
- Material.
- Función transparente u opaca.
- Orientación.
- Área.

## 19. Vistas de control

Se prepararán:

- Alzados por orientación con filtros de estado.
- Vista 3D con huecos resaltados por clase.
- Secciones de lucernarios y retranqueos.
- Plantas con antepechos y puertas exteriores.
- Vista aislada de muros cortina, paneles y montantes.
- Vista del modelo analítico con superficies de abertura.

Los colores deben distinguir ventanas, puertas opacas, elementos acristalados, paneles opacos, lucernarios y aberturas de aire.

## 20. Comprobaciones geométricas

Para cada hueco o grupo de tipos se verificará:

1. El anfitrión queda realmente perforado.
2. La abertura está íntegramente contenida en el cerramiento.
3. No invade forjados, cubiertas ni huecos vecinos.
4. Su posición coincide con el espacio correspondiente.
5. Ancho, alto y área son positivos.
6. El contorno no contiene aristas residuales.
7. No existen duplicados.
8. La orientación es correcta.
9. El IFC conserva la entidad y el hueco.
10. El receptor asigna la superficie al cerramiento correcto.

## 21. Comparación de áreas

La revisión se realizará en tres niveles:

| Nivel | Magnitud |
|---|---|
| Revit | Área bruta y transparente por tipo y orientación |
| IFC | Área geométrica de huecos y elementos exportados |
| Receptor | Área utilizada en el modelo analítico y cálculo |

Se registrarán diferencias absolutas y relativas. La tolerancia se definirá antes del ensayo y será más estricta para fachadas repetitivas que para huecos de forma especial justificados.

No basta con comparar el área total del edificio: un exceso en la fachada norte podría compensar una carencia en la fachada oeste y ocultar un error solar importante.

## 22. Procedimiento de homologación de familias

1. Seleccionar una familia y duplicarla en un archivo de prueba.
2. Crear tipos mínimo, medio y máximo.
3. Colocarlos en cerramientos de distintos espesores.
4. Revisar corte, dimensiones y orientación.
5. Crear tablas de hueco bruto y área transparente.
6. Generar el modelo analítico de Revit.
7. Exportar a IFC con la configuración prevista.
8. Inspeccionar entidad, anfitrión, abertura y propiedades.
9. Importar en Open BIM Analytical Model y TeKton3D.
10. Comparar superficies y construcciones.
11. Registrar limitaciones.
12. Aprobar, corregir o retirar la familia del catálogo energético.

## 23. Errores frecuentes

| Síntoma | Causa probable | Revisión inicial |
|---|---|---|
| La ventana aparece pero el muro no tiene hueco | Vacío incorrecto o geometría superpuesta | Editar familia y comprobar corte |
| El receptor no reconoce una ventana | Categoría o mapeado IFC incorrecto | Entidad exportada y configuración IFC |
| Área acristalada excesiva | Se usa el hueco bruto como vidrio | Fracción de marco y parámetros de familia |
| Puerta acristalada duplicada | Hoja y vidrio exportados como huecos independientes | Subfamilias y descomposición IFC |
| Lucernario convertido en ventana vertical | Pérdida de plano u orientación | Geometría IFC y anfitrión |
| Muro cortina completamente transparente | Paneles opacos no diferenciados | Tipos de panel y materiales |
| Hueco interior convertido en exterior | Falta un espacio adyacente | Volúmenes, fases y límites |
| Desaparece un hueco pequeño | Resolución o tolerancia del receptor | Tamaño mínimo y configuración analítica |
| Sombras incoherentes | Familia invertida o vidrio mal posicionado | Orientación y retranqueo |

## 24. Criterios de aceptación

El conjunto de huecos estará preparado cuando:

- Todos los huecos relevantes tengan categoría y anfitrión reconocibles.
- Las familias corten realmente los cerramientos.
- No existan duplicados ni huecos solapados.
- Dimensión nominal, hueco bruto y área transparente estén documentados.
- Ventanas, puertas, lucernarios y aberturas se distingan correctamente.
- Los paneles opacos y transparentes de muros cortina estén separados.
- Las orientaciones e inclinaciones sean correctas.
- Las propiedades térmicas tengan fuente y alcance definidos.
- El IFC conserve entidades, relaciones y dimensiones suficientes.
- Las áreas del receptor cumplan la tolerancia por orientación y construcción.
- Las limitaciones de cada familia estén registradas.

## 25. Checklist de entrega

- [ ] Todas las ventanas y puertas relevantes están inventariadas.
- [ ] Las categorías nativas se utilizan siempre que es viable.
- [ ] Cada familia corta completamente su anfitrión.
- [ ] Se han probado tamaños extremos y espesores de muro.
- [ ] Se distinguen ancho y alto nominales de los de hueco bruto.
- [ ] El área transparente y la fracción de marco son verificables.
- [ ] Antepechos, dinteles y niveles son coherentes.
- [ ] La orientación interior/exterior está revisada.
- [ ] Las formas especiales disponen de ensayo.
- [ ] Las puertas acristaladas siguen una estrategia documentada.
- [ ] Los lucernarios conservan su inclinación y anfitrión.
- [ ] Los paneles opacos y transparentes del muro cortina están diferenciados.
- [ ] Los montantes no se contabilizan dos veces.
- [ ] Los huecos interiores conservan adyacencias.
- [ ] Fases, opciones y vínculos son coherentes.
- [ ] El modelo analítico de Revit ha sido revisado.
- [ ] El IFC y ambos receptores han superado la comparación de áreas.

## 26. Ensayo de referencia para Revit 2026

El modelo de prueba incorporará:

- Ventana rectangular fija.
- Ventana practicable con marco significativo.
- Ventana arqueada.
- Dos ventanas contiguas.
- Puerta exterior opaca.
- Puerta parcialmente acristalada.
- Lucernario sobre cubierta inclinada.
- Abertura de aire entre dos espacios.
- Muro cortina con paneles transparentes y opacos.
- Puerta insertada en muro cortina.
- Panel curvo o fachada facetada.
- Hueco con retranqueo y voladizo.

Para cada caso se registrarán entidad IFC, área bruta, área transparente, orientación, anfitrión, construcción y resultado en Open BIM Analytical Model, CYPETHERM HE Plus y TK-IFC/TK-CEEP.

## 27. Fuentes principales

- Autodesk, *About Creating Energy Analytical Models from Architectural Elements*, Revit 2026.
- Autodesk, *Window Type Properties*, Revit 2026.
- Autodesk, *Door Type Properties*.
- Autodesk, *Energy Analytical Model Properties*, Revit 2026.
- Autodesk, *About Surfaces in the Energy Analytical Model*.
- Autodesk, *Energy Settings*, Revit 2026.
