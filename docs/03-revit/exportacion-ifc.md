---
title: Configuraciones de exportación IFC desde Revit 2026
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
software:
  nombre: Autodesk Revit
  version_base: "2026"
---

# Configuraciones de exportación IFC desde Revit 2026

La configuración de exportación forma parte del modelo entregado. Dos archivos obtenidos del mismo RVT pueden contener espacios, propiedades, coordenadas y geometrías distintas si cambian la vista, el esquema, la fase o las opciones IFC.

Este capítulo establece un procedimiento reproducible y propone configuraciones candidatas para los flujos con Open BIM Analytical Model, CYPETHERM HE Plus y TeKton3D. Los valores definitivos se aprobarán mediante ensayos con las versiones realmente instaladas.

!!! warning "No utilizar la configuración en sesión para entregas"
    Autodesk indica que los cambios realizados en `<In-Session Setup>` no se conservan entre sesiones. Toda exportación reproducible debe utilizar una configuración con nombre, registrada y verificada.

## 1. Objetivos

La exportación debe:

- Contener solo la geometría necesaria.
- Conservar espacios, cerramientos, huecos y sombras previstos.
- Mantener coordenadas, orientación y niveles.
- Utilizar entidades IFC reconocibles.
- Incluir propiedades y cantidades aprobadas.
- Evitar duplicados y contenido gráfico irrelevante.
- Permitir actualizar el modelo en el receptor.
- Poder repetirse por otra persona con idéntico resultado.

## 2. Componentes de una configuración reproducible

No basta con guardar el nombre del ajuste IFC. Deben registrarse:

- Versión exacta de Revit.
- Compilación de Revit.
- Versión del exportador IFC.
- Esquema y vista de definición del modelo.
- Requisito de intercambio, si se utiliza.
- Vista 3D de exportación.
- Fase.
- Opción de diseño.
- Sistema de coordenadas.
- Tratamiento de vínculos.
- Límites espaciales.
- Categorías incluidas y mapeado.
- Psets, cantidades y archivos externos.
- Nivel de detalle geométrico.
- Opciones avanzadas.
- Nombre y hash del IFC resultante.

## 3. Versiones de Revit y del exportador

Autodesk señala que el exportador IFC se actualiza periódicamente con funciones y correcciones. Por tanto, `Revit 2026` no identifica por sí solo el entorno.

Cada entrega registrará:

```text
Revit: 2026.x
Build: <compilación>
IFC Exporter: <versión>
Sistema operativo: <versión>
Fecha: AAAA-MM-DD
```

Una actualización del exportador obliga a repetir, al menos, el modelo mínimo de regresión antes de adoptarla.

El ensayo del 13 de julio de 2026 registró Revit 2026.2, compilación `26.2.0.20`, y el exportador integrado `Revit.IFC.Export.dll` `26.2.0.20`. Los resultados completos se recogen en [Ensayo Revit 2026–IFC–MVD](ensayo-revit-2026-mvd.md).

## 4. Configuraciones candidatas

Se mantendrán tres perfiles independientes:

| Nombre propuesto | Destino | Estado inicial |
|---|---|---|
| `EEM_CYPE_ANALYTICAL` | BIMserver.center y Open BIM Analytical Model | IFC4 RV SB1, candidato pendiente del receptor |
| `EEM_TEKTON_IMPORT` | Importación en TK-IFC | Comparar IFC2x3 CV2 SB0 y SB1 |
| `EEM_TEKTON_LINK` | Vinculación y actualización en TK-IFC | Comparar IFC4 RV SB0 y SB1 |

Los nombres son convenciones del manual. No implican una certificación por parte de CYPE o iMventa.

La exportación técnica de estos candidatos ya se ha reproducido. La palabra **candidato** significa que el IFC supera o caracteriza el control previo, pero aún no ha sido aprobado dentro de la aplicación receptora.

## 5. Selección del esquema IFC

Revit admite exportación IFC2x3, IFC4 y variantes asociadas a diferentes vistas de definición.

La selección se realizará por este orden:

1. Esquema admitido oficialmente por el receptor y su versión.
2. Esquema que conserva los elementos energéticos necesarios.
3. Esquema que permite actualización estable.
4. Menor complejidad compatible con los requisitos.

### 5.1 IFC2x3 Coordination View 2.0

Es una opción candidata cuando el receptor tiene una trayectoria consolidada con IFC2x3. Debe verificarse:

- Exportación de `IfcSpace`.
- Límites espaciales.
- Cantidades.
- Psets personalizados.
- Geometría de curvas y huecos.
- Persistencia de GlobalIds.

### 5.2 IFC4 Reference View

Es una opción candidata para intercambio de referencia y vinculación cuando el receptor la admita. Debe comprobarse especialmente:

- Representaciones teseladas.
- Entidades de tipo.
- Relaciones de aberturas.
- Materiales y capas.
- Compatibilidad real del importador.

### 5.3 IFC4 Design Transfer View

Puede generar representaciones geométricas diferentes, incluidas BReps avanzadas en ciertos casos. No se elegirá por contener mayor detalle nominal, sino por evidencia de mejor interoperabilidad.

### 5.4 Regla de aprobación

El esquema se aprobará por receptor. No es obligatorio utilizar el mismo IFC para todos los destinos si una configuración específica ofrece mayor fiabilidad.

## 6. Tipo de archivo

Para validación y trazabilidad se recomienda inicialmente `.ifc` STEP sin comprimir porque facilita:

- Inspección del encabezado.
- Cálculo de diferencias.
- Diagnóstico de entidades.
- Uso por validadores.

`.ifczip` puede utilizarse para distribución cuando todos los receptores lo admitan. El archivo descomprimido original y su hash se conservarán en el registro de entrega.

IFC XML no se utilizará salvo requisito explícito.

## 7. Vista 3D de exportación

Se creará una vista dedicada, por ejemplo:

`EEM_IFC_EXPORT_<DESTINO>`

Características:

- Vista 3D no dependiente.
- Disciplina y detalle documentados.
- Fase y filtro de fase correctos.
- Opción de diseño prevista.
- Plantilla de vista bloqueada.
- Categorías controladas.
- Sin ocultaciones temporales.
- Caja de sección desactivada para entrega completa, salvo exportación parcial intencionada.

### 7.1 Elementos visibles

Autodesk indica que la opción **Export only elements visible in view** utiliza la visibilidad de la vista, con matices sobre elementos ocultos, recortes y ocultación temporal. Por ello no se confiará en una inspección superficial.

La vista debe verificarse mediante:

- Visibilidad/gráficos.
- Filtros.
- Subcategorías.
- Worksets.
- Vínculos.
- Fases.
- Opciones.
- Elementos ocultos permanentemente.

### 7.2 Ocultación temporal

No se utilizará como mecanismo de preparación porque puede no comportarse como espera el usuario y no queda suficientemente documentada.

## 8. Categorías incluidas

Para el núcleo energético se evaluarán:

- Habitaciones o espacios.
- Muros.
- Suelos.
- Cubiertas.
- Techos relevantes.
- Ventanas.
- Puertas.
- Muros cortina, paneles y montantes necesarios.
- Aberturas.
- Elementos de sombra.
- Topografía necesaria.

Se excluirán salvo necesidad:

- Anotaciones 2D.
- Mobiliario.
- Equipamiento no relacionado con zonas o cargas.
- Detalles constructivos.
- Barandillas y perfiles menores irrelevantes.
- Vegetación gráfica.
- Importaciones auxiliares.

La exclusión se gestionará mediante vista y plantilla de mapeado, no eliminando elementos del modelo de autoría.

## 9. Mapeado de categorías IFC

Revit 2026 permite crear plantillas de mapeado, seleccionar categorías y asignar clase IFC y tipo predefinido.

El repositorio conservará un archivo por perfil cuando existan diferencias:

```text
config/ifc/category-mapping/
  EEM_CYPE_ANALYTICAL_v001.txt
  EEM_TEKTON_IMPORT_v001.txt
  EEM_TEKTON_LINK_v001.txt
```

Reglas:

- Partir de una plantilla Autodesk identificada.
- Modificar solo categorías justificadas.
- No exportar categorías irrelevantes.
- No usar `IfcBuildingElementProxy` como solución general.
- Registrar clase y tipo predefinido esperados.
- Ensayar familias con `IfcExportAs` por separado.

## 10. Fase de exportación

La fase debe coincidir con el estado energético analizado:

- Existente.
- Proyecto o reformado.
- Escenario específico.

Cuando se exporta solo lo visible en vista, la fase puede depender de la propia vista. Debe comprobarse la interacción entre:

- Fase de la vista.
- Filtro de fase.
- Fase seleccionada en el ajuste IFC.
- Fase de habitaciones o espacios.

No se admitirán cerramientos existentes y nuevos superpuestos por una combinación incorrecta.

## 11. Opciones de diseño

Se exportará una alternativa completa cada vez. El nombre del archivo y registro deben indicar la opción.

Antes de exportar:

- Confirmar opción primaria o visible.
- Revisar elementos del modelo principal.
- Comprobar habitaciones y espacios.
- Evitar mezclar huecos de una opción con cerramientos de otra.

## 12. Niveles y plantas de edificio

Solo los niveles que estructuran el edificio deben marcarse como plantas de edificio.

Se comprobará:

- `Building Story`.
- Cota.
- Nombre único.
- Orden vertical.
- Correspondencia con plantas analíticas.
- Contenedor `IfcBuildingStorey`.

Niveles auxiliares de antepecho, cubierta o coordinación no deben crear plantas IFC innecesarias.

## 13. División por niveles

La opción de dividir muros, pilares y conductos por nivel puede mejorar la contención por plantas, pero también cambia entidades y GlobalIds.

Se decidirá por perfil mediante ensayo:

### Activada

Ventajas posibles:

- Elementos asociados a cada planta.
- Geometría más manejable.
- Correspondencia con superficies por nivel.

Riesgos:

- Fragmentación excesiva.
- Dificultad de seguimiento de un muro continuo.
- Cambios de identificadores.

### Desactivada

Ventajas posibles:

- Conservación del elemento de autoría.
- Menos entidades.

Riesgos:

- Receptor incapaz de dividir correctamente por espacios o plantas.

## 14. Habitaciones y espacios

Se elegirá una única fuente principal, como se estableció en el capítulo correspondiente.

Con exportación limitada a una vista 3D, Autodesk ofrece una opción específica para incluir habitaciones dentro de la caja de sección o todas si no existe caja activa.

Comprobar:

- Que se exportan como `IfcSpace`.
- Que tienen geometría 3D.
- Que pertenecen al nivel correcto.
- Que no se duplican habitaciones y espacios MEP.
- Que área y volumen son coherentes.
- Que conservan nombre, número y códigos EEM.

## 15. Límites espaciales

Revit permite exportar:

- Ninguno.
- Primer nivel.
- Segundo nivel.

### 15.1 Sin límites

Puede reducir el archivo, pero obliga al receptor a reconstruir completamente las relaciones.

### 15.2 Primer nivel

Incluye límites sin optimizarlos respecto a espacios al otro lado.

### 15.3 Segundo nivel

Considera espacios adyacentes y puede dividir límites con mayor detalle, ofreciendo información útil para propiedades térmicas.

### 15.4 Criterio de selección

No se asumirá que segundo nivel siempre es mejor. Para cada receptor se comparará:

- Número de relaciones.
- Tiempo y tamaño.
- Superficies duplicadas.
- Adyacencias recuperadas.
- Errores de importación.
- Necesidad de reconstrucción en el receptor.

## 16. Volumen de habitaciones

La opción de utilizar límites 2D para el volumen simplifica las habitaciones como extrusiones. Puede ser inadecuada para cubiertas inclinadas, dobles alturas o geometría compleja.

Para el flujo energético se preferirá inicialmente la geometría volumétrica calculada por Revit, sometida a comparación, salvo que el receptor requiera expresamente el método 2D o el ensayo demuestre mayor estabilidad.

Se comprobarán:

- Cubiertas inclinadas.
- Espacios bajo escalera.
- Atrios.
- Plénums.
- Habitaciones con límites no verticales.

## 17. Vínculos Revit e IFC

Autodesk permite:

- No exportar vínculos.
- Exportarlos como IFC separados.
- Incluirlos en un mismo `IfcProject`.
- Incluirlos en un mismo `IfcSite`.

### 17.1 Estrategia preferente inicial

Cuando sea viable, cada disciplina exportará su archivo desde el modelo fuente y se coordinará mediante coordenadas compartidas. Esto preserva autoría y reduce duplicidades.

### 17.2 Exportación conjunta

Solo se utilizará si el receptor lo requiere y después de comprobar:

- Posición.
- Fases.
- Contenedores espaciales.
- GlobalIds.
- Materiales.
- Duplicidad de elementos.
- Tamaño del archivo.

### 17.3 Vínculos delimitadores

La condición `Room Bounding` del vínculo afecta a habitaciones y espacios del anfitrión, pero no implica automáticamente que el vínculo se incluya en el IFC. Son decisiones independientes.

## 18. Coordenadas y referencia geográfica

La base de coordenadas debe ser coherente con la estrategia del proyecto y con el receptor.

Se ensayarán solo las opciones necesarias, documentando:

- Origen interno.
- Punto base del proyecto.
- Punto topográfico.
- Coordenadas compartidas.
- Emplazamiento seleccionado.
- Elevación de `IfcSite`.
- Ángulo respecto al norte verdadero.

### 18.1 Modelo federado

Para coordinación, todos los archivos deben coincidir sin movimientos manuales posteriores.

### 18.2 Modelo analítico local

Si un receptor funciona mejor cerca del origen, podrá utilizarse una exportación local específica, siempre que se conserve una transformación documentada y no se pierda la orientación solar.

### 18.3 Elevación del emplazamiento

La opción de incluir la elevación de `IfcSite` en el origen local puede cambiar la interpretación vertical. Se comprobará con un punto de control de cota conocida.

## 19. Norte verdadero

Después de exportar se verificará:

- Orientación del edificio.
- Ángulo del emplazamiento.
- Fachada de control.
- Posición solar en el receptor.

No basta con que el IFC se superponga visualmente: una rotación compensada por el visor podría ocultar un norte incorrecto.

## 20. Conjuntos de propiedades

Se activarán de forma selectiva:

### 20.1 Psets comunes IFC

Recomendados cuando aportan propiedades normalizadas y el receptor las interpreta.

### 20.2 Psets de Revit

Pueden ser útiles para diagnóstico, pero aumentan el archivo y exponen información interna. No se activarán en la configuración mínima sin necesidad.

### 20.3 Tablas como Psets

Se utilizarán solo las tablas destinadas al intercambio y, si está disponible, se limitarán a nombres con `IFC`, `Pset` o `Common` según la regla definida.

### 20.4 Psets personalizados

Se asociará el archivo o configuración `EEM_EnergyExchange` aprobado para la versión de Revit.

### 20.5 Tabla de mapeado

La ruta, versión y hash se incluirán en el registro de exportación.

## 21. Cantidades base

Se activarán para comparar geometría cuando el esquema y receptor las admitan.

Revisar:

- Área bruta y neta.
- Volumen.
- Ancho y alto de huecos.
- Longitud y espesor.
- Tratamiento de aberturas.

Las cantidades base no sustituyen el cálculo geométrico del receptor; sirven para contrastarlo.

## 22. Nivel de detalle geométrico

Revit permite varios niveles que afectan a teselación y representación de determinados elementos.

La elección seguirá este procedimiento:

1. Exportar en nivel bajo o medio.
2. Comprobar superficies relevantes.
3. Aumentar detalle solo si falta geometría necesaria.
4. Comparar tamaño, tiempo y resultados.

Un nivel alto puede mejorar curvas y perfiles, pero también crear más caras y errores. No se utilizará por defecto.

## 23. Geometría teselada y BRep

Opciones como conservar triangulación o permitir representaciones mixtas pueden mejorar compatibilidad con ciertos visores y empeorarla con otros.

Se comprobarán con:

- Muros curvos.
- Cubiertas complejas.
- Rampas y escaleras.
- Espacios no prismáticos.
- Sombras.

No se activarán opciones avanzadas que se aparten de la vista de definición sin una necesidad documentada.

## 24. Piezas y elementos constructivos

La exportación de piezas como elementos estándar o `IfcBuildingElementPart` puede cambiar la interpretación de la envolvente.

Para análisis energético se preferirá inicialmente el anfitrión completo, salvo que:

- La división represente construcciones térmicas diferentes.
- El receptor gestione las piezas correctamente.
- No se dupliquen superficies.

## 25. Nombres de tipos y referencias

Se decidirá si el nombre IFC del tipo incluye familia y tipo o solo tipo. El criterio debe:

- Mantener códigos de construcción.
- Evitar nombres duplicados.
- Ser legible en el receptor.
- Permanecer estable entre revisiones.

No se cambiará esta opción después de iniciar una vinculación sin evaluar su efecto en la actualización.

## 26. Almacenamiento de GUID IFC

Guardar el GUID IFC en parámetros Revit puede facilitar trazabilidad, pero modifica el modelo después de exportar.

Antes de activarlo se definirá:

- Quién tiene permiso para modificar el RVT.
- Cuándo se sincroniza.
- Cómo afecta al trabajo compartido.
- Si conserva GUID entre configuraciones y esquemas.
- Qué ocurre con elementos divididos por nivel.

La opción se aprobará mediante ensayo de persistencia.

## 27. Cabecera, dirección y clasificación

La cabecera debe contener información coherente de autoría y aplicación. La dirección y localización deben corresponder al proyecto.

Se evitarán:

- Datos de prueba.
- Nombres personales innecesarios.
- Direcciones incompletas que aparenten validación.
- Clasificaciones sin sistema y edición identificados.

## 28. Nomenclatura del archivo

Propuesta:

```text
<PROYECTO>_<DISCIPLINA>_<DESTINO>_<ESTADO>_<REV>_<AAAA-MM-DD>.ifc
```

Ejemplo:

```text
EEM_ARQ_CYPE_TEST_R03_2026-07-12.ifc
```

El nombre no sustituye metadatos ni hash, pero facilita identificar entregas.

## 29. Registro de exportación

Cada IFC tendrá un registro con:

- Nombre y hash SHA-256.
- Tamaño.
- Fecha y hora.
- Autor de exportación.
- RVT fuente y revisión.
- Vista.
- Configuración IFC.
- Esquema.
- Fase y opción.
- Coordenadas.
- Archivos de mapeado y Psets.
- Número de espacios y elementos principales.
- Validadores utilizados.
- Receptores probados.
- Incidencias conocidas.

## 30. Propuesta inicial por perfil

Los siguientes valores son una **hipótesis de ensayo**, no una receta aprobada:

| Ajuste | CYPE Analytical | TeKton Import | TeKton Link |
|---|---|---|---|
| Esquema | Probar IFC2x3 CV2.0 e IFC4 RV | Probar primero el recomendado por TK-IFC | Priorizar esquema con mejor persistencia |
| Vista dedicada | Sí | Sí | Sí |
| Espacios | Sí | Sí | Sí |
| Límites | Comparar 1.º/2.º/ninguno | Según reconstrucción | Según actualización |
| Psets comunes | Sí, a verificar | Sí, a verificar | Sí, a verificar |
| Cantidades base | Sí | Sí | Sí |
| Pset EEM | Sí | Sí | Sí |
| Vínculos | Preferentemente separados | Según proyecto | Según estrategia de vínculo |
| Detalle | Bajo/medio inicial | Bajo/medio inicial | Bajo/medio inicial |

La primera matriz del exportador quedó ejecutada con Revit 2026.2. En el modelo mínimo, SB2 no aportó más relaciones espaciales que SB1 en IFC2x3 CV2 o IFC4 RV y elevó de cuatro a doce las incidencias de esquema. Por ello no se adopta SB2 como ajuste general para el exportador `26.2.0.20`. La matriz por receptor se cerrará después de las importaciones en Open BIM Analytical Model y TeKton3D.

## 31. Procedimiento de exportación

1. Abrir la revisión RVT aprobada.
2. Confirmar versión de Revit y exportador.
3. Resolver advertencias que afecten al alcance.
4. Revisar tablas EEM y campos obligatorios.
5. Activar cálculo de volúmenes si corresponde.
6. Abrir la vista de exportación.
7. Confirmar fase, opción, categorías y vínculos.
8. Seleccionar la configuración IFC con nombre.
9. Verificar rutas de mapeados y Psets.
10. Exportar a carpeta de trabajo limpia.
11. Calcular hash y registrar tamaño.
12. Abrir en un visor independiente.
13. Ejecutar validaciones geométricas y semánticas.
14. Importar o actualizar en el receptor.
15. Registrar resultados y aprobar o rechazar.

## 32. Comprobación inmediata

Antes de entregar se verificarán:

- El archivo abre sin error.
- Proyecto, sitio, edificio y plantas existen.
- Coordenadas y norte son correctos.
- Los espacios están presentes.
- Los cerramientos y huecos tienen entidades adecuadas.
- No faltan cubiertas, suelos o fachadas.
- Las sombras previstas están disponibles o documentadas.
- Psets y cantidades aparecen.
- No se ha exportado contenido irrelevante masivo.

## 33. Comparación entre exportaciones

Cuando se cambie un ajuste, solo debe modificarse una variable cada vez.

Comparar:

- Tamaño del archivo.
- Número de entidades por clase.
- Número de espacios.
- GlobalIds conservados.
- Áreas y volúmenes.
- Tiempo de importación.
- Incidencias del receptor.

Así se identifica qué opción produce cada efecto.

## 34. Ensayo de actualización

La vinculación exige una prueba específica:

1. Exportar versión A.
2. Vincular o importar.
3. Asignar datos en el receptor.
4. Mover un hueco.
5. Cambiar el tipo de un cerramiento.
6. Añadir un espacio.
7. Eliminar un elemento.
8. Exportar versión B con idéntica configuración.
9. Actualizar.
10. Comprobar qué datos y correcciones se conservan.

Una configuración que importa bien pero destruye asignaciones al actualizar no es adecuada para un flujo iterativo.

## 35. Errores frecuentes

| Síntoma | Causa probable | Revisión inicial |
|---|---|---|
| Faltan habitaciones | Vista 3D sin opción de exportarlas | Contenido adicional y caja de sección |
| Aparecen elementos demolidos | Fase o filtro incorrectos | Vista y ajuste IFC |
| El edificio está desplazado | Base de coordenadas o `IfcSite` | Punto de control y referencia geográfica |
| Se duplican vínculos | Exportación conjunta y archivos separados | Estrategia de vínculos |
| Faltan propiedades EEM | Archivo de Psets o mapeado no activo | Rutas y versión |
| IFC demasiado pesado | Psets Revit, detalle alto o contexto | Contenido y teselación |
| Muros fragmentados | División por niveles | Ajuste y plantas de edificio |
| Se pierden asignaciones al actualizar | GlobalIds o descomposición cambiantes | Persistencia y configuración |
| Curvas deformadas | Nivel de detalle o representación | Ensayo bajo/medio/alto |
| Receptor rechaza IFC4 | Compatibilidad parcial | Esquema realmente admitido |

## 36. Criterios de aceptación

Una configuración estará aprobada para un receptor cuando:

- Está guardada con nombre y versión.
- Se conoce la versión de Revit y exportador.
- El esquema es admitido por el receptor.
- Coordenadas, norte y plantas son correctos.
- Los espacios y límites necesarios se conservan.
- Entidades, Psets y cantidades cumplen el diccionario.
- La geometría está dentro de tolerancias.
- El archivo tiene complejidad manejable.
- La importación no requiere reparaciones no documentadas.
- La actualización conserva identificadores y asignaciones aceptables.
- El ensayo de regresión está registrado.

## 37. Checklist de entrega

- [ ] Se utiliza una configuración guardada, no la de sesión.
- [ ] Revit y el exportador IFC están identificados.
- [ ] El esquema corresponde al receptor.
- [ ] La vista 3D dedicada está activa y revisada.
- [ ] Fase y opción de diseño son correctas.
- [ ] Solo se incluyen categorías necesarias.
- [ ] Habitaciones o espacios se exportan una sola vez.
- [ ] Los límites espaciales siguen el perfil aprobado.
- [ ] Niveles de edificio y división por plantas están verificados.
- [ ] La estrategia de vínculos evita duplicados.
- [ ] Coordenadas, elevación y norte verdadero están comprobados.
- [ ] Psets, cantidades y mapeados corresponden a su versión.
- [ ] El detalle geométrico ha superado el ensayo.
- [ ] Los GlobalIds siguen la estrategia de persistencia.
- [ ] Cabecera y dirección son correctas.
- [ ] El nombre, hash y registro de exportación están creados.
- [ ] El IFC se ha inspeccionado en un visor independiente.
- [ ] El receptor ha importado o actualizado correctamente.

## 38. Modelo de ensayo

El mismo modelo de referencia se exportará con combinaciones controladas de:

- IFC2x3 CV2.0 e IFC4 RV.
- Límites espaciales ninguno, primero y segundo.
- División por niveles activada y desactivada.
- Volumen 2D y geometría calculada.
- Detalle bajo, medio y alto.
- Vínculos separados y combinados.
- Coordenadas locales y compartidas.
- Psets mínimos y ampliados.

Los resultados completarán la matriz definitiva de cada receptor en las versiones 0.3 y 0.4.

## 39. Fuentes principales

- Autodesk, *Exporting to Industry Foundation Classes (IFC)*, Revit 2026.
- Autodesk, *About Revit and IFC*, Revit 2026.
- Autodesk, *Export a Model to IFC*, Revit 2026.
- Autodesk, *Customize the IFC Setup*, Revit 2026.
- Autodesk, *IFC Export Setup Options*.
- Autodesk, *Manage IFC Export Mapping Settings*, Revit 2026.
- Autodesk, *Supported IFC Classes*, Revit 2026.
- Autodesk, *Use Room Boundaries in a Linked Model*, Revit 2026.
