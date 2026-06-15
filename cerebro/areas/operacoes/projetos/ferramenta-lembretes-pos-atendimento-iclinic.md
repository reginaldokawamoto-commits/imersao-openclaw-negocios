# Ferramenta de lembretes pós-atendimento via iClinic

## Objetivo
Criar uma forma de transformar marcações da agenda do iClinic em tarefas/lembretes operacionais para a secretária/Paola, garantindo que pacientes recebam follow-up no prazo correto após consultas, programas e procedimentos.

## Ideia central

1. A agenda do iClinic registra o que aconteceu com o paciente.
2. Cada tipo de marcação/evento terá uma regra operacional.
3. A regra gera uma tarefa para a Paola com:
   - paciente;
   - origem do evento;
   - prazo de ação;
   - ação esperada;
   - mensagem ou orientação sugerida;
   - status de execução.

## Exemplos trazidos pelo Reginaldo

### 1. Paciente do Programa de Medicina do Estilo de Vida

**Evento no iClinic:** paciente passou hoje em consulta/programa de Medicina do Estilo de Vida.

**Regra desejada:** paciente deve ter nova consulta/agendamento em aproximadamente 30 dias.

**Tarefa gerada para Paola:**
- Data da tarefa: próxima janela definida pela regra, ex.: D+25 ou D+30.
- Ação: entrar em contato com a paciente para agendar a próxima consulta ou verificar se já está agendada.
- Observação: não deixar depender de controle manual.

### 2. Paciente que realizou procedimento

**Evento no iClinic:** paciente realizou procedimento hoje.

**Regra desejada:** no dia seguinte, logo pela manhã, Paola deve mandar mensagem para saber como o paciente está e organizar retorno.

**Tarefa gerada para Paola:**
- Data da tarefa: D+1 pela manhã.
- Ação: enviar mensagem de pós-procedimento.
- Segunda ação possível: agendar retorno/consulta em prazo clínico definido, exemplo D+15.

## Fluxo proposto

```text
iClinic / agenda
    ↓
exportação ou leitura das marcações
    ↓
tabela de regras por tipo de marcação
    ↓
geração de tarefas
    ↓
agenda/lista da Paola
    ↓
execução + status
```

## Campos mínimos necessários da agenda do iClinic

Para montar a automação, precisamos que cada registro tenha, se possível:

- Data do atendimento/procedimento;
- Nome do paciente;
- Telefone ou identificador do paciente;
- Tipo de marcação salvo no iClinic;
- Profissional/unidade, se aplicável;
- Status da consulta, ex.: realizado, faltou, cancelado, remarcado;
- Observações relevantes, se existirem.

## Tabela de regras — versão inicial preenchida

A primeira matriz foi preenchida com os nomes enviados pelo Reginaldo em 15/06/2026.

Arquivo operacional: `cerebro/areas/operacoes/projetos/template-regras-lembretes-iclinic.csv`.

Interpretação dos campos enviados:

- **Nome:** nome exato do tipo salvo no iClinic.
- **Dias:** ciclo/intervalo de referência do atendimento, retorno ou procedimento.
- **Lembrar em (dias):** quando a tarefa deve ser criada após o evento realizado no iClinic.

Regras consolidadas:

| Grupo | Tipos | Ciclo | Criar tarefa | Ação principal |
|---|---|---:|---:|---|
| Consultas e retornos | Consulta, Retorno, Retorno - Bloqueio, Retorno - Procedimento, Consulta - HPS, Consulta - Reembolso Convênio, Consulta _Domiciliar, Consulta 1ª vez - GLM, Avaliação Pré Anestésica | 30 dias | D+16 | Verificar evolução/necessidade de retorno e lembrar/agendar próxima consulta |
| Programa MEV | 1ª Consulta - Programa MEV, Consulta - Programa MEV | 30 dias | D+16 | Organizar próxima consulta do programa MEV |
| Procedimentos e bloqueios | Procedimento, Bloqueio, Bloqueio Botox, 31602118 - Bloqueio de nervo periférico - bloqueios anes... | 15 dias | D+1 | Mensagem pós-procedimento perguntando como está; segunda tarefa em D+15 para retorno |
| Acompanhamentos curtos | Bioimpedância, Curativo, Laser | 7 dias | D+0 | Acompanhamento/orientação no mesmo dia conforme fluxo específico |

## Saída esperada da ferramenta

A ferramenta deve gerar uma lista de tarefas simples, por exemplo:

```text
Data da tarefa: 12/06/2026, 08h30
Responsável: Paola
Paciente: [nome]
Origem: Procedimento realizado em 11/06/2026
Ação: Enviar mensagem perguntando como está após o procedimento e verificar necessidade de agendar retorno.
Status: pendente
```

## Possíveis formatos de implantação

### Opção A — Planilha operacional
Mais simples para começar.

- Exporta agenda do iClinic.
- Aplica regras em planilha/script.
- Gera lista diária de tarefas para Paola.

**Vantagem:** rápido de testar.
**Limite:** depende de exportação/importação manual ou semi-manual.

### Opção B — Integração com Google Agenda / tarefas

- Cada regra cria um evento/tarefa na agenda da Paola.
- Pode ter alerta no horário certo.

**Vantagem:** entra no fluxo diário da secretária.
**Limite:** precisa definir onde a Paola realmente acompanha as tarefas.

### Opção C — Integração com CRM

- Cada regra cria card/tarefa no CRM.
- Fica integrado com vendas, atendimento e pós-atendimento.

**Vantagem:** melhor visão de funil e pendências.
**Limite:** depende dos recursos/API do CRM.

### Opção D — Robô diário

- Todo dia cedo, o robô lê a base/exportação.
- Gera resumo de tarefas do dia para Paola e/ou Reginaldo.

**Vantagem:** reduz esquecimento e cria rotina.
**Limite:** precisa fonte de dados confiável.

## Recomendação inicial

Começar com uma versão simples:

1. Reginaldo envia exemplos reais dos nomes/tipos salvos no iClinic.
2. Montamos a tabela de regras.
3. Criamos um template de tarefas.
4. Testamos por alguns dias com saída em planilha ou mensagem diária.
5. Só depois integramos com agenda/CRM se o fluxo estiver validado.

## Próximos dados que Reginaldo pode enviar

- Print ou exportação da agenda do iClinic com exemplos dos tipos de marcação.
- Lista dos nomes exatos usados para salvar cada tipo de atendimento/procedimento.
- Quais prazos a Dra. Lígia quer para cada caso: D+1, D+7, D+15, D+30 etc.
- Onde a Paola deve receber/acompanhar as tarefas: agenda, CRM, WhatsApp, planilha ou relatório diário.
