# Rotina — Follow-up semanal de procedimentos

**Frequência sugerida:** semanal, segunda-feira de manhã.

**Fonte:** aba [**Controle de Procedimentos**](https://docs.google.com/spreadsheets/d/122ARYktTi1RsuCnJNXIV_Bhzg-8lmofOb64yxydmxX8/edit#gid=1236342738) da planilha operacional oficial. A extração é executada por `cerebro/areas/operacoes/scripts/gerar_relatorio_followup_procedimentos.py`.

> O arquivo `template-controle-procedimentos.csv` é somente um modelo de colunas e nunca deve ser lido como dado operacional.

## Objetivo

Gerar um painel semanal das solicitações de procedimento para o Reginaldo cobrar a responsável interna e manter o follow-up vivo com pacientes e convênios.

## Checklist semanal

1. Verificar todos os casos com `Próximo follow-up` vencido ou vazio.
2. Separar por tipo de fluxo:
   - particular;
   - convênio;
   - misto;
   - negativa/reclamação.
3. Marcar casos críticos:
   - mais de 3 dias sem atualização em proposta particular;
   - mais de 7 dias aguardando convênio sem movimentação;
   - negativa sem orientação registrada ao paciente;
   - paciente orientado a reclamar, mas sem confirmação da reclamação;
   - aceite de orçamento sem avanço na autorização hospitalar.
4. Preparar cobrança objetiva para a secretária/responsável.
5. Sugerir ajustes no processo se houver gargalo recorrente.

## Formato do relatório

```markdown
## Follow-up de procedimentos — semana de DD/MM

### Resumo
- Total de casos abertos:
- Particular em follow-up:
- Convênio aguardando autorização:
- Negativas/reclamações:
- Casos mistos:
- Críticos para cobrar hoje:

### Prioridades de cobrança
1. Paciente — procedimento — status — próxima ação — responsável

### Mensagem sugerida para secretária
Texto direto para cobrança operacional.

### Melhorias de processo observadas
- ...
```
