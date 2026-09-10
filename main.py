"""
Point d'entrée principal de l'application de bureau MATRIXCALC.
Projet universitaire : Calculatrice et solveur matriciel.

Pour lancer l'application :
    python main.py
"""

import sys
import os

# S'assurer que le répertoire racine est dans sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app import MatrixCalcApp

def main():
    print("Démarrage de MATRIXCALC...")
    app = MatrixCalcApp()
    app.mainloop()

if __name__ == "__main__":
    main()
