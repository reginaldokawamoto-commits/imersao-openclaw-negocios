#!/usr/bin/env python3
"""Marca tarefas de um checklist Tamires/Paola como concluídas e regenera checklists.

Uso típico:
  python cerebro/areas/operacoes/scripts/marcar_tarefas_checklist.py \
    --responsavel Tamires --checklist-date 2026-08-19 --feito 1-10 \
    --done-at 2026-08-19T09:40:00-03:00 --origem "Tamires via Telegram"

Importante: o número é resolvido pelo ID gravado no checklist do dia, não pela
posição atual do CSV. Isso evita o erro de marcar a tarefa errada quando há
pendências antigas que mudam a ordem da lista.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Iterable

FIELDS = [
    "id",
    "status",
    "responsavel",
    "data_atendimento",
    "horario",
    "paciente",
    "procedimento",
    "convenio",
    "data_followup",
    "tipo_followup",
    "acao_sugerida",
    "observacao",
    "concluido_em",
]

ROOT_DEFAULT = Path("/root/cerebro-minhaempresa")
FOLLOWUP_REL = Path("cerebro/areas/operacoes/followup")


def parse_number_spec(specs: Iterable[str]) -> list[int]:
    out: set[int] = set()
    for spec in specs:
        for part in re.split(r"[,;\s]+", spec.strip()):
            if not part:
                continue
            m = re.fullmatch(r"(?:<)?(\d+)(?:>)?(?:-(?:<)?(\d+)(?:>)?)?", part)
            if not m:
                raise SystemExit(f"Número/faixa inválido: {part!r}")
            a = int(m.group(1)); b = int(m.group(2) or a)
            if b < a:
                a, b = b, a
            out.update(range(a, b + 1))
    return sorted(out)


def load_tasks(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_tasks(csv_path: Path, tasks: list[dict[str, str]]) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(tasks)


def checklist_path(root: Path, responsavel: str, checklist_date: str) -> Path:
    slug = responsavel.strip().lower()
    return root / FOLLOWUP_REL / f"checklist-{slug}-{checklist_date}.md"


def ids_from_checklist(path: Path) -> dict[int, str]:
    text = path.read_text(encoding="utf-8")
    result: dict[int, str] = {}
    current: int | None = None
    for line in text.splitlines():
        m_num = re.match(r"^(\d+)\.\s+\*\*", line)
        if m_num:
            current = int(m_num.group(1))
            continue
        m_id = re.search(r"- ID: `([^`]+)`", line)
        if m_id and current is not None:
            result[current] = m_id.group(1)
            current = None
    return result


def render_checklist(path: Path, tasks: list[dict[str, str]], responsavel: str, checklist_date: str) -> None:
    due_tasks = sorted(
        [
            t for t in tasks
            if t.get("status") == "pendente"
            and t.get("responsavel", "").strip().lower() == responsavel.strip().lower()
            and t.get("data_followup", "") <= checklist_date
        ],
        key=lambda t: (t.get("data_followup", ""), t.get("paciente", ""), t.get("tipo_followup", ""), t.get("id", "")),
    )
    title_date = datetime.strptime(checklist_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    lines = [
        f"# Checklist {responsavel} — {title_date}",
        "",
        "## Como marcar",
        "",
        "Responder no Telegram com:",
        "",
        "- `feito <número>`",
        "- `feito <número>-<número>`",
        "- `não respondeu <número>`",
        "- `reagendar <número> para DD/MM`",
        "- `atenção médica <número> - observação`",
        "",
        "## Tarefas pendentes até hoje",
        "",
    ]
    if not due_tasks:
        lines.append("Nenhuma tarefa pendente até hoje.")
    for idx, task in enumerate(due_tasks, 1):
        atendimento = datetime.strptime(task["data_atendimento"], "%Y-%m-%d").strftime("%d/%m/%Y")
        followup = datetime.strptime(task["data_followup"], "%Y-%m-%d").strftime("%d/%m/%Y")
        lines += [
            f'{idx}. **{task["paciente"]}** — {task["procedimento"]} — {task["tipo_followup"]}',
            f"   - Follow-up previsto: {followup}",
            f'   - Atendimento: {atendimento} às {task.get("horario", "")}',
            f'   - Convênio: {task.get("convenio", "")}',
            f'   - Ação: {task.get("acao_sugerida", "")}',
            "   - Status: ⬜ Pendente",
            f'   - ID: `{task["id"]}`',
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", type=Path, default=ROOT_DEFAULT)
    ap.add_argument("--responsavel", required=True)
    ap.add_argument("--checklist-date", required=True, help="YYYY-MM-DD do checklist usado para numerar")
    ap.add_argument("--feito", nargs="+", required=True, help="Números ou faixas: 1 2 5-8")
    ap.add_argument("--done-at", required=True, help="Timestamp ISO, ex. 2026-08-19T09:40:00-03:00")
    ap.add_argument("--origem", default="Telegram")
    ap.add_argument("--regenerate-until", help="YYYY-MM-DD; default: checklist-date + 1")
    args = ap.parse_args()

    outdir = args.workspace / FOLLOWUP_REL
    csv_path = outdir / "tarefas-followup.csv"
    cpath = checklist_path(args.workspace, args.responsavel, args.checklist_date)
    if not cpath.exists():
        raise SystemExit(f"Checklist não encontrado: {cpath}")

    requested = parse_number_spec(args.feito)
    number_to_id = ids_from_checklist(cpath)
    missing = [n for n in requested if n not in number_to_id]
    if missing:
        raise SystemExit(f"Números não encontrados no checklist {cpath.name}: {missing}")
    ids = {number_to_id[n] for n in requested}

    tasks = load_tasks(csv_path)
    now_note = f"Marcado como feito por {args.origem}."
    changed: list[dict[str, str]] = []
    for task in tasks:
        if task.get("id") in ids:
            if task.get("status") != "concluido" or not task.get("concluido_em"):
                obs = task.get("observacao", "").strip()
                task["status"] = "concluido"
                task["concluido_em"] = args.done_at
                task["observacao"] = (obs + " " + now_note).strip() if obs else now_note
                changed.append(task)

    if len(changed) != len(ids):
        already = len(ids) - len(changed)
        print(f"Aviso: {already} tarefa(s) já estavam concluídas.")

    save_tasks(csv_path, tasks)

    end = args.regenerate_until or (datetime.strptime(args.checklist_date, "%Y-%m-%d").date() + timedelta(days=1)).isoformat()
    d = datetime.strptime(args.checklist_date, "%Y-%m-%d").date()
    end_d = datetime.strptime(end, "%Y-%m-%d").date()
    regenerated: list[str] = []
    while d <= end_d:
        p = checklist_path(args.workspace, args.responsavel, d.isoformat())
        render_checklist(p, tasks, args.responsavel, d.isoformat())
        regenerated.append(str(p))
        d += timedelta(days=1)

    print(f"requested_numbers={requested}")
    print(f"changed={len(changed)} ids={','.join(sorted(ids))}")
    print("regenerated=" + ",".join(regenerated))


if __name__ == "__main__":
    main()
