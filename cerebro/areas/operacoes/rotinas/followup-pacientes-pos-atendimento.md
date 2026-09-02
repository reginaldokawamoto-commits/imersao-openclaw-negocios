# Rotina — Follow-up de pacientes pós-atendimento

## Objetivo

Criar uma rotina operacional para evitar perda de pacientes após consulta, procedimento ou acompanhamento, garantindo que a Tamires tenha um checklist claro do que precisa ser feito diariamente.

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

## Checklist diário para Tamires

Todo dia pela manhã, idealmente às 08h, Tamires recebe um checklist do dia com:

- paciente;
- procedimento;
- origem/data do atendimento;
- tipo de follow-up: D+1, D+7, D+30 etc.;
- ação sugerida;
- status pendente.

Regra crítica: **pendência não some automaticamente**. Se uma tarefa de sábado,
domingo ou qualquer dia anterior não tiver sido explicitamente marcada como
`feito`, `reagendada`, `não respondeu` ou `atenção médica`, ela continua entrando
nos checklists seguintes como pendente acumulada. O checklist diário deve listar
**tudo que está pendente e vencido até a data do checklist**, não apenas as
tarefas criadas para aquele dia.

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
- responsável: Tamires;
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
- Tamires recebe checklist diário;
- Tamires responde com status por mensagem;
- robô atualiza a base;
- Reginaldo recebe resumo diário.

### Evolução futura

Criar painel interno para Tamires marcar:

- feito;
- não respondeu;
- reagendar;
- precisa falar com a Dra. Lígia;
- agendou retorno.

## Resumo diário para Reginaldo

No relatório diário do iClinic, o robô deve enviar para Reginaldo não apenas a contagem/caminho do arquivo, mas também os dados operacionais do checklist gerado:

- paciente;
- procedimento;
- tipo de follow-up;
- ação sugerida;
- total de follow-ups previstos;
- quantos foram feitos;
- quantos ficaram pendentes;
- pacientes sem resposta;
- pacientes que precisam de atenção;
- oportunidades de agendamento/retorno.

A mensagem enviada no Telegram deve trazer **todas** as tarefas pendentes do checklist no corpo da mensagem, sem truncar e sem substituir por caminho de arquivo. Para cada tarefa, incluir paciente, procedimento, tipo de follow-up, data do atendimento, convênio e ação sugerida.

Além das tarefas geradas pelo iClinic, o robô deve manter na mesma base os
follow-ups manuais enviados por Reginaldo ou Tamires no Telegram. Esses follow-ups
manuais também devem acumular enquanto não houver confirmação explícita de
resolução.

### Regra obrigatória para respostas da Tamires no Telegram

Quando Tamires responder `feito 1`, `feito 1-11`, `feito 1, 2, 3` ou formato equivalente, **não basta confirmar no chat**. O agente deve, na mesma hora:

1. localizar o checklist ativo mais recente (`checklist-tamires-YYYY-MM-DD.md`);
2. converter os números informados nos IDs correspondentes;
3. atualizar `tarefas-followup.csv` com status `concluido`, observação e `concluido_em`;
4. regenerar o checklist do dia para remover os itens concluídos;
5. responder confirmando quantos itens foram realmente baixados da base.

Script de apoio: `cerebro/areas/operacoes/scripts/atualizar_followup_paola.py`.

Exemplo:

```bash
python3 cerebro/areas/operacoes/scripts/atualizar_followup_paola.py feito \
  --checklist-date 2026-07-02 \
  --itens 1-11 \
  --origem "Tamires via Telegram" \
  --quando "2026-07-02T09:30:00-03:00"
```

Quando Tamires ou Reginaldo enviar uma **nova tarefa manual de follow-up de paciente**, ela também deve entrar em `tarefas-followup.csv` como `Follow-up manual`, além de qualquer lembrete cron se houver data/horário.

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
| Laser | Não gerar tarefa automática | Paciente costuma vir semanalmente em pacote/sessões; não aplicar follow-up geral. |

## Regra de exceção para laser

A partir de 18/08/2026, atendimentos/procedimentos de **Laser** não devem entrar no checklist automático de follow-up da Tamires. Esses pacientes normalmente vêm a cada 7 dias em pacotes de sessões, então o acompanhamento já acontece na própria agenda.

As regras dos demais procedimentos permanecem ativas.

## Pendências para operacionalizar

1. Definir regras finais por procedimento.
2. Definir horário do checklist da Tamires.
3. Definir canal de envio para Tamires.
4. Definir como Tamires vai marcar status:
   - resposta por mensagem;
   - planilha;
   - painel.
5. Definir modelo de mensagem para cada tipo de follow-up.

## Recomendação

Começar pelo MVP:

- 23h: gerar relatório e tarefas.
- 08h: enviar checklist para Tamires.
- Durante o dia: Tamires responde status.
- 18h: enviar resumo para Reginaldo.

Depois de validar por alguns dias, evoluir para painel próprio se fizer sentido.
