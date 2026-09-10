"""
Module de calcul du déterminant.
Implémentation algorithmique manuelle (formule directe 2x2, règle de Sarrus / cofacteurs 3x3,
et méthode d'élimination de Gauss triangulaire pour n x n).
"""

from typing import List, Tuple
from utils.validators import validate_square
from utils.formatter import format_number, format_matrix_str

def determinant(A: List[List[float]]) -> Tuple[float, List[str]]:
    """
    Calcule le déterminant d'une matrice carrée de taille n x n.
    Refuse les matrices non carrées.
    
    Algorithme :
    - 1x1 : det = A[0][0]
    - 2x2 : ad - bc
    - n x n : Méthode de Gauss (triangularisation) avec suivi des permutations de lignes.
              Det = (-1)^(permutations) * produit(diagonale).
    """
    valid, msg = validate_square(A)
    if not valid:
        raise ValueError(msg)
    
    n = len(A)
    steps = [f"Calcul du déterminant d'une matrice {n}×{n} :"]
    
    # Cas 1x1
    if n == 1:
        det = float(A[0][0])
        steps.append(f"Matrice 1×1 : Det = {det}")
        return det, steps
    
    # Cas 2x2
    if n == 2:
        a, b = A[0][0], A[0][1]
        c, d = A[1][0], A[1][1]
        det = (a * d) - (b * c)
        steps.append(f"Formule 2×2 : |a  b| / |c  d| = a·d - b·c")
        steps.append(f"Det = ({a} × {d}) - ({b} × {c}) = {a * d} - {b * c} = {det}")
        return det, steps
    
    # Cas 3x3 - Explication par règle de Sarrus ou réduction
    # Pour la généralité et la transparence pédagogique, faisons la méthode d'élimination de Gauss
    # en traçant chaque opération élémentaire
    
    # Copie de travail de la matrice
    M = [row[:] for row in A]
    row_swaps = 0
    steps.append("Méthode de triangularisation de Gauss :")
    steps.append("Objectif : Transformer la matrice en matrice triangulaire supérieure via les opérations élémentaires sur les lignes :")
    steps.append("  • Opération 3 (L_i ↔ L_j) : Échanger deux lignes (multiplie le déterminant par -1).")
    steps.append("  • Opération 2 (L_i ← L_i + c · L_j) : Ajouter à une ligne le multiple d'une autre ligne (ne modifie pas le déterminant).")
    steps.append("Propriété fondamentale : Le déterminant d'une matrice triangulaire est le produit des éléments de sa diagonale principale.")
    steps.append("")
    
    for col in range(n):
        # Recherche du pivot maximal dans la colonne pour la stabilité numérique
        pivot_row = col
        max_val = abs(M[col][col])
        for r in range(col + 1, n):
            if abs(M[r][col]) > max_val:
                max_val = abs(M[r][col])
                pivot_row = r
                
        # Si le plus grand pivot est 0, le déterminant est 0 (colonnes/lignes liées)
        if abs(M[pivot_row][col]) < 1e-12:
            steps.append(f"Colonne C_{col+1} : Tous les pivots potentiels sont nuls. Lignes linéairement dépendantes.")
            steps.append("Théorème : det(A) = 0.")
            return 0.0, steps
        
        # Échange de lignes si nécessaire
        if pivot_row != col:
            M[col], M[pivot_row] = M[pivot_row], M[col]
            row_swaps += 1
            steps.append(f"Opération 3 (L_i ↔ L_j) : L{col+1} ↔ L{pivot_row+1}")
            steps.append(f"  • Description : Échanger la ligne L{col+1} et la ligne L{pivot_row+1} (Changement de signe : facteur × (-1)).")
            steps.append(format_matrix_str(M))
            steps.append("")
            
        # Élimination sous le pivot
        pivot = M[col][col]
        for r in range(col + 1, n):
            if abs(M[r][col]) > 1e-12:
                factor = M[r][col] / pivot
                for c in range(col, n):
                    M[r][c] -= factor * M[col][c]
                factor_str = format_number(abs(factor))
                if factor >= 0:
                    op_str = f"L{r+1} ← L{r+1} - {factor_str} · L{col+1}"
                    desc = f"Ajouter à la ligne L{r+1} le multiple (-{factor_str}) · L{col+1} sous le pivot (le déterminant reste invariant)."
                else:
                    op_str = f"L{r+1} ← L{r+1} + {factor_str} · L{col+1}"
                    desc = f"Ajouter à la ligne L{r+1} le multiple (+{factor_str}) · L{col+1} sous le pivot (le déterminant reste invariant)."
                steps.append(f"Opération 2 (L_i ← L_i + c · L_j) : {op_str}")
                steps.append(f"  • Description : {desc}")
                steps.append(format_matrix_str(M))
                steps.append("")
                
    # Calcul du produit de la diagonale
    diag_product = 1.0
    diag_terms = []
    for i in range(n):
        diag_val = M[i][i]
        diag_product *= diag_val
        diag_terms.append(format_number(diag_val))
        
    sign = (-1) ** row_swaps
    det = sign * diag_product
    
    steps.append("Produit des éléments de la diagonale principale :")
    steps.append(f"Produit = {' × '.join(diag_terms)} = {format_number(diag_product)}")
    if row_swaps > 0:
        steps.append(f"Nombre d'échanges de lignes = {row_swaps} => Facteur de signe = (-1)^{row_swaps} = {sign}")
        
    steps.append(f"Déterminant final Det(A) = {format_number(det)}")
    return det, steps
