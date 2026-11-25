# Rotina Semanal — AIOS Comercial

## Objetivo

Transformar os dois painéis operacionais do AIOS em uma reunião semanal curta, com controle de execução, gargalos e oportunidades de melhoria. A fonte operacional é o AIOS; nenhum número deve ser completado por estimativa.

## Frequência e entrega

- **Segunda-feira, 07h10 (America/Sao_Paulo).**
- Entrega privada ao Reginaldo.
- Período-base: segunda 00h00 até domingo 23h59 anterior, comparado à semana imediatamente anterior quando existirem dados comparáveis.
- Se a sessão do AIOS estiver expirada, informar a falha e não reutilizar dado antigo como se fosse atual.

## Painel 1 — Campanhas Meta Ads e Google Ads

**Responsável acompanhado:** Tamires.

Extrair, por etapa do funil e por origem/campanha quando preenchida:

1. leads novos;
2. em tentativa de contato e triagem;
3. qualificados;
4. agendados/pagamento; ganhos e perdas;
5. taxas: lead → qualificado, lead → agendamento e lead → ganho; usar `n/a` quando o denominador for zero;
6. cartões sem responsável, sem origem, sem próxima ação ou sem atualização da semana;
7. tempo de primeira resposta quando a data/hora permitir a conta.

### Leitura qualitativa de conversas

Revisar apenas uma amostra mínima e proporcional de conversas dos leads novos/perdidos da semana, preservando privacidade:

- nunca enviar a transcrição bruta no relatório;
- descrever o padrão e citar somente identificador interno/cartão se indispensável;
- verificar demora de resposta, acolhimento inicial, clareza da próxima etapa, tentativa de agendamento, objeção identificada, retorno prometido e registro no cartão;
- separar **fato observado** de **hipótese de melhoria**.

## Painel 2 — Comercial – Procedimento Particular + Follow up

**Responsável acompanhado:** Paola.

Extrair, por etapa:

1. orçamento a enviar;
2. aguardando resposta/follow-up;
3. paciente de acordo aguardando autorização/agendamento;
4. negativas;
5. follow-up/reclamação;
6. ganhos e perdas da semana;
7. valor potencial por etapa, apenas quando o cartão tiver valor;
8. cartões atrasados e cartões sem observação datada, próxima ação ou próximo follow-up.

### Auditoria individual por cartão

Além da leitura do kanban, abrir **cada cartão ativo** do painel e confrontar três fontes antes de concluir o status:

1. **Fase atual do card:** onde o caso está no funil e se essa etapa corresponde ao último desfecho registrado;
2. **Anotações/Histórico:** data da última anotação e evidência do contato realizado;
3. **Relatório estruturado do AIOS:** status do caso, ganho/perda, motivo da perda e status da reclamação/negativa, quando aplicável.

Classificar cada cartão em apenas uma situação de controle:

- **Follow-up em dia:** anotação compatível com a cadência semanal ou com a data combinada, com próximo passo definido;
- **Follow-up vence nesta semana:** contato comprovado, mas a próxima data chega até o próximo relatório;
- **Follow-up vencido:** última anotação ultrapassou sete dias ou a data combinada sem nova evidência de contato;
- **Atualização incompleta:** existe anotação, mas faltam resumo, próxima ação ou próxima data;
- **Etapa/relatório divergente:** fase do card, anotação e campo estruturado apontam desfechos diferentes;
- **Dependência externa:** pendência de paciente, convênio, hospital, Dra. Lígia ou Reginaldo; registrar dono e prazo de cobrança.

Nenhum cartão será considerado acompanhado apenas por estar em uma fase do painel: a anotação datada e o próximo passo são a evidência operacional.

### Regras de controle da Paola

Cada contato semanal, ou no prazo combinado com o paciente, deve registrar no cartão:

- data e canal;
- resumo objetivo da conversa;
- status resultante;
- próxima ação;
- próxima data de follow-up;
- dependência de Reginaldo, Dra. Lígia, hospital ou convênio, quando houver.

Sem esses campos, o item deve aparecer como **atualização não comprovada** — não como ausência de trabalho.

### Leitura qualitativa de conversas

Amostra dos casos em follow-up, perda, negativa/reclamação e aceite sem agenda. Verificar:

- prazo entre orçamento e primeiro retorno;
- se a dúvida/objeção foi registrada;
- clareza sobre próximo passo e prazo;
- convite objetivo para avançar ou para uma pausa com data de retomada;
- consistência da atualização do cartão;
- escalonamento correto de dúvida clínica, pagamento e convênio.

Não avaliar conduta clínica nem recomendar abordagem clínica por conversa. Insights comerciais são para feedback interno; informações identificáveis permanecem restritas ao Reginaldo e à equipe autorizada.

## Formato obrigatório do relatório

1. **Resumo executivo:** até cinco indicadores e comparação disponível.
2. **Tamires — campanhas:** funil, pendências, gargalo principal, até três ações da semana.
3. **Paola — procedimentos:** funil, atrasados, valor potencial, casos sem atualização, até cinco prioridades.
   - Incluir uma lista de exceções por cartão: última anotação, idade da anotação, classificação de controle, próximo passo e responsável.
   - Consolidar perdas por motivo e negativas/reclamações por status, usando o relatório estruturado do AIOS.
4. **Insights de conversa:** fatos observados, oportunidade de feedback e exemplo de comportamento esperado; sem transcrição.
5. **Decisões necessárias do Reginaldo/Dra. Lígia:** somente o que depender deles.
6. **Qualidade da base:** campos ausentes, possíveis duplicidades ou etapas que impedem taxa confiável.

## Critérios de qualidade

- Não tratar “sem dado” como zero.
- Não atribuir uma causa de baixa conversão sem evidência no cartão/conversa.
- Não prometer conversão; propor teste, responsável e métrica de acompanhamento.
- Sempre diferenciar tarefa atrasada, ausência de atualização e dependência externa.
