const form = document.getElementById('conversion-form');
const runButton = document.getElementById('run-button');
const clearLogButton = document.getElementById('clear-log');
const logOutput = document.getElementById('log-output');
const browseWavButton = document.getElementById('browse-wav');
const browseOutputButton = document.getElementById('browse-output');
const browsePythonButton = document.getElementById('browse-python');

const appendLog = (message, type = 'log') => {
  const formatted = type === 'error' ? `⚠️ ${message}` : message;
  logOutput.textContent += formatted;
  logOutput.scrollTop = logOutput.scrollHeight;
};

const resetLog = () => {
  logOutput.textContent = '';
};

window.tts2sv.subscribe({
  onLog: (message) => appendLog(message),
  onError: (message) => appendLog(message, 'error'),
  onComplete: ({ code }) => {
    appendLog(`\nProcess finished with exit code ${code}.\n`);
    runButton.disabled = false;
  },
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  runButton.disabled = true;
  resetLog();

  const wavPath = document.getElementById('wav-path').value.trim();
  const text = document.getElementById('text-input').value.trim();
  const outputPrefix = document.getElementById('output-prefix').value.trim();
  const bpm = parseFloat(document.getElementById('bpm').value) || 120;
  const lang = document.getElementById('lang').value.trim() || 'en';
  const minNoteBeats = parseFloat(document.getElementById('min-note-beats').value) || 0.125;
  const timebase = parseInt(document.getElementById('timebase').value, 10) || 480;
  const strict = document.getElementById('strict').checked;
  const pythonCommand = document.getElementById('python-path').value.trim();

  if (!wavPath || !text || !outputPrefix) {
    appendLog('Please provide WAV, text, and output prefix before running.\n', 'error');
    runButton.disabled = false;
    return;
  }

  try {
    await window.tts2sv.run({
      wavPath,
      text,
      outputPrefix,
      bpm,
      lang,
      minNoteBeats,
      timebase,
      strict,
      pythonCommand,
    });
  } catch (err) {
    appendLog(`Run failed: ${err.message}\n`, 'error');
    runButton.disabled = false;
  }
});

clearLogButton.addEventListener('click', () => {
  resetLog();
});

browseWavButton.addEventListener('click', async () => {
  const path = await window.tts2sv.chooseWav();
  if (path) {
    document.getElementById('wav-path').value = path;
  }
});

browseOutputButton.addEventListener('click', async () => {
  const path = await window.tts2sv.chooseOutputPrefix();
  if (path) {
    document.getElementById('output-prefix').value = path;
  }
});

browsePythonButton.addEventListener('click', async () => {
  const path = await window.tts2sv.choosePython();
  if (path) {
    document.getElementById('python-path').value = path;
  }
});
