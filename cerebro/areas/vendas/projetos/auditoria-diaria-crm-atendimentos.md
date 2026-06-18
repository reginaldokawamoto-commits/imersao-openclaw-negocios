# Auditoria diária de CRM e atendimentos

Criado em 2026-06-18 a partir de solicitação do Reginaldo.

## Objetivo

Avaliar diariamente os atendimentos e movimentações do CRM para identificar erros, acertos, gargalos e oportunidades de melhoria no processo de vendas, de forma tempestiva e contínua.

## Recomendação principal

Começar com **exportação diária de relatórios do CRM** antes de liberar acesso direto ao sistema para o agente.

Motivos:

- Menor risco operacional e de privacidade.
- Mais fácil de auditar e versionar.
- Evita depender de navegação manual em sistema web.
- Permite padronizar indicadores e comparar evolução diária.
- Facilita validar primeiro quais dados realmente ajudam na gestão.

Após 1 a 2 semanas de validação do modelo, avaliar acesso direto/API ao CRM para automatizar coleta e reduzir trabalho manual.

## Opção 1 — Exportação diária do CRM

### Como funcionaria

1. Todos os dias, baixar relatório do CRM referente ao dia anterior ou ao dia corrente.
2. Enviar o arquivo para o agente ou salvar em pasta padrão.
3. O agente processa o arquivo e gera relatório diário de aderência e oportunidades.
4. O relatório é salvo no `cerebro` e enviado para Reginaldo.

### Vantagens

- Implementação rápida.
- Controle sobre o que é compartilhado.
- Baixo risco de alteração acidental no CRM.
- Bom para validar o modelo analítico.

### Limitações

- Depende de alguém baixar/enviar o relatório, salvo se o CRM permitir agendamento automático.
- Pode não trazer conversas completas se o export não incluir histórico de mensagens.

## Opção 2 — Acesso direto ao CRM pelo agente

### Como funcionaria

O agente acessaria o CRM via navegador ou integração/API para consultar leads, tarefas, histórico de atendimento e pendências.

### Vantagens

- Menos trabalho manual depois de configurado.
- Possibilidade de análise mais completa do funil.
- Pode capturar contexto que não aparece no relatório exportado.

### Riscos/cuidados

- Exige credenciais e controle de permissão.
- Preferir usuário específico de auditoria, com permissão somente leitura quando possível.
- Risco maior se o sistema permitir edição sem confirmação.
- Pode quebrar se a interface do CRM mudar.

## Recomendação de implantação

### Fase 1 — 7 a 14 dias

Usar relatório exportado diariamente.

Objetivo: validar quais métricas realmente importam e criar padrão de análise.

### Fase 2 — Automação

Se o relatório diário funcionar, verificar se o CRM permite:

- envio automático por e-mail;
- exportação agendada;
- webhook;
- API;
- acesso com usuário somente leitura.

### Fase 3 — Auditoria contínua

Gerar relatório diário automático com alertas de exceção.

## Campos mínimos desejados no relatório do CRM

### Identificação do lead/paciente

- ID do lead/card.
- Nome.
- Telefone.
- Origem/campanha.
- Data de entrada.
- Responsável.

### Funil comercial

- Etapa atual.
- Etapa anterior.
- Data/hora da última movimentação.
- Próxima tarefa.
- Data da próxima tarefa.
- Status: aberto, ganho, perdido, sem resposta, aguardando paciente etc.
- Motivo de perda, quando houver.

### Atendimento

- Histórico de contatos ou pelo menos resumo/última mensagem.
- Quantidade de tentativas.
- Tempo até primeiro contato.
- Tempo desde último contato.
- Se houve resposta do paciente.
- Se houve agendamento.
- Se houve comparecimento.
- Se houve follow-up após consulta/procedimento.

### Qualificação

- Queixa principal.
- Procedimento/serviço de interesse.
- Capacidade financeira percebida ou etapa de qualificação.
- Objeção principal.
- Temperatura do lead.
- Prioridade.

## Indicadores diários sugeridos

- Novos leads recebidos.
- Leads contatados no dia.
- Leads sem primeiro contato.
- Tempo médio até primeiro contato.
- Leads parados sem próxima ação.
- Tarefas vencidas.
- Tarefas concluídas.
- Taxa de marcação de tarefas pela equipe.
- Agendamentos realizados.
- No-shows ou cancelamentos.
- Leads perdidos e motivos.
- Oportunidades quentes sem follow-up.
- Pacientes atendidos sem pós-atendimento registrado.

## O que o relatório diário deve apontar

### Erros ou riscos

- Lead sem responsável.
- Lead sem próxima tarefa.
- Lead parado há mais de X horas/dias.
- Primeiro contato demorado.
- Conversa encerrada sem tentativa de contorno de objeção.
- Paciente qualificado sem avanço para agendamento.
- Follow-up prometido e não executado.
- Card em etapa errada.
- Perda sem motivo registrado.

### Acertos

- Primeiro contato rápido.
- Boa qualificação.
- Registro claro da objeção.
- Próximo passo agendado.
- Follow-up bem executado.
- Lead recuperado.
- Conversão para agendamento.

### Oportunidades de melhoria

- Ajustes de script.
- Treinamento por objeção recorrente.
- Mudança em etapa do funil.
- Automação de lembrete.
- Criação de tarefa obrigatória.
- Priorização de leads quentes.

## Saída esperada do agente

Relatório diário com:

1. Resumo executivo.
2. Indicadores do dia.
3. Lista de pendências críticas.
4. Erros operacionais encontrados.
5. Bons exemplos de atendimento.
6. Oportunidades de melhoria.
7. Ações recomendadas para o mesmo dia.
8. Mensagens/modelos prontos para a equipe quando necessário.

## Perguntas para configurar

- Qual é o nome do CRM?
- Ele permite exportar relatório em CSV/XLSX?
- Quais relatórios estão disponíveis hoje?
- O relatório inclui histórico de conversa ou apenas status do card?
- Existe API, webhook ou envio automático por e-mail?
- É possível criar usuário somente leitura?
- Quem será responsável por baixar/enviar o relatório na fase 1?
- Qual horário ideal do relatório diário?
