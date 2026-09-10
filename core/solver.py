"""
Module de résolution de systèmes d'équations linéaires AX = B.
Utilise l'élimination de Gauss-Jordan sur la matrice augmentée [A | B]
et détecte automatiquement le type de solution :
- CAS 1 : Solution unique
- CAS 2 : Infinité de solutions
- CAS 3 : Aucune solution
"""

from typing import List, Tuple, Dict, Any, Optional
from utils.formatter import format_number, format_matrix_str

def solve_system(A: List[List[float]], B: List[float]) -> Tuple[str, Optional[List[float]], List[List[float]], List[Dict[str, Any]], str]:
    """
    Routier principal de résolution du système linéaire A X = B.
    
    Paramètres :
        A : Matrice des coefficients (m × n)
        B : Vecteur des constantes (m × 1)
        
    Retourne :
        (type_solution, vecteur_solution, matrice_augmentee_finale, etapes, message_explicatif)
        
        type_solution : "UNIQUE", "INFINITE", "NONE"
    """
    if not A or not A[0] or not B:
        raise ValueError("Le système d'équations ne peut pas être vide.")
        
    rows = len(A)
    cols = len(A[0])
    
    if len(B) != rows:
        raise ValueError(f"Incompatibilité : La matrice A a {rows} équations mais B a {len(B)} constantes.")
        
    # Construction de la matrice augmentée [A | B]
    aug = []
    for i in range(rows):
        aug.append(A[i][:] + [float(B[i])])
        
    def format_aug_system(M):
        lines = []
        for r in M:
            left = "  ".join(format_number(x).rjust(6) for x in r[:-1])
            right = format_number(r[-1]).rjust(6)
            lines.append(f"[ {left}  |  {right} ]")
        return "\n".join(lines)

    steps = [{
        "step": 0,
        "operation": "Matrice Augmentée Initiale [A | B]",
        "matrix": [row[:] for row in aug],
        "formatted": format_aug_system(aug),
        "description": "Représentation matricielle du système d'équations linéaires."
    }]
    
    step_counter = 1
    pivot_row = 0
    pivot_cols = []
    
    # Gauss-Jordan sur [A | B]
    for col in range(cols):
        if pivot_row >= rows:
            break
            
        # Recherche du pivot
        sel = pivot_row
        while sel < rows and abs(aug[sel][col]) < 1e-12:
            sel += 1
            
        if sel == rows:
            continue  # Pas de pivot dans cette colonne (variable libre)
            
        pivot_cols.append(col)
        
        # Échange de lignes
        if sel != pivot_row:
            aug[pivot_row], aug[sel] = aug[sel], aug[pivot_row]
            steps.append({
                "step": step_counter,
                "operation": f"L{pivot_row+1} ↔ L{sel+1}",
                "matrix": [row[:] for row in aug],
                "formatted": format_aug_system(aug),
                "description": f"Opération 3 (L_i ↔ L_j) : Échanger la ligne L{pivot_row+1} et la ligne L{sel+1}."
            })
            step_counter += 1
            
        # Normalisation du pivot à 1
        pivot_val = aug[pivot_row][col]
        if abs(pivot_val - 1.0) > 1e-12:
            scale_factor = 1.0 / pivot_val
            for c in range(cols + 1):
                aug[pivot_row][c] *= scale_factor
            scale_str = format_number(scale_factor)
            steps.append({
                "step": step_counter,
                "operation": f"L{pivot_row+1} ← {scale_str} · L{pivot_row+1}",
                "matrix": [row[:] for row in aug],
                "formatted": format_aug_system(aug),
                "description": f"Opération 1 (L_i ← c · L_i) : Multiplier la ligne L{pivot_row+1} par le scalaire non nul c = 1 / ({format_number(pivot_val)}) = {scale_str} pour obtenir un pivot unitaire."
            })
            step_counter += 1
            
        # Élimination dans les autres lignes
        for r in range(rows):
            if r != pivot_row and abs(aug[r][col]) > 1e-12:
                factor = aug[r][col]
                for c in range(cols + 1):
                    aug[r][c] -= factor * aug[pivot_row][c]
                    
                factor_str = format_number(abs(factor))
                if factor >= 0:
                    op_str = f"L{r+1} ← L{r+1} - {factor_str} · L{pivot_row+1}"
                    desc = f"Opération 2 (L_i ← L_i + c · L_j) : Ajouter à la ligne L{r+1} le multiple (-{factor_str}) · L{pivot_row+1} pour annuler le coefficient en colonne C_{col+1}."
                else:
                    op_str = f"L{r+1} ← L{r+1} + {factor_str} · L{pivot_row+1}"
                    desc = f"Opération 2 (L_i ← L_i + c · L_j) : Ajouter à la ligne L{r+1} le multiple (+{factor_str}) · L{pivot_row+1} pour annuler le coefficient en colonne C_{col+1}."
                    
                steps.append({
                    "step": step_counter,
                    "operation": op_str,
                    "matrix": [row[:] for row in aug],
                    "formatted": format_aug_system(aug),
                    "description": desc
                })
                step_counter += 1
                
        pivot_row += 1

    # Nettoyage des zéros
    for r in range(rows):
        for c in range(cols + 1):
            if abs(aug[r][c]) < 1e-12:
                aug[r][c] = 0.0

    # ANALYSE DE LA SOLUTION (Théorème de Rouché-Capelli)
    
    # 1. Vérification de l'incompatibilité (0 = k avec k != 0)
    for r in range(rows):
        all_zeros = all(abs(aug[r][c]) < 1e-12 for c in range(cols))
        constant = aug[r][cols]
        if all_zeros and abs(constant) > 1e-12:
            msg = f"Incompatibilité détectée à la ligne {r+1} : 0 = {format_number(constant)} (Contradiction). Le système n'a aucune solution."
            return "NONE", None, aug, steps, msg
            
    # 2. Nombre de pivots = rang de A
    rank = len(pivot_cols)
    
    if rank == cols:
        # Solution unique
        solution = [0.0] * cols
        for i, col in enumerate(pivot_cols):
            solution[col] = aug[i][cols]
            
        vars_str = ", ".join(f"x{i+1} = {format_number(val)}" for i, val in enumerate(solution))
        msg = f"Le système possède une SOLUTION UNIQUE : {vars_str}"
        return "UNIQUE", solution, aug, steps, msg
    else:
        # Infinité de solutions
        num_free = cols - rank
        msg = f"Le système possède une INFINITÉ DE SOLUTIONS (Système indéterminé avec {num_free} variable(s) libre(s))."
        return "INFINITE", None, aug, steps, msg
