from tts2sv import align
from tts2sv.utils import Note


def test_alignment_with_extra_notes():
    notes = [
        Note(start_sec=0.0, duration_beats=1.0, midi_pitch=60),
        Note(start_sec=0.0, duration_beats=1.0, midi_pitch=62),
        Note(start_sec=0.0, duration_beats=1.0, midi_pitch=64),
    ]
    syllables = ["la", "la"]
    result = align.align_syllables_to_notes(notes, syllables, bpm=120.0, min_note_beats=0.25)
    lyrics = [n.lyric for n in result.notes]
    assert lyrics == ["la", "la", "—"]
    assert result.filler_notes == 1


def test_alignment_splits_notes():
    notes = [Note(start_sec=0.0, duration_beats=2.0, midi_pitch=60)]
    syllables = ["la", "la", "la"]
    result = align.align_syllables_to_notes(notes, syllables, bpm=120.0, min_note_beats=0.25)
    assert len(result.notes) == 3
    assert result.splits_applied >= 2
    assert [n.lyric for n in result.notes] == syllables
