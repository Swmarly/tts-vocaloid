"""MIDI exporter using music21."""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .export_musicxml import build_stream
from .utils import Note


def export_midi(notes: Sequence[Note], bpm: float, out_path: str | Path) -> Path:
    score = build_stream(notes, bpm)
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    score.write("midi", fp=str(path))
    return path
