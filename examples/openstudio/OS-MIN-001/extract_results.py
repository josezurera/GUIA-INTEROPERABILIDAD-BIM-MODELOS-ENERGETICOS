#!/usr/bin/env python3
"""Extrae los indicadores anuales principales de eplusout.sql."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


SQL_PATH = Path(__file__).parent / "run" / "eplusout.sql"


def tabular_value(connection: sqlite3.Connection, table: str, row: str, column: str) -> float:
    query = """
        SELECT Value
        FROM TabularDataWithStrings
        WHERE ReportName = 'AnnualBuildingUtilityPerformanceSummary'
          AND TableName = ? AND RowName = ? AND ColumnName = ?
    """
    result = connection.execute(query, (table, row, column)).fetchone()
    if result is None:
        raise RuntimeError(f"Resultado ausente: {table} / {row} / {column}")
    return float(result[0])


if not SQL_PATH.is_file():
    raise SystemExit(f"No existe {SQL_PATH}. Ejecute primero: openstudio run -w workflow.osw")

with sqlite3.connect(SQL_PATH) as connection:
    area = tabular_value(connection, "Building Area", "Net Conditioned Building Area", "Area")
    values = {
        "calefaccion_gj": tabular_value(connection, "End Uses", "Heating", "District Heating Water"),
        "refrigeracion_gj": tabular_value(connection, "End Uses", "Cooling", "District Cooling"),
        "iluminacion_interior_gj": tabular_value(connection, "End Uses", "Interior Lighting", "Electricity"),
        "equipos_interiores_gj": tabular_value(connection, "End Uses", "Interior Equipment", "Electricity"),
    }
    values["total_gj"] = sum(values.values())
    values["superficie_acondicionada_m2"] = area
    values["intensidad_total_kwh_m2_ano"] = values["total_gj"] * 1000.0 / 3.6 / area

print(json.dumps({key: round(value, 2) for key, value in values.items()}, indent=2, ensure_ascii=False))
