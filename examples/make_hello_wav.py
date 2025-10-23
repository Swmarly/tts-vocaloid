"""Utility to generate the example hello.wav file used in documentation."""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import soundfile as sf


def generate_sine(
    duration: float = 1.0,
    sample_rate: int = 22050,
    frequency: float = 220.0,
    amplitude: float = 0.2,
) -> np.ndarray:
    """Generate a mono sine wave with a short fade in/out to avoid clicks."""
    t = np.linspace(0.0, duration, int(sample_rate * duration), endpoint=False)
    waveform = amplitude * np.sin(2.0 * math.pi * frequency * t)

    # Apply a short fade to avoid a harsh start/end.
    fade_samples = int(sample_rate * 0.01)
    if fade_samples > 0:
        fade = np.linspace(0.0, 1.0, fade_samples)
        waveform[:fade_samples] *= fade
        waveform[-fade_samples:] *= fade[::-1]

    return waveform.astype(np.float32)


def main() -> None:
    output = Path(__file__).with_name("hello.wav")
    waveform = generate_sine()
    sf.write(output, waveform, 22050)
    print(f"Wrote example WAV to {output}")


if __name__ == "__main__":
    main()
