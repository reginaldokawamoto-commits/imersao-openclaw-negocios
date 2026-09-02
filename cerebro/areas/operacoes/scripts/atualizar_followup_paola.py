#!/usr/bin/env python3
"""Atualiza a base de follow-up a partir de respostas do Telegram.

Uso comum:
  # marcar itens do checklist do dia como feitos
  python3 cerebro/areas/operacoes/scripts/atualizar_followup_paola.py feito --checklist-date 2026-07-02 --itens 1-11 --origem "Tamires via Telegram"

  # incluir tarefa manual no mesmo fluxo do checklist
  python3 cerebro/areas/operacoes/scripts/atualizar_followup_paola.py add-manual --paciente "Nome" --due 2026-07-07 --acao "Entrar em contato..." --origem "Tamires via Telegram"

O script também atualiza o checklist de origem para evitar que uma mensagem
posterior reutilize um arquivo antigo com itens já baixados.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
from datetime import datetime
from pathlib import Path

FIELDS = [
    "id", "status", "responsavel", "data_atendimento", "horario", "paciente",
    "procedimento", "convenio", "data_followup", "tipo_followup", "acao_sugerida",
    "observacao", "concluido_em",
]

WORKSPACE = Path('/root/cerebro-minhaempresa')
BASE = WORKSPACE / 'cerebro/areas/operacoes/followup'
CSV_PATH = BASE / 'tarefas-followup.csv'


def load_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_rows(rows: list[dict[str, str]]) -> None:
    with CSV_PATH.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def checklist_ids(checklist_date: str) -> list[str]:
    path = BASE / f'checklist-tamires-{checklist_date}.md'
    if not path.exists():
        legacy_path = BASE / f'checklist-paola-{checklist_date}.md'
        if legacy_path.exists():
            path = legacy_path
        else:
            raise SystemExit(f'Checklist não encontrado: {path}')
    ids = []
    for line in path.read_text(encoding='utf-8').splitlines():
        m = re.search(r'ID: `([^`]+)`', line)
        if m:
            ids.append(m.group(1))
    return ids


def checklist_path(checklist_date: str) -> Path:
    path = BASE / f'checklist-tamires-{checklist_date}.md'
    if path.exists():
        return path
    legacy_path = BASE / f'checklist-paola-{checklist_date}.md'
    if legacy_path.exists():
        return legacy_path
    raise SystemExit(f'Checklist não encontrado: {path}')


def expand_itens(spec: str) -> list[int]:
    out: list[int] = []
    for part in spec.replace(' ', '').split(','):
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def append_obs(existing: str, note: str) -> str:
    existing = (existing or '').strip()
    return f'{existing} {note}'.strip() if existing else note


def update_checklist_status(checklist_date: str, selected_ids: set[str], status_line: str) -> None:
    """Atualiza o status visual no checklist que originou a numeração.

    A base oficial é o CSV, mas o checklist também precisa ser alterado porque
    algumas rotinas/mensagens consultam o markdown já gerado. Se ele ficar velho,
    itens concluídos podem ser cobrados novamente.
    """
    path = checklist_path(checklist_date)
    lines = path.read_text(encoding='utf-8').splitlines()
    status_idx_by_id: dict[str, int] = {}
    for idx, line in enumerate(lines):
        m = re.search(r'ID: `([^`]+)`', line)
        if m:
            task_id = m.group(1)
            # O status fica algumas linhas acima do ID.
            for j in range(idx - 1, max(-1, idx - 8), -1):
                if lines[j].startswith('   - Status: '):
                    status_idx_by_id[task_id] = j
                    break

    changed = False
    for tid in selected_ids:
        idx = status_idx_by_id.get(tid)
        if idx is not None:
            lines[idx] = f'   - Status: {status_line}'
            changed = True
    if changed:
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def cmd_feito(args: argparse.Namespace) -> None:
    ids = checklist_ids(args.checklist_date)
    selected = []
    for n in expand_itens(args.itens):
        if n < 1 or n > len(ids):
            raise SystemExit(f'Item fora do checklist: {n}')
        selected.append(ids[n - 1])

    rows = load_rows()
    now = args.quando or datetime.now().isoformat(timespec='seconds')
    note = f'Marcado como feito por {args.origem}.'
    changed = 0
    for row in rows:
        if row['id'] in selected:
            row['status'] = 'concluido'
            row['observacao'] = append_obs(row.get('observacao', ''), note)
            row['concluido_em'] = now
            changed += 1
    save_rows(rows)
    update_checklist_status(args.checklist_date, set(selected), f'✅ Feito em {now} por {args.origem}')
    print(f'concluidos={changed}')


def cmd_atencao(args: argparse.Namespace) -> None:
    ids = checklist_ids(args.checklist_date)
    selected = []
    for n in expand_itens(args.itens):
        if n < 1 or n > len(ids):
            raise SystemExit(f'Item fora do checklist: {n}')
        selected.append(ids[n - 1])

    rows = load_rows()
    now = args.quando or datetime.now().isoformat(timespec='seconds')
    detalhe = f' — {args.observacao}' if args.observacao else ''
    note = f'Atenção médica informada por {args.origem}{detalhe}.'
    changed = 0
    for row in rows:
        if row['id'] in selected:
            row['status'] = 'atencao_medica'
            row['observacao'] = append_obs(row.get('observacao', ''), note)
            row['concluido_em'] = now
            changed += 1
    save_rows(rows)
    update_checklist_status(args.checklist_date, set(selected), f'⚠️ Atenção médica em {now}{detalhe}')
    print(f'atencao_medica={changed}')


def task_id(paciente: str, procedimento: str, tipo: str, due: str) -> str:
    raw = f'{paciente}|{procedimento}|{tipo}|{due}'
    return hashlib.sha1(raw.encode('utf-8')).hexdigest()[:10]


def cmd_add_manual(args: argparse.Namespace) -> None:
    rows = load_rows()
    tid = task_id(args.paciente, 'Follow-up manual', 'Manual', args.due)
    if any(r['id'] == tid for r in rows):
        print(f'existente id={tid}')
        return
    rows.append({
        'id': tid,
        'status': 'pendente',
        'responsavel': args.responsavel,
        'data_atendimento': args.criado_em,
        'horario': '',
        'paciente': args.paciente,
        'procedimento': 'Follow-up manual',
        'convenio': '',
        'data_followup': args.due,
        'tipo_followup': 'Manual',
        'acao_sugerida': args.acao,
        'observacao': f'Solicitado por {args.origem}.',
        'concluido_em': '',
    })
    save_rows(rows)
    print(f'adicionado id={tid}')


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(required=True)

    feito = sub.add_parser('feito')
    feito.add_argument('--checklist-date', required=True)
    feito.add_argument('--itens', required=True, help='Ex.: 1,2,5-8 ou 1-11')
    feito.add_argument('--origem', default='Tamires via Telegram')
    feito.add_argument('--quando')
    feito.set_defaults(func=cmd_feito)

    atencao = sub.add_parser('atencao-medica')
    atencao.add_argument('--checklist-date', required=True)
    atencao.add_argument('--itens', required=True, help='Ex.: 1,2,5-8 ou 1-11')
    atencao.add_argument('--origem', default='Tamires via Telegram')
    atencao.add_argument('--observacao', default='')
    atencao.add_argument('--quando')
    atencao.set_defaults(func=cmd_atencao)

    manual = sub.add_parser('add-manual')
    manual.add_argument('--paciente', required=True)
    manual.add_argument('--due', required=True, help='YYYY-MM-DD')
    manual.add_argument('--acao', required=True)
    manual.add_argument('--origem', default='Tamires via Telegram')
    manual.add_argument('--responsavel', default='Tamires')
    manual.add_argument('--criado-em', default=datetime.now().date().isoformat())
    manual.set_defaults(func=cmd_add_manual)

    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
