from tts2sv import export_ust
from tts2sv.utils import Note


def test_export_ust(tmp_path):
    notes = [
        Note(start_sec=0.0, duration_beats=1.5, midi_pitch=60, lyric="la"),
        Note(start_sec=0.0, duration_beats=0.5, midi_pitch=62, lyric="—"),
    ]
    out = tmp_path / "demo.ust"
    export_ust.export_ust(notes, bpm=120.0, timebase=480, out_path=out)

    text = out.read_text(encoding="utf-8")
    assert "[#0000]" in text
    assert "Lyric=la" in text
    assert "NoteNum=60" in text
    assert "Length=720" in text  # 1.5 beats * 480
    assert "Lyric=-" in text  # filler lyric normalised
    assert text.strip().endswith("[#TRACKEND]")
