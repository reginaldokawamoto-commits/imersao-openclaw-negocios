# Rotina — Relatório Semanal de Leads AIOS CRM

## Frequência

- Toda segunda-feira às **06:00 America/Sao_Paulo**.
- Exportar sempre a base inteira do AIOS CRM, sem filtro de data.

## Objetivo

Gerar resumo semanal de leads e conversão do AIOS CRM:

- atendimentos da semana atual vs. semana anterior;
- leads novos da semana, deduplicados por telefone;
- convertidos e taxa de conversão;
- canal #1 de origem;
- alerta/destaque operacional.

## Fonte

- URL: `https://app.aioscrm.com/reports/sessions`
- Tela esperada: **Relatório de atendimentos**.
- Se aparecer login, parar e pedir ao Reginaldo para entrar com `reginaldo.kawamoto@gmail.com`. Não digitar senha.
- A exportação do AIOS abre em Google Sheets; baixar como `.xlsx`.

## Saídas locais

- Downloads: `cerebro/areas/vendas/relatorios/aios/downloads/`
- Relatórios processados: `cerebro/areas/vendas/relatorios/aios/outputs/`
- Script: `cerebro/areas/vendas/scripts/processar_relatorio_aios.py`
- Instrução original recebida: `cerebro/areas/vendas/rotinas/instrucoes-relatorio-aios-original.md`

## Processo resumido

1. Abrir AIOS em `/reports/sessions`.
2. Clicar em **Exportar** → **Exportar relatório**.
3. Aguardar a notificação de exportação finalizar.
4. Abrir a planilha gerada no Google Sheets.
5. Baixar como Excel (`.xlsx`) para a pasta de downloads.
6. Rodar:

```bash
.venv-aios/bin/python cerebro/areas/vendas/scripts/processar_relatorio_aios.py \
  cerebro/areas/vendas/relatorios/aios/downloads/Relatorio_atendimentos_AIOS.xlsx \
  --output-md cerebro/areas/vendas/relatorios/aios/outputs/relatorio-aios-YYYY-MM-DD.md \
  --output-json cerebro/areas/vendas/relatorios/aios/outputs/relatorio-aios-YYYY-MM-DD.json
```

7. Enviar ao Reginaldo um resumo curto em português com período, leads novos, convertidos, variação, canal #1 e alerta.

## Regras importantes

- Semana começa na segunda-feira.
- Cada telefone conta como lead novo apenas na primeira semana em que aparece.
- Conversão = classificação contendo `Cliente` ou `Convertido`, ou data de primeira conversão quando a coluna existir.
- Se colunas mudarem, ajustar aliases no script e registrar a mudança em `cerebro/areas/vendas/contexto/lessons.md`.

## Agendamento OpenClaw

- Cron ID: `4d1062cf-34fa-434c-b8f0-52ce75d1c827`
- Expressão: `0 6 * * 1` em `America/Sao_Paulo`
- Entrega: Telegram do Reginaldo (`telegram:952775153`)

## Status

- 2026-06-26: rotina documentada, script criado e dependências instaladas em `.venv-aios`. Checagem inicial encontrou tela de login do AIOS; Reginaldo precisa entrar manualmente no navegador OpenClaw antes da execução automática.
