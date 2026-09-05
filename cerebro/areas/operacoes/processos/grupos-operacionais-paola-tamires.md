# Processo — Grupos Operacionais com Paola e Tamires

- **Solicitante:** Reginaldo Kawamoto
- **Data:** 2026-09-05
- **Objetivo:** criar grupos operacionais com participação do agente para capturar tarefas, acompanhar pendências e evitar que solicitações se percam em mensagens/áudios.
- **Status:** proposta operacional inicial

## Problema identificado

Demandas enviadas por WhatsApp ou conversas soltas acabam ficando para trás porque:

- entram misturadas com outras mensagens;
- podem estar em áudio;
- não viram tarefa rastreável;
- não têm data clara de envio;
- não há baixa padronizada;
- no fim do dia fica difícil saber o que foi resolvido e o que segue pendente.

## Proposta

Criar grupos no Telegram com o agente incluído:

1. **Operacional — Paola**
   - Participantes: Reginaldo, Paola e agente.
   - Foco: atendimento, vendas, mensagens para pacientes, retornos, pendências comerciais/operacionais.

2. **Operacional — Tamires**
   - Participantes: Reginaldo, Tamires e agente.
   - Foco: follow-up iClinic, tarefas de rotina, confirmações de baixa, pendências de contato.

> Recomendação: manter grupos separados para reduzir ruído e permitir relatórios por responsável.

## Função do agente no grupo

O agente deve:

- identificar tarefas novas;
- registrar data e origem da solicitação;
- acompanhar status;
- reconhecer baixas como “feito”, “resolvido”, “mandei”, “concluído”;
- manter pendências abertas quando não houver confirmação;
- apontar tarefas atrasadas;
- enviar resumo de pendências no fim do dia ou começo do dia seguinte;
- evitar que solicitações fiquem perdidas em áudios ou sequência de mensagens.

## Formato ideal das solicitações

Sempre que possível, Reginaldo ou a responsável devem mandar no grupo:

```text
Tarefa: enviar mensagem para paciente José
Responsável: Paola
Prazo: hoje
Contexto: retorno sobre orçamento / agendamento / documento
```

Mas o agente também deve interpretar mensagens naturais, como:

```text
Paola, manda mensagem para o José sobre o retorno do orçamento.
```

E registrar como tarefa.

## Campos mínimos de controle

Cada tarefa deve ter:

- **ID:** identificador simples, ex.: PAO-2026-09-05-001
- **Data de entrada:** quando a tarefa foi solicitada
- **Responsável:** Paola ou Tamires
- **Solicitante:** geralmente Reginaldo
- **Paciente/assunto:** quando aplicável
- **Descrição da tarefa**
- **Prazo:** se informado; se não informado, classificar como “a definir” ou “hoje” quando for claramente operacional do dia
- **Status:** aberta, aguardando retorno, concluída, cancelada ou precisa de tratativa
- **Data da baixa:** quando resolvida
- **Observação:** detalhes relevantes sem expor informação clínica desnecessária

## Status sugeridos

- **Aberta:** tarefa capturada, ainda sem confirmação de execução.
- **Aguardando retorno:** mensagem enviada, mas depende de resposta do paciente/terceiro.
- **Concluída:** responsável confirmou que executou e não há próxima ação pendente.
- **Precisa de tratativa:** houve problema, falta informação ou decisão do Reginaldo/Dra. Lígia.
- **Cancelada:** tarefa não será mais feita.

## Como dar baixa

A responsável pode responder de forma simples:

```text
Feito PAO-001
```

ou:

```text
Mandei mensagem para o José. Aguardando retorno.
```

ou:

```text
Resolvido, paciente confirmou.
```

O agente deve interpretar:

- “mandei” como **aguardando retorno**, salvo se a mensagem indicar conclusão;
- “resolvido/concluído/feito” como **concluída**, se não houver próxima ação;
- “não consegui/faltou informação/deu problema” como **precisa de tratativa**.

## Resumo diário recomendado

### Final do dia

Enviar resumo no grupo, por exemplo:

```text
Resumo operacional — Paola — 05/09

Concluídas:
- PAO-001 — Mensagem enviada para José sobre orçamento.

Aguardando retorno:
- PAO-002 — Paciente Maria recebeu orientação e ficou de responder.

Pendentes:
- PAO-003 — Confirmar documento de Ana. Entrada: 05/09, 14:20.

Precisa de tratativa:
- PAO-004 — Falta definir valor/condição antes de responder paciente.
```

### Começo do dia seguinte

Enviar apenas o que ficou aberto:

```text
Pendências para hoje — Paola — 06/09

1. PAO-003 — Confirmar documento de Ana. Entrada: 05/09, 14:20. Atraso: 1 dia.
2. PAO-004 — Falta definir valor/condição antes de responder paciente. Entrada: 05/09, 16:10.
```

## Frequência sugerida

- **Durante o dia:** agente registra e atualiza conforme mensagens aparecem.
- **Fim do dia:** resumo das concluídas, aguardando retorno e pendentes.
- **Manhã seguinte:** lista objetiva das pendências abertas e atrasadas.

## Boas práticas para o grupo

1. Usar uma mensagem por tarefa sempre que possível.
2. Quando for áudio, o agente deve resumir e transformar em tarefa.
3. Evitar misturar vários pacientes na mesma mensagem.
4. Confirmar baixas com palavras simples: “feito”, “resolvido”, “aguardando retorno”.
5. Não expor diagnósticos, exames ou informações clínicas sensíveis no grupo.
6. Para assuntos clínicos/individuais, encaminhar para canal privado ou avaliação da Dra. Lígia.

## Atenção à privacidade

O grupo operacional pode conter nomes de pacientes e informações administrativas. Evitar registrar:

- diagnóstico;
- exame;
- imagem clínica;
- lista de medicamentos;
- dados pessoais sensíveis;
- detalhes íntimos;
- informações clínicas desnecessárias.

Usar o mínimo necessário para identificar a tarefa administrativa.

## Recomendação de implantação

### Fase 1 — Piloto com Paola

Criar primeiro o grupo **Operacional — Paola** e testar por 7 dias.

Objetivo do piloto:

- validar se o agente captura bem as tarefas;
- ajustar padrão de baixa;
- definir melhor horário dos resumos;
- reduzir retrabalho do Reginaldo.

### Fase 2 — Replicar para Tamires

Depois de estabilizar com Paola, criar **Operacional — Tamires**, aproveitando o padrão validado.

Como Tamires já possui rotina de follow-up iClinic, o grupo dela deve ser mais rigoroso na baixa por ID/checklist.

## Mensagem sugerida para abrir o grupo da Paola

```text
Pessoal, criei este grupo para centralizar as demandas operacionais da Paola e evitar que tarefas se percam no WhatsApp ou em áudios.

A ideia é simples:
- toda solicitação vira uma tarefa;
- quando for feita, a Paola responde “feito”, “resolvido” ou “aguardando retorno”;
- o agente acompanha o que ficou pendente;
- no fim do dia ou no começo do dia seguinte, recebemos um resumo do que ainda precisa de tratativa.

Vamos testar por 7 dias e ajustar o formato.
```

## Mensagem sugerida para abrir o grupo da Tamires

```text
Pessoal, criei este grupo para centralizar as tarefas da Tamires, principalmente follow-ups e pendências operacionais.

A ideia é que cada solicitação seja registrada, acompanhada e baixada quando for concluída.

Quando uma tarefa for feita, basta responder com “feito”, “resolvido” ou “aguardando retorno”. O agente vai organizar as pendências e trazer um resumo diário do que ficou aberto.

Vamos testar o fluxo e ajustar conforme a rotina.
```

## Decisões pendentes

- Confirmar se os grupos serão no Telegram.
- Definir nomes finais dos grupos.
- Definir horário do resumo diário: final do dia, manhã seguinte ou ambos.
- Definir se Reginaldo quer relatórios diários no próprio grupo ou também no privado.
- Definir se Paola e Tamires terão grupos separados desde o início ou se começa apenas com Paola.
