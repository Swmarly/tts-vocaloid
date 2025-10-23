# tts2sv

`tts2sv` turns a spoken TTS line into a simple melody that can be imported into Synthesizer V, UTAU, or OpenUtau.

The tool extracts pitch from an input WAV, splits the spoken text into syllables, lines the syllables up with the detected notes, and exports MusicXML, MIDI, and UST.

## Features

- Automatic f0 extraction using `librosa.pyin`
- Rule-based or Pyphen-powered syllabification
- Automatic alignment between syllables and detected notes with optional strictness checks
- Export to MusicXML, MIDI, and UST (UTAU) with shared timing

Limitations: speech contours rarely map cleanly to musical phrasing; manual editing is still recommended.

## Quick start

### Automated setup (recommended)

The repository now ships with a convenience script that prepares a Python
virtual environment and installs the optional Electron GUI in one go:

```bash
./install.sh
```

By default the script creates a `.venv` folder in the project root. Set the
`PYTHON` environment variable or pass an alternate directory if you prefer a
different interpreter or virtual environment location:

```bash
PYTHON=python3.11 ./install.sh my-env
```

After the script finishes you can activate the environment with:

```bash
source my-env/bin/activate  # or .venv/bin/activate if you kept the default
```

If `npm` is detected the script also runs `npm install` inside
`electron-app/`. Without Node.js you can still use the CLI—install Node later
and run `npm install` in that directory to enable the GUI.

### Manual installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Usage

First, generate the bundled sine-wave example (skipping this step if you already
have your own TTS line):

```bash
python examples/make_hello_wav.py
```

Then run the CLI:

```bash
tts2sv --wav examples/hello.wav --text "Hello, world!" --out-prefix out/demo --bpm 120
```

Outputs are written to `out/demo.musicxml`, `out/demo.mid`, and `out/demo.ust`.

## Electron GUI

Prefer a graphical interface? After running `./install.sh` (or manually
executing `npm install` inside `electron-app/`) you can start the desktop app:

```bash
cd electron-app
npm start
```

The GUI exposes all of the CLI switches, streams the command output to a log
panel, and lets you browse for WAV files, choose an output prefix, and specify
which Python interpreter to use. The app ultimately calls the same
`tts2sv` command under the hood, so it retains the full feature set.

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
