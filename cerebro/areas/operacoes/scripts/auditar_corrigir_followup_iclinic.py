#!/usr/bin/env python3
"""Audita e corrige tarefas de follow-up contra a tabela oficial de regras.

Uso:
  python3 cerebro/areas/operacoes/scripts/auditar_corrigir_followup_iclinic.py \
    --from-date 2026-08-24 --to-date 2026-09-02 --regenerate-until 2026-09-18

A correção é conservadora:
- não altera tarefas concluídas;
- só cancela pendências de procedimentos que têm regra oficial na tabela;
- adiciona pendências oficiais ausentes;
- regenera checklists da Tamires para refletir o CSV.
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

from gerar_tarefas_followup_iclinic import (
    FIELDS,
    FOLLOWUP_REL,
    build_checklist,
    load_rules,
    rules_for,
    task_id,
)

ROOT_DEFAULT = Path("/root/cerebro-minhaempresa")


def load_tasks(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_tasks(csv_path: Path, tasks: list[dict[str, str]]) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(tasks)


def append_obs(existing: str, note: str) -> str:
    existing = (existing or "").strip()
    return f"{existing} {note}".strip() if existing else note


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", type=Path, default=ROOT_DEFAULT)
    ap.add_argument("--from-date", required=True, help="Data de atendimento inicial YYYY-MM-DD")
    ap.add_argument("--to-date", required=True, help="Data de atendimento final YYYY-MM-DD")
    ap.add_argument("--checklist-from", help="Primeiro checklist a regenerar; default: from-date")
    ap.add_argument("--regenerate-until", required=True, help="Último checklist a regenerar YYYY-MM-DD")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    csv_path = args.workspace / FOLLOWUP_REL / "tarefas-followup.csv"
    tasks = load_tasks(csv_path)
    rule_map = load_rules(args.workspace)

    start = args.from_date
    end = args.to_date
    now = datetime.now().isoformat(timespec="seconds")
    note = f"Cancelado automaticamente em {now}: tarefa pendente incompatível com a tabela oficial de regras."

    groups: dict[tuple[str, str, str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for t in tasks:
        attended = t.get("data_atendimento", "")
        if start <= attended <= end and t.get("procedimento") != "Follow-up manual":
            key = (
                attended,
                t.get("horario", ""),
                t.get("paciente", ""),
                t.get("procedimento", ""),
                t.get("convenio", ""),
                t.get("responsavel", ""),
            )
            groups[key].append(t)

    cancelled = 0
    added = 0
    skipped_unmatched: set[str] = set()

    for key, rows in groups.items():
        attended, horario, paciente, procedimento, convenio, _responsavel = key
        entries, official = rules_for(procedimento, rule_map)
        if not official:
            skipped_unmatched.add(procedimento)
            for r in rows:
                if r.get("status") == "pendente":
                    r["status"] = "cancelado_sem_regra_oficial"
                    r["observacao"] = append_obs(
                        r.get("observacao", ""),
                        f"Cancelado automaticamente em {now}: procedimento sem regra oficial na tabela; exige decisão antes de gerar follow-up.",
                    )
                    cancelled += 1
            continue

        attended_date = datetime.strptime(attended, "%Y-%m-%d").date()
        expected: dict[tuple[str, str], tuple[str, str]] = {}
        for days, tipo, acao, responsavel in entries:
            due = (attended_date + timedelta(days=days)).isoformat()
            expected[(tipo, due)] = (acao, responsavel)

        existing_any = {(r.get("tipo_followup", ""), r.get("data_followup", "")) for r in rows}

        for r in rows:
            pair = (r.get("tipo_followup", ""), r.get("data_followup", ""))
            if r.get("status") == "pendente" and pair not in expected:
                r["status"] = "cancelado_regra_corrigida"
                r["observacao"] = append_obs(r.get("observacao", ""), note)
                cancelled += 1

        existing_ids = {r.get("id", "") for r in tasks}
        for (tipo, due), (acao, responsavel) in expected.items():
            if (tipo, due) in existing_any:
                continue
            tid = task_id(paciente, procedimento, tipo, due, attended, horario)
            if tid in existing_ids:
                continue
            tasks.append({
                "id": tid,
                "status": "pendente",
                "responsavel": responsavel,
                "data_atendimento": attended,
                "horario": horario,
                "paciente": paciente,
                "procedimento": procedimento,
                "convenio": convenio,
                "data_followup": due,
                "tipo_followup": tipo,
                "acao_sugerida": acao,
                "observacao": f"Criado automaticamente em {now} após auditoria contra tabela oficial de regras.",
                "concluido_em": "",
            })
            existing_ids.add(tid)
            added += 1

    if not args.dry_run:
        save_tasks(csv_path, tasks)
        d = datetime.strptime(args.checklist_from or args.from_date, "%Y-%m-%d").date()
        end_d = datetime.strptime(args.regenerate_until, "%Y-%m-%d").date()
        outdir = args.workspace / FOLLOWUP_REL
        while d <= end_d:
            build_checklist(outdir / f"checklist-tamires-{d.isoformat()}.md", tasks, d.isoformat(), "Tamires")
            d += timedelta(days=1)

    print(f"cancelled={cancelled} added={added} dry_run={args.dry_run}")
    if skipped_unmatched:
        print("skipped_unmatched=" + "; ".join(sorted(skipped_unmatched)))


if __name__ == "__main__":
    main()
