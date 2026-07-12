---
title: Sombras y geometría exterior en Revit 2026
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
software:
  nombre: Autodesk Revit
  version_base: "2026"
---

# Sombras y geometría exterior en Revit 2026

Las sombras modifican la radiación solar incidente sobre huecos y cerramientos. Una representación insuficiente puede sobreestimar ganancias solares; una representación excesivamente detallada puede generar miles de superficies, errores geométricos o falsos recintos.

El objetivo es conservar únicamente la geometría exterior que produzca un efecto solar relevante y transformarla en superficies de sombra reconocibles por el flujo analítico.

!!! warning "Visible no significa calculable"
    Que un elemento proyecte sombra en una vista de Revit no demuestra que se exporte a IFC ni que CYPE o TeKton3D lo utilicen. La comprobación debe realizarse en el modelo receptor y, cuando sea posible, mediante un caso con y sin sombra.

## 1. Alcance

Este capítulo incluye:

- Voladizos y aleros.
- Balcones y terrazas superiores.
- Jambas, dinteles y retranqueos.
- Lamas y parasoles fijos.
- Elementos móviles representados mediante escenarios.
- Petos y cuerpos salientes.
- Vegetación y obstáculos.
- Edificios colindantes.
- Relieve próximo cuando produzca obstrucción relevante.

No desarrolla los algoritmos solares internos de cada motor, que se documentarán en sus capítulos específicos.

## 2. Requisitos previos

Antes de estudiar sombras deben estar fijados:

- Ubicación geográfica.
- Norte verdadero.
- Cotas y niveles.
- Geometría de huecos.
- Fase y opción de diseño.
- Estado de cálculo.

Una sombra geométricamente correcta sobre un modelo mal orientado produce un resultado incorrecto.

## 3. Clasificación de la geometría exterior

Cada elemento se asignará a una de estas clases:

| Clase | Función analítica |
|---|---|
| Envolvente | Transmite calor y puede recibir sombra |
| Hueco | Transmite calor y radiación solar |
| Sombra propia | Obstruye radiación sin cerrar un espacio |
| Sombra remota | Obstáculo exterior o edificio próximo |
| Terreno | Condición de contorno y posible obstrucción |
| Contexto gráfico | No interviene en el análisis |

La clasificación se registrará con un parámetro funcional y no dependerá únicamente de categoría, material o subcategoría gráfica.

## 4. Cómo interpreta Revit las sombras analíticas

Autodesk indica que Revit no dispone de una categoría arquitectónica específica para sombras. Las superficies analíticas de tipo `Shade` se generan, entre otros casos, a partir de:

- Partes de elementos arquitectónicos situadas fuera del edificio.
- Masas conceptuales sin plantas de masa.

Estas superficies no se crean manualmente como elementos analíticos. Por tanto, la geometría física y la configuración de generación determinan si aparecen.

Este comportamiento es útil como diagnóstico, pero no garantiza que la misma clasificación se conserve en IFC ni en los receptores del manual.

## 5. Principio de relevancia solar

Un elemento se conservará si puede modificar de forma apreciable la radiación sobre una superficie de interés durante el periodo de cálculo.

Se considerarán:

- Tamaño angular visto desde el hueco.
- Distancia al hueco.
- Orientación de la fachada.
- Altura solar estacional.
- Horas de ocupación.
- Repetición del elemento.
- Sensibilidad del uso a ganancias solares.

No existe una dimensión mínima universal. El umbral debe definirse mediante ensayo y sensibilidad.

## 6. Nivel de simplificación

### 6.1 Conservar

- Contorno exterior que produce la sombra.
- Posición, cota y orientación.
- Profundidad del voladizo.
- Separación respecto al hueco.
- Inclinación de lamas relevantes.
- Silueta de edificios vecinos.

### 6.2 Simplificar

- Espesores que no cambian la máscara solar.
- Redondeos y chaflanes pequeños.
- Herrajes y fijaciones.
- Perfiles complejos sustituidos por planos equivalentes.
- Juntas y subdivisiones decorativas.

### 6.3 Excluir

- Mobiliario exterior temporal sin escenario definido.
- Elementos ocultos para todo el recorrido solar relevante.
- Detalles de escala muy inferior a la resolución del receptor.
- Contexto lejano sin obstrucción del horizonte.
- Geometría importada duplicada.

## 7. Voladizos y aleros

### 7.1 Geometría mínima

Un voladizo puede representarse mediante un plano o sólido simple que conserve:

- Anchura.
- Profundidad.
- Cota inferior.
- Desfase horizontal respecto al hueco.
- Inclinación, si existe.

El espesor solo se conservará cuando sus caras produzcan diferencias significativas o el receptor necesite un sólido cerrado.

### 7.2 Relación con el cerramiento

El voladizo no debe:

- Delimitar una habitación exterior ficticia.
- Cortar el cerramiento anfitrión.
- Convertirse en cubierta térmica del espacio inferior si solo actúa como sombra.
- Duplicarse como parte de una cubierta y como familia independiente.

### 7.3 Aleros de cubierta

La parte de cubierta que sobresale del volumen puede generar sombra automáticamente en el modelo analítico de Revit. Se comprobará que la parte interior continúa actuando como cerramiento y la exterior como sombra, sin perder la continuidad del borde.

## 8. Balcones y terrazas

Un balcón puede desempeñar simultáneamente varias funciones:

- Forjado exterior de sombra para el hueco inferior.
- Puente geométrico con el forjado interior.
- Suelo de un espacio exterior.
- Soporte de petos o barandillas.

Para el modelo energético se separarán conceptualmente la parte transmisora y la parte que solo obstruye radiación.

Se comprobará:

- Proyección del canto.
- Profundidad de la losa.
- Posición respecto a los huecos inferiores.
- Laterales que actúan como aletas.
- Petos opacos.
- Balcones repetidos en altura.

Las barandillas transparentes o de barrotes no se modelarán como planos opacos salvo que el método de cálculo permita asignar una transmitancia solar equivalente.

## 9. Retranqueos, jambas y dinteles

El retranqueo del vidrio genera autosombreamiento. Puede representarse mediante la geometría real del hueco o mediante protecciones equivalentes en el receptor.

Se medirán:

- Profundidad desde la cara exterior hasta el vidrio.
- Anchura de jambas.
- Altura del dintel.
- Antepecho exterior.
- Inclinación de derrames.

Cuando el receptor coloca el hueco sobre el plano del cerramiento, debe documentarse si pierde estas sombras y cómo se compensan.

No conviene exportar molduras o recercados pequeños si generan polígonos problemáticos sin efecto solar relevante.

## 10. Lamas fijas

### 10.1 Datos esenciales

- Orientación.
- Ángulo de inclinación.
- Anchura de lama.
- Separación entre lamas.
- Distancia al vidrio.
- Extensión lateral y vertical.
- Opacidad o transmitancia solar, cuando el motor la admita.

### 10.2 Representación explícita

Modelar cada lama puede ser adecuado cuando son pocas, grandes y el receptor conserva su geometría. Debe evitarse si produce una cantidad desproporcionada de superficies.

### 10.3 Plano equivalente

Para celosías repetitivas puede utilizarse una superficie equivalente si el motor permite definir porosidad, factor de sombra o propiedades solares. El porcentaje de huecos no debe sustituirse sin más por transparencia gráfica.

### 10.4 Ensayo de equivalencia

Comparar:

1. Modelo detallado.
2. Plano o dispositivo equivalente.
3. Caso sin protección.

La simplificación se aceptará si reproduce el efecto sobre ganancias solares dentro de la tolerancia establecida y reduce de forma apreciable la complejidad.

## 11. Protecciones móviles

Persianas, estores y lamas móviles no se describen adecuadamente mediante una única posición geométrica.

Se tratarán mediante:

- Propiedad específica del motor.
- Factor reductor reglamentario.
- Horario o control de operación.
- Escenarios independientes de posición.

La geometría de Revit puede documentar una posición de referencia, pero no debe interpretarse como funcionamiento anual.

En el modelo de intercambio se evitará exportar simultáneamente varias posiciones superpuestas.

## 12. Toldos y elementos estacionales

Se registrarán como sistemas móviles o estacionales. Si el receptor no admite control, se definirán escenarios:

- Sin toldo.
- Toldo desplegado.
- Condición equivalente según el procedimiento de cálculo.

La comparación debe utilizar idénticas condiciones climáticas y de ocupación.

## 13. Petos, pretiles y muretes

Los petos pueden sombrear cubiertas, terrazas o lucernarios, pero no deben generar espacios analíticos falsos.

Revisar:

- Condición `Room Bounding`.
- Altura real.
- Continuidad alrededor de la cubierta.
- Distancia a lucernarios.
- Clasificación como sombra en el receptor.

Un peto modelado como muro no debe incorporarse automáticamente a la envolvente térmica por compartir categoría.

## 14. Pilares, vigas y estructura exterior

Los elementos estructurales exteriores se conservarán si producen sombras relevantes. Su sección puede simplificarse manteniendo silueta y posición.

Los pilares adosados a fachada requieren especial atención: una parte puede afectar a la envolvente y otra actuar como aleta de sombra. Se verificará que no fragmenten espacios ni creen superficies térmicas duplicadas.

## 15. Edificios colindantes

### 15.1 Información necesaria

Para obstrucción solar normalmente basta con:

- Planta simplificada.
- Altura.
- Cota respecto al proyecto.
- Distancia.
- Orientación.
- Silueta de cubiertas relevante.

No se necesitan distribuciones interiores, huecos ni detalles constructivos.

### 15.2 Masas de contexto

Autodesk propone utilizar masas sin plantas para representar edificios circundantes que producen sombra en estudios de masa. Este criterio permite diferenciarlas del edificio analizado.

Debe ensayarse si estas masas:

- Aparecen como superficies de sombra en Revit.
- Se incluyen en la exportación IFC prevista.
- Son reconocidas por Open BIM Analytical Model y TeKton3D.

Si el flujo IFC no conserva su función, se recrearán como obstáculos en la aplicación receptora.

### 15.3 Alcance del contexto

Se incluirán los edificios que intercepten una parte significativa del cielo visto desde las fachadas estudiadas. La distancia por sí sola no es criterio suficiente: un edificio alto y lejano puede ser más relevante que uno bajo y próximo.

## 16. Medianerías y patios

En patios estrechos, los cerramientos opuestos producen sombras mutuas y no son simples obstáculos remotos. Deben conservarse como parte del edificio y mantener sus huecos y orientaciones.

En medianerías se distinguirá entre:

- Superficie en contacto con otro edificio.
- Parte expuesta por encima del colindante.
- Volumen vecino que solo produce sombra.

Puede ser necesario dividir el cerramiento o corregir su condición de contorno en el receptor.

## 17. Vegetación

La vegetación es variable, permeable y estacional. Un árbol modelado como sólido opaco suele sobreestimar la sombra.

Opciones:

- Excluirla del modelo reglamentario si el procedimiento no la contempla.
- Representar una copa simplificada con transmitancia equivalente.
- Utilizar escenarios con y sin follaje.
- Definir obstáculos específicos en el motor.

Se documentarán especie o tipología, altura, diámetro de copa, caducidad y escenario. Los RPC y componentes de aspecto no deben suponerse exportables como geometría analítica.

## 18. Topografía y horizonte

El relieve cercano puede obstruir el sol en emplazamientos con pendientes, desmontes o montañas. El toposólido completo puede resultar demasiado pesado para IFC.

Se preferirá:

- Conservar taludes próximos que oculten directamente fachadas bajas.
- Simplificar el relieve lejano mediante perfil de horizonte si el motor lo admite.
- Eliminar triangulación que no cambie la silueta.
- No permitir que el terreno invada el volumen del edificio.

La condición de contacto con terreno y la obstrucción solar son funciones diferentes y deben revisarse por separado.

## 19. Geometría importada

Los archivos DWG, SAT, 3DM o nubes de puntos pueden servir como referencia, pero no son automáticamente geometría energética válida.

Antes de utilizarlos:

- Confirmar unidades y coordenadas.
- Eliminar capas innecesarias.
- Simplificar mallas.
- Asignar una categoría controlada.
- Comprobar si se exportan a IFC.
- Evitar duplicar el contexto ya modelado.

Una nube de puntos no debe exportarse como obstáculo solar. Se extraerá de ella una envolvente simplificada.

## 20. Categorías y familias recomendadas

No existe una única categoría nativa de sombra. La elección dependerá del elemento y del exportador:

| Elemento | Representación candidata |
|---|---|
| Alero integrado | Parte exterior de cubierta |
| Voladizo o balcón | Suelo simplificado o familia controlada |
| Lama fija | Familia de modelo genérico simplificada |
| Edificio vecino | Masa sin plantas o volumen simplificado |
| Perfil de horizonte | Objeto específico del receptor |
| Vegetación | Escenario o volumen equivalente |

Cada categoría candidata deberá superar una prueba de exportación. No se propondrá una categoría universal sin evidencia en los flujos previstos.

## 21. Parámetros mínimos

Se recomienda registrar:

- `ENERGY_ROLE`: `SHADE_SELF`, `SHADE_REMOTE` o `CONTEXT_ONLY`.
- Código de tipo.
- Fijo o móvil.
- Escenario de operación.
- Opacidad o factor equivalente, si procede.
- Fuente geométrica.
- Estado de revisión.
- Aplicaciones en las que se ha validado.

El nombre definitivo y su mapeado IFC se fijarán en el capítulo de parámetros.

## 22. Orientación y estudio solar en Revit

Autodesk documenta que la trayectoria solar utiliza la ubicación del proyecto y muestra la orientación respecto al norte verdadero. Antes del ensayo:

1. Confirmar ubicación y zona horaria.
2. Mostrar norte verdadero.
3. Activar trayectoria solar y sombras.
4. Preparar vistas 3D y alzados adecuados.
5. Crear estudios estáticos y de un día.
6. Revisar fechas y horas críticas.

Los estudios solares de Revit son una herramienta de inspección visual. No sustituyen el cálculo anual del motor energético ni validan la transferencia IFC.

## 23. Fechas y horas de control

El protocolo incluirá, como mínimo:

- Solsticio de invierno.
- Equinoccio.
- Solsticio de verano.
- Mañana, mediodía solar y tarde.
- Horas críticas de ocupación.

En fachadas este y oeste se prestará especial atención a alturas solares bajas. En fachadas sur serán relevantes profundidad y separación de protecciones horizontales. La fachada norte también puede recibir radiación directa según latitud, estación y orientación exacta.

## 24. Vistas de control

### 24.1 Vista `QA_SHD_01_MODELO`

Mostrar únicamente envolvente, huecos y sombras aprobadas. Colorear por función analítica.

### 24.2 Vista `QA_SHD_02_CONTEXTO`

Mostrar edificio y obstáculos remotos, con coordenadas y norte verdadero visibles.

### 24.3 Vistas solares

Guardar presets con ubicación, fecha, hora y orientación. El nombre debe permitir reproducir el estudio.

### 24.4 Vista analítica

Revisar la categoría **Analytical Surfaces: Shades** y comprobar:

- Presencia de elementos esperados.
- Ausencia de contexto gráfico irrelevante.
- Posición respecto a los huecos.
- Fragmentación de superficies.

## 25. Control de complejidad

Se registrarán antes y después de simplificar:

- Número de elementos de sombra.
- Número de caras o polígonos.
- Tamaño del IFC.
- Tiempo de exportación.
- Tiempo de importación.
- Tiempo de cálculo.
- Diferencia en ganancias solares o demanda.

Una simplificación es adecuada cuando reduce el coste de proceso sin alterar materialmente los resultados.

## 26. Verificación en IFC

La inspección debe confirmar:

- Que la geometría se exporta.
- Que su posición y unidades son correctas.
- Que no se clasifica como espacio o cerramiento térmico por error.
- Que no corta ni duplica la envolvente.
- Que conserva una geometría utilizable.
- Que puede relacionarse con su elemento Revit.

La mera presencia visual en un visor IFC no demuestra que el receptor energético la use como sombra.

## 27. Verificación en aplicaciones receptoras

Para Open BIM Analytical Model y TeKton3D se comprobará:

- Superficies de sombra creadas.
- Huecos afectados.
- Posición relativa.
- Capacidad de edición o recreación.
- Conservación después de actualizar el IFC.
- Tratamiento de protecciones móviles.
- Efecto en resultados mediante ensayo comparativo.

CYPETHERM HE Plus se revisará después de generar el modelo analítico, confirmando que las sombras transferidas corresponden al escenario previsto.

## 28. Ensayo con y sin sombra

La validación mínima utilizará dos variantes idénticas:

1. Caso base sin dispositivo de sombra.
2. Caso con el dispositivo activado.

Se mantendrán constantes clima, orientación, construcciones, horarios y sistemas. Se compararán:

- Radiación o ganancias solares, si están disponibles.
- Cargas de refrigeración.
- Demanda de refrigeración.
- Demanda de calefacción.
- Horas de sobrecalentamiento, cuando proceda.

Si no cambia ninguna magnitud sensible, debe investigarse si la sombra se ha ignorado o si realmente no es relevante.

## 29. Errores frecuentes

| Síntoma | Causa probable | Revisión inicial |
|---|---|---|
| El voladizo aparece como cubierta térmica | Categoría o relación espacial incorrecta | Clasificación y límites de espacios |
| El edificio vecino crea un recinto | Masa con plantas o elemento delimitador | Tipo de masa y `Room Bounding` |
| Las lamas desaparecen | Dimensión inferior a tolerancia o categoría omitida | Simplificación y exportación IFC |
| El IFC es excesivamente pesado | Geometría repetitiva demasiado detallada | Plano equivalente o reducción de malla |
| No varían las ganancias solares | La sombra no llega al motor | Entidades receptoras y ensayo A/B |
| La sombra cae en dirección incorrecta | Norte o ubicación erróneos | Coordenadas, norte verdadero y zona horaria |
| Vegetación produce sombra total | Copa modelada como sólido opaco | Escenario o transmitancia equivalente |
| Un balcón duplica el forjado | Elementos interior y exterior superpuestos | Límites y clasificación funcional |
| El hueco queda sombreado todo el año | Posición o escala incorrectas | Unidades, cotas y retranqueos |

## 30. Procedimiento de preparación

1. Confirmar ubicación y norte verdadero.
2. Inventariar elementos exteriores.
3. Clasificarlos por función analítica.
4. Excluir el contexto sin relevancia.
5. Simplificar geometrías repetitivas o complejas.
6. Revisar sombras en fechas y horas críticas.
7. Generar el modelo analítico de Revit.
8. Comprobar superficies `Shade`.
9. Exportar el IFC de ensayo.
10. Inspeccionar posición, categoría y complejidad.
11. Importar en los receptores.
12. Ejecutar comparación con y sin sombra.
13. Registrar diferencias y limitaciones.
14. Aprobar la representación o recrearla en el receptor.

## 31. Criterios de aceptación

El modelo de sombras estará preparado cuando:

- La ubicación y orientación estén verificadas.
- Cada elemento exterior tenga una función definida.
- No existan falsos recintos ni cerramientos duplicados.
- Voladizos, balcones y retranqueos relevantes conserven posición y tamaño.
- Las protecciones móviles se traten mediante escenarios o controles.
- El contexto remoto esté suficientemente simplificado.
- El IFC mantenga una geometría manejable y trazable.
- El receptor reconozca o permita reconstruir las sombras necesarias.
- El ensayo con y sin sombra produzca un efecto coherente.
- Las simplificaciones y exclusiones estén documentadas.

## 32. Checklist de entrega

- [ ] Ubicación, zona horaria y norte verdadero están comprobados.
- [ ] Se ha inventariado la geometría exterior.
- [ ] Cada objeto está clasificado como envolvente, sombra o contexto.
- [ ] Los elementos de sombra no delimitan espacios por error.
- [ ] Voladizos y aleros conservan sus dimensiones esenciales.
- [ ] Balcones y petos no duplican cerramientos.
- [ ] Retranqueos relevantes están representados o compensados.
- [ ] Las lamas siguen una estrategia explícita o equivalente.
- [ ] Las protecciones móviles tienen escenario de operación.
- [ ] Los edificios vecinos están simplificados y correctamente situados.
- [ ] Vegetación y topografía siguen criterios documentados.
- [ ] Se han revisado fechas y horas solares críticas.
- [ ] El modelo analítico muestra las sombras esperadas.
- [ ] El IFC no contiene geometría exterior innecesaria.
- [ ] Open BIM Analytical Model y TeKton3D han sido comprobados.
- [ ] Se ha realizado un ensayo con y sin sombra.

## 33. Ensayo de referencia para Revit 2026

El modelo de prueba incorporará:

- Voladizo horizontal sobre una ventana sur.
- Aleta vertical en una fachada oeste.
- Hueco retranqueado.
- Balcón con peto.
- Conjunto de lamas fijas.
- Protección móvil mediante dos escenarios.
- Lucernario próximo a un peto.
- Patio con sombras mutuas.
- Edificio vecino como masa sin plantas.
- Árbol o copa equivalente.
- Talud simplificado.
- Elemento exterior irrelevante que deba excluirse.

Se compararán geometría, número de superficies, tamaño del archivo, tiempo de proceso y efecto energético en Revit, Open BIM Analytical Model, CYPETHERM HE Plus y TK-IFC/TK-CEEP.

## 34. Fuentes principales

- Autodesk, *About Creating Energy Analytical Models from Architectural Elements*, Revit 2026.
- Autodesk, *About the Sun Path*, Revit 2026.
- Autodesk, *Workflow: Solar Studies*, Revit 2026.
- Autodesk, *Solar Studies*, Revit 2026.
- Autodesk, *Create the Energy Analytical Model: Massing*, Revit 2026.
- Autodesk, *Interactive Solar Studies*, Revit 2026.
