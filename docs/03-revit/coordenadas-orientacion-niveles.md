---
title: Coordenadas, orientación y niveles en Revit 2026
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
software:
  nombre: Autodesk Revit
  version_base: "2026"
---

# Coordenadas, orientación y niveles en Revit 2026

La ubicación, la orientación y la estructura vertical condicionan la radiación solar, las sombras, el contacto con terreno, la organización de espacios y la posición relativa de las aportaciones IFC. Un edificio geométricamente correcto puede producir resultados erróneos si se exporta con el norte equivocado, plantas duplicadas o una base de coordenadas diferente de la acordada.

Este capítulo establece una estrategia reproducible para Revit 2026 y separa tres cuestiones que suelen confundirse:

1. Posición interna del modelo.
2. Posición real o compartida en el emplazamiento.
3. Posición y orientación elegidas para la exportación IFC.

## 1. Por qué importa en análisis energético

### 1.1 Orientación

La orientación de fachadas y huecos influye directamente en:

- Radiación solar incidente.
- Ganancias solares.
- Funcionamiento de protecciones.
- Distribución de cargas por orientaciones.
- Sombras propias y remotas.

Un giro de todo el edificio puede mantener intactas áreas y volúmenes, pero modificar sustancialmente el resultado energético.

### 1.2 Ubicación

La ubicación geográfica permite seleccionar o asociar:

- Datos climáticos.
- Latitud y longitud.
- Altitud.
- Zona climática reglamentaria.
- Trayectoria solar.

El programa energético puede solicitar estos datos de nuevo, pero deben ser coherentes con el modelo geométrico y con el norte exportado.

### 1.3 Cotas

Las elevaciones afectan a:

- Altura de plantas y espacios.
- Contacto con terreno.
- Sombras.
- Superficies exteriores.
- Relación entre edificios y obstáculos.
- Estructura `IfcBuildingStorey`.

## 2. Sistemas de referencia en Revit

Revit utiliza un sistema interno y proporciona puntos de referencia para trabajar con coordenadas de proyecto y levantamiento.

### 2.1 Origen interno

El origen interno es el punto de partida del sistema de coordenadas interno. Constituye la referencia fundamental para la geometría del modelo y no debe tratarse como un marcador que pueda reubicarse libremente.

Recomendaciones:

- Modelar el edificio cerca del origen interno.
- Mantener la geometría principal dentro de límites razonables.
- No desplazar el edificio grandes distancias para alcanzar coordenadas geográficas reales.
- Utilizar coordenadas compartidas o georreferenciación para relacionarlo con el mundo real.

Autodesk recomienda mantener toda la geometría dentro de 10 millas o 16 km del origen interno. Para interoperabilidad analítica se buscará una extensión mucho más contenida siempre que sea posible.

### 2.2 Punto base del proyecto

El punto base establece una referencia local útil para medir y posicionar el proyecto. Puede situarse, por ejemplo, en:

- Intersección de ejes principales.
- Esquina estable del edificio.
- Punto de replanteo acordado.
- Origen contractual del proyecto.

Debe documentarse:

- Descripción del punto.
- Coordenadas locales.
- Elevación.
- Ángulo respecto al norte verdadero.
- Estado fijado o protegido.

Mover el punto base no equivale necesariamente a mover la geometría. Debe evitarse su manipulación sin conocer el efecto sobre las coordenadas mostradas y compartidas.

### 2.3 Punto topográfico

El punto topográfico relaciona el modelo con el sistema de levantamiento o coordenadas compartidas. Resulta especialmente importante cuando existen:

- Varios edificios.
- Topografía.
- Modelos de distintas disciplinas.
- Obstáculos remotos.
- Coordenadas cartográficas.

No debe utilizarse como sustituto del origen interno. Su función es proporcionar contexto real al modelo.

### 2.4 Coordenadas de proyecto y compartidas

Las coordenadas de proyecto permiten trabajar en un sistema local cómodo. Las coordenadas compartidas permiten mantener una posición común entre archivos.

La estrategia recomendada es:

1. Modelar cerca del origen interno.
2. Definir un punto base local estable.
3. Establecer la relación con el levantamiento mediante coordenadas compartidas.
4. Verificar la posición de vínculos.
5. Seleccionar explícitamente la base de exportación IFC.

## 3. Proyecto Norte y Norte verdadero

Revit mantiene dos orientaciones:

- **Proyecto Norte:** orienta el edificio para facilitar el modelado y la documentación.
- **Norte verdadero:** representa el norte real del emplazamiento.

Autodesk recomienda comenzar el modelado con el eje predominante del edificio alineado según Proyecto Norte y definir el Norte verdadero cuando existan datos fiables del emplazamiento.

### 3.1 Regla para análisis energético

El modelo energético debe utilizar el Norte verdadero, directa o indirectamente. La vista de trabajo puede mantenerse orientada a Proyecto Norte, pero la exportación debe conservar el ángulo real.

### 3.2 Comprobaciones

- Mostrar una vista de emplazamiento orientada a Norte verdadero.
- Colocar una flecha o referencia gráfica de comprobación.
- Registrar el ángulo entre ambos nortes.
- Comparar una fachada conocida con su orientación esperada.
- Verificar el resultado en el visor IFC y en el receptor.

### 3.3 Riesgos

- Girar la geometría en lugar de configurar el Norte verdadero.
- Girar el Norte de proyecto después de documentar.
- Duplicar el giro en Revit y en el programa energético.
- Exportar usando una base orientada a Proyecto Norte cuando el receptor espera Norte verdadero.
- Aplicar manualmente una rotación adicional en el receptor.

## 4. Ubicación geográfica

El modelo debe registrar, al menos:

- Municipio o emplazamiento.
- Latitud y longitud cuando proceda.
- Altitud.
- Zona horaria.
- Norte verdadero.

La ubicación utilizada para trayectoria solar debe coincidir con la utilizada por el motor energético. Si el programa energético selecciona sus propios datos climáticos, la ubicación de Revit seguirá siendo relevante para comprobar orientación y sombras.

## 5. Base de coordenadas para exportación IFC

El exportador IFC de Revit permite seleccionar diferentes bases:

- Coordenadas compartidas.
- Punto topográfico.
- Punto base del proyecto.
- Origen interno.
- Punto base orientado al Norte verdadero.
- Origen interno orientado al Norte verdadero.

No existe una opción universal para todos los proyectos. La elección depende de si el archivo se utilizará aislado o coordinado con otras aportaciones.

### 5.1 Modelo aislado

Para un edificio analizado sin contexto federado puede ser conveniente utilizar una base próxima al edificio y orientada al Norte verdadero. Esto reduce magnitudes de coordenadas y mantiene la orientación solar.

### 5.2 Proyecto federado

Cuando el modelo debe coincidir con topografía, otros edificios o sombras remotas, normalmente será necesario utilizar coordenadas compartidas verificadas.

### 5.3 Decisión por flujo

| Flujo | Base candidata | Condición |
|---|---|---|
| Open BIM Analytical Model | Compartidas o base acordada | Debe coincidir con BIMserver.center y otras aportaciones. |
| TK-IFC importación | Base local próxima | Debe conservar orientación y evitar coordenadas excesivas. |
| TeKton3D vinculación | Compartidas o local documentada | Debe coincidir con referencias usadas para calcar. |

La tabla es una hipótesis inicial. Se cerrará mediante pruebas.

## 6. Referencia cartográfica y EPSG

En exportaciones IFC4, Revit puede incluir una referencia de sistema proyectado mediante código EPSG. Esta información permite documentar:

- Sistema de referencia.
- Datum geodésico.
- Coordenadas Este y Norte.
- Elevación.
- Ángulo respecto al Norte verdadero.

Debe utilizarse únicamente cuando el proyecto disponga de una referencia cartográfica confirmada. No debe inventarse un EPSG para completar el campo.

## 7. Precisión y distancia al origen

Las coordenadas de gran magnitud pueden reducir la precisión de algunas operaciones geométricas o receptores. Para minimizar riesgos:

- Mantener la geometría de Revit cerca del origen interno.
- Evitar importar CAD con geometría remota.
- Limpiar puntos u objetos alejados.
- No trasladar físicamente el modelo a coordenadas UTM.
- Ensayar la base IFC con el receptor.

El control debe medir tanto la posición del edificio como la extensión total de toda la geometría exportada.

## 8. Vínculos y coordenadas compartidas

Todos los vínculos relevantes deben usar una estrategia coherente:

- Origen a origen durante etapas tempranas controladas.
- Punto base a punto base cuando exista una convención común.
- Coordenadas compartidas para coordinación consolidada.

Antes de exportar se comprobará:

- Método de posicionamiento.
- Sitio compartido activo.
- Giro.
- Elevación.
- Coincidencia de ejes y niveles.
- Ausencia de desplazamientos manuales no registrados.

Restablecer coordenadas compartidas rompe relaciones con modelos vinculados y devuelve el punto topográfico al origen interno. Esta operación no debe realizarse como corrección improvisada en un modelo coordinado.

## 9. Niveles de Revit

Un nivel es un datum horizontal que puede representar una planta funcional o una referencia auxiliar. No todos los niveles deben convertirse en plantas IFC.

### 9.1 Niveles funcionales

Representan plantas utilizables o divisiones espaciales relevantes:

- Planta baja.
- Plantas superiores.
- Sótanos.
- Cubierta cuando constituye una planta funcional.
- Entreplantas.

### 9.2 Niveles auxiliares

Sirven para modelado o documentación:

- Coronación de peto.
- Cara inferior de forjado.
- Nivel de cimentación.
- Arranque de cubierta.
- Cota de falso techo.
- Descansillo.
- Nivel estructural auxiliar.

Estos niveles no deberían generar automáticamente `IfcBuildingStorey` salvo que representen una división espacial necesaria.

## 10. Parámetro Planta de edificio

El parámetro `Building Story` o Planta de edificio indica que el nivel corresponde a una planta funcional, frente a niveles como antepechos o descansillos.

Autodesk indica que:

- Revit exporta los niveles con Planta de edificio activada.
- Si ningún nivel la tiene activada, puede exportar niveles utilizados como base de elementos.
- La opción de dividir muros, columnas y conductos por nivel utiliza estos niveles.

### 10.1 Regla recomendada

Activar Planta de edificio únicamente en niveles que deban aparecer como `IfcBuildingStorey`.

### 10.2 Excepciones

Un nivel auxiliar puede necesitar exportarse si:

- Define una planta parcial con espacios propios.
- Se utiliza como contenedor espacial real.
- El receptor necesita distinguir esa cota.

La excepción debe documentarse.

## 11. Parámetro Planta superior

`Story Above` permite indicar cuál es la siguiente planta cuando se dividen elementos por niveles. Por defecto suele adoptar la siguiente planta de edificio superior.

Debe revisarse en:

- Dobles alturas.
- Plantas partidas.
- Entreplantas.
- Niveles auxiliares intercalados.
- Edificios con sectores verticales diferentes.

Una relación incorrecta puede producir cortes de elementos o alturas de planta inesperadas.

## 12. Cota del nivel y altura de planta

La cota de un nivel no contiene por sí sola la altura de planta. Esta se deduce mediante la relación con el nivel superior o mediante los límites de los espacios.

Debe diferenciarse:

- Cota de suelo acabado.
- Cota estructural.
- Cota de cara superior de forjado.
- Altura libre.
- Altura total del espacio.

La convención de niveles debe indicar qué representa cada cota.

## 13. Altura de cálculo de habitaciones

El parámetro `Computation Height` define la altura sobre el nivel a la que Revit calcula el perímetro, área y volumen de la habitación.

Puede afectar a recintos con:

- Muros inclinados.
- Cubiertas inclinadas.
- Cambios de sección.
- Huecos o retranqueos próximos al suelo.

No debe modificarse globalmente para resolver un caso aislado sin comprobar su impacto en todas las habitaciones del nivel.

## 14. Relación entre habitaciones y niveles

Cada habitación debe revisar:

- Nivel base.
- Desfase de base.
- Límite superior.
- Desfase de límite.
- Volumen resultante.

El límite superior no debe elegirse solo porque sea el siguiente nivel en la lista. Debe representar el cierre real del volumen térmico.

## 15. Edificios con plantas partidas

En edificios *split-level* pueden existir varias cotas funcionales dentro de una planta general.

Estrategias posibles:

1. Varios niveles de planta de edificio.
2. Un nivel principal y desfases en espacios y elementos.
3. Plantas parciales relacionadas mediante una convención.

La elección debe minimizar plantas IFC innecesarias y mantener los espacios en cotas correctas. Se ensayará cuál interpreta mejor cada receptor.

## 16. Dobles alturas

Una doble altura no debe cerrarse artificialmente mediante un nivel intermedio. Se comprobará:

- Habitación o espacio continuo.
- Límite superior real.
- Forjados parciales.
- Adyacencias verticales.
- Planta IFC de pertenencia.

El espacio puede pertenecer a la planta donde se sitúa su base aunque atraviese otra planta.

## 17. Sótanos y contacto con terreno

Las cotas deben permitir distinguir:

- Planta completamente enterrada.
- Planta semienterrada.
- Muros parcialmente en contacto con terreno.
- Solera.
- Superficies expuestas a exterior.

Un único plano de terreno global puede ser insuficiente para edificios escalonados. La condición final deberá verificarse en el modelo analítico.

## 18. Cubiertas y niveles superiores

No siempre es necesario crear una planta IFC para cada nivel de cubierta. Se distinguirán:

- Nivel de planta bajo cubierta.
- Arranque de cubierta.
- Cumbrera.
- Coronación.
- Planta técnica de cubierta.

Solo los niveles que organizan espacios o elementos como una planta funcional deberían marcarse como Planta de edificio.

## 19. Varios edificios en un proyecto

Cuando un archivo Revit contiene varios edificios, deben definirse:

- Referencia común de coordenadas.
- Norte verdadero común.
- Estructura de sitios y edificios IFC.
- Niveles propios o compartidos.
- Responsabilidad de sombras entre edificios.

Puede ser preferible separar los modelos o las aportaciones cuando cada edificio se calcula independientemente.

## 20. Tabla de planificación de niveles

Se recomienda una tabla con:

- Nombre.
- Elevación.
- Planta de edificio.
- Planta superior.
- Estructural.
- Descripción o código.
- Uso en IFC.
- Observaciones.

Debe existir una revisión explícita que identifique niveles auxiliares y funcionales.

## 21. Vista de control de coordenadas

Se preparará una vista de emplazamiento o 3D que muestre:

- Origen interno.
- Punto base.
- Punto topográfico.
- Ejes principales.
- Flecha de Norte verdadero.
- Vínculos relevantes.
- Punto de control conocido.

La vista formará parte del informe QA/QC.

## 22. Comprobación en IFC

Después de exportar debe verificarse:

- Orientación respecto al Norte verdadero.
- Cotas de plantas.
- Número y nombre de `IfcBuildingStorey`.
- Contención de elementos.
- Posición de vínculos u obstáculos.
- Unidades.
- Coordenadas globales o locales esperadas.
- Ausencia de desplazamientos o giros duplicados.

## 23. Comprobación en Open BIM Analytical Model

Se revisará:

- Coincidencia con el resto de aportaciones de BIMserver.center.
- Orientación de fachadas.
- Sombras propias y remotas.
- Plantas cargadas.
- Cotas de espacios.
- Contacto con terreno.

## 24. Comprobación en TeKton3D

En importación:

- Plantas nativas creadas.
- Elevaciones y alturas.
- Orientación.
- Posición de espacios y cerramientos.

En vinculación:

- Niveles IFC cargados como plantas cuando se usa `Insertar/Edificio IFC`.
- Coincidencia de cota cero por planta.
- Norte y posición del vínculo.
- Actualización sin desplazamiento.

## 25. Matriz de decisiones

| Decisión | Debe quedar registrada en |
|---|---|
| Punto base local | BEP o protocolo del modelo |
| Sistema compartido | Protocolo de coordinación |
| Norte verdadero | Información de proyecto |
| Base de exportación IFC | Configuración IFC |
| EPSG | Información geográfica |
| Niveles de planta | Matriz de niveles |
| Niveles auxiliares | Matriz de exclusión |
| Planta superior | Tabla de niveles |
| Criterio de cota | Convención de modelado |

## 26. Checklist previo a exportación

- [ ] Geometría principal cerca del origen interno.
- [ ] Punto base definido y documentado.
- [ ] Punto topográfico y coordenadas compartidas verificados.
- [ ] Ubicación geográfica confirmada.
- [ ] Norte verdadero comprobado.
- [ ] Ángulo respecto a Proyecto Norte registrado.
- [ ] Base de exportación IFC seleccionada.
- [ ] EPSG confirmado o conscientemente omitido.
- [ ] Vínculos posicionados mediante un método conocido.
- [ ] Niveles funcionales identificados.
- [ ] Niveles auxiliares excluidos como plantas IFC.
- [ ] `Building Story` revisado.
- [ ] `Story Above` revisado en casos especiales.
- [ ] Cotas y alturas de habitaciones verificadas.
- [ ] Sótanos, terreno y cubiertas revisados.

## 27. Ensayo propuesto para Revit 2026

Se generarán exportaciones controladas utilizando:

1. Origen interno.
2. Origen interno orientado al Norte verdadero.
3. Punto base del proyecto.
4. Punto base orientado al Norte verdadero.
5. Coordenadas compartidas.

El modelo de prueba tendrá:

- Giro conocido de 30° respecto al Norte verdadero.
- Tres plantas funcionales.
- Dos niveles auxiliares.
- Un edificio vinculado.
- Un obstáculo remoto.
- Una planta semienterrada.

Se documentará qué opción conserva correctamente posición, norte, plantas y sombras en cada receptor.

## 28. Fuentes principales

- Autodesk, *About Positioning*, Revit 2026.
- Autodesk, *About Project North and True North*, Revit 2026.
- Autodesk, *Move the Project Base Point*, Revit 2026.
- Autodesk, *IFC Export Setup Options*.
- Autodesk, *Level Instance Properties*.
- CYPE, *Guía de interoperabilidad CYPE-Revit v2.0* (`CYPE-REVIT-20`).

