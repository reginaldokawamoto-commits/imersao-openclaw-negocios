# STT — Mensagens de Voz no Telegram

## Objetivo

Permitir que o agente receba mensagens de voz no Telegram e use a transcrição como contexto da conversa.

## Status

- **Ativo desde:** 2026-06-02
- **Canal:** Telegram
- **Idioma principal:** Português (`pt`)
- **Modo:** STT local no VPS, sem envio do áudio para API externa

## Componentes instalados

### Sistema

- `ffmpeg` — leitura/conversão de áudio `.ogg`/Opus vindo do Telegram.
- `python3.12-venv` — criação do ambiente Python isolado.

### Workspace

- Ambiente virtual: `/root/cerebro-minhaempresa/.venv-stt/`
- Pacote STT: `faster-whisper`
- Script operacional: `/root/cerebro-minhaempresa/scripts/transcribe_audio.py`

## Configuração OpenClaw

O OpenClaw foi configurado em `/root/.openclaw/openclaw.json` com:

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "language": "pt",
        "timeoutSeconds": 180,
        "maxChars": 20000,
        "echoTranscript": true,
        "echoFormat": "📝 Transcrição: \"{transcript}\"",
        "models": [
          {
            "command": "/root/cerebro-minhaempresa/.venv-stt/bin/python",
            "args": [
              "/root/cerebro-minhaempresa/scripts/transcribe_audio.py",
              "{{MediaPath}}",
              "--language",
              "pt"
            ],
            "timeoutSeconds": 180,
            "maxChars": 20000
          }
        ]
      }
    }
  }
}
```

> Observação: não registrar tokens ou segredos nessa documentação. A configuração real fica fora do repositório.

## Teste realizado

Arquivo de teste recebido via Telegram:

`/root/.openclaw/media/inbound/file_22---6bd7faf6-63d7-49db-b85b-2df975f9275f.ogg`

Transcrição recebida automaticamente:

> “testando aqui veja se você está conseguindo transcrever o meu áudio”

Resultado: **funcionando**.

## Como testar manualmente

```bash
cd /root/cerebro-minhaempresa
. .venv-stt/bin/activate
python scripts/transcribe_audio.py /caminho/para/audio.ogg --language pt
```

## Notas operacionais

- A primeira transcrição pode demorar mais por carregamento/cache do modelo.
- O modelo padrão usado pelo script é `small`, CPU, `int8`.
- Para trocar modelo sem editar o script:

```bash
OPENCLAW_STT_MODEL=medium python scripts/transcribe_audio.py /caminho/para/audio.ogg --language pt
```

- Se a transcrição parar de funcionar, checar:
  1. `ffmpeg` instalado e disponível.
  2. `.venv-stt` existente.
  3. `faster-whisper` importando corretamente.
  4. `tools.media.audio.enabled` ativo no `openclaw.json`.
  5. Gateway recarregado/reiniciado após mudança de config.
