#!/usr/bin/env python3
"""Processa exportação completa do AIOS CRM e gera relatório semanal de leads.

Uso:
  python3 processar_relatorio_aios.py caminho/Relatorio_atendimentos_AIOS.xlsx \
    --output-md cerebro/areas/vendas/relatorios/aios/outputs/relatorio-aios-YYYY-MM-DD.md

A semana de referência começa na segunda-feira. Por padrão usa a data atual em
America/Sao_Paulo; use --today YYYY-MM-DD para testes/reprocessamento.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

TZ = ZoneInfo("America/Sao_Paulo")

COLUMN_ALIASES = {
    "telefone": ["Contato/Telefone", "Telefone", "Contato Telefone", "Contato", "Phone"],
    "data": ["Data criação", "Data de criação", "Criado em", "Data", "Created At", "Data atendimento"],
    "status": ["Classificação", "Status", "Etapa", "Resultado"],
    "utm": ["UTM/Origem", "Origem", "UTM Origem", "UTM", "Canal", "Fonte"],
    "tags": ["Tags", "Tag"],
    "data_conv": ["Data 1ª Conv.", "Data 1a Conv.", "Data primeira conversão", "Data Conversão", "Data conversao"],
}

CANAL_PATTERNS = [
    ("CAMPANHA", ["campanha", "meta", "facebook ads", "fb ads", "ads", "anuncio", "anúncio"]),
    ("INSTAGRAM", ["instagram", "insta", "ig"]),
    ("TIKTOK", ["tiktok", "tik tok"]),
    ("FACEBOOK", ["facebook", "fb"]),
    ("GOOGLE", ["google", "gads", "adwords"]),
    ("INDICAÇÃO", ["indicacao", "indicação", "indicaçao", "indicado"]),
    ("SITE", ["site", "organico", "orgânico", "website"]),
    ("HOSPITAL", ["hospital"]),
    ("EMPRESA", ["empresa", "outbound", "prospeccao", "prospecção"]),
    ("CONTATO DIRETO", ["contato direto", "whatsapp", "direto"]),
]


def norm_text(value: object) -> str:
    text = "" if value is None or (isinstance(value, float) and math.isnan(value)) else str(value)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text).strip().lower()


def find_column(df: pd.DataFrame, key: str, required: bool = True) -> str | None:
    normalized = {norm_text(c): c for c in df.columns}
    for alias in COLUMN_ALIASES[key]:
        if norm_text(alias) in normalized:
            return normalized[norm_text(alias)]
    if required:
        raise KeyError(f"Coluna obrigatória não encontrada para {key}. Colunas disponíveis: {list(df.columns)}")
    return None


def normalize_phone(value: object) -> str:
    digits = re.sub(r"\D+", "", "" if pd.isna(value) else str(value))
    if len(digits) > 11 and digits.startswith("55"):
        digits = digits[2:]
    return digits or "SEM_TELEFONE"


def detect_channel(row: pd.Series, utm_col: str | None, tags_col: str | None) -> str:
    parts = []
    if utm_col:
        parts.append(str(row.get(utm_col, "") or ""))
    if tags_col:
        parts.append(str(row.get(tags_col, "") or ""))
    raw = norm_text(" ".join(parts))
    if not raw:
        return "CONTATO DIRETO"
    for canal, patterns in CANAL_PATTERNS:
        if any(norm_text(p) in raw for p in patterns):
            return canal
    return "NÃO RASTREADO"


def week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


def pct(num: int | float, den: int | float) -> float:
    return round((num / den * 100), 1) if den else 0.0


@dataclass
class WeekMetrics:
    semana: date
    atendimentos: int
    leads_novos: int
    convertidos: int
    conv_pct: float
    canal_top: str
    canal_top_n: int
    canais: dict[str, int]


def analyze(input_path: Path, today: date | None = None) -> dict:
    today = today or datetime.now(TZ).date()
    current_week = week_start(today)
    previous_week = current_week - timedelta(weeks=1)

    df = pd.read_excel(input_path, dtype=str, sheet_name=0)
    df = df.dropna(how="all").copy()

    col_phone = find_column(df, "telefone")
    col_date = find_column(df, "data")
    col_status = find_column(df, "status", required=False)
    col_utm = find_column(df, "utm", required=False)
    col_tags = find_column(df, "tags", required=False)
    col_conv = find_column(df, "data_conv", required=False)

    df["_telefone_norm"] = df[col_phone].apply(normalize_phone)
    df["_data"] = pd.to_datetime(df[col_date], dayfirst=True, errors="coerce")
    df = df[df["_data"].notna()].copy()
    df["_semana"] = df["_data"].dt.date.apply(week_start)
    df["Canal"] = df.apply(lambda row: detect_channel(row, col_utm, col_tags), axis=1)

    df_sorted = df.sort_values("_data")
    primeira_vez = df_sorted.drop_duplicates(subset=["_telefone_norm"], keep="first").copy()
    first_week_by_phone = dict(zip(primeira_vez["_telefone_norm"], primeira_vez["_semana"]))
    df["EhLeadNovo"] = df.apply(lambda r: first_week_by_phone.get(r["_telefone_norm"]) == r["_semana"], axis=1)

    if col_conv:
        df["_data_conv"] = pd.to_datetime(df[col_conv], dayfirst=True, errors="coerce")
    else:
        df["_data_conv"] = pd.NaT

    def converted_count_for_week(semana: date, sub: pd.DataFrame) -> int:
        start = pd.Timestamp(semana)
        end = start + timedelta(weeks=1)
        if col_conv and df["_data_conv"].notna().any():
            mask = (df["_data_conv"] >= start) & (df["_data_conv"] < end)
            return int(df.loc[mask, "_telefone_norm"].nunique())
        if col_status:
            status = sub[col_status].astype(str).map(norm_text)
            return int(sub.loc[status.str.contains("cliente|convertido", na=False), "_telefone_norm"].nunique())
        return 0

    def metrics_for_week(semana: date) -> WeekMetrics:
        sub = df[df["_semana"] == semana]
        leads = sub[sub["EhLeadNovo"]]
        canais = {str(k): int(v) for k, v in leads["Canal"].value_counts().to_dict().items()}
        top = next(iter(canais.items()), ("N/A", 0))
        convertidos = converted_count_for_week(semana, sub)
        return WeekMetrics(
            semana=semana,
            atendimentos=int(len(sub)),
            leads_novos=int(leads["_telefone_norm"].nunique()),
            convertidos=convertidos,
            conv_pct=pct(convertidos, int(leads["_telefone_norm"].nunique())),
            canal_top=top[0],
            canal_top_n=top[1],
            canais=canais,
        )

    atual = metrics_for_week(current_week)
    anterior = metrics_for_week(previous_week)
    total_leads = int(primeira_vez["_telefone_norm"].nunique())
    total_conv = 0
    if col_status:
        total_conv = int(df[col_status].astype(str).map(norm_text).str.contains("cliente|convertido", na=False).sum())

    return {
        "arquivo": str(input_path),
        "gerado_em": datetime.now(TZ).isoformat(timespec="seconds"),
        "colunas": {"telefone": col_phone, "data": col_date, "status": col_status, "utm": col_utm, "tags": col_tags, "data_conv": col_conv},
        "periodo_base": {"inicio": str(df["_data"].min().date()), "fim": str(df["_data"].max().date())},
        "total_atendimentos": int(len(df)),
        "total_leads_unicos": total_leads,
        "taxa_geral_pct": pct(total_conv, total_leads),
        "semana_atual": atual.__dict__,
        "semana_anterior": anterior.__dict__,
        "variacao_leads": atual.leads_novos - anterior.leads_novos,
        "variacao_atendimentos": atual.atendimentos - anterior.atendimentos,
    }


def format_report(result: dict) -> str:
    atual = result["semana_atual"]
    anterior = result["semana_anterior"]
    var = result["variacao_leads"]
    var_pct = pct(var, anterior["leads_novos"]) if anterior["leads_novos"] else 0.0
    sinal = "+" if var >= 0 else ""
    canais = atual["canais"] or {}
    canais_txt = ", ".join(f"{k}: {v}" for k, v in canais.items()) or "sem leads novos"

    alerta = ""
    if anterior["leads_novos"] and var_pct <= -20:
        alerta = f"Queda relevante de leads novos vs. semana anterior ({var_pct:.1f}%)."
    elif atual["canal_top"] in {"NÃO RASTREADO", "CONTATO DIRETO"}:
        alerta = f"Canal #1 ficou como {atual['canal_top']}; vale revisar rastreamento/UTMs."
    elif var > 0:
        alerta = "Semana mostra crescimento de leads novos vs. semana anterior."
    else:
        alerta = "Sem alerta crítico automático; acompanhar conversão e origem dos leads."

    return f"""# Relatório Semanal de Leads — AIOS CRM

Gerado em: {result['gerado_em']}
Arquivo analisado: `{result['arquivo']}`

## Resumo executivo

📊 Semana {atual['semana']} — **{atual['leads_novos']} leads novos**, {atual['convertidos']} convertidos ({atual['conv_pct']}%). Canal #1: {atual['canal_top']} ({atual['canal_top_n']} leads).

Vs. semana anterior: {sinal}{var} leads novos ({var_pct:.1f}%). Atendimentos: {atual['atendimentos']} vs. {anterior['atendimentos']} na semana anterior ({result['variacao_atendimentos']:+d}).

## Base

- Período coberto: {result['periodo_base']['inicio']} a {result['periodo_base']['fim']}
- Total de atendimentos na base: {result['total_atendimentos']}
- Total de leads únicos: {result['total_leads_unicos']}
- Taxa geral: {result['taxa_geral_pct']}%

## Semana atual

- Atendimentos: {atual['atendimentos']}
- Leads novos: {atual['leads_novos']}
- Convertidos: {atual['convertidos']} ({atual['conv_pct']}%)
- Canal #1: {atual['canal_top']} ({atual['canal_top_n']})
- Canais: {canais_txt}

## Semana anterior

- Atendimentos: {anterior['atendimentos']}
- Leads novos: {anterior['leads_novos']}
- Convertidos: {anterior['convertidos']} ({anterior['conv_pct']}%)
- Canal #1: {anterior['canal_top']} ({anterior['canal_top_n']})

## Alerta/destaque

{alerta}

## Colunas usadas

```json
{json.dumps(result['colunas'], ensure_ascii=False, indent=2)}
```
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("arquivo", type=Path)
    parser.add_argument("--today", help="Data de referência YYYY-MM-DD")
    parser.add_argument("--output-md", type=Path)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()

    today = date.fromisoformat(args.today) if args.today else None
    result = analyze(args.arquivo, today=today)
    md = format_report(result)

    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(md, encoding="utf-8")
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    print(md)


if __name__ == "__main__":
    main()
