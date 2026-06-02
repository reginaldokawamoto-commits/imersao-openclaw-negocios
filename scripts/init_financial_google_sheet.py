#!/usr/bin/env python3
"""Initialize the Dra. Ligia financial consolidation Google Sheet.

Usage:
  FINANCE_SHEET_ID=<spreadsheet_id> python scripts/init_financial_google_sheet.py

The target spreadsheet must be shared as editor with:
  finx-scraper@finx-scraper.iam.gserviceaccount.com
"""
from __future__ import annotations

from datetime import datetime, timezone
import os
import sys

import gspread
from google.oauth2.service_account import Credentials

CREDS = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE', '/root/finx/credentials.json')
SPREADSHEET_ID = os.environ.get('FINANCE_SHEET_ID')

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

HEADERS = [
    'id_lancamento', 'data_lancamento', 'data_venda', 'responsavel', 'paciente',
    'servico', 'categoria', 'valor_bruto', 'forma_pagamento', 'parcelamento',
    'origem', 'indicador', 'status_pagamento', 'comprovante_recebido',
    'arquivo_comprovante', 'observacoes', 'telegram_chat_id', 'telegram_message_id',
    'registrado_por_agente_em', 'conferencia_status'
]

VALIDACOES = [
    ['Campo', 'Valores sugeridos'],
    ['servico', 'Consulta; Programa 6 meses; Bloqueio; Botox enxaqueca; Radiofrequência/Rizotomia; Outro'],
    ['categoria', 'Consulta; Programa; Procedimento; Outro'],
    ['forma_pagamento', 'Pix; Cartão crédito; Cartão débito; Dinheiro; Transferência; Outro'],
    ['parcelamento', 'À vista; 2x; 3x; 4x; 5x; 6x; Outro'],
    ['origem', 'Instagram; TikTok; Google; Facebook; Indicação; WhatsApp; Retorno; Outro'],
    ['status_pagamento', 'Pago; Sinal pago; Parcial; Pendente; Parcelado; Cancelado'],
    ['comprovante_recebido', 'Sim; Não'],
    ['conferencia_status', 'OK; Pendente; Revisar'],
]


def ensure_ws(sh, title, rows=1000, cols=20):
    try:
        ws = sh.worksheet(title)
        ws.clear()
        return ws
    except gspread.WorksheetNotFound:
        return sh.add_worksheet(title=title, rows=rows, cols=cols)


def main() -> int:
    if not SPREADSHEET_ID:
        print('Missing FINANCE_SHEET_ID', file=sys.stderr)
        return 2

    creds = Credentials.from_service_account_file(CREDS, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SPREADSHEET_ID)

    ws = ensure_ws(sh, 'Lançamentos', rows=10000, cols=20)
    ws.update('A1:T1', [HEADERS])
    ws.freeze(rows=1)
    try:
        ws.set_basic_filter('A1:T10000')
        ws.format('A1:T1', {'textFormat': {'bold': True}, 'backgroundColor': {'red': 0.88, 'green': 0.94, 'blue': 1.0}})
        ws.format('H:H', {'numberFormat': {'type': 'CURRENCY', 'pattern': 'R$ #,##0.00'}})
        ws.format('B:C', {'numberFormat': {'type': 'DATE', 'pattern': 'dd/mm/yyyy'}})
    except Exception:
        pass

    pend = ensure_ws(sh, 'Pendências', rows=1000, cols=12)
    pend.update('A1:L1', [[
        'data', 'id_lancamento', 'responsavel', 'paciente', 'servico', 'valor_bruto',
        'tipo_pendencia', 'campo_faltante', 'observacao', 'telegram_message_id', 'status', 'resolvido_em'
    ]])
    pend.freeze(rows=1)

    res_dia = ensure_ws(sh, 'Resumo Diário', rows=1000, cols=12)
    res_dia.update('A1:D1', [['Métrica', 'Valor', 'Observação', 'Atualização']])
    res_dia.update('A2:B8', [
        ['Total faturado', '=SUM(Lançamentos!H2:H)'],
        ['Quantidade de vendas', '=COUNTA(Lançamentos!A2:A)'],
        ['Ticket médio', '=IFERROR(B2/B3,0)'],
        ['Pagos', '=COUNTIF(Lançamentos!M2:M,"Pago")'],
        ['Pendentes/parciais', '=COUNTIF(Lançamentos!M2:M,"Pendente")+COUNTIF(Lançamentos!M2:M,"Parcial")+COUNTIF(Lançamentos!M2:M,"Sinal pago")'],
        ['Com comprovante', '=COUNTIF(Lançamentos!N2:N,"Sim")'],
        ['Sem comprovante', '=COUNTIF(Lançamentos!N2:N,"Não")'],
    ])
    try:
        res_dia.format('A1:D1', {'textFormat': {'bold': True}, 'backgroundColor': {'red': 0.88, 'green': 0.94, 'blue': 1.0}})
        res_dia.format('B2:B4', {'numberFormat': {'type': 'CURRENCY', 'pattern': 'R$ #,##0.00'}})
    except Exception:
        pass

    res_sem = ensure_ws(sh, 'Resumo Semanal', rows=1000, cols=12)
    res_sem.update('A1:E1', [['Semana', 'Total faturado', 'Qtd vendas', 'Ticket médio', 'Observações']])

    res_mes = ensure_ws(sh, 'Resumo Mensal', rows=1000, cols=12)
    res_mes.update('A1:E1', [['Mês', 'Total faturado', 'Qtd vendas', 'Ticket médio', 'Observações']])

    val = ensure_ws(sh, 'Validações', rows=100, cols=4)
    val.update(f'A1:B{len(VALIDACOES)}', VALIDACOES)
    val.freeze(rows=1)

    modelo = ensure_ws(sh, 'Modelo Telegram', rows=100, cols=4)
    modelo.update('A1', [['Modelo para enviar no grupo']])
    modelo.update('A2', [["""#fechamento
Data:
Responsável:
Paciente:
Serviço:
Valor:
Forma de pagamento:
Parcelamento:
Origem:
Indicação por:
Status:
Observações:
Comprovante: anexar imagem/PDF"""]])

    stamp = datetime.now(timezone.utc).isoformat()
    print(f'initialized={sh.url}')
    print(f'updated_at={stamp}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
