#!/usr/bin/env python3
"""Local Portuguese STT for OpenClaw media audio CLI."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from faster_whisper import WhisperModel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_path")
    parser.add_argument("--model", default=os.environ.get("OPENCLAW_STT_MODEL", "small"))
    parser.add_argument("--language", default=os.environ.get("OPENCLAW_STT_LANGUAGE", "pt"))
    args = parser.parse_args()

    audio = Path(args.audio_path)
    if not audio.exists():
        print(f"audio file not found: {audio}", file=sys.stderr)
        return 2

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(
        str(audio),
        language=args.language or None,
        vad_filter=True,
        beam_size=5,
    )
    text = " ".join(seg.text.strip() for seg in segments if seg.text.strip()).strip()
    if text:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
