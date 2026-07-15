#!/usr/bin/env python3
"""Valida modelo, diagnóstico y resultados de OS-MIN-001 contra el registro YAML."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml


CASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CASE_DIR.parents[2]
DATA_PATH = ROOT_DIR / "data" / "casos-prueba.yml"
ERR_PATH = CASE_DIR / "run" / "eplusout.err"
RESULTS_SCRIPT = CASE_DIR / "extract_results.py"


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=CASE_DIR, check=True, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout.rstrip())
    return result.stdout


parser = argparse.ArgumentParser()
parser.add_argument("--openstudio", default="openstudio", help="Ruta o comando de OpenStudio CLI")
parser.add_argument("--execute", action="store_true", help="Ejecuta de nuevo el OSW antes de validar")
args = parser.parse_args()

if args.execute:
    run([args.openstudio, "run", "-w", "workflow.osw"])

run([args.openstudio, "verify_model.rb"])

if not ERR_PATH.is_file():
    raise SystemExit("Falta run/eplusout.err. Use --execute después de descargar el EPW.")

err_text = ERR_PATH.read_text(encoding="utf-8", errors="replace")
summary = re.search(r"Completed Successfully--\s*(\d+) Warning;\s*(\d+) Severe Errors", err_text)
if summary is None:
    raise SystemExit("No se encontró un cierre correcto de EnergyPlus en eplusout.err")
warnings, severe = map(int, summary.groups())

registry = yaml.safe_load(DATA_PATH.read_text(encoding="utf-8"))["casos"][0]
expected_execution = registry["ultima_ejecucion"]
if severe != expected_execution["errores_severos"]:
    raise SystemExit(f"Errores severos: esperados {expected_execution['errores_severos']}, obtenidos {severe}")
if warnings != expected_execution["advertencias"]:
    raise SystemExit(f"Advertencias: esperadas {expected_execution['advertencias']}, obtenidas {warnings}")

results = json.loads(run([sys.executable, str(RESULTS_SCRIPT)]))
expected_results = expected_execution["resultados_anuales"]
for key, expected in expected_results.items():
    if key.startswith("horas_fuera_consigna"):
        continue
    actual = results[key]
    if abs(actual - expected) > 0.02:
        raise SystemExit(f"{key}: esperado {expected}, obtenido {actual}")

print(f"OK energyplus_severe={severe}")
print(f"OK energyplus_warnings={warnings}")
print("Validación integral OS-MIN-001 superada.")
