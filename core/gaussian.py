"""
Module pour les opérations élémentaires sur les lignes et les formes échelonnées (REF et RREF).
Implémentation algorithmique manuelle de l'élimination de Gauss et Gauss-Jordan.
"""

from typing import List, Tuple, Dict, Any
from utils.formatter import format_number, format_matrix, format_matrix_str

def swap_rows(M: List[List[float]], r1: int, r2: int) -> None:
    """Opération élémentaire E1 : Échange deux lignes L_{r1} <-> L_{r2} (0-indexed)."""
    M[r1], M[r2] = M[r2], M[r1]

def scale_row(M: List[List[float]], r: int, factor: float) -> None:
    """Opération élémentaire E2 : Multiplie une ligne par un scalaire non nul L_r <- factor * L_r."""
    for c in range(len(M[r])):
        M[r][c] *= factor

def add_multiple_of_row(M: List[List[float]], target_row: int, source_row: int, factor: float) -> None:
    """Opération élémentaire E3 : L_{target} <- L_{target} + factor * L_{source}."""
    for c in range(len(M[target_row])):
        M[target_row][c] += factor * M[source_row][c]

def row_echelon(A: List[List[float]]) -> Tuple[List[List[float]], List[Dict[str, Any]]]:
    """
    Calcule la Forme Échelonnée sur les Lignes (REF / Row Echelon Form) par l'élimination de Gauss.
    
    Retourne:
        (Matrice_REF, Liste_d_etapes)
        Où chaque étape est un dictionnaire {"operation": str, "matrix": List[List[float]], "description": str}
    """
    if not A or not A[0]:
        raise ValueError("La matrice ne peut pas être vide.")
        
    rows = len(A)
    cols = len(A[0])
    M = [row[:] for row in A]
    
    steps = [{
        "step": 0,
        "operation": "Matrice Initiale A",
        "matrix": [row[:] for row in M],
        "description": "Matrice de départ avant l'application des opérations élémentaires sur les lignes (L_i)."
    }]
    
    pivot_row = 0
    step_counter = 1
    
    for col in range(cols):
        if pivot_row >= rows:
            break
            
        # Recherche du meilleur pivot non nul
        sel = pivot_row
        while sel < rows and abs(M[sel][col]) < 1e-12:
            sel += 1
            
        if sel == rows:
            # Aucun pivot dans cette colonne
            continue
            
        # Échange de lignes si le pivot n'est pas sur la ligne courante
        if sel != pivot_row:
            swap_rows(M, pivot_row, sel)
            steps.append({
                "step": step_counter,
                "operation": f"L{pivot_row+1} ↔ L{sel+1}",
                "matrix": [row[:] for row in M],
                "description": f"Opération 3 (L_i ↔ L_j) : Échanger la ligne L{pivot_row+1} et la ligne L{sel+1} pour placer un pivot non nul en colonne {col+1}."
            })
            step_counter += 1
            
        # Élimination des éléments sous le pivot
        pivot_val = M[pivot_row][col]
        for r in range(pivot_row + 1, rows):
            if abs(M[r][col]) > 1e-12:
                factor = M[r][col] / pivot_val
                add_multiple_of_row(M, r, pivot_row, -factor)
                
                factor_str = format_number(factor)
                if factor >= 0:
                    op_str = f"L{r+1} ← L{r+1} - {factor_str} · L{pivot_row+1}"
                    desc = f"Opération 2 (L_i ← L_i + c · L_j) : Ajouter à la ligne L{r+1} le multiple (-{factor_str}) · L{pivot_row+1} pour annuler l'élément sous le pivot (colonne {col+1})."
                else:
                    abs_factor_str = format_number(abs(factor))
                    op_str = f"L{r+1} ← L{r+1} + {abs_factor_str} · L{pivot_row+1}"
                    desc = f"Opération 2 (L_i ← L_i + c · L_j) : Ajouter à la ligne L{r+1} le multiple (+{abs_factor_str}) · L{pivot_row+1} pour annuler l'élément sous le pivot (colonne {col+1})."
                
                steps.append({
                    "step": step_counter,
                    "operation": op_str,
                    "matrix": [row[:] for row in M],
                    "description": desc
                })
                step_counter += 1
                
        pivot_row += 1
        
    # Nettoyage des zéros proches de 0
    for r in range(rows):
        for c in range(cols):
            if abs(M[r][c]) < 1e-12:
                M[r][c] = 0.0
                
    return M, steps

def rref(A: List[List[float]]) -> Tuple[List[List[float]], List[Dict[str, Any]]]:
    """
    Calcule la Forme Échelonnée Réduite sur les Lignes (RREF / Reduced Row Echelon Form) par Gauss-Jordan.
    Chaque pivot devient égal à 1, et tous les éléments dans sa colonne (au-dessus et en-dessous) deviennent 0.
    """
    if not A or not A[0]:
        raise ValueError("La matrice ne peut pas être vide.")
        
    rows = len(A)
    cols = len(A[0])
    M = [row[:] for row in A]
    
    steps = [{
        "step": 0,
        "operation": "Matrice Initiale A",
        "matrix": [row[:] for row in M],
        "description": "Matrice de départ avant l'application de la méthode de Gauss-Jordan (RREF)."
    }]
    
    pivot_row = 0
    step_counter = 1
    
    for col in range(cols):
        if pivot_row >= rows:
            break
            
        # Recherche du pivot
        sel = pivot_row
        while sel < rows and abs(M[sel][col]) < 1e-12:
            sel += 1
            
        if sel == rows:
            continue
            
        if sel != pivot_row:
            swap_rows(M, pivot_row, sel)
            steps.append({
                "step": step_counter,
                "operation": f"L{pivot_row+1} ↔ L{sel+1}",
                "matrix": [row[:] for row in M],
                "description": f"Opération 3 (L_i ↔ L_j) : Échanger la ligne L{pivot_row+1} et la ligne L{sel+1}."
            })
            step_counter += 1
            
        # Normalisation du pivot à 1
        pivot_val = M[pivot_row][col]
        if abs(pivot_val - 1.0) > 1e-12:
            scale_row(M, pivot_row, 1.0 / pivot_val)
            scale_c = format_number(1.0 / pivot_val)
            steps.append({
                "step": step_counter,
                "operation": f"L{pivot_row+1} ← {scale_c} · L{pivot_row+1}",
                "matrix": [row[:] for row in M],
                "description": f"Opération 1 (L_i ← c · L_i) : Multiplier la ligne L{pivot_row+1} par le scalaire non nul c = 1 / ({format_number(pivot_val)}) = {scale_c} pour obtenir un pivot unitaire égal à 1."
            })
            step_counter += 1
            
        # Élimination au-dessus et au-dessous du pivot (Gauss-Jordan)
        for r in range(rows):
            if r != pivot_row and abs(M[r][col]) > 1e-12:
                factor = M[r][col]
                add_multiple_of_row(M, r, pivot_row, -factor)
                
                factor_str = format_number(abs(factor))
                if factor >= 0:
                    op_str = f"L{r+1} ← L{r+1} - {factor_str} · L{pivot_row+1}"
                    desc = f"Opération 2 (L_i ← L_i + c · L_j) : Ajouter à la ligne L{r+1} le multiple (-{factor_str}) · L{pivot_row+1} pour annuler le coefficient en ligne {r+1}, colonne {col+1}."
                else:
                    op_str = f"L{r+1} ← L{r+1} + {factor_str} · L{pivot_row+1}"
                    desc = f"Opération 2 (L_i ← L_i + c · L_j) : Ajouter à la ligne L{r+1} le multiple (+{factor_str}) · L{pivot_row+1} pour annuler le coefficient en ligne {r+1}, colonne {col+1}."
                
                steps.append({
                    "step": step_counter,
                    "operation": op_str,
                    "matrix": [row[:] for row in M],
                    "description": desc
                })
                step_counter += 1
                
        pivot_row += 1
        
    for r in range(rows):
        for c in range(cols):
            if abs(M[r][c]) < 1e-12:
                M[r][c] = 0.0
                
    return M, steps
