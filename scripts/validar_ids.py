"""Prevalida IFC, comprueba IDS y genera informes HTML/JSON consolidados."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import ifcopenshell
import ifcopenshell.validate
from ifcopenshell.util.element import get_psets
from ifctester import ids as ids_module
from ifctester import reporter


PROFILES = {
    "minimum": [
        Path("config/ids/eem-ifc-minimo-v0.1.ids"),
        Path("config/ids/eem-ifc2x3-complemento-v0.1.ids"),
    ],
    "energy": [
        Path("config/ids/eem-ifc-minimo-v0.1.ids"),
        Path("config/ids/eem-ifc2x3-complemento-v0.1.ids"),
        Path("config/ids/eem-energia-semantica-v0.1.ids"),
    ],
}

INVENTORY_CLASSES = [
    "IfcProject",
    "IfcSite",
    "IfcBuilding",
    "IfcBuildingStorey",
    "IfcSpace",
    "IfcZone",
    "IfcWall",
    "IfcWallStandardCase",
    "IfcSlab",
    "IfcRoof",
    "IfcWindow",
    "IfcDoor",
    "IfcCurtainWall",
    "IfcColumn",
    "IfcBuildingElementProxy",
]


def safe_name(path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", path.stem)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def audit_ids(ids_paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for ids_path in ids_paths:
        try:
            ids_module.open(str(ids_path), validate=True)
            print(f"IDS válido: {ids_path}")
        except Exception as exc:  # pragma: no cover - mensaje depende de xmlschema
            errors.append(f"IDS no válido: {ids_path}: {exc}")
    return errors


def count_exact(ifc: ifcopenshell.file, class_name: str) -> int:
    try:
        return len(ifc.by_type(class_name, include_subtypes=False))
    except (RuntimeError, TypeError):
        try:
            return len(ifc.by_type(class_name))
        except RuntimeError:
            return 0


def header_metadata(ifc: ifcopenshell.file) -> dict[str, Any]:
    file_name = ifc.header.file_name
    return {
        "name": getattr(file_name, "name", None),
        "timestamp": getattr(file_name, "time_stamp", None),
        "preprocessor_version": getattr(file_name, "preprocessor_version", None),
        "originating_system": getattr(file_name, "originating_system", None),
        "authorization": getattr(file_name, "authorization", None),
    }


def application_metadata(ifc: ifcopenshell.file) -> list[dict[str, Any]]:
    applications: list[dict[str, Any]] = []
    for app in ifc.by_type("IfcApplication"):
        applications.append(
            {
                "name": getattr(app, "ApplicationFullName", None),
                "version": getattr(app, "Version", None),
                "identifier": getattr(app, "ApplicationIdentifier", None),
            }
        )
    return applications


def global_id_diagnostics(ifc: ifcopenshell.file) -> dict[str, Any]:
    roots = ifc.by_type("IfcRoot")
    values = [getattr(element, "GlobalId", None) for element in roots]
    missing = [element.id() for element, value in zip(roots, values) if not value]
    counts = Counter(value for value in values if value)
    duplicates = sorted(value for value, count in counts.items() if count > 1)
    invalid = sorted(
        value
        for value in counts
        if ifcopenshell.validate.validate_guid(value) is not None
    )
    return {
        "ifc_root_count": len(roots),
        "missing_count": len(missing),
        "missing_entity_ids": missing[:100],
        "duplicate_count": len(duplicates),
        "duplicate_values": duplicates[:100],
        "invalid_count": len(invalid),
        "invalid_values": invalid[:100],
    }


def schema_diagnostics(ifc_path: Path) -> dict[str, Any]:
    logger = ifcopenshell.validate.json_logger()
    ifcopenshell.validate.validate(str(ifc_path), logger, express_rules=False)
    statements = logger.statements
    return {
        "status": not statements,
        "issue_count": len(statements),
        "issues": statements[:500],
        "truncated": len(statements) > 500,
    }


def property_coverage(
    ifc: ifcopenshell.file, class_names: list[str], pset_name: str, property_name: str
) -> dict[str, Any]:
    elements = []
    for class_name in class_names:
        try:
            elements.extend(ifc.by_type(class_name, include_subtypes=False))
        except (RuntimeError, TypeError):
            continue
    passed = 0
    for element in elements:
        values = get_psets(element, psets_only=False, qtos_only=False).get(pset_name, {})
        if property_name in values and values[property_name] is not None:
            passed += 1
    total = len(elements)
    return {
        "classes": class_names,
        "pset": pset_name,
        "property": property_name,
        "total": total,
        "present": passed,
        "missing": total - passed,
        "percent": round(100 * passed / total, 2) if total else None,
    }


def quantity_coverage(ifc: ifcopenshell.file) -> dict[str, Any]:
    quantity_names = {
        "GrossFloorArea", "NetFloorArea", "GrossVolume", "NetVolume", "Area", "Volume"
    }
    spaces = ifc.by_type("IfcSpace", include_subtypes=False)
    with_area = 0
    with_volume = 0
    for space in spaces:
        psets = get_psets(space, psets_only=False, qtos_only=False)
        keys = {
            key
            for set_name, values in psets.items()
            if set_name.startswith("Qto_") or set_name == "BaseQuantities"
            for key in values
            if key != "id"
        }
        with_area += int(bool(keys & {"GrossFloorArea", "NetFloorArea", "Area"}))
        with_volume += int(bool(keys & {"GrossVolume", "NetVolume", "Volume"}))
    total = len(spaces)
    return {
        "space_total": total,
        "with_area_quantity": with_area,
        "with_volume_quantity": with_volume,
        "area_percent": round(100 * with_area / total, 2) if total else None,
        "volume_percent": round(100 * with_volume / total, 2) if total else None,
        "recognized_names": sorted(quantity_names),
    }


def entity_reference(entity: Any) -> dict[str, Any]:
    """Return stable identifiers suitable for JSON and QA/QC reports."""
    return {
        "entity_id": entity.id(),
        "ifc_class": entity.is_a(),
        "global_id": getattr(entity, "GlobalId", None),
        "name": getattr(entity, "Name", None),
    }


def containing_storey_name(element: Any) -> str | None:
    for relation in getattr(element, "ContainedInStructure", ()) or ():
        structure = getattr(relation, "RelatingStructure", None)
        if structure and structure.is_a("IfcBuildingStorey"):
            return getattr(structure, "Name", None)
    return None


def column_room_boundary_diagnostics(ifc: ifcopenshell.file) -> dict[str, Any]:
    """Detect columns exported as physical boundaries of IFC spaces.

    IDS 1.0 cannot express this relationship constraint. It is therefore a
    custom QA/QC rule evaluated from IfcRelSpaceBoundary relationships.
    """
    spaces = ifc.by_type("IfcSpace", include_subtypes=False)
    boundaries = ifc.by_type("IfcRelSpaceBoundary")
    incidents: list[dict[str, Any]] = []
    for boundary in boundaries:
        space = getattr(boundary, "RelatingSpace", None)
        element = getattr(boundary, "RelatedBuildingElement", None)
        if not space or not space.is_a("IfcSpace"):
            continue
        if not element or not element.is_a("IfcColumn"):
            continue
        incidents.append(
            {
                "boundary": entity_reference(boundary),
                "space": entity_reference(space),
                "column": entity_reference(element),
                "storey": containing_storey_name(element),
                "physical_or_virtual": getattr(
                    boundary, "PhysicalOrVirtualBoundary", None
                ),
                "internal_or_external": getattr(
                    boundary, "InternalOrExternalBoundary", None
                ),
            }
        )

    if not spaces:
        result = "NOT_APPLICABLE"
        explanation = "El modelo no contiene IfcSpace."
    elif incidents:
        result = "FAIL"
        explanation = "Uno o más pilares participan como límites de espacios."
    elif not boundaries:
        result = "NOT_EVALUABLE"
        explanation = (
            "El modelo contiene espacios, pero no exporta IfcRelSpaceBoundary; "
            "no puede certificarse que los pilares no delimiten habitaciones."
        )
    else:
        result = "PASS"
        explanation = "Ningún IfcColumn participa como límite de un IfcSpace."

    return {
        "rule": "EEM-SPA-001",
        "title": "Los pilares no deben delimitar habitaciones o espacios",
        "result": result,
        "status": result in {"PASS", "NOT_APPLICABLE"},
        "explanation": explanation,
        "space_count": len(spaces),
        "space_boundary_count": len(boundaries),
        "incident_count": len(incidents),
        "incidents": incidents[:500],
        "truncated": len(incidents) > 500,
    }


def energy_diagnostics(ifc: ifcopenshell.file) -> dict[str, Any]:
    coverage = [
        property_coverage(ifc, ["IfcSpace"], "Pset_SpaceCommon", "Reference"),
        property_coverage(ifc, ["IfcWall", "IfcWallStandardCase"], "Pset_WallCommon", "IsExternal"),
        property_coverage(ifc, ["IfcWall", "IfcWallStandardCase"], "Pset_WallCommon", "ThermalTransmittance"),
        property_coverage(ifc, ["IfcSlab"], "Pset_SlabCommon", "IsExternal"),
        property_coverage(ifc, ["IfcSlab"], "Pset_SlabCommon", "ThermalTransmittance"),
        property_coverage(ifc, ["IfcRoof"], "Pset_RoofCommon", "IsExternal"),
        property_coverage(ifc, ["IfcRoof"], "Pset_RoofCommon", "ThermalTransmittance"),
        property_coverage(ifc, ["IfcWindow"], "Pset_WindowCommon", "IsExternal"),
        property_coverage(ifc, ["IfcWindow"], "Pset_WindowCommon", "ThermalTransmittance"),
        property_coverage(ifc, ["IfcDoor"], "Pset_DoorCommon", "IsExternal"),
        property_coverage(ifc, ["IfcDoor"], "Pset_DoorCommon", "ThermalTransmittance"),
    ]
    boundaries = len(ifc.by_type("IfcRelSpaceBoundary"))
    materials = len(ifc.by_type("IfcRelAssociatesMaterial"))
    quantities = quantity_coverage(ifc)
    column_boundaries = column_room_boundary_diagnostics(ifc)
    warnings = []
    if quantities["space_total"] and boundaries == 0:
        warnings.append("Existen espacios, pero no se han exportado IfcRelSpaceBoundary.")
    if quantities["space_total"] and quantities["with_area_quantity"] < quantities["space_total"]:
        warnings.append("No todos los espacios tienen una cantidad de área reconocida.")
    if quantities["space_total"] and quantities["with_volume_quantity"] < quantities["space_total"]:
        warnings.append("No todos los espacios tienen una cantidad de volumen reconocida.")
    if column_boundaries["result"] == "FAIL":
        warnings.append(
            f"EEM-SPA-001: {column_boundaries['incident_count']} límites espaciales usan pilares."
        )
    elif column_boundaries["result"] == "NOT_EVALUABLE":
        warnings.append(f"EEM-SPA-001: {column_boundaries['explanation']}")
    return {
        "space_boundaries": boundaries,
        "material_relationships": materials,
        "space_quantities": quantities,
        "column_room_boundaries": column_boundaries,
        "property_coverage": coverage,
        "warnings": warnings,
    }


def preflight(ifc_path: Path, output_dir: Path) -> tuple[ifcopenshell.file, dict[str, Any]]:
    ifc = ifcopenshell.open(str(ifc_path))
    schema = schema_diagnostics(ifc_path)
    global_ids = global_id_diagnostics(ifc)
    inventory = {name: count_exact(ifc, name) for name in INVENTORY_CLASSES}
    status = (
        schema["status"]
        and global_ids["missing_count"] == 0
        and global_ids["duplicate_count"] == 0
        and global_ids["invalid_count"] == 0
    )
    result = {
        "ifc": str(ifc_path),
        "status": status,
        "sha256": sha256(ifc_path),
        "size_bytes": ifc_path.stat().st_size,
        "schema": ifc.schema,
        "header": header_metadata(ifc),
        "applications": application_metadata(ifc),
        "inventory_exact": inventory,
        "global_ids": global_ids,
        "schema_validation": schema,
        "energy_diagnostics": energy_diagnostics(ifc),
    }
    path = output_dir / f"{safe_name(ifc_path)}__preflight.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    result["json"] = str(path)
    return ifc, result


def validate_pair(
    ifc: ifcopenshell.file, ifc_path: Path, ids_path: Path, output_dir: Path
) -> dict[str, Any]:
    specification = ids_module.open(str(ids_path), validate=True)
    specification.validate(ifc)

    base = f"{safe_name(ifc_path)}__{safe_name(ids_path)}"
    json_path = output_dir / f"{base}.json"
    html_path = output_dir / f"{base}.html"

    json_reporter = reporter.Json(specification)
    report = json_reporter.report()
    json_reporter.to_file(str(json_path))

    html_reporter = reporter.Html(specification)
    html_reporter.report()
    html_reporter.to_file(str(html_path))

    failed = [
        {
            "name": item.name,
            "applicable": len(item.applicable_entities),
        }
        for item in specification.specifications
        if not item.status and item.is_ifc_version
    ]
    return {
        "ifc": str(ifc_path),
        "ids": str(ids_path),
        "schema": ifc.schema,
        "status": bool(report.get("status")),
        "failed_specifications": failed,
        "html": str(html_path),
        "json": str(json_path),
    }


def render_summary(summary: dict[str, Any], output_path: Path) -> None:
    rows: list[str] = []
    for model in summary["models"]:
        pre = model["preflight"]
        source = ", ".join(
            f"{item.get('name') or '?'} {item.get('version') or ''}".strip()
            for item in pre["applications"]
        ) or "No declarada"
        ids_items = "".join(
            f"<li><strong>{html.escape(Path(item['ids']).name)}</strong>: "
            f"{'CUMPLE' if item['status'] else 'NO CUMPLE'}</li>"
            for item in model["ids_results"]
        )
        failures = "".join(
            f"<li>{html.escape(str(failure.get('name') or ''))}</li>"
            for item in model["ids_results"]
            for failure in item.get("failed_specifications", [])
        ) or "<li>Ninguno</li>"
        inventory = "".join(
            f"<tr><td>{html.escape(name)}</td><td>{value}</td></tr>"
            for name, value in pre["inventory_exact"].items()
        )
        energy = pre["energy_diagnostics"]
        coverage = "".join(
            f"<tr><td>{html.escape(item['pset'])}.{html.escape(item['property'])}</td>"
            f"<td>{item['present']}/{item['total']}</td><td>{item['percent'] if item['percent'] is not None else 'N/A'}%</td></tr>"
            for item in energy["property_coverage"]
        )
        warnings = "".join(f"<li>{html.escape(item)}</li>" for item in energy["warnings"]) or "<li>Ninguna</li>"
        column_rule = energy["column_room_boundaries"]
        column_incidents = "".join(
            "<tr>"
            f"<td>{html.escape(str(item['space'].get('global_id') or ''))}</td>"
            f"<td>{html.escape(str(item['space'].get('name') or ''))}</td>"
            f"<td>{html.escape(str(item['column'].get('global_id') or ''))}</td>"
            f"<td>{html.escape(str(item['column'].get('name') or ''))}</td>"
            f"<td>{html.escape(str(item.get('storey') or ''))}</td>"
            "</tr>"
            for item in column_rule["incidents"]
        ) or "<tr><td colspan='5'>Ninguna</td></tr>"
        rows.append(
            f"<section><h2>{html.escape(Path(model['ifc']).name)}</h2>"
            f"<p><strong>Resultado:</strong> {'CUMPLE' if model['status'] else 'NO CUMPLE'} · "
            f"<strong>Esquema:</strong> {html.escape(pre['schema'])} · "
            f"<strong>Origen:</strong> {html.escape(source)}</p>"
            f"<p><strong>SHA-256:</strong> <code>{pre['sha256']}</code></p>"
            f"<h3>Prevalidación</h3><ul>"
            f"<li>Esquema: {'correcto' if pre['schema_validation']['status'] else 'con incidencias'}</li>"
            f"<li>GlobalIds ausentes: {pre['global_ids']['missing_count']}</li>"
            f"<li>GlobalIds duplicados: {pre['global_ids']['duplicate_count']}</li>"
            f"<li>GlobalIds no válidos: {pre['global_ids']['invalid_count']}</li></ul>"
            f"<h3>IDS</h3><ul>{ids_items}</ul><h3>Requisitos fallidos</h3><ul>{failures}</ul>"
            f"<h3>Diagnóstico energético</h3><ul>"
            f"<li>Límites espaciales: {energy['space_boundaries']}</li>"
            f"<li>Relaciones de materiales: {energy['material_relationships']}</li>"
            f"<li>Espacios con área: {energy['space_quantities']['with_area_quantity']}/{energy['space_quantities']['space_total']}</li>"
            f"<li>Espacios con volumen: {energy['space_quantities']['with_volume_quantity']}/{energy['space_quantities']['space_total']}</li></ul>"
            f"<h4>{html.escape(column_rule['rule'])} — Pilares no delimitadores</h4>"
            f"<p><strong>Resultado:</strong> {html.escape(column_rule['result'])}. "
            f"{html.escape(column_rule['explanation'])}</p>"
            f"<table><tr><th>GlobalId espacio</th><th>Espacio</th><th>GlobalId pilar</th><th>Pilar</th><th>Planta</th></tr>{column_incidents}</table>"
            f"<table><tr><th>Propiedad</th><th>Cobertura</th><th>Porcentaje</th></tr>{coverage}</table>"
            f"<h4>Advertencias energéticas</h4><ul>{warnings}</ul>"
            f"<h3>Inventario exacto</h3><table><tr><th>Entidad</th><th>Número</th></tr>{inventory}</table>"
            f"</section>"
        )
    document = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Resumen QA/QC IFC</title>
<style>body{{font:16px Arial,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#222}}
section{{border-top:4px solid #455a64;margin:2rem 0;padding-top:1rem}}table{{border-collapse:collapse}}
th,td{{border:1px solid #bbb;padding:.35rem .7rem;text-align:left}}code{{word-break:break-all}}</style></head>
<body><h1>Resumen de prevalidación IFC e IDS</h1>
<p>Generado: {html.escape(summary['generated_at'])}</p>{''.join(rows)}</body></html>"""
    output_path.write_text(document, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prevalida IFC, audita IDS 1.0 y genera informes consolidados."
    )
    parser.add_argument("ifc", nargs="*", type=Path, help="Archivos IFC que se validarán.")
    parser.add_argument(
        "--ids", action="append", dest="ids_files", type=Path,
        help="Especificación IDS. Puede repetirse; sin esta opción se aplican todas las predeterminadas."
    )
    parser.add_argument(
        "--profile", choices=sorted(PROFILES), default="minimum",
        help="Perfil IDS: minimum para intercambio básico; energy añade requisitos semánticos energéticos."
    )
    parser.add_argument(
        "--output", type=Path, default=Path("reports/ids"),
        help="Carpeta para informes HTML y JSON."
    )
    parser.add_argument(
        "--audit-only", action="store_true", help="Comprueba los IDS sin validar ningún IFC."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ids_paths = args.ids_files or PROFILES[args.profile]
    missing = [path for path in [*ids_paths, *args.ifc] if not path.is_file()]
    if missing:
        for path in missing:
            print(f"No existe: {path}", file=sys.stderr)
        return 2

    audit_errors = audit_ids(ids_paths)
    if audit_errors:
        for error in audit_errors:
            print(error, file=sys.stderr)
        return 2
    if args.audit_only:
        return 0
    if not args.ifc:
        print("Debe indicar al menos un IFC o utilizar --audit-only.", file=sys.stderr)
        return 2

    args.output.mkdir(parents=True, exist_ok=True)
    models: list[dict[str, Any]] = []
    for ifc_path in args.ifc:
        try:
            ifc, preflight_result = preflight(ifc_path, args.output)
            ids_results = [
                validate_pair(ifc, ifc_path, ids_path, args.output) for ids_path in ids_paths
            ]
            energy_rule_status = (
                args.profile != "energy"
                or preflight_result["energy_diagnostics"]["column_room_boundaries"]["status"]
            )
            status = (
                preflight_result["status"]
                and all(item["status"] for item in ids_results)
                and energy_rule_status
            )
            models.append(
                {"ifc": str(ifc_path), "status": status, "preflight": preflight_result,
                 "ids_results": ids_results}
            )
            print(f"{'CUMPLE' if status else 'NO CUMPLE'}: {ifc_path}")
        except Exception as exc:
            models.append({"ifc": str(ifc_path), "status": False, "error": str(exc)})
            print(f"ERROR: {ifc_path}: {exc}", file=sys.stderr)

    overall = bool(models) and all(item["status"] for item in models)
    summary = {
        "status": overall,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "profile": args.profile,
        "models": models,
    }
    json_path = args.output / "resumen.json"
    html_path = args.output / "resumen.html"
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    render_summary(summary, html_path)
    print(f"Resumen HTML: {html_path}")
    print(f"Resumen JSON: {json_path}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
