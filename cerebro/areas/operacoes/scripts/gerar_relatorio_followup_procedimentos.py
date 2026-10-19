#!/usr/bin/env python3
"""Gera o follow-up semanal a partir da aba operacional oficial no Google Sheets.

Esta rotina nunca usa o CSV de template como fonte de dados. Falha de forma
explícita se a aba, os cabeçalhos ou o acesso à planilha não estiverem válidos.
"""

from __future__ import annotations

import sys
from datetime import date, datetime

import gspread
from google.oauth2.service_account import Credentials


SPREADSHEET_ID = "122ARYktTi1RsuCnJNXIV_Bhzg-8lmofOb64yxydmxX8"
WORKSHEET_NAME = "Controle de Procedimentos"
CREDENTIALS_FILE = "/root/finx/credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
HEADERS = [
    "ID",
    "Paciente",
    "Procedimento",
    "Tipo de fluxo",
    "Convênio",
    "Responsável interno",
    "Data da indicação/solicitação",
    "Data do envio da proposta",
    "Valor particular/honorários",
    "Data do envio ao convênio",
    "Protocolo do convênio",
    "Status atual",
    "Último contato",
    "Próximo follow-up",
    "Dias sem atualização",
    "Próxima ação",
    "Observações",
    "Motivo de perda/negação",
]


def normalized(value: str) -> str:
    return " ".join(value.strip().casefold().split())


def parse_date(value: str) -> date | None:
    value = value.strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    return None


def load_cases() -> list[dict[str, str]]:
    credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    worksheet = gspread.authorize(credentials).open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)
    values = worksheet.get_all_values()
    if not values:
        raise RuntimeError(f"A aba '{WORKSHEET_NAME}' está vazia.")
    if [normalized(item) for item in values[0]] != [normalized(item) for item in HEADERS]:
        raise RuntimeError("Os cabeçalhos da aba oficial foram alterados; relatório bloqueado para evitar leitura incorreta.")
    return [dict(zip(HEADERS, row + [""] * (len(HEADERS) - len(row)))) for row in values[1:] if any(cell.strip() for cell in row)]


def is_open(case: dict[str, str]) -> bool:
    return normalized(case["Status atual"]) not in {"agendado", "fechado", "perdido", "pausado"}


def render(cases: list[dict[str, str]]) -> str:
    today = date.today()
    active = [case for case in cases if is_open(case)]
    by_flow = {
        "particular": sum(normalized(case["Tipo de fluxo"]) == "particular" for case in active),
        "convenio": sum(normalized(case["Tipo de fluxo"]) == "convênio" for case in active),
        "misto": sum(normalized(case["Tipo de fluxo"]) == "misto" for case in active),
    }
    negative_statuses = {"negado", "reclamacao_orientada", "aguardando_reclamacao_paciente", "reclamacao_feita", "reanalise_convenio"}
    negatives = sum(normalized(case["Status atual"]) in negative_statuses for case in active)
    critical = [
        case
        for case in active
        if not parse_date(case["Próximo follow-up"]) or parse_date(case["Próximo follow-up"]) <= today
    ]

    lines = [
        f"Follow-up de procedimentos — {today.strftime('%d/%m/%Y')}",
        "Fonte: aba oficial ‘Controle de Procedimentos’ no Google Sheets.",
        "",
        "Resumo executivo",
        f"• Total de casos ativos: {len(active)}.",
        f"• Particular em follow-up: {by_flow['particular']}.",
        f"• Convênio aguardando status: {by_flow['convenio']}.",
        f"• Negativas/reclamações: {negatives}.",
        f"• Casos mistos: {by_flow['misto']}.",
        f"• Críticos para cobrar hoje: {len(critical)}.",
    ]
    if critical:
        lines += ["", "Prioridades de cobrança"]
        for index, case in enumerate(critical, start=1):
            lines.append(
                f"{index}. {case['Paciente']} — {case['Procedimento'] or 'procedimento a definir'} — "
                f"{case['Status atual']} — {case['Próxima ação'] or 'definir próxima ação'} — "
                f"{case['Responsável interno'] or 'responsável a definir'}"
            )
    else:
        lines += ["", "Nenhum caso com follow-up vencido ou sem data de acompanhamento."]
    return "\n".join(lines)


def main() -> int:
    try:
        print(render(load_cases()))
    except Exception as exc:
        print(f"ERRO: não foi possível extrair o controle de procedimentos: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
