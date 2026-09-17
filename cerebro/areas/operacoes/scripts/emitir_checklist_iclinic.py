#!/usr/bin/env python3
"""Emite checklist iClinic somente quando a coleta da véspera foi validada.

Este é o portão de segurança da entrega de 07h: falha fechada é preferível a
reenviar uma lista antiga e corroer a confiança da equipe.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/root/cerebro-minhaempresa")
FOLLOWUP = ROOT / "cerebro/areas/operacoes/followup"
DOWNLOADS = ROOT / "cerebro/areas/operacoes/relatorios/iclinic/downloads"


def sao_paulo_today() -> str:
    return datetime.now(ZoneInfo("America/Sao_Paulo")).date().isoformat()


def checklist_text(path: Path, label: str) -> str:
    raw = path.read_text(encoding="utf-8")
    lines: list[str] = []
    capture = False
    for line in raw.splitlines():
        if line == "## Tarefas pendentes até hoje":
            capture = True
            continue
        if not capture:
            continue
        if line.startswith("#"):
            break
        clean = line.replace("**", "").replace("`", "")
        if clean.strip():
            lines.append(clean)
    body = "\n".join(lines).strip() or "Nenhuma tarefa pendente até hoje."
    return f"{label}\n\n{body}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checklist-date", default=sao_paulo_today())
    args = ap.parse_args()

    check_date = date.fromisoformat(args.checklist_date)
    report_date = check_date - timedelta(days=1)
    report_name = f"pacientes_periodo_{report_date.strftime('%d_%m_%Y')}.xlsx"
    report = DOWNLOADS / report_name
    manifest_path = FOLLOWUP / f"integridade-checklist-{check_date.isoformat()}.json"
    tamires = FOLLOWUP / f"checklist-tamires-{check_date.isoformat()}.md"
    paola = FOLLOWUP / f"checklist-paola-{check_date.isoformat()}.md"

    failures: list[str] = []
    if not report.is_file() or report.stat().st_size == 0:
        failures.append(f"relatório ausente ou vazio: {report_name}")
    if not manifest_path.is_file():
        failures.append("selo de integridade ausente")
        manifest = {}
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("report_date") != report_date.isoformat():
            failures.append("selo aponta para outra data de relatório")
        if manifest.get("checklist_date") != check_date.isoformat():
            failures.append("selo aponta para outro checklist")
        if report.is_file() and report.stat().st_size:
            actual_hash = hashlib.sha256(report.read_bytes()).hexdigest()
            if manifest.get("sha256") != actual_hash:
                failures.append("relatório foi alterado após validação")
    if not tamires.is_file() or not paola.is_file():
        failures.append("checklist não foi gerado")

    if failures:
        raise SystemExit(
            "ENVIO BLOQUEADO — checklist iClinic não atualizado: " + "; ".join(failures)
        )

    parts = [checklist_text(tamires, "Tarefas da Tamires")]
    paola_body = checklist_text(paola, "Cópia de acompanhamento — tarefas da Paola")
    parts.append(paola_body)
    parts.append(
        "Baixa: feito <número>, não respondeu <número>, reagendar <número> para DD/MM ou atenção médica <número> - observação."
    )
    print("\n\n".join(parts))


if __name__ == "__main__":
    main()
