# Guía de preparación de modelos BIM para análisis energético

Manual técnico vivo sobre preparación geométrica en Autodesk Revit, intercambio IFC y generación de modelos analíticos para motores de cálculo energético.

## Alcance inicial

- Autodesk Revit 2026 y posteriores.
- Open BIM Analytical Model y CYPETHERM HE Plus.
- TeKton3D TK-IFC y TK-CEEP.
- Arquitectura preparada para incorporar DesignBuilder y otras aplicaciones.

## Estado

Versión `0.2.0` en revisión - Revit 2026, preparación IFC y procedimiento QA/QC. Las páginas identifican por separado los contenidos confirmados, recomendados, pendientes de validación y obsoletos.

## Desarrollo local

1. Instalar Python 3.11 o posterior.
2. Ejecutar `pip install -r requirements.txt`.
3. Ejecutar `mkdocs serve`.
4. Abrir la dirección local indicada por MkDocs.

La fuente oficial es el contenido Markdown de `docs/`. La web y los PDF son productos derivados.

## Validación IFC mediante IDS

El repositorio incluye una especificación IDS 1.0 y un validador reproducible basado en IfcTester:

1. Instalar `pip install -r requirements-ids.txt`.
2. Ejecutar `python scripts/validar_ids.py --audit-only` para auditar el IDS.
3. Ejecutar `python scripts/validar_ids.py ruta/al/modelo.ifc` para validar un IFC.

Los informes HTML y JSON se guardan en `reports/ids/`. GitHub también ejecuta esta comprobación sobre los modelos no confidenciales incluidos en `tests/ifc/`.

## Lectura y revisión

- La rama `main` se publica como web estable mediante GitHub Pages.
- Cada solicitud de cambios genera una vista previa HTML en `pr-preview/pr-N/` y añade el enlace a la conversación de GitHub.
- Cada etiqueta de versión con formato `v*` genera una GitHub Release con el manual completo en PDF.
- Markdown continúa siendo la fuente editable y trazable.

## Contribuciones

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) antes de proponer cambios. Las modificaciones técnicas deben indicar su fuente, versión de software y estado de validación.

## Licencia

El contenido se publica bajo [Creative Commons Attribution 4.0 International](LICENSE).
