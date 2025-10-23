"""Align syllables to detected notes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

from .utils import Note, duration_seconds


@dataclass
class AlignmentResult:
    notes: List[Note]
    splits_applied: int = 0
    filler_notes: int = 0


class AlignmentError(ValueError):
    """Raised when alignment cannot be satisfied."""


THRESHOLD = 0.3


def align_syllables_to_notes(
    notes: Sequence[Note],
    syllables: Sequence[str],
    bpm: float,
    min_note_beats: float,
    strict: bool = False,
) -> AlignmentResult:
    if not notes:
        raise AlignmentError("No notes available for alignment")
    if not syllables:
        raise AlignmentError("No syllables extracted from text")

    notes_list = [Note(start_sec=note.start_sec, duration_beats=note.duration_beats, midi_pitch=note.midi_pitch) for note in notes]

    note_count = len(notes_list)
    syll_count = len(syllables)

    if syll_count > note_count:
        mismatch = (syll_count - note_count) / max(note_count, 1)
        if strict and mismatch > THRESHOLD:
            raise AlignmentError(
                "Syllable count exceeds note count by more than 30% in strict mode",
            )
        splits_applied = _expand_notes(notes_list, syll_count, min_note_beats)
    else:
        splits_applied = 0

    if len(notes_list) < syll_count:
        raise AlignmentError("Unable to split notes to accommodate all syllables")

    filler_notes = 0
    if len(notes_list) > syll_count:
        filler_notes = len(notes_list) - syll_count
        syllables = list(syllables) + ["—"] * filler_notes

    aligned_notes = _assign_lyrics(notes_list, syllables, bpm)
    return AlignmentResult(notes=aligned_notes, splits_applied=splits_applied, filler_notes=filler_notes)


def _expand_notes(notes: List[Note], target_count: int, min_note_beats: float) -> int:
    splits = 0
    while len(notes) < target_count:
        idx = max(range(len(notes)), key=lambda i: notes[i].duration_beats)
        note = notes[idx]
        half_duration = note.duration_beats / 2.0
        if half_duration < min_note_beats:
            break
        replacement = [
            Note(start_sec=0.0, duration_beats=half_duration, midi_pitch=note.midi_pitch),
            Note(start_sec=0.0, duration_beats=half_duration, midi_pitch=note.midi_pitch),
        ]
        notes[idx : idx + 1] = replacement
        splits += 1
    return splits


def _assign_lyrics(notes: List[Note], syllables: Sequence[str], bpm: float) -> List[Note]:
    cumulative_beats = 0.0
    aligned: List[Note] = []
    for note, lyric in zip(notes, syllables):
        start_sec = duration_seconds(cumulative_beats, bpm)
        aligned.append(
            Note(
                start_sec=start_sec,
                duration_beats=note.duration_beats,
                midi_pitch=note.midi_pitch,
                lyric=lyric,
            )
        )
        cumulative_beats += note.duration_beats
    return aligned
