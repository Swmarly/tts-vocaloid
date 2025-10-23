"""UST exporter."""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .utils import Note


HEADER = "[#SETTING]"
TRACK_END = "[#TRACKEND]"


def export_ust(
    notes: Sequence[Note],
    bpm: float,
    timebase: int,
    out_path: str | Path,
    project_name: str = "tts2sv",
) -> Path:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [HEADER]
    lines.extend(
        [
            f"ProjectName={project_name}",
            "VoiceDir=",
            f"OutFile={path.with_suffix('.wav').name}",
            "CacheDir=cache",
            "Mode2=True",
            f"Tempo={bpm}",
            "",  # spacer
        ]
    )

    for idx, note in enumerate(notes):
        index = f"[# {idx:04d}]".replace(" ", "")
        lyric = _normalise_lyric(note.lyric)
        length = max(int(round(note.duration_beats * timebase)), 1)
        lines.extend(
            [
                index,
                f"Lyric={lyric}",
                f"NoteNum={note.midi_pitch}",
                f"Length={length}",
                "PreUtterance=",
                "VoiceOverlap=",
                "Intensity=100",
                "Modulation=0",
                "PBType=5",
                "",
            ]
        )

    lines.append(TRACK_END)

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _normalise_lyric(lyric: str | None) -> str:
    if lyric is None or lyric.strip() == "":
        return "-"
    lyric = lyric.strip()
    return "-" if lyric == "—" else lyric
