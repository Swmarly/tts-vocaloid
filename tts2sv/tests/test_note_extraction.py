import numpy as np

from tts2sv import notes


def test_extract_notes_from_sine_wave():
    sr = 22050
    duration = 1.0
    silence = np.zeros(int(0.1 * sr))
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    note_a = 0.2 * np.sin(2 * np.pi * 440 * t)
    note_e = 0.2 * np.sin(2 * np.pi * 660 * t)
    audio = np.concatenate([note_a, silence, note_e]).astype(np.float32)

    summary = notes.extract_notes(audio, sr=sr, bpm=120.0, min_note_beats=0.25)
    midi_pitches = [n.midi_pitch for n in summary.notes]

    assert len(summary.notes) >= 2
    assert midi_pitches[0] in (69, 70)  # A4
    assert midi_pitches[1] in (76, 77)  # E5 approx
    assert summary.notes[0].duration_beats >= 1.75
