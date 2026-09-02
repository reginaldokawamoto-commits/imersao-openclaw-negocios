#!/usr/bin/env python3
"""Gera tarefas de follow-up a partir do relatório Pacientes por período do iClinic.

Entrada: arquivo .xlsx exportado pelo iClinic.
Saídas:
- cerebro/areas/operacoes/followup/tarefas-followup.csv
- cerebro/areas/operacoes/followup/checklist-tamires-YYYY-MM-DD.md

Regra importante: as regras de negócio não ficam hardcoded neste script.
A fonte de verdade é:
  cerebro/areas/operacoes/projetos/template-regras-lembretes-iclinic.csv
"""
from __future__ import annotations

from zipfile import ZipFile
from pathlib import Path
import argparse
import csv
import hashlib
import re
import unicodedata
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

RULES_REL = Path("cerebro/areas/operacoes/projetos/template-regras-lembretes-iclinic.csv")
FOLLOWUP_REL = Path("cerebro/areas/operacoes/followup")


def excel_col_to_idx(cell_ref: str) -> int:
    """Converte A1/BC12 em índice zero-based da coluna."""
    letters = "".join(ch for ch in cell_ref if ch.isalpha()).upper()
    idx = 0
    for ch in letters:
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


def read_xlsx(path: Path) -> list[list[str]]:
    """Lê XLSX preservando células vazias.

    A implementação antiga iterava apenas células presentes no XML. Quando uma
    célula vazia era omitida pelo Excel/iClinic, os valores da linha podiam
    deslocar de coluna. Aqui usamos a referência da célula (A, B, C...) para
    montar a linha na posição correta.
    """
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
            vals_by_col: dict[int, str] = {}
            max_col = -1
            for cell in row.findall("a:c", NS):
                ref = cell.get("r", "")
                col_idx = excel_col_to_idx(ref) if ref else max_col + 1
                max_col = max(max_col, col_idx)
                v = cell.find("a:v", NS)
                val = ""
                if v is not None:
                    raw = v.text or ""
                    if cell.get("t") == "s" and raw.isdigit() and int(raw) < len(shared):
                        val = shared[int(raw)]
                    else:
                        val = raw
                vals_by_col[col_idx] = val
            vals = [vals_by_col.get(i, "") for i in range(max_col + 1)]
            if any(str(x).strip() for x in vals):
                rows.append(vals)
        return rows


def brdate_to_date(value: str) -> date:
    return datetime.strptime(value.strip(), "%d/%m/%Y").date()


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"\s+", " ", value).strip().casefold()
    return value


def parse_offset(value: str) -> tuple[int, str] | None:
    value = (value or "").strip().upper()
    if not value or value in {"NÃO GERAR", "NAO GERAR", "N/A", "-"}:
        return None
    m = re.fullmatch(r"D\+(\d+)", value)
    if not m:
        raise ValueError(f"Prazo de regra inválido: {value!r}")
    days = int(m.group(1))
    return days, f"D+{days}"


def load_rules(workspace: Path) -> dict[str, list[tuple[int, str, str, str]]]:
    rules_path = workspace / RULES_REL
    with rules_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    mapping: dict[str, list[tuple[int, str, str, str]]] = {}
    for row in rows:
        proc = row.get("tipo_salvo_iclinic", "").strip()
        if not proc:
            continue
        key = normalize(proc)
        status = normalize(row.get("condicao", ""))
        if "sem follow-up" in status or "nao gerar" in normalize(row.get("criar_tarefa_em", "")):
            mapping[key] = []
            continue

        responsavel = (row.get("responsavel") or "Tamires").strip() or "Tamires"
        entries: list[tuple[int, str, str, str]] = []
        first = parse_offset(row.get("criar_tarefa_em", ""))
        if first:
            days, label = first
            entries.append((days, label, row.get("acao", "").strip(), responsavel))
        second = parse_offset(row.get("segunda_tarefa_em", ""))
        if second:
            days, label = second
            action = row.get("segunda_acao", "").strip() or row.get("acao", "").strip()
            entries.append((days, label, action, responsavel))
        mapping[key] = entries
    return mapping


def rules_for(procedimento: str, rule_map: dict[str, list[tuple[int, str, str, str]]]) -> tuple[list[tuple[int, str, str, str]], bool]:
    """Retorna regras para o procedimento e se veio de regra oficial.

    Prioridade: match exato normalizado. Como fallback controlado, usa o maior
    tipo da tabela contido no nome exportado (útil para códigos truncados), mas
    não usa heurísticas antigas por palavra-chave para não recriar erro oculto.
    """
    proc_norm = normalize(procedimento)
    if proc_norm in rule_map:
        return rule_map[proc_norm], True

    candidates = [(key, val) for key, val in rule_map.items() if key and (key in proc_norm or proc_norm in key)]
    if candidates:
        key, val = max(candidates, key=lambda kv: len(kv[0]))
        return val, True

    # Procedimento sem regra oficial não deve gerar tarefa automaticamente.
    # Isso evita que uma heurística genérica crie follow-ups indevidos; o nome
    # vai para o resumo como unmatched_procedimentos para decisão do Reginaldo.
    return [], False


def task_id(paciente: str, procedimento: str, tipo: str, due: str, atendimento: str = "", horario: str = "") -> str:
    # Inclui data/horário de atendimento para evitar colisão se o mesmo paciente
    # tiver o mesmo procedimento e o mesmo vencimento em contextos diferentes.
    raw = f"{paciente}|{procedimento}|{tipo}|{due}|{atendimento}|{horario}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]


def legacy_task_id(paciente: str, procedimento: str, tipo: str, due: str) -> str:
    raw = f"{paciente}|{procedimento}|{tipo}|{due}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]


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


def build_checklist(path: Path, tasks: list[dict[str, str]], due_date: str, responsavel: str = "Tamires") -> None:
    due_tasks = sorted(
        [
            t for t in tasks
            if t.get("status") == "pendente"
            and t.get("data_followup", "") <= due_date
            and t.get("responsavel", "").strip().lower() == responsavel.strip().lower()
        ],
        key=lambda t: (t.get("data_followup", ""), t.get("paciente", ""), t.get("tipo_followup", ""), t.get("id", "")),
    )
    title_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%d/%m/%Y")
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
        lines += [
            f'{idx}. **{task["paciente"]}** — {task["procedimento"]} — {task["tipo_followup"]}',
            f'   - Follow-up previsto: {datetime.strptime(task["data_followup"], "%Y-%m-%d").strftime("%d/%m/%Y")}',
            f'   - Atendimento: {atendimento} às {task.get("horario", "")}',
            f'   - Convênio: {task.get("convenio", "")}',
            f'   - Ação: {task.get("acao_sugerida", "")}',
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
        records = [dict(zip(header, row + [""] * (len(header) - len(row)))) for row in rows[1:]]

    outdir = args.workspace / FOLLOWUP_REL
    csv_path = outdir / "tarefas-followup.csv"
    existing = load_existing(csv_path)
    existing_ids = {r["id"] for r in existing}
    rule_map = load_rules(args.workspace)

    new_tasks: list[dict[str, str]] = []
    unmatched: set[str] = set()
    for rec in records:
        required = ["Data", "Paciente", "Procedimento"]
        missing = [key for key in required if not (rec.get(key) or "").strip()]
        if missing:
            raise SystemExit(f"Registro sem campos obrigatórios {missing}: {rec}")

        attended = brdate_to_date(rec["Data"])
        horario = rec.get("Horario") or rec.get("Horário") or ""
        proc = rec.get("Procedimento", "")
        rule_entries, official = rules_for(proc, rule_map)
        if not official:
            unmatched.add(proc)

        for days, tipo, acao, responsavel in rule_entries:
            due = attended + timedelta(days=days)
            due_iso = due.isoformat()
            tid = task_id(rec["Paciente"], proc, tipo, due_iso, attended.isoformat(), horario)
            legacy_tid = legacy_task_id(rec["Paciente"], proc, tipo, due_iso)
            if tid in existing_ids or legacy_tid in existing_ids:
                continue
            new_tasks.append(
                {
                    "id": tid,
                    "status": "pendente",
                    "responsavel": responsavel,
                    "data_atendimento": attended.isoformat(),
                    "horario": horario,
                    "paciente": rec["Paciente"],
                    "procedimento": proc,
                    "convenio": rec.get("Convênio", ""),
                    "data_followup": due_iso,
                    "tipo_followup": tipo,
                    "acao_sugerida": acao,
                    "observacao": "",
                    "concluido_em": "",
                }
            )

    merged = existing + new_tasks
    save_tasks(csv_path, merged)

    if args.checklist_date:
        checklist_date = args.checklist_date
    elif records:
        first_date = brdate_to_date(records[0]["Data"])
        checklist_date = (first_date + timedelta(days=1)).isoformat()
    else:
        checklist_date = (date.today() + timedelta(days=1)).isoformat()

    checklist_path = outdir / f"checklist-tamires-{checklist_date}.md"
    build_checklist(checklist_path, merged, checklist_date, "Tamires")

    due_count = sum(
        1 for t in merged
        if t.get("data_followup", "") <= checklist_date
        and t.get("status") == "pendente"
        and t.get("responsavel", "").strip().lower() == "tamires"
    )
    print(f"records={len(records)} new_tasks={len(new_tasks)} total_tasks={len(merged)} checklist_date={checklist_date} due_pending_tamires={due_count}")
    if unmatched:
        print("unmatched_procedimentos=" + "; ".join(sorted(unmatched)))
    print(csv_path)
    print(checklist_path)


if __name__ == "__main__":
    main()
