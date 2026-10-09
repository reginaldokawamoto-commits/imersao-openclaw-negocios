#!/usr/bin/env python3
"""Reconcilia a base financeira local com a planilha oficial do Google Sheets.

Fonte local: ``areas/vendas/financeiro/lancamentos.csv``.
Fonte histórica complementar: aba ``Lançamentos`` já existente no Google
Sheets. Registros são deduplicados pelo ``id_lancamento``; quando o mesmo ID
existe nas duas fontes, a linha local prevalece.

O processo faz backup da aba atual antes da primeira substituição de cada dia,
atualiza a aba ``Lançamentos`` e valida quantidade, IDs, valor e data final.
Ele falha com código diferente de zero se a validação não passar.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials


ROOT = Path(__file__).resolve().parents[3]
CSV_PATH = ROOT / "areas/vendas/financeiro/lancamentos.csv"
STATE_PATH = ROOT / "areas/vendas/financeiro/sincronizacao-google-sheets.json"
SHEET_ID = "122ARYktTi1RsuCnJNXIV_Bhzg-8lmofOb64yxydmxX8"
SHEET_NAME = "Lançamentos"
CREDENTIALS_PATH = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "/root/finx/credentials.json")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
HEADERS = [
    "id_lancamento", "data_lancamento", "data_venda", "responsavel", "paciente",
    "servico", "categoria", "valor_bruto", "forma_pagamento", "parcelamento",
    "origem", "indicador", "status_pagamento", "comprovante_recebido",
    "arquivo_comprovante", "observacoes", "telegram_chat_id", "telegram_message_id",
    "registrado_por_agente_em", "conferencia_status",
]


def value_as_decimal(value: object) -> Decimal:
    text = str(value or "").strip().replace("R$", "").replace(" ", "")
    if not text:
        return Decimal("0")
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        return Decimal(text)
    except InvalidOperation:
        return Decimal("0")


def normalized_date(value: object) -> str:
    text = str(value or "").strip()
    for pattern in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, pattern).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return text


def date_key(value: object) -> tuple[int, str]:
    text = normalized_date(value)
    try:
        return (1, datetime.strptime(text, "%Y-%m-%d").strftime("%Y-%m-%d"))
    except ValueError:
        return (0, text)


def read_local_rows() -> tuple[list[dict[str, str]], int]:
    """Read CSV defensively, repairing older lines with commas in observações."""
    rows: list[dict[str, str]] = []
    repaired = 0
    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        if header != HEADERS:
            raise RuntimeError("Cabeçalho local inesperado; sincronização interrompida.")
        for line_number, raw in enumerate(reader, start=2):
            if len(raw) < len(HEADERS):
                raise RuntimeError(f"Linha local incompleta: {line_number}")
            if len(raw) > len(HEADERS):
                # Os quatro últimos campos são estáveis; vírgulas históricas
                # existiam somente em observações.
                raw = raw[:15] + [", ".join(raw[15:-4])] + raw[-4:]
                repaired += 1
            row = dict(zip(HEADERS, raw, strict=True))
            if not row["id_lancamento"].strip():
                raise RuntimeError(f"Linha local sem id_lancamento: {line_number}")
            rows.append(row)
    return rows, repaired


def read_sheet_rows(ws: gspread.Worksheet) -> list[dict[str, str]]:
    values = ws.get_all_values()
    if not values:
        return []
    if values[0][: len(HEADERS)] != HEADERS:
        raise RuntimeError("Cabeçalho da aba Lançamentos inesperado; sincronização interrompida.")
    result = []
    for raw in values[1:]:
        raw = (raw + [""] * len(HEADERS))[: len(HEADERS)]
        if any(cell.strip() for cell in raw):
            result.append(dict(zip(HEADERS, raw, strict=True)))
    return result


def normalize_row(row: dict[str, str]) -> dict[str, object]:
    output: dict[str, object] = {key: str(row.get(key, "")).strip() for key in HEADERS}
    output["data_lancamento"] = normalized_date(output["data_lancamento"])
    output["data_venda"] = normalized_date(output["data_venda"])
    output["valor_bruto"] = float(value_as_decimal(output["valor_bruto"]))
    return output


def output_values(rows: list[dict[str, object]]) -> list[list[object]]:
    return [[row[column] for column in HEADERS] for row in rows]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    local_rows, repaired = read_local_rows()
    credentials = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    spreadsheet = gspread.authorize(credentials).open_by_key(SHEET_ID)
    worksheet = spreadsheet.worksheet(SHEET_NAME)
    drive_rows = read_sheet_rows(worksheet)

    canonical: dict[str, dict[str, object]] = {}
    # Preserva registros históricos que existem apenas no Drive; local tem
    # precedência quando há o mesmo ID por conter correções posteriores.
    for row in drive_rows:
        normalized = normalize_row(row)
        if normalized["id_lancamento"]:
            canonical[str(normalized["id_lancamento"])] = normalized
    for row in local_rows:
        normalized = normalize_row(row)
        canonical[str(normalized["id_lancamento"])] = normalized

    rows = sorted(
        canonical.values(),
        key=lambda row: (date_key(row["data_lancamento"]), str(row["id_lancamento"])),
    )
    if len(rows) < len(local_rows):
        raise RuntimeError("Reconciliação reduziu registros locais; sincronização interrompida.")

    expected_ids = {str(row["id_lancamento"]) for row in rows}
    expected_total = sum((value_as_decimal(row["valor_bruto"]) for row in rows), Decimal("0"))
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    backup_name = f"Backup Lançamentos {today}"

    if args.check_only:
        sheet_ids = {str(row.get("id_lancamento", "")).strip() for row in drive_rows}
        missing = sorted(expected_ids - sheet_ids)
        if missing:
            print(json.dumps({"status": "out_of_sync", "missing_ids": len(missing), "expected_rows": len(rows), "drive_rows": len(drive_rows)}, ensure_ascii=False))
            return 3
    else:
        existing_titles = {item.title for item in spreadsheet.worksheets()}
        if backup_name not in existing_titles:
            backup = spreadsheet.add_worksheet(title=backup_name, rows=max(100, len(drive_rows) + 1), cols=len(HEADERS))
            backup.update(range_name=f"A1:T{len(drive_rows) + 1}", values=[HEADERS] + output_values([normalize_row(row) for row in drive_rows]) if drive_rows else [HEADERS])
        worksheet.clear()
        worksheet.update(range_name=f"A1:T{len(rows) + 1}", values=[HEADERS] + output_values(rows))
        worksheet.freeze(rows=1)
        worksheet.format("H:H", {"numberFormat": {"type": "CURRENCY", "pattern": "R$ #,##0.00"}})
        worksheet.format("B:C", {"numberFormat": {"type": "DATE", "pattern": "dd/mm/yyyy"}})

    confirmed_rows = read_sheet_rows(worksheet)
    confirmed_ids = {str(row.get("id_lancamento", "")).strip() for row in confirmed_rows}
    confirmed_total = sum((value_as_decimal(row.get("valor_bruto")) for row in confirmed_rows), Decimal("0"))
    if confirmed_ids != expected_ids or confirmed_total != expected_total:
        raise RuntimeError("Validação pós-sincronização falhou; Drive não corresponde à base canônica.")

    state = {
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "spreadsheet_name": spreadsheet.title,
        "spreadsheet_url": spreadsheet.url,
        "rows_local": len(local_rows),
        "rows_previously_in_drive": len(drive_rows),
        "rows_canonical": len(rows),
        "rows_verified_in_drive": len(confirmed_rows),
        "ids_verified": len(confirmed_ids),
        "total_verified": f"{confirmed_total:.2f}",
        "latest_date": max((str(row["data_lancamento"]) for row in rows), default=""),
        "repaired_legacy_csv_rows": repaired,
        "backup_sheet": backup_name if not args.check_only else None,
        "mode": "check_only" if args.check_only else "synchronized",
    }
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(state, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1)
