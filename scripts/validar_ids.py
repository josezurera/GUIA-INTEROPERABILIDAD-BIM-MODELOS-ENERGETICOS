"""Valida archivos IFC mediante especificaciones IDS y genera informes HTML/JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import ifcopenshell
from ifctester import ids as ids_module
from ifctester import reporter


def safe_name(path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", path.stem)


def audit_ids(ids_paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for ids_path in ids_paths:
        try:
            ids_module.open(str(ids_path), validate=True)
            print(f"IDS válido: {ids_path}")
        except Exception as exc:  # pragma: no cover - mensaje depende de xmlschema
            errors.append(f"IDS no válido: {ids_path}: {exc}")
    return errors


def validate_pair(ifc_path: Path, ids_path: Path, output_dir: Path) -> dict:
    specification = ids_module.open(str(ids_path), validate=True)
    ifc = ifcopenshell.open(str(ifc_path))
    specification.validate(ifc)

    base = f"{safe_name(ifc_path)}__{safe_name(ids_path)}"
    json_path = output_dir / f"{base}.json"
    html_path = output_dir / f"{base}.html"

    json_reporter = reporter.Json(specification)
    result = json_reporter.report()
    json_reporter.to_file(str(json_path))

    html_reporter = reporter.Html(specification)
    html_reporter.report()
    html_reporter.to_file(str(html_path))

    return {
        "ifc": str(ifc_path),
        "ids": str(ids_path),
        "schema": ifc.schema,
        "status": bool(result.get("status")),
        "html": str(html_path),
        "json": str(json_path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audita IDS 1.0 y valida uno o varios IFC con IfcTester."
    )
    parser.add_argument("ifc", nargs="*", type=Path, help="Archivos IFC que se validarán.")
    parser.add_argument(
        "--ids",
        action="append",
        dest="ids_files",
        type=Path,
        help="Especificación IDS. Puede repetirse.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/ids"),
        help="Carpeta para informes HTML y JSON.",
    )
    parser.add_argument(
        "--audit-only",
        action="store_true",
        help="Comprueba los IDS sin validar ningún IFC.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ids_paths = args.ids_files or [Path("config/ids/eem-ifc-minimo-v0.1.ids")]

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
    results: list[dict] = []
    for ifc_path in args.ifc:
        for ids_path in ids_paths:
            try:
                result = validate_pair(ifc_path, ids_path, args.output)
                results.append(result)
                label = "CUMPLE" if result["status"] else "NO CUMPLE"
                print(f"{label}: {ifc_path} / {ids_path}")
            except Exception as exc:
                results.append(
                    {"ifc": str(ifc_path), "ids": str(ids_path), "status": False, "error": str(exc)}
                )
                print(f"ERROR: {ifc_path} / {ids_path}: {exc}", file=sys.stderr)

    summary_path = args.output / "resumen.json"
    summary_path.write_text(
        json.dumps({"status": all(item["status"] for item in results), "results": results}, indent=2),
        encoding="utf-8",
    )
    print(f"Resumen: {summary_path}")
    return 0 if results and all(item["status"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
