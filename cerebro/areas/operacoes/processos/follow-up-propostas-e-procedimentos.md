# Playbook — Follow-up de propostas e procedimentos

## Objetivo

Garantir que toda proposta, orçamento ou solicitação de procedimento tenha um responsável, uma próxima ação e uma próxima data de follow-up até chegar a um desfecho: agendado, fechado, pausado ou perdido.

## Fonte única de controle

Usar exclusivamente a aba **Controle de Procedimentos** da [planilha operacional](https://docs.google.com/spreadsheets/d/122ARYktTi1RsuCnJNXIV_Bhzg-8lmofOb64yxydmxX8/edit#gid=1236342738).

Não criar listas paralelas em WhatsApp, cadernos ou planilhas pessoais. O WhatsApp serve para conversar com o paciente; o controle precisa ser atualizado na planilha logo após cada contato.

## Regra inegociável

**Nenhum caso fica aberto sem “Próxima ação”, “Próximo follow-up” e “Responsável interno”.**

Se o paciente disser que só poderá fazer no mês seguinte, isso não é encerramento: registrar como `pausado`, anotar o motivo e colocar o próximo follow-up na data combinada ou na primeira semana do mês informado.

## Campos a preencher em cada novo caso

1. Paciente
2. Procedimento proposto
3. Tipo de fluxo: `particular`, `convênio` ou `misto`
4. Convênio, quando aplicável
5. Responsável interno: Paola, salvo exceção definida
6. Data da indicação/solicitação
7. Data de envio do orçamento/proposta, quando aplicável
8. Valor de honorários/proposta, quando aplicável
9. Status atual
10. Último contato
11. Próxima ação
12. Próximo follow-up
13. Observações: resposta do paciente, objeção, prazo prometido ou motivo da pausa/perda

## Status que a equipe deve usar

| Situação real | Status na planilha |
|---|---|
| Caso acabou de entrar | `novo` |
| Orçamento enviado; ainda não houve retorno | `proposta_enviada` |
| Está sendo cobrado/avaliado pelo paciente | `followup_comercial` |
| Paciente concordou com os honorários | `aceitou_orcamento` |
| Solicitação enviada ao convênio | `solicitado_convenio` ou `aguardando_convenio` |
| Falta documento/exame | `pendente_documento` |
| Convênio autorizou | `autorizado` |
| Convênio negou o procedimento/material | `negado` |
| Paciente foi orientado sobre reclamação | `reclamacao_orientada` |
| Aguardar o paciente registrar a reclamação | `aguardando_reclamacao_paciente` |
| Reclamação registrada; aguardar resposta | `reclamacao_feita` |
| Reanálise/recurso enviado ao convênio | `reanalise_convenio` |
| Paciente/hospital ainda precisa definir data | `agendamento_pendente` |
| Data marcada | `agendado` |
| Paciente não fará por agora, mas poderá retomar | `pausado` |
| Paciente decidiu não fazer ou não houve retorno após a cadência | `perdido` |
| Processo finalizado | `fechado` |

## Cadência de follow-up — proposta/orçamento particular

| Momento | Ação | Próximo registro |
|---|---|---|
| Dia do envio | Confirmar que recebeu o orçamento e se colocar à disposição para dúvidas administrativas | `proposta_enviada`; próximo follow-up D+1 |
| D+1 | Perguntar se conseguiu avaliar e se há alguma dúvida administrativa | registrar resposta; próximo follow-up D+3 |
| D+3 | Retomar de forma objetiva e perguntar se está de acordo para avançar para o agendamento | `followup_comercial`; próximo follow-up D+7 |
| D+7 | Solicitar uma definição sem pressionar: seguir, pausar ou não realizar agora | definir próximo passo e data |
| Depois de D+7 | Follow-up semanal por até 30 dias, se o paciente demonstrar interesse | sempre registrar nova data |

Após 30 dias sem resposta, classificar como `perdido` ou `pausado` conforme contexto. Não apagar o caso.

## Respostas esperadas e como registrar

### 1. Paciente está de acordo e quer fazer

- Status: `aceitou_orcamento`.
- Próxima ação: verificar hospital, modalidade de pagamento/reembolso, equipe e datas possíveis.
- Próximo follow-up: em até 1 dia útil, até virar `agendamento_pendente` ou `agendado`.

### 2. Paciente está de acordo, mas depende do convênio/hospital

- Tipo: `misto` ou `convênio`, conforme o caso.
- Status: `solicitado_convenio` ou `aguardando_convenio`.
- Próxima ação: protocolar ou conferir protocolo/documentos.
- Próximo follow-up: duas vezes por semana enquanto aguarda.

### 3. Paciente não consegue fazer agora

- Status: `pausado`.
- Observação: registrar o mês/condição informados pelo paciente, sem expor conteúdo clínico desnecessário.
- Próxima ação: retomar conforme combinado.
- Próximo follow-up: data combinada; se não houver data, primeira semana do mês mencionado.

### 4. Paciente não concorda ou não quer fazer

- Status: `perdido`.
- Observação: registrar motivo objetivo, quando informado (valor, momento, escolha pessoal, outro).
- Não fazer nova cobrança automática sem novo contato do paciente ou decisão de reativação.

### 5. Paciente pede tempo para decidir

- Manter `followup_comercial`.
- Registrar a data prometida pelo paciente.
- Próximo follow-up: no primeiro dia útil depois da data informada; nunca deixar em branco.

### 6. Procedimento ou material negado pelo convênio

- Status inicial: `negado`.
- Próxima ação: orientar o paciente sobre o próximo passo administrativo definido pela clínica; registrar a orientação sem conteúdo clínico desnecessário.
- Se a orientação for reclamação: usar `reclamacao_orientada` e agendar retorno em até 3 dias úteis.
- Após o paciente confirmar o protocolo: usar `reclamacao_feita`; registrar somente data e número de protocolo, quando fornecido.
- Se houver reanálise: usar `reanalise_convenio`; seguir duas vezes por semana até o desfecho.
- Não encerrar caso negado sem registrar a orientação e a próxima data de acompanhamento.

## Scripts de WhatsApp

### Após envio do orçamento

> Olá, [Nome]. Tudo bem?
>
> Enviamos as informações do procedimento conforme conversado. Quando puder, nos confirme se conseguiu avaliar. Caso tenha alguma dúvida administrativa sobre orçamento, hospital, pagamento ou organização do agendamento, estamos à disposição.

### D+3 — decisão para avançar

> Olá, [Nome]. Tudo bem?
>
> Retomando as informações enviadas sobre o procedimento. Você conseguiu avaliar se está de acordo para seguirmos com a organização do agendamento? Se preferir, também podemos esclarecer alguma dúvida administrativa por aqui.

### Paciente quer pausar

> Perfeito, [Nome]. Vamos respeitar o seu momento.
>
> Podemos retomar esse assunto em [mês/data] para verificar se faz sentido avançar? Ficamos à disposição caso precise antes.

### Retomada no mês combinado

> Olá, [Nome]. Tudo bem?
>
> Conforme combinado, estamos retomando o contato sobre o procedimento. Gostaria de verificar se este é um bom momento para conversarmos sobre os próximos passos e disponibilidade de agendamento.

## Rotina operacional da Paola

1. No início do dia, filtrar a aba por `Próximo follow-up` igual ou anterior a hoje.
2. Fazer os contatos previstos.
3. Após cada retorno, atualizar **status, último contato, próxima ação, próximo follow-up e observações** no mesmo dia.
4. No fim do dia, revisar se algum caso aberto ficou sem próxima data.
5. Casos sem resposta, convênio pendente e aceite sem agendamento devem continuar no controle até o desfecho.
6. Negativas e reclamações só saem da fila após confirmação de desfecho, desistência explícita ou nova decisão registrada.

## Acompanhamento do Reginaldo

O resumo deve priorizar somente:

- follow-ups vencidos;
- propostas enviadas sem resposta;
- pacientes que aceitaram, mas ainda não agendaram;
- casos pausados que vencem no mês;
- convênios/negativas que bloqueiam o agendamento;
- responsáveis sem atualização.

## Reunião semanal Reginaldo + Paola

Seguir a [rotina de 15 minutos](../rotinas/reuniao-semanal-paola-procedimentos.md), sempre a partir do relatório gerado pela aba oficial. A reunião serve para remover bloqueios e definir próximos passos; não deve recontar todo o histórico dos casos.

## Ferramenta recomendada

Manter a **aba já existente no Google Sheets** como fonte única neste momento. Ela já suporta responsável, status, último contato, próxima ação e próximo follow-up, e o agente já consegue gerar uma lista de críticos a partir dela.

Antes de adotar um CRM novo, consolidar o uso diário da aba por 30 dias. Depois disso, se a equipe estiver atualizando os campos corretamente, avaliar automação de lembretes e dashboard; criar outra ferramenta agora aumentaria o risco de duplicidade e desatualização.
