const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

const createWindow = () => {
  const win = new BrowserWindow({
    width: 900,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  win.loadFile(path.join(__dirname, 'index.html'));
};

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

const buildArgs = (options) => {
  const args = ['-m', 'tts2sv.cli'];
  args.push('--wav', options.wavPath);
  args.push('--text', options.text);
  args.push('--out-prefix', options.outputPrefix);
  args.push('--bpm', String(options.bpm));
  args.push('--lang', options.lang);
  args.push('--min-note-beats', String(options.minNoteBeats));
  args.push('--timebase', String(options.timebase));
  if (options.strict) {
    args.push('--strict');
  }
  return args;
};

ipcMain.handle('run-tts2sv', async (event, options) => {
  const pythonCmd = options.pythonCommand || process.env.TTS2SV_PYTHON || 'python';
  const args = buildArgs(options);

  event.sender.send('tts2sv-log', `$ ${pythonCmd} ${args.join(' ')}\n`);

  return new Promise((resolve) => {
    try {
      const child = spawn(pythonCmd, args, {
        cwd: options.workingDirectory || process.cwd(),
        env: process.env,
      });

      child.stdout.on('data', (data) => {
        event.sender.send('tts2sv-log', data.toString());
      });

      child.stderr.on('data', (data) => {
        event.sender.send('tts2sv-error', data.toString());
      });

      child.on('close', (code) => {
        event.sender.send('tts2sv-complete', { code });
        resolve({ code });
      });

      child.on('error', (err) => {
        const message = `Failed to start Python process: ${err.message}\n`;
        event.sender.send('tts2sv-error', message);
        event.sender.send('tts2sv-complete', { code: -1 });
        resolve({ code: -1, error: message });
      });
    } catch (err) {
      const message = `Unexpected error: ${err.message}\n`;
      event.sender.send('tts2sv-error', message);
      event.sender.send('tts2sv-complete', { code: -1 });
      resolve({ code: -1, error: message });
    }
  });
});

ipcMain.handle('choose-wav', async () => {
  const result = await dialog.showOpenDialog({
    properties: ['openFile'],
    filters: [{ name: 'WAV Files', extensions: ['wav'] }],
  });
  if (result.canceled || result.filePaths.length === 0) {
    return null;
  }
  return result.filePaths[0];
});

ipcMain.handle('choose-output-prefix', async () => {
  const result = await dialog.showSaveDialog({
    title: 'Select output prefix (files will share this name)',
    defaultPath: path.join(process.cwd(), 'out', 'tts_line'),
  });
  if (result.canceled || !result.filePath) {
    return null;
  }
  return result.filePath;
});

ipcMain.handle('choose-python', async () => {
  const result = await dialog.showOpenDialog({
    title: 'Select Python executable',
    properties: ['openFile'],
  });
  if (result.canceled || result.filePaths.length === 0) {
    return null;
  }
  return result.filePaths[0];
});
