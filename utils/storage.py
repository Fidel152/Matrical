"""
Module de gestion du stockage de l'historique des calculs.
Enregistre et lit les calculs dans un fichier JSON persistant et accessible en écriture.
Gère correctement les environnements packagés (.exe sous Program Files) et évite
toute pollution de stdout pour ne pas casser la communication IPC JSON.
"""

import json
import os
import sys
import tempfile
from datetime import datetime
from typing import List, Dict, Any

def get_writable_data_dir() -> str:
    """
    Détermine un dossier accessible en écriture pour stocker l'historique :
    1. Variable d'environnement MATRICAL_USER_DATA ou MATRICAL_DATA_DIR (définie par Electron / Express)
    2. %APPDATA%/MATRICAL/data (sur Windows)
    3. ~/Library/Application Support/MATRICAL/data (sur macOS)
    4. ~/.local/share/matrical/data ou ~/.matrical/data (sur Linux)
    5. Dossier local 'data' (si accessible en écriture et non dans Program Files)
    6. Répertoire temporaire système en dernier recours.
    """
    candidates = []

    # 1. Variable d'environnement injectée par Electron ou Express
    env_user_data = os.environ.get("MATRICAL_USER_DATA") or os.environ.get("MATRICAL_DATA_DIR")
    if env_user_data:
        candidates.append(os.path.join(env_user_data, "data") if not env_user_data.endswith("data") else env_user_data)

    # 2. Répertoires standards système utilisateur
    if sys.platform == "win32" or "APPDATA" in os.environ:
        appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
        candidates.append(os.path.join(appdata, "MATRICAL", "data"))
        candidates.append(os.path.join(os.path.expanduser("~"), "AppData", "Local", "MATRICAL", "data"))
    elif sys.platform == "darwin":
        candidates.append(os.path.join(os.path.expanduser("~"), "Library", "Application Support", "MATRICAL", "data"))
    else:
        xdg = os.environ.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share")
        candidates.append(os.path.join(xdg, "matrical", "data"))
        candidates.append(os.path.join(os.path.expanduser("~"), ".matrical", "data"))

    # 3. Dossier local du projet (uniquement si hors Program Files)
    local_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    is_protected = any(p in local_dir.lower() for p in ["program files", "system32", "/usr/", "/opt/"])
    if not is_protected:
        candidates.append(local_dir)

    # 4. Dossier temporaire système
    candidates.append(os.path.join(tempfile.gettempdir(), "matrical_data"))

    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            test_file = os.path.join(candidate, ".write_test")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("ok")
            if os.path.exists(test_file):
                os.remove(test_file)
            return candidate
        except Exception:
            continue

    # Repli ultime
    return tempfile.gettempdir()

def get_history_file() -> str:
    """Renvoie le chemin complet vers le fichier history.json."""
    return os.path.join(get_writable_data_dir(), "history.json")

def ensure_data_dir():
    """S'assure que le dossier de données existe."""
    data_dir = get_writable_data_dir()
    try:
        os.makedirs(data_dir, exist_ok=True)
    except Exception as e:
        sys.stderr.write(f"Impossible de créer le dossier de données ({data_dir}): {e}\n")

def load_history() -> List[Dict[str, Any]]:
    """Lit l'historique depuis le fichier JSON."""
    history_path = get_history_file()
    if not os.path.exists(history_path):
        return []
    try:
        with open(history_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        sys.stderr.write(f"Erreur lors de la lecture de l'historique ({history_path}) : {e}\n")
        return []

def save_history_item(
    operation: str,
    matrices: Dict[str, Any],
    result: Any,
    steps: List[Any] = None,
    action_type: str = "",
    formula: str = "",
    dimensions: str = "",
    result_summary: str = "",
    solution_type: str = None
) -> Dict[str, Any]:
    """
    Ajoute un nouvel enregistrement détaillé à l'historique JSON local.
    Ne lève jamais d'exception fatale pour ne pas interrompre le calcul de l'utilisateur.
    """
    new_id = int(datetime.now().timestamp() * 1000)
    
    item = {
        "id": new_id,
        "date": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "operation": operation,
        "action_type": action_type,
        "formula": formula,
        "dimensions": dimensions,
        "result_summary": result_summary,
        "matrix_a": matrices.get("A"),
        "matrix_b": matrices.get("B"),
        "inputs": matrices,
        "result": result,
        "steps": steps or [],
        "solution_type": solution_type
    }
    
    try:
        ensure_data_dir()
        history = load_history()
        history.insert(0, item)  # Le plus récent en premier
        history = history[:100]  # Limiter à 100 enregistrements
        
        history_path = get_history_file()
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # Toujours écrire dans stderr pour ne jamais polluer stdout (utilisé par IPC JSON)
        sys.stderr.write(f"Avertissement lors de la sauvegarde de l'historique : {e}\n")
        
    return item

def delete_history_item(item_id: Any):
    """Supprime un enregistrement spécifique de l'historique."""
    try:
        ensure_data_dir()
        history = load_history()
        updated_history = [item for item in history if str(item.get("id")) != str(item_id)]
        history_path = get_history_file()
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(updated_history, f, ensure_ascii=False, indent=2)
        return updated_history
    except Exception as e:
        sys.stderr.write(f"Erreur lors de la suppression de l'élément : {e}\n")
        return []

def clear_history():
    """Efface tout l'historique."""
    try:
        ensure_data_dir()
        history_path = get_history_file()
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    except Exception as e:
        sys.stderr.write(f"Erreur lors de l'effacement de l'historique : {e}\n")

