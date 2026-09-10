process.env.NODE_ENV = 'production';
process.env.PORT = '3000';

const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

let mainWindow;

function startServer() {
  try {
    // Configurer le dossier des données utilisateur accessible en écriture
    try {
      process.env.MATRICAL_USER_DATA = app.getPath('userData');
    } catch (e) {
      console.warn('Impossible de récupérer userData depuis Electron:', e);
    }

    const serverPath = path.join(__dirname, 'dist', 'server.cjs');
    if (fs.existsSync(serverPath)) {
      console.log('Démarrage du serveur Express depuis:', serverPath);
      require(serverPath);
    } else {
      const errMsg = 'Fichier serveur introuvable à: ' + serverPath;
      console.error(errMsg);
      dialog.showErrorBox("Erreur Serveur", errMsg);
    }
  } catch (err) {
    console.error('Erreur démarrage serveur Express:', err);
    dialog.showErrorBox("Erreur Démarrage Serveur", err.stack || err.message);
  }
}

function createWindow() {
  // 1. Démarrer le serveur Express
  startServer();

  // 2. Créer la fenêtre Electron
  let iconPath = path.join(__dirname, 'icon.ico');
  if (!fs.existsSync(iconPath)) iconPath = path.join(__dirname, 'dist', 'icon.png');
  if (!fs.existsSync(iconPath)) iconPath = path.join(__dirname, 'icon.png');
  if (!fs.existsSync(iconPath)) iconPath = path.join(__dirname, 'public', 'icon.png');

  mainWindow = new BrowserWindow({
    width: 1280,
    height: 850,
    title: "MATRICAL",
    icon: fs.existsSync(iconPath) ? iconPath : undefined,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  // 3. Charger l'application localement
  const loadApp = (attempts = 0) => {
    mainWindow.loadURL('http://localhost:3000').catch((err) => {
      console.log(`Tentative de connexion ${attempts + 1}/15...`);
      if (attempts < 15) {
        setTimeout(() => loadApp(attempts + 1), 400);
      } else {
        dialog.showErrorBox(
          "Erreur de connexion",
          "Impossible de se connecter au serveur local (http://localhost:3000).\n\nDétails: " + (err.message || err)
        );
      }
    });
  };

  setTimeout(loadApp, 500);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

