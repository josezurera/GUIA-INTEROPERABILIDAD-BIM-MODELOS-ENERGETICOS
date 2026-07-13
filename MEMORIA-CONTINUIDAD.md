# Memoria de continuidad del proyecto

Última actualización: 13 de julio de 2026  
Estado: documento vivo  
Repositorio: <https://github.com/josezurera/GUIA-INTEROPERABILIDAD-BIM-MODELOS-ENERGETICOS>  
Rama de trabajo: `agent/revit-ifc-0.2`  
Pull request de revisión: <https://github.com/josezurera/GUIA-INTEROPERABILIDAD-BIM-MODELOS-ENERGETICOS/pull/1>  
Último commit antes de esta memoria: `165fbe0`

## 1. Objetivo del proyecto

Elaborar y mantener una guía versionada sobre preparación de modelos BIM para análisis energético, con especial atención a:

- Autodesk Revit 2026 y versiones posteriores.
- Exportación IFC reproducible.
- Preparación del modelo geométrico y analítico.
- CYPETHERM HE Plus mediante BIMserver.center y Open BIM Analytical Model.
- TeKton3D TK-IFC y TK-CEEP.
- OpenStudio y EnergyPlus.
- Validación IFC mediante IDS y reglas geométricas complementarias.
- Control de versiones, trazabilidad y QA/QC.

El manual se redacta en Markdown, se publica mediante MkDocs Material y se mantiene en GitHub. La publicación PDF se reserva para versiones etiquetadas.

## 2. Decisiones vigentes

1. La guía se aplica a Revit 2026 y versiones posteriores.
2. IFC se considera un contenedor de intercambio sometido a requisitos, no una garantía automática de calculabilidad.
3. Se distinguen tres modelos:
   - Modelo físico de Revit/IFC.
   - Modelo geométrico analítico.
   - Modelo energético utilizado por el motor de cálculo.
4. Los defectos deben corregirse en la fuente más temprana que los produce.
5. Las correcciones manuales en aplicaciones receptoras deben registrarse y comprobarse después de cada actualización.
6. No se aprobará una configuración IFC únicamente porque el archivo abra o se visualice correctamente.
7. La selección de esquema y MVD se realizará por receptor y mediante ensayos.
8. DesignBuilder queda pospuesto como ampliación futura.
9. OpenStudio es el nuevo receptor prioritario para la ampliación del manual.
10. Para OpenStudio se compararán tres rutas:
    - IFC directo.
    - IFC/modelo analítico a gbXML.
    - Generación directa de OSM mediante OpenStudio SDK.
11. La hipótesis preferente para OpenStudio es crear un modelo analítico intermedio común y generar OSM mediante SDK, pero todavía debe demostrarse mediante ensayo.
12. El documento de normas de modelado facilitado en `fuentes mias` es únicamente una fuente de contraste. El usuario indicó expresamente que no se modifique la guía a partir de ese documento sin una nueva autorización.

## 3. Estado de la documentación

### 3.1 Revit y preparación del modelo

Los siguientes capítulos están ampliamente redactados:

- Estrategia de modelado.
- Coordenadas, orientación y niveles.
- Habitaciones, espacios y zonas.
- Preparación de la envolvente.
- Huecos y elementos transparentes.
- Sombras y geometría exterior.
- Geometrías de riesgo.
- Parámetros y mapeado IFC.
- Configuración y exportación IFC.
- Checklist de Revit.

Estado real: **documentación base avanzada, todavía en revisión**.

### 3.2 IFC y MVD

La guía ya documenta conceptualmente:

- Diferencia entre esquema IFC, serialización y MVD.
- IFC2x3 Coordination View 2.0.
- IFC4 Reference View.
- IFC4 Design Transfer View.
- Estructura espacial.
- `IfcSpace`, `IfcZone` e `IfcRelSpaceBoundary`.
- Límites espaciales de primer y segundo nivel.
- Entidades, propiedades, cantidades, materiales y GUID.
- Criterios generales de selección por receptor.

Estado real: **no cerrado**. Las configuraciones siguen siendo hipótesis de ensayo.

### 3.3 CYPE

Están desarrollados:

- BIMserver.center y Plugin Open BIM - Revit.
- Open BIM Analytical Model.
- CYPETHERM HE Plus.
- Importación, actualización, publicación y trazabilidad.
- Geometría, recintos, superficies, huecos, sombras y aristas.
- Construcciones, zonas, sistemas y resultados.
- Revisión de avisos y ficheros de EnergyPlus.
- Ensayos de sensibilidad y criterios de aceptación.

El flujo principal documentado es:

`Revit 2026+ → Plugin Open BIM - Revit → BIMserver.center → Open BIM Analytical Model → BIMserver.center → CYPETHERM HE Plus`.

### 3.4 TeKton3D

Existe documentación sobre:

- TK-IFC y TK-CEEP.
- Importación y vinculación IFC.
- Diferenciación entre importación y enlace.
- Criterios generales de actualización y control.

Estado: documentado, pendiente de completar los ensayos por esquema y versión.

### 3.5 OpenStudio

Se ha creado la sección inicial con:

- Componentes del ecosistema OpenStudio.
- IFC, gbXML, OSM, OSW, IDF y EPW.
- Comparación de las tres rutas.
- Diagnóstico de los IFC disponibles.
- Propuesta de modelo analítico intermedio común.
- Correspondencia inicial de objetos IFC/analíticos con OpenStudio.
- Estrategia de actualización.
- QA/QC hasta EnergyPlus.
- Protocolo comparativo.

Página de vista previa:

<https://josezurera.github.io/GUIA-INTEROPERABILIDAD-BIM-MODELOS-ENERGETICOS/pr-preview/pr-1/04-aplicaciones/openstudio/>

## 4. Estado de las normas de modelado y del MVD

No debe afirmarse todavía que el bloque Revit–IFC–MVD está terminado.

### 4.1 Parte redactada

Las normas de modelado cubren prácticamente todos los temas previstos:

- Recintos y límites.
- Envolvente.
- Huecos.
- Sombras.
- Coordenadas.
- Niveles.
- Pilares no delimitadores.
- Geometrías complejas.
- Parámetros y mapeado.
- Exportación y QA/QC.

### 4.2 Parte pendiente de aprobación

Falta ejecutar y documentar el ensayo definitivo con Revit 2026 o posterior para aprobar:

1. Versión exacta de Revit y compilación.
2. Versión exacta del exportador IFC.
3. MVD recomendado para Open BIM Analytical Model.
4. MVD para importación en TK-IFC.
5. MVD para vinculación en TeKton3D.
6. MVD o ruta de intercambio para OpenStudio.
7. Exportación de habitaciones o espacios.
8. Límites espaciales de primer y segundo nivel.
9. Mapeado de `IsExternal`.
10. Cantidades de área y volumen.
11. Materiales, capas y propiedades térmicas.
12. Puertas acristaladas, muros cortina y huecos especiales.
13. Vínculos, coordenadas y Norte verdadero.
14. Estabilidad de `GlobalId`.
15. Conservación de asignaciones después de actualizar.

### 4.3 Perfiles que deben cerrarse

| Perfil | Destino | Estado |
|---|---|---|
| `EEM_CYPE_ANALYTICAL` | BIMserver.center/Open BIM Analytical Model | Pendiente de matriz por versión |
| `EEM_TEKTON_IMPORT` | Importación TK-IFC | Pendiente de ensayo IFC2x3/IFC4 |
| `EEM_TEKTON_LINK` | Vinculación TeKton3D | Pendiente de persistencia |
| `EEM_OPENSTUDIO` | OpenStudio | Pendiente de crear y comparar rutas |

## 5. Próxima prioridad recomendada

Antes de seguir profundizando en OpenStudio, cerrar experimentalmente el bloque Revit–IFC–MVD:

1. Crear el modelo mínimo de interoperabilidad en Revit 2026.
2. Registrar Revit, compilación y exportador.
3. Preparar perfiles candidatos:
   - IFC2x3 Coordination View 2.0.
   - IFC4 Reference View.
   - IFC4 Design Transfer View, cuando esté disponible y tenga sentido.
4. Exportar exactamente el mismo modelo con cada perfil.
5. Ejecutar el validador IDS y las reglas geométricas.
6. Comparar entidades, espacios, áreas, volúmenes, límites, huecos, materiales y coordenadas.
7. Probar las exportaciones en Open BIM Analytical Model, TeKton3D y OpenStudio.
8. Modificar controladamente el modelo y repetir la exportación.
9. Medir persistencia de identificadores y asignaciones.
10. Aprobar un perfil por receptor.
11. Guardar las configuraciones y evidencias.
12. Cambiar el estado documental solo cuando el ensayo esté aprobado.

## 6. Herramienta de validación IFC

El repositorio incluye:

- Especificaciones IDS versionadas en `config/ids/`.
- Validador en `scripts/validar_ids.py`.
- Informes HTML y JSON.
- Auditoría de esquema y GUID.
- Inventario de entidades.
- Cobertura de propiedades energéticas.
- Regla `EEM-SPA-001`: pilares que delimitan espacios.
- Regla `EEM-GEO-001`: intersecciones entre espacios.
- Pruebas automáticas y flujo de GitHub Actions.

IDS no puede comprobar por sí solo todas las condiciones geométricas. Las intersecciones, coplanaridad, cierre de sólidos y relaciones espaciales complejas requieren reglas complementarias.

## 7. Diagnóstico de los IFC locales

Los IFC reales utilizados para ensayo se encuentran localmente en `tests/ifc`, pero están ignorados por Git y no se transferirán al clonar el repositorio en otro equipo.

### 7.1 `nave industrial.ifc`

- Revit 2019.
- IFC2X3.
- Sin `IfcSpace`.
- Sin `IfcZone`.
- Sin `IfcRelSpaceBoundary`.
- No sirve como base directa para generar un modelo energético.

### 7.2 `SUAREZ SOMONTE v2_Rv24_MDV_4STR.ifc`

- Revit 2024.
- IFC2X3.
- 17 `IfcSpace`.
- 17 espacios con geometría procesable.
- Sin intersecciones superiores a 2 mm en el ensayo realizado.
- Sin `IfcZone`.
- Sin `IfcRelSpaceBoundary`.
- Sin cantidades de área y volumen reconocidas.
- Cobertura aproximada de transmitancia:
  - Muros: 51 %.
  - Losas: 14 %.
  - Cubiertas: 0 %.
  - Ventanas y puertas: 100 % en las entidades comprobadas.

Conclusión: permite estudiar sólidos de espacios, pero requiere reconstruir superficies y adyacencias para generar gbXML u OSM.

### 7.3 Traslado a otro equipo

Los IFC de proyecto no deben publicarse sin autorización. Para continuar en otro equipo:

- Copiarlos por un medio autorizado a la misma carpeta `tests/ifc`, o
- Utilizar un modelo sintético no confidencial y versionarlo expresamente.

El archivo `eem-minimo-conforme.ifc` sí está versionado, pero no contiene geometría y solo prueba el funcionamiento básico del IDS.

## 8. Archivos locales que no están en GitHub

La carpeta `fuentes mias/` aparece como no versionada y pertenece al usuario. No se ha añadido a Git ni se ha modificado durante los últimos trabajos.

Al cambiar de equipo deben trasladarse separadamente, si siguen siendo necesarias:

- `fuentes mias/`.
- Los IFC reales de `tests/ifc` ignorados por Git.
- Cualquier modelo RVT.
- Informes locales no versionados.
- Manuales o PDF sujetos a derechos o confidencialidad.

## 9. Cómo retomar el proyecto en otro equipo

### 9.1 Obtener el repositorio

```powershell
git clone https://github.com/josezurera/GUIA-INTEROPERABILIDAD-BIM-MODELOS-ENERGETICOS.git
cd GUIA-INTEROPERABILIDAD-BIM-MODELOS-ENERGETICOS
git switch agent/revit-ifc-0.2
```

Si la rama ya se ha fusionado, utilizar `main` y consultar el pull request número 1 para recuperar el contexto histórico.

### 9.2 Preparar la documentación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
mkdocs serve
```

La dirección local habitual será `http://127.0.0.1:8000/`.

### 9.3 Preparar el validador IDS

```powershell
python -m pip install -r requirements-ids.txt
python scripts/validar_ids.py --profile energy --audit-only
python -m unittest discover -s tests -p "test_*.py"
```

Para validar un IFC local:

```powershell
python scripts/validar_ids.py --profile energy --output reports/ids "tests/ifc/modelo.ifc"
```

### 9.4 Comprobar el estado antes de trabajar

```powershell
git status
git log --oneline -10
```

No añadir automáticamente archivos locales o privados. Revisar siempre el alcance antes de ejecutar `git add`.

## 10. Publicación y control de calidad

La rama de trabajo actualiza una vista previa mediante el pull request número 1:

<https://josezurera.github.io/GUIA-INTEROPERABILIDAD-BIM-MODELOS-ENERGETICOS/pr-preview/pr-1/>

Los flujos automáticos comprueban:

- Construcción estricta de MkDocs.
- Vista previa HTML.
- Auditoría IDS y pruebas complementarias.
- Validación de los IFC de ensayo disponibles en el repositorio.

La publicación estable se realiza desde `main`. El PDF se genera al crear una versión etiquetada.

## 11. Últimos hitos

| Commit | Contenido |
|---|---|
| `13b5e3b` | BIMserver.center y Plugin Open BIM - Revit |
| `488d782` | Flujo Open BIM Analytical Model |
| `96088d7` | Flujo completo de CYPETHERM HE Plus |
| `165fbe0` | Análisis inicial de OpenStudio |

Todas las comprobaciones de GitHub asociadas al commit `165fbe0` finalizaron correctamente.

## 12. Regla para mantener esta memoria

Actualizar este archivo cuando cambie alguno de los siguientes elementos:

- Objetivo o receptor prioritario.
- Decisión sobre esquema o MVD.
- Versión base de Revit.
- Perfil IFC aprobado.
- Estado de una aplicación.
- Regla de validación.
- Ubicación de datos de ensayo.
- Rama, pull request o procedimiento de publicación.
- Próxima prioridad de trabajo.

La memoria describe el estado y las decisiones. La documentación técnica detallada permanece en `docs/` y el historial de cambios en Git.
