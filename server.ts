import express from "express";
import path from "path";
import fs from "fs";
import { execFile } from "child_process";

const currentDir = typeof __dirname !== "undefined" ? __dirname : process.cwd();

async function startServer() {
  const app = express();
  const PORT = Number(process.env.PORT) || 3000;

  app.use(express.json());

  // Helper function to call Python cli.py
  const callPythonCore = (payload: any): Promise<any> => {
    return new Promise((resolve, reject) => {
      let cliPath = path.join(process.cwd(), "cli.py");
      
      const candidatePaths = [
        path.join(process.cwd(), "cli.py"),
        path.join(currentDir, "cli.py"),
        path.join(currentDir, "..", "cli.py"),
        path.join(currentDir, "..", "..", "cli.py"),
        path.join(process.cwd(), "resources", "app", "cli.py"),
        path.join(process.cwd(), "release", "win-unpacked", "cli.py")
      ];

      for (const p of candidatePaths) {
        if (fs.existsSync(p)) {
          cliPath = p;
          break;
        }
      }

      if (!fs.existsSync(cliPath)) {
        return reject(new Error(`Fichier Moteur Python (cli.py) introuvable à: ${cliPath}`));
      }

      const pythonCmd = process.platform === "win32" ? "python" : "python3";
      
      const defaultUserData = process.env.MATRICAL_USER_DATA || 
        (process.platform === "win32" 
          ? path.join(process.env.APPDATA || path.join(process.env.USERPROFILE || "", "AppData", "Roaming"), "MATRICAL")
          : path.join(process.env.HOME || "", ".matrical"));

      execFile(
        pythonCmd,
        [cliPath, JSON.stringify(payload)],
        {
          env: {
            ...process.env,
            MATRICAL_USER_DATA: defaultUserData,
            PYTHONIOENCODING: "utf-8"
          },
          encoding: "utf8"
        },
        (error, stdout, stderr) => {
          if (error) {
            console.error("Python exec error:", stderr || error.message);
            return reject(error);
          }
          try {
            const trimmed = (stdout || "").trim();
            try {
              const jsonRes = JSON.parse(trimmed);
              return resolve(jsonRes);
            } catch {
              // Extraction résiliente de l'objet JSON si du texte a été émis avant ou après
              const firstBrace = trimmed.indexOf('{');
              const lastBrace = trimmed.lastIndexOf('}');
              if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
                const sub = trimmed.substring(firstBrace, lastBrace + 1);
                const jsonRes = JSON.parse(sub);
                return resolve(jsonRes);
              }
              throw new Error(`Réponse Python invalide: ${stdout}`);
            }
          } catch (e: any) {
            reject(new Error(e.message || `Réponse Python invalide: ${stdout}`));
          }
        }
      );
    });
  };

  // API Endpoints
  app.post("/api/matrix/calculate", async (req, res) => {
    try {
      const pyResult = await callPythonCore(req.body);
      res.json(pyResult);
    } catch (err: any) {
      res.status(500).json({ success: false, error: err.message || "Erreur de calcul serveur Python" });
    }
  });

  app.get("/api/matrix/history", async (req, res) => {
    try {
      const pyResult = await callPythonCore({ action: "get_history" });
      res.json(pyResult);
    } catch (err: any) {
      res.status(500).json({ success: false, error: err.message });
    }
  });

  app.post("/api/matrix/clear-history", async (req, res) => {
    try {
      const pyResult = await callPythonCore({ action: "clear_history" });
      res.json(pyResult);
    } catch (err: any) {
      res.status(500).json({ success: false, error: err.message });
    }
  });

  app.post("/api/matrix/delete-history-item", async (req, res) => {
    try {
      const pyResult = await callPythonCore({ action: "delete_history_item", id: req.body.id });
      res.json(pyResult);
    } catch (err: any) {
      res.status(500).json({ success: false, error: err.message });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const { createServer: createViteServer } = await import("vite");
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    let distPath = path.join(process.cwd(), "dist");
    if (fs.existsSync(path.join(currentDir, "index.html"))) {
      distPath = currentDir;
    }
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server MATRICAL running on http://localhost:${PORT}`);
  });
}

startServer();
