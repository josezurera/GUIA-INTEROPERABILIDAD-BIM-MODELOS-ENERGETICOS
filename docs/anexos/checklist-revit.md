---
title: Checklist operativo Revit–IFC
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
---

# Checklist operativo Revit–IFC

Esta lista resume los controles de las puertas 1 y 2. Debe utilizarse junto con los criterios detallados del capítulo QA/QC.

## A. Identificación

- [ ] Proyecto, edificio y estado de cálculo identificados.
- [ ] Archivo RVT y revisión correctos.
- [ ] Versión y compilación de Revit registradas.
- [ ] Versión del exportador IFC registrada.
- [ ] Receptor y versión definidos.
- [ ] Configuración IFC aprobada seleccionada.
- [ ] Archivos de parámetros y mapeado versionados.

## B. Coordenadas y orientación

- [ ] Ubicación geográfica comprobada.
- [ ] Norte verdadero comprobado con una fachada conocida.
- [ ] Punto base y punto topográfico revisados.
- [ ] Coordenadas compartidas verificadas.
- [ ] Geometría cerca del origen interno.
- [ ] Punto de control X, Y, Z documentado.
- [ ] Cotas y unidades correctas.

## C. Niveles, fases y opciones

- [ ] Niveles relevantes tienen nombres únicos.
- [ ] Cotas y orden vertical son correctos.
- [ ] Solo niveles reales están marcados como plantas de edificio.
- [ ] La división por nivel sigue el perfil IFC aprobado.
- [ ] Fase de la vista y del ajuste IFC son coherentes.
- [ ] Elementos demolidos no se superponen a los nuevos.
- [ ] La opción de diseño exportada es completa.

## D. Habitaciones, espacios y zonas

- [ ] Se ha elegido habitaciones o espacios como fuente única.
- [ ] Todos los volúmenes relevantes están representados.
- [ ] No quedan recintos sin colocar o no cerrados sin justificar.
- [ ] El cálculo de áreas y volúmenes está activo.
- [ ] Límites superior e inferior son correctos.
- [ ] Patinillos, cámaras, plénums y atrios están resueltos.
- [ ] Espacios no acondicionados están identificados.
- [ ] Códigos de zona térmica están completos.
- [ ] No existen espacios duplicados o solapados.

## E. Envolvente

- [ ] Muros, suelos y cubiertas forman un cierre razonable.
- [ ] No faltan cerramientos principales.
- [ ] No existen elementos duplicados.
- [ ] Uniones muro–suelo y muro–cubierta están revisadas.
- [ ] Restricciones verticales son coherentes.
- [ ] Exterior, terreno, medianería e interiores están clasificados.
- [ ] Cerramientos parcialmente enterrados están identificados.
- [ ] Elementos decorativos no delimitan espacios.
- [ ] Estructuras compuestas y materiales están revisados.

## F. Huecos

- [ ] Ventanas y puertas utilizan categorías adecuadas.
- [ ] Las familias cortan el anfitrión.
- [ ] Dimensiones nominales y de hueco están documentadas.
- [ ] Área transparente y fracción de marco son verificables.
- [ ] Antepechos, dinteles, niveles y orientación son correctos.
- [ ] Puertas acristaladas siguen una estrategia definida.
- [ ] Lucernarios conservan anfitrión e inclinación.
- [ ] Muros cortina distinguen paneles transparentes y opacos.
- [ ] Los montantes no se contabilizan dos veces.

## G. Sombras y contexto

- [ ] Elementos de sombra relevantes están inventariados.
- [ ] Voladizos, balcones y retranqueos conservan dimensiones.
- [ ] Lamas fijas están simplificadas de forma controlada.
- [ ] Protecciones móviles tienen escenario.
- [ ] Edificios vecinos están correctamente situados.
- [ ] Vegetación y topografía siguen criterios documentados.
- [ ] El contexto gráfico innecesario está excluido.
- [ ] El estudio solar de control es coherente.

## H. Geometrías de riesgo

- [ ] Aristas cortas y ángulos agudos están revisados.
- [ ] No existen grandes solapes ni caras concurrentes.
- [ ] Curvas, muros inclinados y elípticos tienen ensayo.
- [ ] Dobles curvaturas están facetadas o simplificadas.
- [ ] Cubiertas complejas conservan volumen.
- [ ] Huecos próximos a bordes no crean residuos.
- [ ] Recintos pequeños y cámaras siguen una estrategia.
- [ ] Escaleras, rampas y atrios están revisados.
- [ ] Dobles pieles responden al modelo térmico previsto.
- [ ] Mallas y familias in situ han sido validadas.

## I. Parámetros

- [ ] Archivo de parámetros compartidos correcto.
- [ ] GUID, nombres y tipos de dato son los aprobados.
- [ ] Campos obligatorios completos.
- [ ] Enumeraciones contienen valores permitidos.
- [ ] Códigos de elemento no están duplicados.
- [ ] Espacios y zonas tienen códigos estables.
- [ ] Cerramientos y huecos tienen código de construcción.
- [ ] Prestaciones térmicas incluyen fuente y alcance.
- [ ] No quedan valores de prueba.
- [ ] Elementos pendientes aparecen como `TO_REVIEW`.

## J. Vista y configuración IFC

- [ ] Vista 3D dedicada y plantilla correctas.
- [ ] No se utiliza ocultación temporal.
- [ ] Caja de sección corresponde al alcance.
- [ ] Categorías y vínculos están revisados.
- [ ] Se usa configuración guardada, no de sesión.
- [ ] Esquema IFC corresponde al receptor.
- [ ] Fuente de espacios está incluida.
- [ ] Nivel de límites espaciales está aprobado.
- [ ] Estrategia de vínculos evita duplicidades.
- [ ] Base de coordenadas está documentada.
- [ ] Psets comunes y personalizados están configurados.
- [ ] Cantidades base están activadas si corresponde.
- [ ] Nivel de detalle geométrico está aprobado.
- [ ] Estrategia de GlobalIds está definida.

## K. Validación del IFC

- [ ] Nombre y hash del IFC registrados.
- [ ] El archivo abre en un visor independiente.
- [ ] Esquema y cabecera son correctos.
- [ ] Proyecto, sitio, edificio y plantas existen.
- [ ] Punto de control y norte coinciden.
- [ ] `IfcSpace` contiene todos los espacios previstos.
- [ ] Entidades principales tienen recuentos coherentes.
- [ ] No faltan fachadas, suelos o cubiertas.
- [ ] Huecos están relacionados con sus anfitriones.
- [ ] No existen elementos duplicados o muy alejados.
- [ ] Psets EEM están presentes.
- [ ] El IFC cumple la especificación IDS aplicable.
- [ ] El informe HTML/JSON de IDS está archivado.
- [ ] Unidades y tipos de propiedades son correctos.
- [ ] Cantidades base se compararon con Revit.
- [ ] GlobalIds son válidos y únicos.
- [ ] Diferencias de área y volumen cumplen tolerancias.

## L. Importación y actualización

- [ ] Aplicación, versión y método de importación registrados.
- [ ] No existen mensajes bloqueantes.
- [ ] Espacios analíticos coinciden con el alcance.
- [ ] Superficies tienen tipo y adyacencias correctos.
- [ ] Huecos están asignados al cerramiento correcto.
- [ ] Sombras necesarias están presentes.
- [ ] Construcciones se transfieren o reasignan de forma controlada.
- [ ] Se ha realizado ensayo de actualización.
- [ ] Asignaciones manuales se conservan o se pueden repetir.

## M. Cierre

- [ ] No existen incidencias S1 o S2 abiertas.
- [ ] Incidencias S3 están cuantificadas y aceptadas.
- [ ] Evidencias están archivadas.
- [ ] Archivos entregados coinciden con sus hashes.
- [ ] Las cuatro puertas aplicables están aprobadas.
- [ ] Revisor, fecha y resultado final están registrados.

## Datos de aprobación

```text
Proyecto:
Estado de cálculo:
RVT y revisión:
IFC y hash:
Configuración IFC:
Receptor y versión:
Resultado:
Limitaciones:
Revisado por:
Fecha:
```
