# Instruções: Relatório Semanal de Leads — AIOS CRM

Este documento ensina você a gerar o relatório semanal de leads e conversão a partir do AIOS CRM. Siga os passos na ordem.

---

## Contexto

O Reginaldo é dono de uma clínica/consultório. Ele usa o AIOS CRM para gerenciar atendimentos via WhatsApp. Todo atendimento novo entra como um lead. O objetivo do relatório é responder: **quantos leads novos chegaram essa semana, de qual canal, e quantos viraram clientes?**

A base do AIOS é exportada **sempre inteira** (histórico desde ago/2025). Isso é correto — permite comparar semana a semana e mês a mês.

---

## Passo 1 — Acessar e exportar o relatório no AIOS

1. Abra o navegador e acesse: `https://app.aioscrm.com/reports/sessions`
2. Confirme que a página mostra o título **"Relatório de atendimentos"** com o total de atendimentos no topo.
   - Se aparecer tela de login, pare e avise o Reginaldo para entrar com `reginaldo.kawamoto@gmail.com`. Nunca tente digitar a senha.
3. Clique no botão **"Exportar"** no canto superior direito.
4. Na janela que aparecer, selecione **"Exportar relatório"** (já vem selecionado por padrão) e clique em **"Exportar"**.
5. Aguarde a exportação processar — a base tem ~7 mil atendimentos, pode levar de 1 a 3 minutos.
6. Quando concluir, clique no **ícone de sino (�bell)** no canto superior direito. Vai aparecer um painel de notificações.
7. Clique na notificação mais recente que diga **"Exportação de atendimentos — X atendimentos exportados"** (a de agora, não as antigas).
8. Isso vai abrir o arquivo no **Google Sheets** em uma nova aba.

> **Importante:** O AIOS não faz download de .xlsx direto — ele salva em Google Sheets. A URL da planilha terá este formato:
> `https://docs.google.com/spreadsheets/d/ID_DA_PLANILHA/edit`

---

## Passo 2 — Baixar o arquivo como Excel (.xlsx)

Com a planilha do Google Sheets aberta, baixe o arquivo em formato Excel:

**Opção A — pelo menu do Google Sheets:**
- Clique em **Arquivo → Fazer download → Microsoft Excel (.xlsx)**

**Opção B — pela URL direta** (substitua `ID_DA_PLANILHA` pelo ID real):
```
https://docs.google.com/spreadsheets/d/ID_DA_PLANILHA/export?format=xlsx
```

Salve o arquivo com o nome: `Relatorio_atendimentos_AIOS.xlsx`

---

## Passo 3 — Processar os dados com Python

Use o interpretador de código (Code Interpreter) para analisar o arquivo. Cole e execute o código abaixo, apontando para o arquivo baixado.

```python
import pandas as pd
from datetime import date, timedelta
from collections import defaultdict

# ── CONFIGURAÇÃO ──────────────────────────────────────────────
ARQUIVO = "Relatorio_atendimentos_AIOS.xlsx"   # caminho do arquivo baixado

# ── LEITURA ───────────────────────────────────────────────────
df = pd.read_excel(ARQUIVO, dtype=str)
print(f"✅ Lido: {len(df)} linhas | Colunas: {list(df.columns)}")
```

> Se as colunas impressas forem diferentes do esperado, me mostre e ajuste os nomes abaixo.

```python
# ── MAPEAMENTO DE COLUNAS (ajuste conforme necessário) ────────
COL_TELEFONE    = "Contato/Telefone"
COL_DATA        = "Data criação"          # data do atendimento
COL_STATUS      = "Classificação"         # Cliente / Perdido / etc.
COL_CANAL_UTM   = "UTM/Origem"
COL_CANAL_TAG   = "Tags"                  # pode não existir — ok
COL_DATA_CONV   = "Data 1ª Conv."         # data da primeira conversão

# ── NORMALIZAÇÃO ──────────────────────────────────────────────
df[COL_DATA] = pd.to_datetime(df[COL_DATA], dayfirst=True, errors='coerce')
df['SemanaChave'] = df[COL_DATA].dt.to_period('W-SUN').dt.start_time.dt.date

# Semana atual e anterior
hoje = date.today()
dias_desde_segunda = hoje.weekday()
semana_atual = hoje - timedelta(days=dias_desde_segunda)
semana_anterior = semana_atual - timedelta(weeks=1)

print(f"Semana atual:   {semana_atual}")
print(f"Semana anterior: {semana_anterior}")

# ── LEADS ÚNICOS (deduplicação por telefone) ──────────────────
# Um telefone conta como lead novo apenas na semana em que apareceu pela 1ª vez
df_sorted = df.sort_values(COL_DATA)
primeira_vez = df_sorted.drop_duplicates(subset=[COL_TELEFONE], keep='first').copy()
primeira_vez['EhLeadNovo'] = True
df = df.merge(primeira_vez[[COL_TELEFONE, 'EhLeadNovo']], on=COL_TELEFONE, how='left')
df['EhLeadNovo'] = df['EhLeadNovo'].fillna(False)

# ── CANAL ─────────────────────────────────────────────────────
CANAIS_CONHECIDOS = [
    'CAMPANHA', 'INSTAGRAM', 'TIKTOK', 'FACEBOOK', 'GOOGLE',
    'INDICAÇÃO', 'SITE', 'HOSPITAL', 'CONTATO DIRETO',
    'EMPRESA', 'OUTBOUND'
]

def detectar_canal(row):
    utm = str(row.get(COL_CANAL_UTM, '') or '').upper()
    for c in CANAIS_CONHECIDOS:
        if c in utm:
            return c
    return 'NÃO RASTREADO'

if COL_CANAL_UTM in df.columns:
    df['Canal'] = df.apply(detectar_canal, axis=1)
else:
    df['Canal'] = 'NÃO RASTREADO'

# ── ANÁLISE SEMANAL ───────────────────────────────────────────
def analise_semana(semana):
    s = str(semana)
    mask = df['SemanaChave'].astype(str) == s
    sub = df[mask]
    leads = sub[sub['EhLeadNovo'] == True]

    # Conversões que aconteceram nessa semana
    if COL_DATA_CONV in df.columns:
        df['DataConv'] = pd.to_datetime(df[COL_DATA_CONV], dayfirst=True, errors='coerce')
        conv_mask = (
            (df['DataConv'] >= pd.Timestamp(semana)) &
            (df['DataConv'] < pd.Timestamp(semana) + timedelta(weeks=1))
        )
        convertidos = df[conv_mask][COL_TELEFONE].nunique()
    else:
        convertidos = sub[sub[COL_STATUS].str.upper().str.contains('CLIENTE', na=False)][COL_TELEFONE].nunique()

    canal_top = leads['Canal'].value_counts().idxmax() if len(leads) > 0 else 'N/A'
    canal_top_n = leads['Canal'].value_counts().max() if len(leads) > 0 else 0

    return {
        'atendimentos': len(sub),
        'leads_novos': len(leads),
        'convertidos': convertidos,
        'conv_pct': round(convertidos / len(leads) * 100, 1) if len(leads) > 0 else 0,
        'canal_top': canal_top,
        'canal_top_n': canal_top_n,
        'canais': leads['Canal'].value_counts().to_dict()
    }

atual = analise_semana(semana_atual)
anterior = analise_semana(semana_anterior)

# ── RELATÓRIO ─────────────────────────────────────────────────
print("\n" + "="*50)
print(f"📊 RELATÓRIO SEMANAL — {semana_atual}")
print("="*50)
print(f"\n📅 Período da base: {df[COL_DATA].min().date()} a {df[COL_DATA].max().date()}")
print(f"   Total atendimentos: {len(df):,}")
total_leads = len(primeira_vez)
total_conv = df[COL_STATUS].str.upper().str.contains('CLIENTE', na=False).sum() if COL_STATUS in df.columns else 0
print(f"   Total leads únicos: {total_leads:,} | Taxa geral: {total_conv/total_leads*100:.1f}%")

print(f"\n🗓️  SEMANA ATUAL ({semana_atual} — em andamento):")
print(f"   Atendimentos: {atual['atendimentos']}")
print(f"   Leads novos:  {atual['leads_novos']}")
print(f"   Convertidos:  {atual['convertidos']} ({atual['conv_pct']}%)")
print(f"   Canal #1:     {atual['canal_top']} ({atual['canal_top_n']} leads)")
print(f"   Todos canais: {atual['canais']}")

print(f"\n📆 SEMANA ANTERIOR ({semana_anterior} — completa):")
print(f"   Atendimentos: {anterior['atendimentos']}")
print(f"   Leads novos:  {anterior['leads_novos']}")
print(f"   Convertidos:  {anterior['convertidos']} ({anterior['conv_pct']}%)")
print(f"   Canal #1:     {anterior['canal_top']} ({anterior['canal_top_n']} leads)")

variacao = atual['leads_novos'] - anterior['leads_novos']
sinal = "+" if variacao >= 0 else ""
print(f"\n📈 Variação leads novos vs. semana anterior: {sinal}{variacao}")
print("="*50)
```

---

## Passo 4 — Resumo para o Reginaldo

Após rodar o código, escreva um resumo curto em português com:

1. Período coberto pela base
2. Total de atendimentos novos vs. semana anterior
3. **Leads novos da semana** (número principal — telefones inéditos)
4. Convertidos da semana + taxa de conversão
5. Tendência vs. semana anterior (% ou diferença)
6. Canal #1 da semana em leads novos
7. 1 alerta ou destaque (ex: canal novo surgindo, queda forte, mês fechando bem)

**Exemplo de formato:**

> 📊 Semana 15–21/jun: **19 leads novos**, 9 convertidos (47%). Canal #1: Contato Direto (8).
> Vs. semana anterior: −2 leads (queda leve). TikTok voltou a aparecer com 1 lead.

---

## Canais reconhecidos

| Canal | Como identificar no UTM |
|---|---|
| CAMPANHA (Meta Ads) | `campanha`, `meta`, `facebook ads` |
| INSTAGRAM | `instagram` |
| TIKTOK | `tiktok` |
| GOOGLE | `google` |
| INDICAÇÃO | `indicacao`, `indicação` |
| SITE | `site`, `organico` |
| CONTATO DIRETO | sem UTM, iniciado pelo cliente |
| EMPRESA (Outbound) | `empresa`, `outbound` |
| NÃO RASTREADO | sem nenhuma informação de origem |

---

## Dicas importantes

- **Nunca** filtre a base por data antes de exportar — exporte tudo sempre. A deduplicação por telefone garante que cada pessoa seja contada como lead novo apenas uma vez.
- A semana começa na **segunda-feira**.
- Se um número aparece em semanas diferentes, ele é lead novo apenas na primeira semana em que entrou.
- Conversão = status "Cliente" ou "Convertido" na coluna de classificação.
- Se o AIOS mudar a estrutura da planilha (colunas diferentes), ajuste o `MAPEAMENTO DE COLUNAS` no início do código.

---

## Solução de problemas

| Problema | O que fazer |
|---|---|
| Tela de login no AIOS | Peça ao Reginaldo para entrar manualmente. Não tente digitar senha. |
| Colunas diferentes do esperado | Imprima `df.columns` e ajuste o mapeamento |
| Erro ao ler o xlsx | Tente `pd.read_excel(ARQUIVO, sheet_name=0)` |
| Datas não parseadas | Tente `dayfirst=False` ou inspecione o formato da coluna |
| Google Sheets pede permissão | Peça ao Reginaldo para compartilhar a planilha com sua conta |
