# Auditoria — Google Sheets de fechamentos financeiros

**Data da auditoria:** 09/10/2026  
**Escopo:** confronto entre a base consolidada local e a planilha oficial do Google Sheets, sem realizar qualquer alteração no Drive.

## Arquivo auditado

- **Nome:** `Financeiro - Fechamentos Dra. Lígia`
- **Link direto:** https://docs.google.com/spreadsheets/d/122ARYktTi1RsuCnJNXIV_Bhzg-8lmofOb64yxydmxX8/edit?usp=drivesdk
- **Abas:** `Lançamentos`, `Pendências`, `Resumo Diário`, `Resumo Semanal`, `Resumo Mensal`, `Validações`, `Modelo Telegram`.
- **Última modificação no Google Drive:** **01/09/2026 às 12:51 UTC**.
- **Pasta-pai retornada pela API do Drive:** nenhuma; o arquivo está acessível pelo link direto acima.

## Resultado

| Verificação | Resultado |
|---|---:|
| Linhas na base local `lancamentos.csv` | 105 |
| Linhas na aba `Lançamentos` do Google Sheets | 35 |
| IDs presentes nas duas bases | 4 |
| IDs presentes apenas na base local | 101 |
| IDs presentes apenas no Drive | 31 |
| Data mais recente registrada no Drive | 01/09/2026 |
| Lançamentos locais de outubro | 10 |
| Lançamentos de outubro encontrados no Drive | 0 |

## Conclusão

A planilha do Google Drive está **desatualizada**. Ela não é, neste momento, um espelho confiável da base consolidada local nem dos fechamentos enviados pela Paola e pela Tamires no grupo Financeiro.

Os 10 lançamentos registrados localmente entre 01 e 09/10 — total de **R$ 50.861,50** — não constam no Drive. A lacuna começou após 01/09 e exige reconciliação antes que a planilha seja usada para fechamento ou tomada de decisão.

## Próximos passos propostos

1. Confirmar que este arquivo é a planilha oficial que deve receber a base atual.
2. Fazer backup/exportação da planilha existente.
3. Atualizar a aba `Lançamentos` a partir da base local, preservando ou recriando abas de resumo e pendências.
4. Criar rotina de sincronização com validação: quantidade de linhas, último ID, valor acumulado e data de atualização.
5. Alertar imediatamente se a planilha ficar mais de 24 horas sem refletir novos fechamentos.

## Correção executada em 09/10/2026

- A aba `Lançamentos` foi recomposta a partir da base local e dos registros históricos existentes no Drive.
- Antes da atualização, foi criada a aba de segurança `Backup Lançamentos 20261009` com o conteúdo anterior.
- Resultado validado após gravação: **136 lançamentos**, total de **R$ 333.148,44**, com último lançamento em **09/10/2026**.
- Uma rotina determinística foi criada para executar todos os dias às **23:15 (America/Sao_Paulo)**. Ela reconcilia IDs, quantidade de linhas, valor acumulado e data final; qualquer falha gera alerta ao Reginaldo.
