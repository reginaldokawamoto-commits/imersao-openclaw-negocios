# Sistema de Contexto Executivo

## Finalidade

Transformar áudios do Reginaldo e conversas relevantes dos grupos em informação acionável, sem tratar conversa bruta como decisão ou tarefa automática.

O sistema organiza cinco tipos de informação:

1. **Contexto** — o que mudou, o que está acontecendo e fatos que ajudam a decidir.
2. **Decisão** — escolha aprovada, responsável por aprovar e impacto esperado.
3. **Ação** — entrega objetiva com responsável e prazo.
4. **Risco/bloqueio** — algo que pode impedir resultado, precisa de resposta ou depende de alguém.
5. **Ideia/hipótese** — proposta ainda não aprovada, que não deve virar execução automaticamente.

## Entradas

### 1. Áudio executivo do Reginaldo

Formato recomendado: uma vez por semana, ou após uma reunião importante. Duração sugerida: 3–8 minutos.

Roteiro de gravação:

1. O que aconteceu desde o último registro?
2. O que continua igual?
3. O que deve começar, parar ou mudar?
4. Quais decisões foram tomadas ou aguardam decisão?
5. Quais ações têm dono e prazo?
6. Quais riscos, dúvidas ou dependências merecem atenção?
7. O que precisa virar meta, projeto ou pauta de reunião?

O áudio não precisa seguir o roteiro à risca. O agente extrai os itens, sinaliza incertezas e pede validação somente quando a interpretação alterar uma decisão, um responsável ou um prazo.

### 2. Conversas dos grupos

Os grupos são fonte de sinais operacionais; não substituem o Cérebro como fonte de verdade.

| Grupo | O que captar | Destino principal |
|---|---|---|
| Diretoria | decisões estratégicas, prioridades, riscos, projetos e metas | `empresa/decisoes/`, `empresa/projetos/` |
| Operacional | pendências, gargalos, mudanças de processo e responsáveis | `areas/operacoes/`, `empresa/projetos/pendencias.md` |
| Social Selling | aprendizados, métricas, testes, regras de relacionamento e demandas de conteúdo | `areas/marketing/` |
| Financeiro/fechamentos | exceções, riscos financeiros, métricas e processos de cobrança | `areas/vendas/financeiro/` |

## Regra de processamento

1. Ler as mensagens novas desde a última consolidação.
2. Deduplicar itens que aparecem em mais de um grupo.
3. Separar **fato**, **decisão confirmada**, **ação solicitada**, **ideia** e **pendência**.
4. Registrar no arquivo de destino correto.
5. Para cada ação, exigir: responsável, próximo passo e prazo ou gatilho de revisão.
6. Não copiar dados clínicos ou financeiros sensíveis para resumos amplos; manter o mínimo necessário e apontar para a fonte operacional autorizada.
7. Nunca converter sugestão ou conversa informal em decisão aprovada sem confirmação explícita.

## Cadência

- **Diária (dias úteis):** triagem curta dos grupos; registrar somente decisões, ações, bloqueios e mudanças relevantes.
- **Semanal:** consolidado para Reginaldo com prioridades, itens vencidos, decisões aguardando validação e riscos.
- **Mensal:** revisão de padrões, metas, projetos, processos que devem parar/continuar/iniciar e decisões estruturais.

## Saídas

- `inbox.md`: entrada temporária e itens que ainda precisam de confirmação.
- `decisoes/YYYY-MM.md`: decisões aprovadas e seu contexto.
- `projetos/pendencias.md`: ações em aberto com dono e prazo.
- Arquivo da área: procedimentos, marketing, financeiro ou atendimento quando o fato pertence a uma operação específica.
- `revisoes-executivas/YYYY-MM.md`: transcrição organizada do áudio executivo e síntese para decisão.

## Indicadores da revisão semanal

- Ações abertas, vencidas e sem responsável.
- Decisões pendentes de validação.
- Bloqueios por área.
- Itens recorrentes por duas ou mais semanas.
- Metas/projetos que precisam de revisão.

## Limite importante

O objetivo é reduzir perda de contexto, não criar um relatório de toda conversa. Mensagens sociais, confirmações simples e informações já registradas não entram na consolidação.
