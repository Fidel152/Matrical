"""
Module de formatage pour les nombres et matrices.
Fournit un affichage propre sans bruits de précision flottante (ex: 2.0000000000000004 -> 2).
"""

import math
from typing import List, Union

def format_number(val: Union[int, float], precision: int = 6) -> str:
    """
    Formate un nombre de manière lisible et propre.
    - Supprime les décimales inutiles (.0)
    - Arrondit à la précision donnée pour éviter les imprécisions binaires
    - Évite l'affichage de '-0' ou '-0.0'
    """
    if val is None:
        return "N/A"
    
    # Arrondi pour supprimer le bruit de virgule flottante
    rounded = round(float(val), precision)
    
    # Traitement de -0.0
    if abs(rounded) < 1e-12:
        rounded = 0.0
        
    # Si c'est un entier
    if rounded.is_integer():
        return str(int(rounded))
    
    # Formatage propre sans zéros inutiles à la fin
    res = f"{rounded:.{precision}f}".rstrip('0').rstrip('.')
    return res if res != "-0" else "0"

def format_matrix(matrix: List[List[Union[int, float]]], precision: int = 6) -> List[List[str]]:
    """
    Convertit une matrice de nombres en une matrice de chaînes formatées.
    """
    return [[format_number(val, precision) for val in row] for row in matrix]

def format_matrix_str(matrix: List[List[Union[int, float]]], precision: int = 6) -> str:
    """
    Retourne une représentation sous forme de chaîne de caractères alignée de la matrice.
    """
    formatted = format_matrix(matrix, precision)
    if not formatted:
        return "[]"
    
    col_widths = [max(len(row[col]) for row in formatted) for col in range(len(formatted[0]))]
    
    lines = []
    for row in formatted:
        line = "  ".join(val.rjust(col_widths[col]) for col, val in enumerate(row))
        lines.append(f"[ {line} ]")
    
    return "\n".join(lines)
