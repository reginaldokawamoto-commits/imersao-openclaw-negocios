# Rotina — Captura de tarefas por áudio no Telegram

## Objetivo

Permitir que Reginaldo envie tarefas rápidas por áudio no Telegram, sem precisar parar para anotar, e que o agente transforme isso em item acompanhável.

## Como Reginaldo pode enviar

Formato livre, mas idealmente contendo:

- **O que precisa ser feito**
- **Para quem / com quem**
- **Prazo**, se existir
- **Prioridade**, se for urgente
- **Responsável**, se não for o próprio Reginaldo

Exemplos:

- “Me lembra amanhã às 9h de enviar o relatório para a Patrícia.”
- “Coloca na minha lista: pagar o boleto do banco até sexta.”
- “Preciso cobrar a Paola hoje à tarde sobre as autorizações de convênio.”
- “Criar tarefa para enviar documento para o paciente João até amanhã.”

## Comportamento do agente

Ao receber uma tarefa por áudio, o agente deve:

1. Interpretar a tarefa.
2. Confirmar de forma curta o que entendeu.
3. Se houver data/horário claros, criar lembrete via cron.
4. Se não houver prazo, registrar como pendência sem data e perguntar apenas se o prazo for necessário.
5. Se a tarefa envolver ação externa sensível — pagamento, transferência, envio de documento, mensagem para terceiros — **não executar automaticamente**; apenas lembrar, organizar ou pedir confirmação.

## Campos padrão da tarefa

- Data de criação
- Tarefa
- Categoria: financeiro, atendimento, marketing, operação, pessoal, outro
- Responsável
- Prazo
- Status: aberto, aguardando, concluído, cancelado
- Próximo lembrete
- Observações

## Arquivo local de inbox

As tarefas sem sistema externo definido podem ser registradas em:

`cerebro/empresa/projetos/inbox-tarefas.md`

## Regras importantes

- Para tarefas com prazo claro, criar lembrete no horário pedido.
- Para “hoje”, se não houver horário, sugerir/assumir fim do dia útil, salvo urgência.
- Para “amanhã”, se não houver horário, assumir 09:00.
- Para tarefas financeiras, lembrar e organizar, mas nunca executar pagamento/transferência sem comando explícito e confirmação.
- Para envio de documentos ou mensagens a terceiros, preparar texto/checklist, mas pedir confirmação antes de enviar.

## Resposta ideal

Curta, exemplo:

> Anotado: enviar relatório para Patrícia amanhã às 9h. Vou te lembrar nesse horário.

Ou, se faltar prazo:

> Anotei: enviar documento para João. Quer que eu coloque algum prazo ou deixo na lista de pendências?
