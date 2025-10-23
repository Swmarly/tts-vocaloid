"""Pitch extraction and note building."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

try:  # pragma: no cover - optional dependency
    import numpy as np
except ImportError:  # pragma: no cover
    np = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import librosa  # type: ignore
except ImportError:  # pragma: no cover
    librosa = None  # type: ignore

from .utils import Note, quantize_beats, sec_to_quarter_length, duration_seconds

HOP_LENGTH = 256
MIN_FRAMES = 3
GAP_TOLERANCE = 0.05  # seconds


@dataclass
class ExtractionSummary:
    """Summary of the note extraction process."""

    notes: List[Note]
    total_duration_sec: float


def extract_notes(
    audio,
    sr: int,
    bpm: float,
    min_note_beats: float,
) -> ExtractionSummary:
    """Extract quantised notes from the audio waveform."""
    if np is None or librosa is None:
        raise ImportError("numpy and librosa are required for note extraction")
    if audio.size == 0:
        raise ValueError("Audio buffer is empty")

    fmin = librosa.note_to_hz("C2")
    fmax = librosa.note_to_hz("C7")
    frame_duration = HOP_LENGTH / sr
    total_duration_sec = float(len(audio) / sr)

    f0, _, _ = librosa.pyin(
        audio,
        fmin=fmin,
        fmax=fmax,
        sr=sr,
        hop_length=HOP_LENGTH,
    )
    times = librosa.times_like(f0, sr=sr, hop_length=HOP_LENGTH)

    rms = librosa.feature.rms(y=audio, hop_length=HOP_LENGTH)[0]
    nonzero_rms = rms[rms > 0]
    if nonzero_rms.size > 0:
        gate = float(np.percentile(nonzero_rms, 25))
    else:
        gate = 0.0

    voiced = (~np.isnan(f0)) & (rms >= gate)
    segments = _find_segments(voiced, frame_duration)

    notes: List[Note] = []
    for start_idx, end_idx in segments:
        if end_idx - start_idx + 1 < MIN_FRAMES:
            continue
        segment_f0 = f0[start_idx : end_idx + 1]
        segment_f0 = segment_f0[~np.isnan(segment_f0)]
        if segment_f0.size == 0:
            continue
        pitch_hz = float(np.median(segment_f0))
        midi_pitch = int(np.round(librosa.hz_to_midi(pitch_hz)))
        start_time = times[start_idx]
        end_time = times[end_idx] + frame_duration
        duration_sec = max(end_time - start_time, frame_duration)
        duration_beats = quantize_beats(
            sec_to_quarter_length(duration_sec, bpm),
            min_note_beats,
        )
        notes.append(Note(start_sec=start_time, duration_beats=duration_beats, midi_pitch=midi_pitch))

    if not notes:
        duration_beats = quantize_beats(
            sec_to_quarter_length(total_duration_sec, bpm),
            min_note_beats,
        )
        notes = [Note(start_sec=0.0, duration_beats=duration_beats, midi_pitch=60)]

    notes = _reflow_start_times(notes, bpm)
    return ExtractionSummary(notes=notes, total_duration_sec=total_duration_sec)


def _find_segments(voiced_mask, frame_duration: float) -> List[tuple[int, int]]:
    segments: List[tuple[int, int]] = []
    start_idx = None
    for idx, is_voiced in enumerate(voiced_mask):
        if is_voiced and start_idx is None:
            start_idx = idx
        elif not is_voiced and start_idx is not None:
            segments.append((start_idx, idx - 1))
            start_idx = None
    if start_idx is not None:
        segments.append((start_idx, len(voiced_mask) - 1))

    if not segments:
        return []

    merged: List[tuple[int, int]] = [segments[0]]
    for start, end in segments[1:]:
        prev_start, prev_end = merged[-1]
        gap = (start - prev_end - 1) * frame_duration
        if gap <= GAP_TOLERANCE:
            merged[-1] = (prev_start, end)
        else:
            merged.append((start, end))
    return merged


def _reflow_start_times(notes: List[Note], bpm: float) -> List[Note]:
    cumulative_beats = 0.0
    updated: List[Note] = []
    for note in notes:
        start_sec = duration_seconds(cumulative_beats, bpm)
        updated.append(Note(start_sec=start_sec, duration_beats=note.duration_beats, midi_pitch=note.midi_pitch))
        cumulative_beats += note.duration_beats
    return updated
