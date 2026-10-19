#!/usr/bin/env python3
"""Coleta validada do iClinic, geração de tarefas e selo de integridade."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("/root/cerebro-minhaempresa")
DOWNLOADS = ROOT / "cerebro/areas/operacoes/relatorios/iclinic/downloads"
FOLLOWUP = ROOT / "cerebro/areas/operacoes/followup"

def today_sao_paulo() -> str:
    return datetime.now(ZoneInfo("America/Sao_Paulo")).date().isoformat()

def run(command: list[str], env: dict[str, str] | None = None) -> None:
    if subprocess.run(command, cwd=ROOT, env=env).returncode:
        raise SystemExit(1)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-date", default=today_sao_paulo(), help="YYYY-MM-DD")
    args = parser.parse_args()
    report_date = datetime.strptime(args.report_date, "%Y-%m-%d").date()
    checklist_date = report_date + timedelta(days=1)
    report_name = f"pacientes_periodo_{report_date.strftime('%d_%m_%Y')}.xlsx"
    report = DOWNLOADS / report_name
    manifest = FOLLOWUP / f"integridade-checklist-{checklist_date.isoformat()}.json"

    # Um selo anterior nunca pode liberar uma coleta que falhou agora.
    manifest.unlink(missing_ok=True)
    env = os.environ.copy()
    env["SP_DATE"] = report_date.isoformat()
    run([sys.executable, "run_iclinic_daily.py"], env)
    run([sys.executable, "cerebro/areas/operacoes/scripts/gerar_tarefas_followup_iclinic.py", str(report),
         "--workspace", ".", "--expected-report-date", report_date.isoformat(),
         "--checklist-date", checklist_date.isoformat()])

    if not report.is_file() or report.stat().st_size == 0:
        raise SystemExit("Relatório ausente após coleta validada")
    for responsible in ("tamires", "paola"):
        if not (FOLLOWUP / f"checklist-{responsible}-{checklist_date.isoformat()}.md").is_file():
            raise SystemExit(f"Checklist de {responsible} ausente após geração")
    manifest.write_text(json.dumps({
        "report_date": report_date.isoformat(), "checklist_date": checklist_date.isoformat(),
        "report_name": report_name, "sha256": hashlib.sha256(report.read_bytes()).hexdigest(),
        "validated_at": datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"COLETA VALIDADA: {report_name}; checklist {checklist_date.isoformat()}")

if __name__ == "__main__":
    main()
