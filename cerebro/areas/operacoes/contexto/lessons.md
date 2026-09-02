# Lições Aprendidas — [Área]

> O que aprendemos com erros e acertos nesta área. Cada lição gera uma ação concreta.

---

## Setembro 2026

### 02/09 — Follow-up iClinic não pode ter regra duplicada no código

- **Problema:** o checklist de follow-up voltou a gerar pendências erradas porque o script usava regras hardcoded antigas em vez da tabela oficial `template-regras-lembretes-iclinic.csv`.
- **Risco:** sempre que a regra operacional muda no CSV/documentação, o script antigo poderia continuar gerando tarefas pelo padrão anterior.
- **Ação:** `gerar_tarefas_followup_iclinic.py` passou a ler a tabela oficial; procedimentos sem regra oficial não geram follow-up genérico automático; criada auditoria `auditar_corrigir_followup_iclinic.py` para corrigir pendências incompatíveis sem mexer no que já foi concluído.
- **Regra daqui pra frente:** toda mudança de follow-up precisa ser feita na tabela oficial e validada com teste/auditoria antes de enviar checklist.

<!-- Template:
### [Título da lição]
- **Contexto:** [O que aconteceu]
- **Lição:** [O que aprendemos]
- **Ação:** [O que fizemos / vamos fazer diferente]
-->

---

_Atualizado: setembro 2026_
