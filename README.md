# tts2sv

`tts2sv` turns a spoken TTS line into a simple melody that can be imported into Synthesizer V, UTAU, or OpenUtau.

The tool extracts pitch from an input WAV, splits the spoken text into syllables, lines the syllables up with the detected notes, and exports MusicXML, MIDI, and UST.

## Features

- Automatic f0 extraction using `librosa.pyin`
- Rule-based or Pyphen-powered syllabification
- Automatic alignment between syllables and detected notes with optional strictness checks
- Export to MusicXML, MIDI, and UST (UTAU) with shared timing

Limitations: speech contours rarely map cleanly to musical phrasing; manual editing is still recommended.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Usage

```bash
tts2sv --wav examples/hello.wav --text "Hello, world!" --out-prefix out/demo --bpm 120
```

Outputs are written to `out/demo.musicxml`, `out/demo.mid`, and `out/demo.ust`.

## Workflow

1. Run the CLI on a clean TTS line (avoid reverb).
2. Import the MusicXML or MIDI into Synthesizer V / OpenUtau, or open the UST directly in UTAU/OpenUtau.
3. Adjust timing, tempo, or transposition inside your DAW or vocal synth editor as needed.

Tips:

- Clear, steady TTS with minimal background noise improves note segmentation.
- Adjust `--bpm` and `--min-note-beats` to match the desired rhythmic feel.
- The tool currently keeps chromatic pitches; transpose or quantize in your DAW for other scales.

## License

MIT
