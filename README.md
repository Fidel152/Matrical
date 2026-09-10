# MATRIXCALC — Calculatrice et Solveur Matriciel

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet.svg)](https://customtkinter.tomschimansky.com/)

**MATRIXCALC** est une application informatique et pédagogique de calcul matriciel et de résolution de systèmes d'équations linéaires, développée en Python avec l'interface graphique **CustomTkinter**.

Ce projet a été conçu dans un cadre universitaire pour présenter et expliquer de manière transparente les algorithmes fondamentaux de l'algèbre linéaire, **sans s'appuyer sur des fonctions boîte noire** de bibliothèques externes.

---

## 🌟 Fonctionnalités Principales

1. **Saisie Dynamique de Matrices (`MatrixInput`)** : Saisie flexible de matrices de toutes dimensions avec validation automatique des entrées numériques.
2. **Opérations Fondamentales** :
   - Addition : $C[i][j] = A[i][j] + B[i][j]$
   - Soustraction : $C[i][j] = A[i][j] - B[i][j]$
   - Multiplication : $C[i][j] = \sum_{k} A[i][k] \times B[k][j]$ (implémentation par triple boucle explicite)
   - Transposée : $A^T[j][i] = A[i][j]$
3. **Déterminant ($Det(A)$)** :
   - Formule directe pour $1\times 1$ et $2\times 2$.
   - Algorithme de triangularisation de Gauss pour $n \times n$ avec suivi des permutations de lignes ($\det(A) = (-1)^{\text{swaps}} \cdot \prod \text{diagonale}$).
4. **Matrice Inverse ($A^{-1}$)** :
   - Méthode d'élimination de Gauss-Jordan sur la matrice augmentée $[A \mid I] \to [I \mid A^{-1}]$.
   - Détection des matrices singulières ($\det(A) = 0$).
5. **Formes Échelonnées** :
   - Forme Échelonnée sur les lignes (REF) via l'élimination de Gauss.
   - Forme Échelonnée Réduite (RREF) via l'élimination de Gauss-Jordan.
6. **Solveur de Systèmes d'Équations Linéaires ($A X = B$)** :
   - Construction automatique de la matrice augmentée $[A \mid B]$.
   - Détection automatique du type de solution selon le théorème de Rouché-Capelli :
     - **CAS 1** : Solution unique (avec affichage des inconnues $x, y, z, \dots$).
     - **CAS 2** : Infinité de solutions (système indéterminé).
     - **CAS 3** : Aucune solution (incompatibilité, ex: $0 = k$ avec $k \neq 0$).
7. **Affichage Détaillé Étape par Étape** : Explication de chaque opération élémentaire sur les lignes ($L_i \leftrightarrow L_j$, $L_i \leftarrow k L_i$, $L_i \leftarrow L_i + k L_j$).
8. **Historique des Calculs** : Enregistrement persistant des calculs effectués dans `data/history.json`.
9. **Interface Graphique Moderne** : Interface responsive CustomTkinter avec support des thèmes **Clair** et **Sombre**.

---

## 📁 Architecture du Projet

```
MatrixCalc/
│
├── main.py                     # Point d'entrée de l'application desktop
├── cli.py                      # Bridge JSON/CLI pour exécution backend
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation complète
│
├── core/                       # Algorithmes mathématiques manuels
│   ├── __init__.py
│   ├── matrix_operations.py    # Addition, Soustraction, Multiplication, Transposée
│   ├── determinant.py          # Déterminant par triangularisation de Gauss
│   ├── inverse.py              # Inversion par Gauss-Jordan [A|I]
│   ├── gaussian.py             # Opérations élémentaires, REF, RREF
│   └── solver.py               # Solveur AX = B et analyse Rouché-Capelli
│
├── ui/                         # Interface graphique CustomTkinter
│   ├── __init__.py
│   ├── app.py                  # Fenêtre principale et navigation
│   ├── home.py                 # Page d'accueil avec cartes raccourcis
│   ├── matrix_input.py         # Composant réutilisable de saisie
│   ├── operations.py           # Vues pour A+B, A-B, A*B, Aᵀ
│   ├── solver_ui.py            # Vues pour Det, Inverse, REF, RREF, AX=B
│   ├── history.py              # Vue d'historique
│   └── help.py                 # Guide théorique et pédagogique
│
├── utils/                      # Utilitaires
│   ├── __init__.py
│   ├── validators.py           # Validation des entrées et dimensions
│   ├── formatter.py            # Formatage propre des nombres sans bruit flottant
│   └── storage.py              # Sauvegarde et lecture de l'historique JSON
│
├── data/                       # Données
│   └── history.json            # Fichier d'historique local
│
└── tests/                      # Suite de tests unitaires
    └── test_matrix.py          # Tests automatisés unittest (13 tests)
```

---

## ⚙️ Installation et Lancement

### 1. Prérequis
- **Python 3.10** ou version ultérieure installée.

### 2. Création et activation de l'environnement virtuel

**Sur Linux / macOS :**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Sur Windows :**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancement de l'application
```bash
python main.py
```

### 5. Exécution des tests unitaires
```bash
python -m unittest tests/test_matrix.py
```

---

## 🧮 Explications des Algorithmes (Pour Soutenance Universitaire)

### 1. Multiplication de matrices (`matrix_multiply`)
Chaque terme $C[i][j]$ est calculé manuellement sans utiliser de fonction préconçue :
```python
for i in range(m):
    for j in range(n):
        sum_val = 0.0
        for k in range(p):
            sum_val += A[i][k] * B[k][j]
        C[i][j] = sum_val
```

### 2. Déterminant par Triangularisation (`determinant`)
Au lieu de la formule récursive d'expansion des cofacteurs en $O(n!)$, nous utilisons la méthode de réduction de Gauss en $O(n^3)$ :
- La matrice est transformée en une matrice triangulaire supérieure $U$.
- Chaque échange de lignes incrémente un compteur de permutations (`row_swaps`).
- Le déterminant est égal à :
  $$\det(A) = (-1)^{\text{row\_swaps}} \times \prod_{i=1}^{n} U[i][i]$$

### 3. Matrice Inverse par Gauss-Jordan (`inverse`)
- On juxtapose la matrice identité $I$ à la matrice $A$ pour former la matrice augmentée $[A \mid I]$.
- On applique les trois opérations élémentaires sur les lignes ($L_i \leftrightarrow L_j$, $L_i \leftarrow k L_i$, $L_i \leftarrow L_i + k L_j$) jusqu'à transformer le bloc de gauche en $I$.
- Si l'opération réussit, le bloc de droite devient $A^{-1}$. Si un pivot nul ne peut être éliminé, la matrice n'est pas inversible ($\det(A) = 0$).

---

## 📜 Licence & Crédits

Projet universitaire réalisé pour le cours d'Algèbre Linéaire et Informatique.
Développé avec Python 3 et CustomTkinter.
