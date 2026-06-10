# Controle de follow-up — Solicitações de procedimento

Objetivo: dar visibilidade semanal ao Reginaldo sobre todas as solicitações de procedimento, separando particular, convênio e casos mistos, para cobrar execução da secretária e reduzir perda de fechamento/autorização.

## Fluxos principais

### 1. Procedimento 100% particular
Quando a parte médica e hospitalar é particular.

- Enviar proposta/orçamento ao paciente.
- Fazer follow-up comercial até fechamento, perda ou pausa.
- Acompanhar motivo de não fechamento.

**Cadência sugerida:** D+1, D+3, D+7 e depois semanal até 30 dias.

### 2. Procedimento via convênio
Quando depende de solicitação/autorização do convênio.

- Registrar data de envio ao convênio.
- Conferir protocolo e prazo estimado.
- Acompanhar status até autorizado, negado, pendente de documento ou expirado.

**Cadência sugerida:** 2x por semana enquanto estiver aguardando convênio.

### 3. Convênio negado → reclamação do paciente
Quando o convênio não autoriza e o paciente precisa reclamar/acionar o convênio.

- Avisar paciente sobre negativa.
- Orientar reclamação no convênio/ouvidoria/ANS, conforme orientação interna.
- Acompanhar se paciente fez a reclamação.
- Oferecer ajuda se houver dificuldade.
- Registrar retorno do convênio.

**Cadência sugerida:** D+1 após orientação, D+3, D+7 e depois semanal enquanto estiver ativo.

### 4. Caso misto: honorários particulares + hospital via convênio
Quando o paciente aceita o orçamento médico, mas a parte hospitalar depende do convênio.

- Confirmar aceite do orçamento médico.
- Enviar/acompanhar solicitação hospitalar no convênio.
- Manter follow-up duplo: status do convênio + prontidão para agendamento/fechamento.

**Cadência sugerida:** 2x por semana para convênio; semanal para manutenção do fechamento.

## Status padronizados

Use sempre um destes status:

- `novo`
- `proposta_enviada`
- `followup_comercial`
- `aceitou_orcamento`
- `solicitado_convenio`
- `aguardando_convenio`
- `pendente_documento`
- `autorizado`
- `negado`
- `reclamacao_orientada`
- `aguardando_reclamacao_paciente`
- `reclamacao_feita`
- `reanalise_convenio`
- `agendamento_pendente`
- `agendado`
- `fechado`
- `perdido`
- `pausado`

## Campos obrigatórios do controle

A planilha/base deve ter, no mínimo:

- ID
- Paciente
- Procedimento
- Tipo de fluxo
- Convênio
- Responsável interno
- Data da indicação/solicitação
- Data do envio da proposta
- Valor particular/honorários
- Data do envio ao convênio
- Protocolo do convênio
- Status atual
- Último contato
- Próximo follow-up
- Dias sem atualização
- Próxima ação
- Observações
- Motivo de perda/negação, quando existir

## Relatório semanal do agente

Toda semana o agente deve levantar:

1. Pendências vencidas ou sem próxima ação.
2. Casos aguardando convênio há muitos dias.
3. Negativas que ainda não viraram follow-up de reclamação.
4. Pacientes com proposta particular enviada e sem resposta.
5. Casos aceitos que ainda dependem de convênio hospitalar.
6. O que precisa ser cobrado da secretária/responsável.

Saída esperada para o Reginaldo:

- **Resumo executivo:** total por status e prioridades.
- **Lista crítica:** pacientes/casos que exigem cobrança imediata.
- **Cobrança sugerida para a secretária:** mensagem objetiva com os pontos.
- **Ajustes de processo:** gargalos recorrentes e melhorias.
