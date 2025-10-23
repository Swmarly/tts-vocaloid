"""Utility helpers for time and beat conversions."""
from __future__ import annotations

from dataclasses import dataclass


QUANTIZATION_STEP = 0.25  # beats (1/16 note at 4/4)


def sec_to_quarter_length(seconds: float, bpm: float) -> float:
    """Convert seconds to quarterLength (beats) based on tempo."""
    if bpm <= 0:
        raise ValueError("BPM must be positive")
    return seconds * (bpm / 60.0)


def duration_seconds(duration_beats: float, bpm: float) -> float:
    """Convert beat duration back into seconds."""
    if bpm <= 0:
        raise ValueError("BPM must be positive")
    return duration_beats * (60.0 / bpm)


def quantize_beats(value: float, minimum: float) -> float:
    """Quantize a beat value to the configured grid while respecting the minimum."""
    if value <= 0:
        return minimum
    quantized = round(value / QUANTIZATION_STEP) * QUANTIZATION_STEP
    if quantized < minimum:
        quantized = minimum
    return quantized


@dataclass
class Note:
    """Simple representation of a musical note."""

    start_sec: float
    duration_beats: float
    midi_pitch: int
    lyric: str | None = None
