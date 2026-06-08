# Consolidado financeiro de vendas — consultas e procedimentos

## Objetivo

Consolidar diariamente as vendas/recebimentos enviados pela equipe no Telegram, gerando visão por dia, semana, mês, origem do paciente, tipo de serviço e responsável pelo fechamento.

## Canal proposto

Criar um grupo privado no Telegram com:

- Reginaldo;
- Paola/secretária ou responsável atual;
- futura colaboradora de vendas;
- agente OpenClaw.

Nome sugerido do grupo:

**Financeiro — Fechamentos Dra. Lígia**

## Regra de privacidade

Como há dados de pacientes e comprovantes:

- usar grupo privado e restrito;
- evitar dados clínicos desnecessários;
- registrar apenas o necessário para conferência financeira/comercial;
- preferir iniciais ou nome reduzido quando possível;
- comprovantes devem ser enviados apenas se forem necessários para conferência;
- qualquer relatório externo deve remover dados pessoais dos pacientes.

## Fluxo diário

A cada venda/recebimento, a colaboradora envia uma mensagem no grupo seguindo o modelo abaixo.

O agente deve:

1. Ler a mensagem e anexos enviados no grupo.
2. Extrair os campos principais.
3. Registrar em uma base/planilha de consolidação.
4. Marcar pendências quando faltar informação.
5. Gerar resumo diário do faturamento.
6. Gerar fechamento semanal e mensal quando solicitado ou em rotina programada.

## Modelo de mensagem para a equipe

```text
#fechamento
Data: 02/06/2026
Responsável: Paola
Paciente: Nome ou iniciais
Serviço: Consulta / Procedimento / Bloqueio / Radiofrequência / Programa 6 meses
Valor: R$ 800,00
Forma de pagamento: Pix / Cartão / Dinheiro / Transferência
Parcelamento: à vista / 2x / 3x / outro
Origem: Instagram / TikTok / Google / Indicação / WhatsApp / Retorno / Outro
Indicação por: nome, se houver
Status: pago / sinal pago / pendente / parcelado
Observações: informação relevante
Comprovante: anexar imagem/PDF, se houver
```

## Campos da planilha/base

| Campo | Descrição |
|---|---|
| data_lancamento | Data em que a informação foi registrada |
| data_venda | Data da venda/recebimento |
| responsavel | Quem fechou/registrou a venda |
| paciente | Nome, iniciais ou identificador interno |
| servico | Consulta, procedimento, programa etc. |
| categoria | Consulta / Programa / Bloqueio / Radiofrequência / Outro |
| valor_bruto | Valor informado |
| forma_pagamento | Pix, cartão, dinheiro, transferência etc. |
| parcelamento | À vista, 2x, 3x etc. |
| origem | Instagram, TikTok, Google, indicação etc. |
| indicador | Pessoa/canal de indicação, se houver |
| status_pagamento | Pago, parcial, pendente, parcelado |
| comprovante_recebido | Sim/não |
| arquivo_comprovante | Referência do anexo, quando disponível |
| observacoes | Campo livre |
| mensagem_origem | Link/id da mensagem no Telegram, quando disponível |

## Relatório diário

Resumo sugerido:

```text
Relatório financeiro — DD/MM/AAAA

Total faturado: R$ X
Quantidade de vendas: Y

Por serviço:
- Consulta: Qtd / R$
- Procedimento: Qtd / R$
- Programa 6 meses: Qtd / R$

Por responsável:
- Paola: Qtd / R$
- Outra colaboradora: Qtd / R$

Por origem:
- Instagram: Qtd / R$
- Indicação: Qtd / R$
- Google: Qtd / R$

Pendências:
- venda sem comprovante
- venda sem origem
- pagamento pendente/parcial
```

## Relatório semanal/mensal

Além dos campos do diário, incluir:

- evolução por dia;
- ranking de origem;
- ranking por responsável;
- ticket médio;
- quantidade de consultas vs procedimentos;
- valores pagos vs pendentes;
- alertas de campos incompletos.

## Recomendação inicial

Começar simples:

1. Criar o grupo privado.
2. Usar obrigatoriamente a tag `#fechamento`.
3. Equipe envia os dados no modelo acima.
4. O agente consolida em arquivo/planilha.
5. Após 7 dias, revisar campos e ajustar o processo.

## Google Sheets

Decisão em 2026-06-02: consolidar em **Google Sheets**.

Planilha oficial:

https://docs.google.com/spreadsheets/d/122ARYktTi1RsuCnJNXIV_Bhzg-8lmofOb64yxydmxX8

Inicializada em 2026-06-08 com abas de lançamentos, pendências, resumos e validações.

Conta de serviço disponível no VPS:

`finx-scraper@finx-scraper.iam.gserviceaccount.com`

Observação operacional: a conta de serviço autentica, mas não conseguiu criar uma planilha nova por cota de Drive excedida. Fluxo recomendado:

1. Reginaldo cria uma planilha vazia no Google Drive.
2. Compartilha a planilha como **Editor** com `finx-scraper@finx-scraper.iam.gserviceaccount.com`.
3. Informar o link/ID da planilha ao agente.
4. Agente roda:

```bash
FINANCE_SHEET_ID=<id_da_planilha> python scripts/init_financial_google_sheet.py
```

Isso cria/limpa e estrutura as abas:

- `Lançamentos`
- `Pendências`
- `Resumo Diário`
- `Resumo Semanal`
- `Resumo Mensal`
- `Validações`
- `Modelo Telegram`
