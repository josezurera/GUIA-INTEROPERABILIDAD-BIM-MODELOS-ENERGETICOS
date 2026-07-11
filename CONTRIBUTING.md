# Cómo contribuir

## Principios

- Una recomendación debe indicar a qué software y versiones aplica.
- Las afirmaciones técnicas deben enlazar una fuente oficial o describir una prueba reproducible.
- No se deben convertir experiencias aisladas en reglas universales.
- Los cambios deben mantener separados el modelo arquitectónico, el IFC, el modelo analítico y el modelo energético.

## Estados de evidencia

- **Confirmado:** respaldado por documentación oficial o prueba reproducible.
- **Recomendado:** criterio técnico razonado pendiente de generalización.
- **Pendiente de validación:** hipótesis que requiere ensayo.
- **Obsoleto:** contenido conservado únicamente como referencia histórica.

## Flujo de trabajo

1. Crear una incidencia describiendo la ampliación o corrección.
2. Crear una rama con un nombre como `feature/designbuilder` o `docs/revit-2027`.
3. Actualizar el contenido y, cuando proceda, `data/fuentes.yml` y `data/compatibilidad.yml`.
4. Actualizar `CHANGELOG.md`.
5. Abrir una solicitud de cambios para revisión.

## Requisitos de las páginas técnicas

Cada página específica de una aplicación debe declarar:

- Software y versión.
- Fecha de revisión.
- Estado de validación.
- Esquema IFC o formato de intercambio.
- Fuentes utilizadas.
- Limitaciones conocidas.

