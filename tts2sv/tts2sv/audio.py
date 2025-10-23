"""Audio loading and normalisation utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

try:  # pragma: no cover - optional dependency at import time
    import numpy as np
except ImportError:  # pragma: no cover - handled at runtime
    np = None  # type: ignore

try:  # pragma: no cover
    import soundfile as sf
except ImportError:  # pragma: no cover
    sf = None  # type: ignore


MAX_PEAK = 0.99
TARGET_RMS = 0.1
EPS = 1e-9


def load_audio(path: str | Path) -> Tuple["np.ndarray", int]:
    """Load a WAV file, downmix to mono, and normalise amplitude."""
    if np is None or sf is None:
        raise ImportError("numpy and soundfile are required to load audio")

    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    audio, sr = sf.read(str(file_path), always_2d=False)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    audio = audio.astype(np.float32)
    peak = float(np.max(np.abs(audio)) + EPS)
    if peak > 0:
        audio = audio / peak * MAX_PEAK

    rms = float(np.sqrt(np.mean(np.square(audio)) + EPS))
    if rms > 0:
        gain = TARGET_RMS / rms
        audio = np.clip(audio * gain, -1.0, 1.0)

    return audio, sr
