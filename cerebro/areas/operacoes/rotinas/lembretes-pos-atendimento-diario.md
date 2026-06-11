# Rotina diária — lembretes pós-atendimento

## Objetivo
Gerar diariamente tarefas para Paola a partir dos atendimentos/procedimentos registrados no iClinic, evitando perda de follow-up.

## Frequência sugerida
Diariamente pela manhã, antes do início dos contatos com pacientes.

## Entradas necessárias

- Agenda/exportação do iClinic do dia anterior e/ou dos últimos dias.
- Tabela de regras: `cerebro/areas/operacoes/projetos/template-regras-lembretes-iclinic.csv`.

## Processo

1. Verificar registros realizados no iClinic.
2. Identificar o tipo salvo na agenda.
3. Aplicar a regra correspondente.
4. Criar tarefa para Paola com data, paciente, origem e ação.
5. Marcar tarefas geradas para evitar duplicidade.
6. Revisar pendências vencidas.

## Saída esperada

Lista diária com:

- tarefas para hoje;
- tarefas vencidas;
- tarefas futuras criadas;
- casos sem regra definida.

## Alerta importante

Todo tipo de marcação novo ou sem regra deve entrar em revisão para Reginaldo decidir o prazo e a ação correta.
