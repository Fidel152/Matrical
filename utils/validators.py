"""
Module de validation des matrices et entrées utilisateur.
Vérifie la validité numérique, les dimensions et les conditions d'inversibilité/résolution.
"""

from typing import List, Tuple, Any, Union

def is_numeric(val: Any) -> bool:
    """Vérifie si une valeur ou chaîne est un nombre valide."""
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False

def parse_matrix(raw_matrix: List[List[Any]]) -> List[List[float]]:
    """
    Convertit une grille brute d'entrées en matrice de float.
    Lève une ValueError si une entrée n'est pas un nombre.
    """
    if not raw_matrix or not raw_matrix[0]:
        raise ValueError("La matrice ne peut pas être vide.")
    
    parsed = []
    for i, row in enumerate(raw_matrix):
        parsed_row = []
        for j, val in enumerate(row):
            str_val = str(val).strip().replace(',', '.')
            if not is_numeric(str_val):
                raise ValueError(f"Valeur invalide à la position ({i+1}, {j+1}) : '{val}'. Un nombre est requis.")
            parsed_row.append(float(str_val))
        parsed.append(parsed_row)
    
    return parsed

def validate_same_dimensions(A: List[List[float]], B: List[List[float]]) -> Tuple[bool, str]:
    """
    Vérifie que deux matrices ont exactement les mêmes dimensions.
    Requis pour l'addition et la soustraction.
    """
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    if rows_A != rows_B or cols_A != cols_B:
        return False, f"Incompatibilité de dimensions : Matrice A ({rows_A}×{cols_A}) et Matrice B ({rows_B}×{cols_B}). Les deux matrices doivent avoir exactement les mêmes dimensions."
    return True, ""

def validate_multiplication_dimensions(A: List[List[float]], B: List[List[float]]) -> Tuple[bool, str]:
    """
    Vérifie que le nombre de colonnes de A égale le nombre de lignes de B.
    Requis pour la multiplication A × B.
    """
    cols_A = len(A[0])
    rows_B = len(B)
    
    if cols_A != rows_B:
        return False, f"Multiplication impossible : Nombre de colonnes de A ({cols_A}) ≠ Nombre de lignes de B ({rows_B})."
    return True, ""

def validate_square(A: List[List[float]]) -> Tuple[bool, str]:
    """
    Vérifie qu'une matrice est carrée (lignes == colonnes).
    Requis pour déterminant et inversion.
    """
    rows, cols = len(A), len(A[0])
    if rows != cols:
        return False, f"La matrice doit être carrée. Taille actuelle : {rows}×{cols}."
    return True, ""
