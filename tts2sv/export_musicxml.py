"""MusicXML exporter."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from .utils import Note

_MUSIC21_IMPORT_ERROR = "music21 is required for MusicXML export"
_MUSIC21_MODULES: tuple[Any, ...] | None = None


def _load_music21() -> tuple[Any, ...]:
    """Lazily import music21 so optional dependency is only needed on demand."""

    global _MUSIC21_MODULES
    if _MUSIC21_MODULES is None:
        try:  # pragma: no cover - exercised in integration
            from music21 import instrument, meter, stream, tempo, note
        except ImportError as exc:  # pragma: no cover
            raise ImportError(_MUSIC21_IMPORT_ERROR) from exc
        _MUSIC21_MODULES = (instrument, meter, stream, tempo, note)
    return _MUSIC21_MODULES


def build_stream(notes: Sequence[Note], bpm: float) -> Any:
    instrument, meter, stream, tempo, note = _load_music21()

    part = stream.Part()
    part.insert(0, instrument.Voice())
    part.insert(0, tempo.MetronomeMark(number=bpm))
    part.insert(0, meter.TimeSignature("4/4"))

    for n in notes:
        m21_note = note.Note()
        m21_note.pitch.midi = n.midi_pitch
        m21_note.quarterLength = n.duration_beats
        if n.lyric is not None:
            m21_note.addLyric(n.lyric)
        part.append(m21_note)

    score = stream.Score()
    score.append(part)
    return score


def export_musicxml(notes: Sequence[Note], bpm: float, out_path: str | Path) -> Path:
    score = build_stream(notes, bpm)
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    score.write("musicxml", fp=str(path))
    return path
