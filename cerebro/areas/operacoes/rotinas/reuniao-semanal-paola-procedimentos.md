# Reunião semanal — Paola + Reginaldo | procedimentos

**Duração máxima:** 15 minutos  
**Frequência:** segunda-feira no início do expediente  
**Fonte única:** aba [Controle de Procedimentos](https://docs.google.com/spreadsheets/d/122ARYktTi1RsuCnJNXIV_Bhzg-8lmofOb64yxydmxX8/edit#gid=1236342738) e relatório extraído dela.

## Objetivo

Sair da reunião com cada pendência relevante classificada, com responsável,
próxima ação e data de retorno. Não usar a reunião para revisar casos já
agendados ou fechados.

## Preparação automática

Antes da reunião, executar:

```bash
python3 cerebro/areas/operacoes/scripts/gerar_relatorio_followup_procedimentos.py
```

O relatório lê exclusivamente a aba oficial. Se falhar por acesso, aba ou
cabeçalho, tratar isso como bloqueio de dados — nunca preencher o resumo por
memória ou template.

## Agenda de 15 minutos

| Tempo | Tema | Resultado obrigatório |
|---|---|---|
| 0–2 min | Painel | Quantos casos ativos, vencidos e sem atualização. |
| 2–6 min | Propostas | Cada orçamento sem resposta: seguir, pausar ou encerrar; definir próxima data. |
| 6–9 min | Aceites sem agenda | Remover a trava: hospital, data, pagamento, reembolso ou documento. |
| 9–12 min | Convênios, negativas e reclamações | Definir a ação da semana e o retorno programado. |
| 12–15 min | Compromissos | Paola confirma as 3–5 prioridades; Reginaldo assume decisões/dependências dele. |

## Perguntas de decisão por caso

1. Qual é o status real hoje?
2. Qual foi o último contato e o que retornou?
3. O que precisa acontecer agora?
4. Quem faz?
5. Qual a data do próximo follow-up?
6. Há bloqueio que depende do Reginaldo, da Dra. Lígia, hospital, convênio ou paciente?

Se uma dessas perguntas ficar sem resposta, o caso não pode sair da reunião sem
registro de `próxima ação` e `próximo follow-up`.

## Saída da reunião

Atualizar a planilha durante ou imediatamente após a reunião e gerar uma nota
curta no formato abaixo:

```markdown
## Follow-up de procedimentos — semana de DD/MM

### Prioridades da Paola
1. Paciente — ação — prazo

### Dependências do Reginaldo/Dra. Lígia
1. Decisão ou liberação necessária — prazo

### Casos pausados/perdidos
- Paciente — motivo — data de retomada, se houver

### Bloqueios
- Caso — bloqueio — próximo responsável
```

## Indicadores semanais

- Casos ativos e casos vencidos.
- Propostas enviadas sem retorno.
- Aceites sem agendamento.
- Convênios parados por mais de 7 dias.
- Negativas sem orientação registrada.
- Reclamações sem protocolo ou retorno.
- Casos sem próxima ação/data: meta é zero.
