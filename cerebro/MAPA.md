# Cérebro — Mapa

## Estrutura

```
cerebro/
├── MAPA.md                         ← Este arquivo
├── README.md                       ← O que é o Cérebro e como funciona
│
├── empresa/                        ← Contexto global da empresa
│   ├── MAPA.md
│   ├── contexto/                   ← Quem somos, equipe, métricas, decisões, lições
│   ├── skills/                     ← Skills cross-área
│   ├── rotinas/                    ← Rotinas automáticas
│   ├── ideias/                     ← Ideias capturadas antes de virarem projetos
│   └── projetos/                   ← Projetos e pendências
│
├── areas/                          ← Áreas da empresa
│   ├── vendas/                     ← Pipeline, leads, follow-up
│   │   ├── MAPA.md
│   │   ├── contexto/
│   │   ├── skills/
│   │   ├── rotinas/
│   │   ├── projetos/
│   │   └── bot/
│   ├── marketing/                  ← Campanhas, criativos, tráfego pago
│   │   ├── MAPA.md
│   │   ├── contexto/
│   │   ├── skills/
│   │   ├── rotinas/
│   │   ├── projetos/
│   │   └── sub-areas/trafego-pago/
│   ├── atendimento/                ← Suporte, FAQ, bot
│   │   ├── MAPA.md
│   │   ├── contexto/
│   │   ├── skills/
│   │   ├── rotinas/
│   │   ├── projetos/
│   │   └── bot/
│   └── operacoes/                  ← Rotinas internas, sync, heartbeat
│       ├── MAPA.md
│       ├── contexto/
│       ├── skills/
│       ├── rotinas/
│       └── projetos/
│
├── agentes/                        ← Configuração de cada agente
│   ├── COMO-CONECTAR.md
│   ├── assistente/
│   ├── marketing/
│   └── bot-suporte/
│
└── seguranca/                      ← Permissões e políticas de acesso
    └── permissoes.md
```

## O que tem em cada lugar

| Pasta | O que o agente encontra |
|-------|------------------------|
| `empresa/` | Contexto global — missão, produto, equipe, métricas, decisões, lições, ideias e projetos |
| `areas/` | Cada área da empresa com a mesma estrutura: contexto, skills, rotinas, projetos |
| `agentes/` | Configuração de cada agente — SOUL, AGENTS, TOOLS, permissões |
| `seguranca/` | Quem pode acessar o quê, políticas de acesso |

## Padrão de navegação

Toda pasta (empresa, área, sub-área) segue a mesma estrutura:

```
qualquer-pasta/
├── MAPA.md         ← Onde estou, o que tem aqui
├── contexto/       ← O que preciso saber
├── skills/         ← O que posso fazer
├── rotinas/        ← O que roda automaticamente
└── projetos/       ← O que está em andamento
```

O agente aprende o padrão uma vez e navega qualquer nível.
