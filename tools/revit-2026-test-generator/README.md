# Generador del ensayo Revit 2026–IFC–MVD

Este complemento crea localmente un modelo mínimo de dos recintos y exporta una matriz controlada de IFC2x3 CV2.0, IFC4 Reference View e IFC4 Design Transfer View con límites espaciales 0, 1 y 2.

## Requisitos

- Autodesk Revit 2026 instalado en la ruta predeterminada.
- Contenido español de Revit 2026.
- .NET SDK 8 o posterior.
- Ninguna sesión de Revit abierta con trabajo pendiente.

## Ejecución

```powershell
powershell -ExecutionPolicy Bypass -File tools/revit-2026-test-generator/run.ps1
```

Los resultados se escriben de forma predeterminada en `tmp/revit-2026-mvd` y no se incorporan a Git.

El complemento solo se activa cuando el lanzador define `EEM_REVIT_TEST_GENERATOR=1`. El manifiesto se instala temporalmente en el perfil del usuario y se elimina al finalizar.

Revit puede solicitar autorización para cargar el ensamblado sin firma. Debe elegirse **Cargar una vez**. En el ensayo documentado se utilizó una firma local temporal, retirada al finalizar, para evitar que ese diálogo interrumpiera el arranque automatizado.

La salida incluye el RVT, siete IFC, sus huellas SHA-256, un manifiesto del entorno y el registro de ejecución. Los resultados de referencia están resumidos en `docs/03-revit/ensayo-revit-2026-mvd.md`.
