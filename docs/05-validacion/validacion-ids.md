---
title: Validación automática de IFC mediante IDS
estado: en_revision
version: 0.2.0
ultima_revision: 2026-07-12
---

# Validación automática de IFC mediante IDS

La guía adopta **Information Delivery Specification (IDS) 1.0**, estándar de buildingSMART, para expresar y comprobar requisitos de información sobre archivos IFC.

La herramienta seleccionada es **IfcTester 0.8.5**, incluida en el ecosistema abierto IfcOpenShell. Permite validar desde línea de comandos y generar informes HTML y JSON reproducibles. El ejecutable de la guía añade una prevalidación del esquema mediante `ifcopenshell.validate`.

## 1. Qué comprueba IDS

IDS puede exigir, entre otros:

- Existencia de entidades.
- Tipo predefinido.
- Atributos.
- Propiedades y valores.
- Clasificaciones.
- Materiales.
- Relaciones de pertenencia.

La especificación inicial `eem-ifc-minimo-v0.1.ids` comprueba:

- Proyecto, emplazamiento y edificio identificados.
- Existencia de plantas.
- Existencia de espacios `IfcSpace`.
- Nombre en muros, losas, cubiertas, ventanas y puertas cuando existan.

El complemento `eem-ifc2x3-complemento-v0.1.ids` incorpora reglas para entidades habituales de IFC2x3, inicialmente `IfcWallStandardCase`.

La especificación `eem-energia-semantica-v0.1.ids` añade controles funcionales:

- Referencia de espacios.
- Clasificación interior/exterior de cerramientos y huecos.
- Transmitancia térmica de elementos clasificados como exteriores.

## 2. Perfiles de validación

La herramienta ofrece dos perfiles:

| Perfil | Uso | Especificaciones |
|---|---|---|
| `minimum` | Intercambio básico y regresión | IDS mínimo y complemento IFC2x3 |
| `energy` | Preparación del modelo energético | Perfil mínimo más semántica energética |

El perfil energético es deliberadamente más exigente y puede fallar en IFC válidos para coordinación general.

Antes de aplicar los IDS, la herramienta registra y comprueba:

- Esquema IFC.
- Conformidad de atributos, tipos y cardinalidades con el esquema.
- Aplicación y versión de origen.
- Hash SHA-256 y tamaño.
- Inventario exacto de entidades principales.
- GlobalIds ausentes, duplicados o inválidos.

## 3. Qué no comprueba IDS por sí solo

- Calidad de la geometría BRep o teselada.
- Cierre de todos los volúmenes.
- Coincidencia de áreas y volúmenes con Revit.
- Orientación solar correcta.
- Adyacencias reconstruidas por el receptor.
- Uso efectivo de una propiedad en CYPE o TeKton3D.
- Coherencia física de resultados.

Por eso IDS se integra en la Puerta 2, pero no sustituye las otras comprobaciones QA/QC.

## 4. Archivos incorporados

```text
config/ids/eem-ifc-minimo-v0.1.ids
config/ids/eem-ifc2x3-complemento-v0.1.ids
config/ids/eem-energia-semantica-v0.1.ids
scripts/validar_ids.py
requirements-ids.txt
.github/workflows/validate-ifc-ids.yml
tests/ifc/
```

## 5. Ejecución local

Instalar una vez las dependencias:

```powershell
python -m pip install -r requirements-ids.txt
```

Auditar el propio IDS:

```powershell
python scripts/validar_ids.py --profile energy --audit-only
```

Validar un IFC:

```powershell
python scripts/validar_ids.py "C:\ruta\modelo.ifc"
```

Validación energética ampliada:

```powershell
python scripts/validar_ids.py --profile energy "C:\ruta\modelo.ifc"
```

Los informes se generan en `reports/ids/`:

- HTML para lectura humana.
- JSON para automatización.
- `resumen.json` con el resultado global.
- `resumen.html` con prevalidación, inventario y requisitos fallidos.
- Un JSON de prevalidación por IFC.

El proceso devuelve:

- `0`: cumple.
- `1`: incumple algún requisito.
- `2`: error de uso, archivo o IDS.

## 6. Ejecución en GitHub

La acción **Validar IFC con IDS**:

1. Instala versiones fijadas de IfcOpenShell e IfcTester.
2. Audita la sintaxis del IDS.
3. Busca archivos en `tests/ifc/`.
4. Valida cada IFC encontrado.
5. Publica informes HTML y JSON como artefactos durante 30 días.
6. Marca la acción como fallida si un IFC no cumple.

Si no existe ningún IFC público de ensayo, la acción audita únicamente la especificación y finaliza correctamente.

Los IFC reales colocados en `tests/ifc/` están excluidos de Git por defecto para impedir su publicación accidental. Solo se versionará un modelo adicional mediante una decisión expresa y después de confirmar que no contiene información confidencial.

## 7. Interpretación del resultado

Un resultado **CUMPLE** significa que el IFC supera la prevalidación y satisface todos los requisitos expresados en los IDS aplicados. No significa que el modelo energético completo esté aprobado.

Un resultado **NO CUMPLE** debe convertirse en una incidencia con:

- Especificación e identificador fallidos.
- GlobalId o entidad afectada.
- Archivo y hash.
- Revit y configuración de exportación.
- Corrección en origen o excepción justificada.

## 8. Versionado del IDS

Los IDS se tratan como configuración de proyecto:

- Nombre con versión.
- Historial en Git.
- Auditoría de sintaxis.
- Prueba contra modelos conformes y no conformes.
- Cambio de versión cuando se añaden o modifican requisitos.

Una entrega debe registrar el nombre y hash del IDS utilizado.

## 9. Diagnóstico energético complementario

El resumen calcula, incluso cuando no se activa el perfil energético:

- Número de `IfcRelSpaceBoundary`.
- Relaciones de materiales.
- Cobertura de `IsExternal`.
- Cobertura de `ThermalTransmittance`.
- Espacios con cantidades de área.
- Espacios con cantidades de volumen.

Estas métricas no sustituyen a IDS: ayudan a identificar si una carencia afecta a un elemento aislado o a toda una categoría.

### 9.1 EEM-SPA-001 — Pilares no delimitadores

Para el modelo energético, los pilares no deben subdividir el contorno de las habitaciones o espacios. Mantenerlos como delimitadores puede generar entrantes, caras muy pequeñas y geometrías analíticas innecesariamente complejas.

En Revit 2026 y versiones posteriores se establece este criterio de preparación:

1. Seleccionar los pilares arquitectónicos y estructurales que estén dentro del volumen térmico.
2. Desactivar el parámetro **Delimitación de habitación** (`Room Bounding`).
3. Regenerar y revisar las habitaciones y los espacios MEP.
4. Comprobar áreas y volúmenes antes de exportar.
5. Exportar los límites espaciales al IFC cuando el flujo y el MVD utilizado lo permitan.

La regla complementaria `EEM-SPA-001` recorre las relaciones `IfcRelSpaceBoundary` y localiza aquellas cuyo elemento relacionado es un `IfcColumn`. Sus resultados son:

- **PASS**: existen límites espaciales y ningún pilar delimita un `IfcSpace`.
- **FAIL**: al menos un `IfcColumn` participa como límite; el informe identifica espacio, pilar, `GlobalId` y planta.
- **NOT_EVALUABLE**: existen espacios, pero el IFC no contiene `IfcRelSpaceBoundary`.
- **NOT_APPLICABLE**: el archivo no contiene ningún `IfcSpace`.

En el perfil `energy`, tanto **FAIL** como **NOT_EVALUABLE** impiden declarar conforme el modelo. Esta comprobación no puede formularse únicamente con IDS 1.0 y se ejecuta como regla QA/QC complementaria. Tampoco permite conocer directamente el valor original del parámetro de Revit: comprueba su consecuencia en las relaciones exportadas.

Autodesk indica que los pilares pueden tener activada por defecto la delimitación de habitación y recomienda desactivarla cuando provoque volúmenes incorrectos o innecesariamente fragmentados. Véanse [About Room Area — Revit 2026](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-ArchDesign/files/GUID-9348929C-18CA-40AC-BB64-71D01CC52F2B.htm) y [Situations That Can Affect Room Volume Computations — Revit 2026](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-ArchDesign/files/GUID-052DFFB9-5076-4CE6-BC8B-420C8D03ACF0.htm).

## 10. Evolución prevista

Después de probar el mapeado `EEM_EnergyExchange`, se añadirá una segunda especificación para exigir:

- `ElementCode`.
- `ConstructionCode`.
- `BoundaryType`.
- `EnergyRole`.
- `ThermalZoneCode`.
- `Conditioning`.
- `ExportStatus`.
- `QAStatus`.

No se activarán estos requisitos como bloqueantes hasta verificar su exportación en IFC2x3 e IFC4 y su compatibilidad con los receptores.

## 11. Validación complementaria

IDS debe combinarse con:

- Validación del esquema IFC.
- Comparación cuantitativa Revit–IFC.
- Inspección geométrica.
- Revisión del modelo analítico.
- Ensayos de actualización.
- Ensayos de sensibilidad del cálculo.

## 12. Fuentes

- buildingSMART International, *Information Delivery Specification (IDS)*.
- buildingSMART International, *IFC Validation Service*.
- IfcOpenShell, *IfcTester documentation*.
