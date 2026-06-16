# Rotina — Follow-up de pacientes pós-atendimento

## Objetivo

Criar uma rotina operacional para evitar perda de pacientes após consulta, procedimento ou acompanhamento, garantindo que a Paola tenha um checklist claro do que precisa ser feito diariamente.

A dor principal é não depender da memória da secretária para lembrar quem precisa receber contato, quando, por qual motivo e qual ação deve ser tomada.

## Fonte de dados

Relatório diário do iClinic:

- Rotina de extração: `iclinic-relatorio-pacientes-atendidos.md`
- Campos disponíveis:
  - Data
  - Horário
  - Paciente
  - Procedimento
  - Convênio

## Fluxo operacional proposto

### 1. Extração diária — 23h

Todo dia às 23h, o robô:

1. Acessa o iClinic.
2. Exporta o relatório **Pacientes por período** do dia.
3. Lê o arquivo `.xlsx` gerado.
4. Identifica pacientes atendidos e procedimentos realizados.
5. Gera tarefas futuras de follow-up conforme regra de negócio.

### 2. Geração de tarefas

Cada linha do relatório pode gerar uma ou mais tarefas.

Exemplo:

- Atendimento em 16/06/2026
- Paciente: Maria Silva
- Procedimento: Bloqueio

Tarefas geradas:

- 17/06/2026 — D+1 pós-bloqueio
- 23/06/2026 — D+7 pós-bloqueio

## Checklist diário para Paola

Todo dia pela manhã, idealmente às 08h, Paola recebe um checklist do dia com:

- paciente;
- procedimento;
- origem/data do atendimento;
- tipo de follow-up: D+1, D+7, D+30 etc.;
- ação sugerida;
- status pendente.

Exemplo de mensagem:

```text
Checklist de follow-up — 17/06/2026

1. Maria Silva — Bloqueio — D+1
   Ação: perguntar como está a dor, se houve reação e se precisa de orientação.
   Status: pendente

2. João Souza — Consulta — D+1
   Ação: confirmar se agendou exames/retorno e se ficou alguma dúvida.
   Status: pendente
```

## Controle de status

A rotina deve manter uma base de tarefas com os seguintes campos:

- id da tarefa;
- paciente;
- procedimento;
- convênio;
- data do atendimento;
- horário do atendimento;
- data prevista do follow-up;
- tipo de follow-up: D+1, D+7, D+30 etc.;
- responsável: Paola;
- ação sugerida;
- status:
  - pendente;
  - feito;
  - não respondeu;
  - reagendar contato;
  - precisa de atenção médica;
- observação;
- data/hora de conclusão.

## Formas possíveis de uso

### MVP recomendado

Começar com controle simples em arquivo/planilha dentro do workspace:

- robô gera tarefas automaticamente;
- Paola recebe checklist diário;
- Paola responde com status por mensagem;
- robô atualiza a base;
- Reginaldo recebe resumo diário.

### Evolução futura

Criar painel interno para Paola marcar:

- feito;
- não respondeu;
- reagendar;
- precisa falar com a Dra. Lígia;
- agendou retorno.

## Resumo diário para Reginaldo

Ao fim do dia, idealmente às 18h, o robô pode enviar:

- total de follow-ups previstos;
- quantos foram feitos;
- quantos ficaram pendentes;
- pacientes sem resposta;
- pacientes que precisam de atenção;
- oportunidades de agendamento/retorno.

## Regras iniciais sugeridas

A confirmar com Reginaldo e equipe:

| Procedimento | Follow-up sugerido | Objetivo |
|---|---:|---|
| Consulta médica | D+1 | Confirmar dúvidas, exames e retorno |
| Bloqueio / infiltração | D+1 e D+7 | Verificar dor, reação e evolução |
| Bloqueio Botox / Botox enxaqueca | D+7 e D+30 | Verificar resposta clínica |
| Procedimento genérico | D+1 e D+7 | Checar evolução e orientar retorno |
| Radiofrequência / rizotomia | D+1, D+7 e D+30 | Acompanhar recuperação e resultado |
| MEV / acompanhamento | D+30 ou antes da próxima consulta | Manter adesão e continuidade |
| Curativo | D+1 | Verificar intercorrência e necessidade de retorno |
| Laser | D+7 | Verificar resposta e continuidade |

## Pendências para operacionalizar

1. Definir regras finais por procedimento.
2. Definir horário do checklist da Paola.
3. Definir canal de envio para Paola.
4. Definir como Paola vai marcar status:
   - resposta por mensagem;
   - planilha;
   - painel.
5. Definir modelo de mensagem para cada tipo de follow-up.

## Recomendação

Começar pelo MVP:

- 23h: gerar relatório e tarefas.
- 08h: enviar checklist para Paola.
- Durante o dia: Paola responde status.
- 18h: enviar resumo para Reginaldo.

Depois de validar por alguns dias, evoluir para painel próprio se fizer sentido.
