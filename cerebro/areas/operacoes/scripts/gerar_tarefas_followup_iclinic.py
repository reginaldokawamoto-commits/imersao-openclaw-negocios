#!/usr/bin/env python3
"""Gera tarefas de follow-up a partir do relatório Pacientes por período do iClinic.

Entrada: arquivo .xlsx exportado pelo iClinic.
Saídas:
- cerebro/areas/operacoes/followup/tarefas-followup.csv
- cerebro/areas/operacoes/followup/checklist-paola-YYYY-MM-DD.md
"""
from __future__ import annotations

from zipfile import ZipFile
from pathlib import Path
import argparse
import csv
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, date

NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

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


def read_xlsx(path: Path) -> list[list[str]]:
    with ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("a:si", NS):
                shared.append("".join((t.text or "") for t in si.findall(".//a:t", NS)))

        sheet_name = [n for n in z.namelist() if n.startswith("xl/worksheets/sheet")][0]
        root = ET.fromstring(z.read(sheet_name))
        rows: list[list[str]] = []
        for row in root.findall(".//a:row", NS):
            vals: list[str] = []
            for cell in row.findall("a:c", NS):
                v = cell.find("a:v", NS)
                val = ""
                if v is not None:
                    raw = v.text or ""
                    if cell.get("t") == "s" and raw.isdigit() and int(raw) < len(shared):
                        val = shared[int(raw)]
                    else:
                        val = raw
                vals.append(val)
            if any(str(x).strip() for x in vals):
                rows.append(vals)
        return rows


def brdate_to_date(value: str) -> date:
    return datetime.strptime(value, "%d/%m/%Y").date()


def task_id(paciente: str, procedimento: str, tipo: str, due: str) -> str:
    raw = f"{paciente}|{procedimento}|{tipo}|{due}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]


def rules(procedimento: str) -> list[tuple[int, str, str]]:
    p = procedimento.lower()
    if "botox" in p:
        return [
            (1, "D+1", "Checar como passou após o procedimento, dor/reação, orientar sinais de alerta e reforçar que o efeito do Botox costuma ser progressivo."),
            (7, "D+7", "Verificar evolução da dor/enxaqueca, intercorrências e se precisa de orientação."),
            (30, "D+30", "Verificar resposta clínica e oportunidade de retorno/continuidade."),
        ]
    if "bloqueio" in p:
        return [
            (1, "D+1", "Checar dor, reação ao procedimento e orientar retorno se necessário."),
            (7, "D+7", "Verificar evolução da dor e necessidade de nova orientação/retorno."),
        ]
    if "consulta" in p and "programa mev" in p:
        return [
            (1, "D+1", "Confirmar dúvidas após primeira consulta MEV, próximos passos e adesão inicial."),
            (30, "D+30", "Verificar continuidade do programa e próxima consulta mensal."),
        ]
    if "consulta" in p:
        return [(1, "D+1", "Confirmar se ficou alguma dúvida, exames/condutas combinadas e retorno.")]
    if "retorno" in p:
        return [(1, "D+1", "Checar se ficou alguma pendência do retorno e próximo passo do cuidado.")]
    if "laser" in p:
        return [
            (1, "D+1", "Checar se houve reação ou dúvida após laser."),
            (7, "D+7", "Verificar resposta ao laser e necessidade de continuidade."),
        ]
    return [(1, "D+1", "Checar evolução, dúvidas e necessidade de retorno/agendamento.")]


def load_existing(csv_path: Path) -> list[dict[str, str]]:
    if not csv_path.exists():
        return []
    with csv_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_tasks(csv_path: Path, tasks: list[dict[str, str]]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(tasks)


def build_checklist(path: Path, tasks: list[dict[str, str]], due_date: str) -> None:
    # Regra operacional: pendência não some.
    # O checklist do dia deve trazer tudo que está pendente e vencido até a data
    # do checklist, não apenas as tarefas com data exatamente igual ao dia.
    due_tasks = sorted(
        [
            t for t in tasks
            if t["status"] == "pendente" and t.get("data_followup", "") <= due_date
        ],
        key=lambda t: (t.get("data_followup", ""), t.get("paciente", ""), t.get("tipo_followup", "")),
    )
    title_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    lines = [
        f"# Checklist Paola — {title_date}",
        "",
        "## Como marcar",
        "",
        "Responder no Telegram com:",
        "",
        "- `feito <número>`",
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
        lines += [
            f'{idx}. **{task["paciente"]}** — {task["procedimento"]} — {task["tipo_followup"]}',
            f'   - Follow-up previsto: {datetime.strptime(task["data_followup"], "%Y-%m-%d").strftime("%d/%m/%Y")}',
            f'   - Atendimento: {atendimento} às {task["horario"]}',
            f'   - Convênio: {task["convenio"]}',
            f'   - Ação: {task["acao_sugerida"]}',
            "   - Status: ⬜ Pendente",
            f'   - ID: `{task["id"]}`',
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("xlsx", type=Path)
    parser.add_argument("--workspace", type=Path, default=Path("/root/cerebro-minhaempresa"))
    parser.add_argument("--checklist-date", help="YYYY-MM-DD. Default: D+1 do primeiro registro.")
    args = parser.parse_args()

    rows = read_xlsx(args.xlsx)
    if not rows:
        records: list[dict[str, str]] = []
    else:
        header = rows[0]
        records = [dict(zip(header, row)) for row in rows[1:]]

    outdir = args.workspace / "cerebro/areas/operacoes/followup"
    csv_path = outdir / "tarefas-followup.csv"
    existing = load_existing(csv_path)
    existing_ids = {r["id"] for r in existing}

    new_tasks: list[dict[str, str]] = []
    for rec in records:
        attended = brdate_to_date(rec["Data"])
        for days, tipo, acao in rules(rec["Procedimento"]):
            due = attended + timedelta(days=days)
            due_iso = due.isoformat()
            new_tasks.append(
                {
                    "id": task_id(rec["Paciente"], rec["Procedimento"], tipo, due_iso),
                    "status": "pendente",
                    "responsavel": "Paola",
                    "data_atendimento": attended.isoformat(),
                    "horario": rec["Horario"],
                    "paciente": rec["Paciente"],
                    "procedimento": rec["Procedimento"],
                    "convenio": rec["Convênio"],
                    "data_followup": due_iso,
                    "tipo_followup": tipo,
                    "acao_sugerida": acao,
                    "observacao": "",
                    "concluido_em": "",
                }
            )

    merged = existing + [t for t in new_tasks if t["id"] not in existing_ids]
    save_tasks(csv_path, merged)

    if args.checklist_date:
        checklist_date = args.checklist_date
    elif records:
        first_date = brdate_to_date(records[0]["Data"])
        checklist_date = (first_date + timedelta(days=1)).isoformat()
    else:
        checklist_date = (date.today() + timedelta(days=1)).isoformat()

    checklist_path = outdir / f"checklist-paola-{checklist_date}.md"
    build_checklist(checklist_path, merged, checklist_date)

    due_count = sum(1 for t in merged if t["data_followup"] <= checklist_date and t["status"] == "pendente")
    print(f"records={len(records)} new_tasks={len(new_tasks)} total_tasks={len(merged)} checklist_date={checklist_date} due_pending={due_count}")
    print(csv_path)
    print(checklist_path)


if __name__ == "__main__":
    main()
