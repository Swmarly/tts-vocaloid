const { contextBridge, ipcRenderer } = require('electron');

const removeExistingListeners = () => {
  ipcRenderer.removeAllListeners('tts2sv-log');
  ipcRenderer.removeAllListeners('tts2sv-error');
  ipcRenderer.removeAllListeners('tts2sv-complete');
};

contextBridge.exposeInMainWorld('tts2sv', {
  chooseWav: () => ipcRenderer.invoke('choose-wav'),
  chooseOutputPrefix: () => ipcRenderer.invoke('choose-output-prefix'),
  choosePython: () => ipcRenderer.invoke('choose-python'),
  run: async (options) => ipcRenderer.invoke('run-tts2sv', options),
  subscribe: (handlers) => {
    removeExistingListeners();
    if (handlers.onLog) {
      ipcRenderer.on('tts2sv-log', (_event, message) => handlers.onLog(message));
    }
    if (handlers.onError) {
      ipcRenderer.on('tts2sv-error', (_event, message) => handlers.onError(message));
    }
    if (handlers.onComplete) {
      ipcRenderer.on('tts2sv-complete', (_event, payload) => handlers.onComplete(payload));
    }
  },
});
