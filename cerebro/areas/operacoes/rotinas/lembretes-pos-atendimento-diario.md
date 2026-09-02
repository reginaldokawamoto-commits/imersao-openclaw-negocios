# Rotina diária — lembretes pós-atendimento

## Objetivo
Gerar diariamente tarefas para Tamires a partir dos atendimentos/procedimentos registrados no iClinic, evitando perda de follow-up.

## Frequência sugerida
Diariamente pela manhã, antes do início dos contatos com pacientes.

## Entradas necessárias

- Agenda/exportação do iClinic do dia anterior e/ou dos últimos dias.
- Tabela de regras: `cerebro/areas/operacoes/projetos/template-regras-lembretes-iclinic.csv`.

## Processo

1. Verificar registros realizados no iClinic.
2. Identificar o tipo salvo na agenda.
3. Aplicar a regra correspondente usando **obrigatoriamente** a tabela oficial `template-regras-lembretes-iclinic.csv`.
4. Criar tarefa para Tamires com data, paciente, origem e ação.
5. Marcar tarefas geradas para evitar duplicidade.
6. Revisar pendências vencidas.
7. Validar se existem procedimentos sem regra oficial. Procedimento sem regra não deve gerar follow-up genérico automaticamente; deve entrar em revisão.
8. Quando Tamires responder `feito <número>` ou `feito <início>-<fim>`, atualizar obrigatoriamente a base `followup/tarefas-followup.csv` usando o ID do checklist do dia. Não basta responder no Telegram.
9. Depois de marcar como feito, regenerar o checklist do dia e o próximo checklist para garantir que tarefas concluídas não reapareçam como pendentes.

## Auditoria anti-regressão

Sempre que houver suspeita de erro, mudança de regra ou checklist estranho, rodar:

```bash
python3 cerebro/areas/operacoes/scripts/auditar_corrigir_followup_iclinic.py \
  --from-date YYYY-MM-DD \
  --to-date YYYY-MM-DD \
  --regenerate-until YYYY-MM-DD
```

A auditoria compara as pendências com a tabela oficial de regras, não altera tarefas já concluídas, cancela pendências incompatíveis e cria tarefas oficiais ausentes.

## Exceção — Laser

A partir de 18/08/2026, pacientes marcados como **Laser** no iClinic não devem gerar tarefa automática de follow-up.

Motivo: laser geralmente é vendido em pacotes/sessões, com retorno semanal a cada 7 dias — muitas vezes 5 sessões. Como o paciente já volta toda semana, não faz sentido aplicar a regra geral de follow-up.

Manter as regras dos demais procedimentos normalmente.

## Baixa de tarefas concluídas

Script operacional:

```bash
python3 cerebro/areas/operacoes/scripts/marcar_tarefas_checklist.py \
  --responsavel Tamires \
  --checklist-date YYYY-MM-DD \
  --feito 1-10 \
  --done-at YYYY-MM-DDTHH:MM:SS-03:00 \
  --origem 'Tamires via Telegram' \
  --regenerate-until YYYY-MM-DD
```

Regra de segurança: resolver o número pelo `ID` dentro do checklist usado por Tamires naquele dia. Nunca marcar por posição atual do CSV, porque a ordem pode mudar quando há pendências antigas.

## Saída esperada

Lista diária com:

- tarefas para hoje;
- tarefas vencidas;
- tarefas futuras criadas;
- casos sem regra definida.

## Alerta importante

Todo tipo de marcação novo ou sem regra deve entrar em revisão para Reginaldo decidir o prazo e a ação correta.
