# Exportación IFC

Se mantendrán configuraciones diferenciadas según el receptor:

- `IFC_CYPE_ANALYTICAL` para BIMserver.center y Open BIM Analytical Model.
- `IFC_TEKTON_IMPORT` para importación IFC2x3 en TK-IFC.
- `IFC_TEKTON_LINK` para vinculación, inicialmente orientada a IFC4.

Los nombres son convenciones de este manual y deberán adaptarse al entorno de cada organización.

OpenStudio no se añade a esta lista porque la ruta inicial propuesta utiliza el modelo analítico de energía de Revit exportado como **gbXML 7.03**, no una importación IFC directa. IFC podrá conservarse como evidencia complementaria y para controles geométricos, pero no se declarará formato de entrada de OpenStudio sin una implementación documentada y ensayada.

