# Rotina diária — lembretes pós-atendimento

## Objetivo
Gerar diariamente tarefas para Tamires a partir dos atendimentos/procedimentos registrados no iClinic, evitando perda de follow-up.

## Frequência e separação de etapas

O processo possui duas rotinas independentes. A entrega não pode substituir a
coleta do iClinic.

1. **23h (São Paulo) — coleta:** baixar o relatório *Pacientes por período* do
   próprio dia, validar data e arquivo e gerar as tarefas para o dia seguinte.
2. **07h (São Paulo) — entrega:** ler exclusivamente a base já atualizada e
   enviar o checklist individual da Tamires.

Se a coleta noturna não produzir o arquivo do dia, a entrega da manhã deve
registrar falha e escalar a correção; nunca apresentar uma lista antiga como se
fosse a atualização do dia anterior.

## Portão de integridade obrigatório

Antes de qualquer envio às 07h, executar:

```bash
python3 cerebro/areas/operacoes/scripts/emitir_checklist_iclinic.py
```

O comando só emite conteúdo quando valida, em conjunto:

- arquivo da véspera existente e não vazio;
- data do arquivo compatível com a data esperada;
- selo de integridade criado na geração noturna;
- hash do relatório igual ao hash validado;
- checklists da Tamires e da Paola regenerados.

Se qualquer condição falhar, o envio é bloqueado e Reginaldo recebe alerta de
falha. Não há fallback para lista antiga.

## Entrega obrigatória

- **Horário:** 07h, horário de São Paulo.
- **Destino:** conversa individual da Tamires no Telegram (ID `1392170583`).
- **Proibido:** publicar este checklist em qualquer grupo.
- O checklist deve trazer primeiro as tarefas da Tamires e, quando houver, uma
  seção separada de cópia para acompanhamento das tarefas atribuídas à Paola.

## Entradas necessárias

- Exportação do iClinic *Pacientes por período* do dia anterior, salva em
  `relatorios/iclinic/downloads/pacientes_periodo_YYYY-MM-DD.xlsx`.
- Tabela de regras: `cerebro/areas/operacoes/projetos/template-regras-lembretes-iclinic.csv`.

## Processo

1. Às 23h, verificar registros realizados no iClinic e baixar o relatório do
   próprio dia.
2. Identificar o tipo salvo na agenda.
3. Aplicar a regra correspondente usando **obrigatoriamente** a tabela oficial `template-regras-lembretes-iclinic.csv`.
4. Criar tarefa para Tamires com data, paciente, origem e ação.
5. Marcar tarefas geradas para evitar duplicidade.
6. Às 07h, revisar pendências vencidas e entregar o checklist somente depois
   de confirmar a existência do relatório mais recente.
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
