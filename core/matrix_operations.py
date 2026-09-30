"""
Module des opérations fondamentales sur les matrices.
Implémentation manuelle explicite en Python (sans numpy.matmul ou numpy.dot).
"""

from typing import List, Tuple
from utils.validators import validate_same_dimensions, validate_multiplication_dimensions

def matrix_add(A: List[List[float]], B: List[List[float]]) -> Tuple[List[List[float]], List[str]]:
    """
    Additionne manuellement deux matrices A et B de mêmes dimensions.
    Formule : C[i][j] = A[i][j] + B[i][j]
    
    Paramètres:
        A: Première matrice (lignes x colonnes)
        B: Deuxième matrice (lignes x colonnes)
        
    Retourne:
        (Matrice résultante C, Liste des étapes explicatives)
    """
    valid, msg = validate_same_dimensions(A, B)
    if not valid:
        raise ValueError(msg)
    
    rows = len(A)
    cols = len(A[0])
    C = []
    steps = [f"Addition de deux matrices de taille {rows}×{cols} :"]
    
    for i in range(rows):
        row_c = []
        for j in range(cols):
            val_a = A[i][j]
            val_b = B[i][j]
            val_c = val_a + val_b
            row_c.append(val_c)
            steps.append(f"Élément C[{i+1}][{j+1}] = A[{i+1}][{j+1}] + B[{i+1}][{j+1}] = {val_a} + {val_b} = {val_c}")
        C.append(row_c)
        
    return C, steps

def matrix_subtract(A: List[List[float]], B: List[List[float]]) -> Tuple[List[List[float]], List[str]]:
    """
    Soustrait manuellement la matrice B de la matrice A.
    Formule : C[i][j] = A[i][j] - B[i][j]
    """
    valid, msg = validate_same_dimensions(A, B)
    if not valid:
        raise ValueError(msg)
    
    rows = len(A)
    cols = len(A[0])
    C = []
    steps = [f"Soustraction de deux matrices de taille {rows}×{cols} :"]
    
    for i in range(rows):
        row_c = []
        for j in range(cols):
            val_a = A[i][j]
            val_b = B[i][j]
            val_c = val_a - val_b
            row_c.append(val_c)
            steps.append(f"Élément C[{i+1}][{j+1}] = A[{i+1}][{j+1}] - B[{i+1}][{j+1}] = {val_a} - {val_b} = {val_c}")
        C.append(row_c)
        
    return C, steps

def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> Tuple[List[List[float]], List[str]]:
    """
    Multiplie manuellement deux matrices A (m x p) et B (p x n) à l'aide d'une triple boucle.
    Formule : C[i][j] = somme_{k=0}^{p-1} (A[i][k] * B[k][j])
    
    Algorithme manuel avec boucles explicites (sans np.matmul / np.dot).
    """
    valid, msg = validate_multiplication_dimensions(A, B)
    if not valid:
        raise ValueError(msg)
    
    m = len(A)
    p = len(A[0])
    n = len(B[0])
    
    C = []
    steps = [f"Multiplication A ({m}×{p}) × B ({p}×{n}) -> Résultat C ({m}×{n}) :"]
    
    for i in range(m):
        row_c = []
        for j in range(n):
            sum_val = 0.0
            terms = []
            for k in range(p):
                prod = A[i][k] * B[k][j]
                sum_val += prod
                terms.append(f"({A[i][k]} × {B[k][j]})")
            
            row_c.append(sum_val)
            expr = " + ".join(terms)
            steps.append(f"C[{i+1}][{j+1}] = {expr} = {sum_val}")
        C.append(row_c)
        
    return C, steps

def identity_matrix(n: int) -> Tuple[List[List[float]], List[str]]:
    """
    Génère la matrice identité I_n de taille n x n avec une explication pédagogique,
    simple et claire expliquant son rôle concret dans le calcul matriciel et l'inversion.
    """
    if n <= 0:
        raise ValueError("La dimension de la matrice identité doit être au moins 1.")
    
    I = []
    for i in range(n):
        row = [1.0 if i == j else 0.0 for j in range(n)]
        I.append(row)
        
    steps = [
        f"Matrice Identité I_{n} (taille {n}×{n}) :",
        "",
        "• Qu'est-ce que c'est ?",
        f"  C'est une matrice carrée {n}×{n} avec des 1 sur la diagonale principale et des 0 partout ailleurs.",
        "",
        "• À quoi sert-elle ?",
        "  Elle joue pour les matrices exactement le même rôle que le chiffre 1 pour les nombres usuels :",
        "  5 × 1 = 5",
        f"  De la même façon, pour toute matrice A de taille {n}×{n} :",
        f"  A × I_{n} = A",
        "",
        "• Comment est-elle utilisée dans l'inversion de matrice (Gauss-Jordan) ?",
        f"  Elle sert de matrice de référence et d'objectif final :",
        f"  On place [A | I_{n}] côte à côte au départ, puis on transforme la partie gauche en I_{n}.",
        "  Dès que la partie gauche devient la matrice identité, la partie droite devient l'inverse A⁻¹."
    ]
    
    return I, steps

def transpose(A: List[List[float]]) -> Tuple[List[List[float]], List[str]]:
    """
    Calcule manuellement la transposée de la matrice A.
    Formule : A_T[j][i] = A[i][j]
    
    Les lignes deviennent les colonnes.
    """
    if not A or not A[0]:
        raise ValueError("La matrice ne peut pas être vide.")
        
    rows = len(A)
    cols = len(A[0])
    
    A_T = []
    steps = [
        f"Transposition de la matrice ({rows}×{cols}) vers ({cols}×{rows}) :",
        "Règle : Les lignes deviennent les colonnes (Aᵀ[j][i] = A[i][j])."
    ]
    
    for j in range(cols):
        new_row = []
        for i in range(rows):
            new_row.append(A[i][j])
        A_T.append(new_row)
        
    return A_T, steps

def matrix_divide(A: List[List[float]], B: List[List[float]]) -> Tuple[List[List[float]], List[str]]:
    """
    Divise la matrice A par la matrice B en calculant A × B⁻¹.
    Vérifie que B est carrée et inversible, et que les dimensions de A et B⁻¹ sont compatibles.
    """
    from core.inverse import inverse
    from utils.formatter import format_matrix, format_number

    rows_B, cols_B = len(B), len(B[0])
    if rows_B != cols_B:
        raise ValueError(
            f"Division impossible : La matrice B ({rows_B}×{cols_B}) doit être carrée pour posséder une inverse (A ÷ B = A × B⁻¹)."
        )

    rows_A, cols_A = len(A), len(A[0])
    if cols_A != rows_B:
        raise ValueError(
            f"Division impossible : Le nombre de colonnes de A ({cols_A}) doit être égal à la dimension de B ({rows_B}×{cols_B})."
        )

    B_inv, inv_steps, is_inv = inverse(B)
    if not is_inv or B_inv is None:
        raise ValueError(
            "Division impossible : La matrice B n'est pas inversible (son déterminant est égal à 0)."
        )

    C, mult_steps = matrix_multiply(A, B_inv)

    steps = [
        f"Division matricielle A ({rows_A}×{cols_A}) ÷ B ({rows_B}×{cols_B}) :",
        "Règle mathématique : Diviser par une matrice B revient à multiplier par son inverse B⁻¹ :",
        "Formule : A ÷ B = A × B⁻¹",
        "",
        "==================================================",
        "ÉTAPE 1 : Calcul de la matrice inverse B⁻¹",
        "==================================================",
    ]
    steps.extend(inv_steps)
    steps.extend([
        "",
        "==================================================",
        "ÉTAPE 2 : Multiplication de A par B⁻¹ (C = A × B⁻¹)",
        "==================================================",
    ])
    steps.extend(mult_steps)

    return C, steps

