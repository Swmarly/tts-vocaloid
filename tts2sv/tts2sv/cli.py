"""Command line interface for tts2sv."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from . import align, audio, export_midi, export_musicxml, export_ust, notes, text


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a TTS line into SynthV/UTAU formats")
    parser.add_argument("--wav", required=True, help="Path to the input WAV file")
    parser.add_argument("--text", required=True, help="Exact text that was synthesised")
    parser.add_argument("--out-prefix", default="./tts_line", help="Prefix for output files")
    parser.add_argument("--bpm", type=float, default=120.0, help="Tempo for quantisation")
    parser.add_argument("--lang", default="en", help="Language code for syllabification")
    parser.add_argument("--min-note-beats", type=float, default=0.125, help="Minimum note duration in beats")
    parser.add_argument("--timebase", type=int, default=480, help="Ticks per quarter for UST/MIDI")
    parser.add_argument("--strict", action="store_true", help="Fail when syllable/note mismatch is too large")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)

    audio_data, sr = audio.load_audio(args.wav)
    syllables = text.syllabify_text(args.text, lang=args.lang)
    extraction = notes.extract_notes(audio_data, sr=sr, bpm=args.bpm, min_note_beats=args.min_note_beats)
    alignment = align.align_syllables_to_notes(
        extraction.notes,
        syllables,
        bpm=args.bpm,
        min_note_beats=args.min_note_beats,
        strict=args.strict,
    )

    prefix = Path(args.out_prefix)
    export_musicxml.export_musicxml(alignment.notes, bpm=args.bpm, out_path=prefix.with_suffix(".musicxml"))
    export_midi.export_midi(alignment.notes, bpm=args.bpm, out_path=prefix.with_suffix(".mid"))
    export_ust.export_ust(
        alignment.notes,
        bpm=args.bpm,
        timebase=args.timebase,
        out_path=prefix.with_suffix(".ust"),
    )

    print(
        f"Exported {len(alignment.notes)} notes / {len(syllables)} syllables "
        f"(splits: {alignment.splits_applied}, filler notes: {alignment.filler_notes})."
    )


if __name__ == "__main__":
    main()
