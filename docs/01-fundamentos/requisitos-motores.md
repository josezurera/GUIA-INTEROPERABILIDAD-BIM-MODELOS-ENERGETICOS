---
title: Requisitos comunes de los motores de cálculo
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-11
alcance:
  - geometria
  - zonificacion
  - envolvente
  - condiciones_de_contorno
  - huecos
  - sombras
---

# Requisitos comunes de los motores de cálculo

Los programas de análisis energético no calculan directamente el modelo arquitectónico. Sus interfaces transforman la información recibida en zonas, superficies, construcciones, cargas, condiciones operacionales y sistemas compatibles con el motor utilizado.

Aunque CYPETHERM HE Plus y TK-CEEP emplean flujos y estructuras propias, comparten una necesidad fundamental: disponer de una representación cerrada, coherente y suficientemente sencilla del edificio. Este capítulo identifica esos requisitos comunes sin atribuir a todos los programas una limitación específica de uno de ellos.

!!! info "Alcance"
    Se describen requisitos de entrada y calidad del modelo, no los algoritmos reglamentarios de cada procedimiento. Las restricciones particulares se documentarán en los módulos de cada aplicación.

## 1. Requisitos mínimos del modelo energético

Para calcular el comportamiento del edificio deben quedar definidos, de forma directa o mediante reglas del programa receptor:

1. Ubicación y datos climáticos.
2. Orientación del edificio.
3. Zonas o volúmenes de cálculo.
4. Superficies que delimitan cada zona.
5. Condición situada al otro lado de cada superficie.
6. Soluciones constructivas y propiedades térmicas.
7. Huecos y elementos transparentes.
8. Sombras relevantes.
9. Condiciones operacionales y cargas internas.
10. Ventilación e infiltración.
11. Sistemas energéticos.

La preparación geométrica en Revit afecta principalmente a los puntos 2 a 8. El resto se completa habitualmente en la aplicación energética.

## 2. Zonas térmicas

### 2.1 Unidad del balance energético

El motor realiza balances sobre zonas térmicas. Una zona es una abstracción: puede coincidir con una habitación, contener varias o representar una fracción de un recinto cuando existen condiciones diferenciadas.

En EnergyPlus una zona debe reunir áreas térmicamente similares respecto a transmisiones, ganancias internas y condiciones de control. La documentación oficial recomienda evitar una zonificación innecesariamente detallada cuando varias áreas pueden representarse como una única entidad térmica.

### 2.2 Criterios de agrupación

Dos espacios son candidatos a pertenecer a la misma zona cuando comparten:

- Uso y horarios.
- Temperaturas de consigna.
- Condiciones de ocupación y cargas internas.
- Estrategia de ventilación.
- Sistema o forma de acondicionamiento.
- Unidad de uso compatible.
- Comportamiento de la envolvente suficientemente próximo.

La coincidencia de estas condiciones debe justificarse. Compartir únicamente el nombre de una habitación o pertenecer a la misma planta no es suficiente.

### 2.3 Criterios de separación

Conviene separar zonas cuando existen diferencias significativas en:

- Orientación o exposición solar.
- Proporción de fachada y huecos.
- Uso u horario.
- Consignas.
- Sistema que las atiende.
- Condición de habitabilidad.
- Necesidad reglamentaria de evaluación independiente.

### 2.4 Volumen y cierre

Cada zona debe poseer un volumen calculable y una envolvente cerrada. Un espacio sin suelo, techo o cierre lateral puede impedir el cálculo o provocar resultados físicamente incoherentes.

En Revit esto exige comprobar que las habitaciones o espacios tengan área y volumen, que sus límites superior e inferior sean correctos y que los elementos delimitadores formen una continuidad tridimensional.

## 3. Superficies térmicas

### 3.1 Función

Las superficies describen la transferencia de energía entre una zona y su entorno. Para cada una deben poder determinarse:

- Zona a la que pertenece.
- Geometría y área.
- Orientación e inclinación.
- Tipo de elemento.
- Construcción asociada.
- Condición de contorno exterior.
- Superficie correspondiente cuando existe adyacencia con otra zona.

### 3.2 Representación sin espesor

Los motores zonales representan normalmente cada cerramiento mediante una superficie matemática sin espesor. El espesor y la masa de los materiales se emplean en el cálculo de transmisión, pero no generan dos caras geométricas separadas en el modelo energético.

Esta diferencia explica por qué un modelado arquitectónico con capas independientes, revestimientos duplicados o pequeños retranqueos puede producir superficies analíticas redundantes. El modelo de cálculo necesita un plano de intercambio coherente, no la reproducción literal de todas las caras del elemento constructivo.

### 3.3 Una construcción por superficie

Una superficie energética debe tener una construcción inequívoca. Si distintas partes de un cerramiento poseen soluciones diferentes, deben representarse como superficies separadas o resolverse mediante el procedimiento admitido por la aplicación.

Por tanto, un muro de Revit que cambia de composición dentro de una misma cara requiere una estrategia explícita: división geométrica, diferenciación por tipos o reconstrucción posterior.

### 3.4 Complejidad geométrica

El número de vértices y superficies influye en la robustez y el tiempo de simulación. Deben evitarse:

- Segmentos de longitud despreciable.
- Superficies casi coplanares duplicadas.
- Entrantes y salientes sin influencia térmica apreciable.
- Contornos autointersecados.
- Superficies degeneradas o de área casi nula.
- Fragmentación causada únicamente por detalle constructivo.

No se establece todavía una tolerancia numérica general porque depende de la aplicación intermediaria y del motor. Las tolerancias deberán documentarse mediante fuentes específicas o pruebas.

## 4. Condiciones de contorno

Toda superficie debe relacionarse con el medio situado al otro lado. Las categorías habituales son:

| Condición | Interpretación |
|---|---|
| Exterior | Intercambio con aire exterior y exposición climática. |
| Terreno | Intercambio con el suelo mediante el modelo admitido. |
| Zona adyacente | Separación entre dos zonas del modelo. |
| Espacio no acondicionado | Separación respecto a un volumen con condiciones diferentes. |
| Adiabática o equivalente | Ausencia de flujo térmico según una hipótesis justificada. |
| Condición especial | Coeficientes o modelos específicos definidos por el programa. |

Una clasificación interior/exterior incorrecta cambia el balance térmico aunque la superficie tenga el área y la construcción correctas.

## 5. Adyacencias

Cuando dos zonas comparten un cerramiento, sus superficies deben ser geométricamente compatibles y estar relacionadas. El modelo receptor necesita reconocer que:

- Ambas superficies representan el mismo límite físico.
- Sus áreas son coherentes.
- Sus normales u orientaciones son opuestas.
- Cada una pertenece a la zona correspondiente.
- La transmisión se produce entre esas zonas y no con el exterior.

Las duplicidades, solapes, desfases de altura o pequeños huecos pueden romper esta correspondencia. En Open BIM Analytical Model la colindancia se almacena explícitamente entre superficies y puede corregirse manualmente.

## 6. Huecos

### 6.1 Asociación con una superficie base

Una ventana, puerta acristalada o lucernario debe estar contenido en una superficie que actúe como cerramiento base. El modelo debe conocer:

- Superficie que lo contiene.
- Zona a la que pertenece.
- Dimensiones y posición.
- Construcción o propiedades térmicas.
- Exposición y orientación.

Una familia visible en Revit no garantiza que el hueco se interprete. Debe cortar realmente su elemento hospedante y exportarse mediante una categoría y clase reconocibles.

### 6.2 Límites geométricos

La documentación de TK-CEEP, por condicionantes de su exportación a EnergyPlus, recomienda que cada hueco quede completamente contenido en una única zona, que no ocupe la totalidad de la superficie base y que no se sitúe exactamente en los vértices del espacio.

Estas reglas se registran como requisitos específicos del flujo TeKton3D/EnergyPlus. No deben trasladarse automáticamente a todos los receptores, pero constituyen buenas precauciones cuando se busca un IFC común robusto.

### 6.3 Muros cortina

Los muros cortina requieren una estrategia específica porque combinan paneles, montantes, huecos y, en ocasiones, puertas. El receptor puede interpretar sus paneles como superficies independientes o necesitar una simplificación equivalente. Se estudiarán por separado en las reglas de Revit y en cada aplicación.

## 7. Cerramientos horizontales y contacto con terreno

El modelo debe diferenciar:

- Suelo entre zonas.
- Techo entre zonas.
- Cubierta exterior.
- Forjado sobre exterior.
- Solera o elemento en contacto con terreno.
- Separación respecto a espacio no habitable.

La posición horizontal no determina por sí sola la función. La relación con los espacios y la condición situada al otro lado son las que permiten clasificar correctamente el elemento.

Las superficies en contacto con terreno pueden requerir modelos o parámetros adicionales que no se deducen del IFC. El IFC debe, como mínimo, permitir identificarlas sin confundirlas con forjados interiores o superficies exteriores.

## 8. Orientación, inclinación y coordenadas

La radiación solar y las condiciones exteriores dependen de la orientación e inclinación de cada superficie. Por ello deben mantenerse coherentes:

- Norte verdadero.
- Ubicación geográfica.
- Rotación entre norte de proyecto y norte real.
- Coordenadas y unidades.
- Cotas de las plantas.

Un desplazamiento global del edificio puede ser irrelevante para algunos balances térmicos, pero una rotación incorrecta altera la exposición solar. Los cambios de origen también pueden afectar a sombras remotas, coordinación y precisión geométrica.

## 9. Sombras y obstrucciones

Los motores necesitan distinguir las superficies que transmiten energía de aquellas que únicamente bloquean radiación. Los elementos de sombra pueden incluir:

- Aleros y vuelos.
- Lamas y protecciones fijas.
- Balcones.
- Retranqueos.
- Edificios próximos.
- Obstáculos remotos significativos.

La simplificación debe conservar la proyección solar relevante. Elementos pequeños, ornamentales o excesivamente fragmentados pueden omitirse cuando su influencia sea despreciable y quede justificado.

## 10. Soluciones constructivas

La geometría debe permitir asignar una solución constructiva única a cada superficie. El modelo energético necesita propiedades como:

- Resistencia y transmitancia térmica.
- Capacidad térmica y masa.
- Orden y espesor de capas cuando el motor lo requiere.
- Propiedades ópticas de los huecos.
- Permeabilidad o infiltración cuando proceda.

No debe suponerse que todos los materiales de Revit se trasladarán y serán utilizados directamente por el motor. La práctica más robusta es conservar identificadores o tipos que permitan mapear cada elemento a una solución validada en el programa energético.

## 11. Condiciones operacionales y sistemas

Las condiciones operacionales no se obtienen de la geometría. Deben asignarse de forma explícita y coherente con la zonificación:

- Ocupación.
- Iluminación y equipos.
- Horarios.
- Consignas.
- Ventilación.
- Infiltración.
- Producción de ACS.
- Sistemas de calefacción y refrigeración.

Una zona geométricamente válida puede seguir siendo incalculable o producir resultados irreales si carece de estas condiciones.

## 12. Requisitos de calidad antes del cálculo

El modelo debe superar, como mínimo, las siguientes comprobaciones:

- [ ] Todas las zonas previstas existen y tienen volumen.
- [ ] Cada zona está completamente delimitada.
- [ ] Todas las superficies poseen condición de contorno.
- [ ] Las adyacencias interiores son coherentes.
- [ ] Los huecos pertenecen a una superficie base.
- [ ] No existen superficies duplicadas o de área nula.
- [ ] La orientación y la inclinación son correctas.
- [ ] Los contactos con terreno están identificados.
- [ ] Las sombras relevantes están presentes.
- [ ] Cada superficie puede mapearse a una solución constructiva.
- [ ] La zonificación permite asignar condiciones operacionales y sistemas.

## 13. Matriz de responsabilidad

| Información | Revit | IFC | Modelo analítico | Modelo energético |
|---|---:|---:|---:|---:|
| Geometría arquitectónica | Principal | Transporta | Simplifica | Consume |
| Recintos | Define | Transporta | Valida o reconstruye | Agrupa en zonas |
| Superficies | Implícitas en elementos | Representa geometría | Genera y relaciona | Asigna construcción |
| Adyacencias | Deben ser deducibles | Puede transportarlas parcialmente | Determina y corrige | Consume |
| Huecos | Modela y hospeda | Clasifica y transporta | Asocia a superficies | Asigna propiedades |
| Sombras | Modela las relevantes | Transporta geometría | Genera o simplifica | Calcula efecto solar |
| Condiciones operacionales | Puede contener datos auxiliares | Puede transportar referencias | Puede agrupar | Define y calcula |
| Sistemas | Modelo separado o datos auxiliares | Puede transportar información | No es su función principal | Define y simula |

## 14. Consecuencia para la preparación en Revit

El modelo Revit no necesita contener todas las variables energéticas, pero sí debe proporcionar una base geométrica que permita:

1. Identificar volúmenes cerrados.
2. Deducir límites y contactos.
3. Reconocer huecos y superficies exteriores.
4. Mantener orientación y estructura vertical.
5. Simplificar sin perder el efecto térmico relevante.
6. Repetir la exportación y comparar versiones.

Estas necesidades se convertirán en reglas concretas en los capítulos posteriores.

## 15. Fuentes principales

- EnergyPlus, *EnergyPlus Essentials*, apartados “Zones Are Not the Same as Rooms”, “Thermal Zones and Surfaces” y “One Construction Per Surface”.
- EnergyPlus 25.1, *Input Output Reference*.
- CYPE, *Open BIM Analytical Model. Manual de uso* (`CYPE-OBAM-01`).
- iMventa Ingenieros, *Manual TK-CEEP* (`IMVENTA-CEEP`).
