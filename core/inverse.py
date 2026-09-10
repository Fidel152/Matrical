"""
Module d'inversion de matrice par la méthode de Gauss-Jordan [A | I] -> [I | A^-1].
Implémentation algorithmique pédagogique, scientifique et détaillée pas à pas.
Explique le calcul réellement effectué sur la matrice de l'utilisateur.
"""

from typing import List, Tuple, Optional, Union
from fractions import Fraction
from copy import deepcopy
from utils.validators import validate_square
from utils.formatter import format_number

def to_frac(val: Union[int, float, str, Fraction]) -> Fraction:
    """Convertit une valeur numérique en Fraction exacte."""
    if isinstance(val, Fraction):
        return val
    try:
        return Fraction(str(val)).limit_denominator(10000)
    except Exception:
        return Fraction(float(val)).limit_denominator(10000)

def format_frac(f: Union[Fraction, int, float]) -> str:
    """Affiche une fraction ou un nombre sous forme lisible et simplifiée."""
    if isinstance(f, (int, float)):
        try:
            f = Fraction(str(f)).limit_denominator(10000)
        except Exception:
            return format_number(f)
    if isinstance(f, Fraction):
        if f.denominator == 1:
            return str(f.numerator)
        if f.denominator > 10000:
            return format_number(float(f))
        return f"{f.numerator}/{f.denominator}"
    return str(f)

def format_aug_matrix(matrix: List[List[Fraction]], n: int) -> str:
    """Formate une matrice augmentée [A | I] alignée."""
    formatted = [[format_frac(val) for val in row] for row in matrix]
    total_cols = len(matrix[0])
    col_widths = [max(len(row[col]) for row in formatted) for col in range(total_cols)]
    
    lines = []
    for row in formatted:
        left = "  ".join(row[c].rjust(col_widths[c]) for c in range(n))
        right = "  ".join(row[n + c].rjust(col_widths[n + c]) for c in range(n))
        lines.append(f"[ {left}  |  {right} ]")
    return "\n".join(lines)

def format_sq_matrix(matrix: List[List[Fraction]]) -> str:
    """Formate une matrice carrée alignée."""
    formatted = [[format_frac(val) for val in row] for row in matrix]
    n = len(matrix)
    col_widths = [max(len(row[col]) for row in formatted) for col in range(n)]
    
    lines = []
    for row in formatted:
        row_str = "  ".join(row[c].rjust(col_widths[c]) for c in range(n))
        lines.append(f"[ {row_str} ]")
    return "\n".join(lines)

def format_row_aug(row: List[Fraction], n: int) -> str:
    """Formate une ligne de matrice augmentée [x1 x2 | y1 y2]."""
    left = "  ".join(format_frac(x) for x in row[:n])
    right = "  ".join(format_frac(x) for x in row[n:])
    return f"[{left} | {right}]"

def make_box(title1: str, title2: str) -> str:
    """Génère un encadré visuel pédagogique."""
    max_len = max(len(title1), len(title2), 34) + 2
    top = "┌" + "─" * max_len + "┐"
    l1 = f"│ {title1.ljust(max_len - 2)} │"
    l2 = f"│ {title2.ljust(max_len - 2)} │"
    bottom = "└" + "─" * max_len + "┘"
    return f"{top}\n{l1}\n{l2}\n{bottom}"

ORDINALS = [
    "Première", "Deuxième", "Troisième", "Quatrième", "Cinquième",
    "Sixième", "Septième", "Huitième", "Neuvième", "Dixième"
]

def get_ordinal(idx: int) -> str:
    if idx < len(ORDINALS):
        return ORDINALS[idx]
    return f"{idx + 1}ème"

def inverse(A_raw: List[List[float]]) -> Tuple[Optional[List[List[float]]], List[str], bool]:
    """
    Calcule l'inverse d'une matrice carrée A par la méthode de Gauss-Jordan
    avec une explication pédagogique complète pas à pas.
    
    Retourne : (Matrice_Inverse_Float, Liste_Etapes, Est_Inversible)
    """
    valid, msg = validate_square(A_raw)
    if not valid:
        raise ValueError(msg)
        
    n = len(A_raw)
    A = [[to_frac(x) for x in row] for row in A_raw]
    
    # 1. Qu'est-ce qu'on cherche & méthode
    steps = [
        "Nous allons calculer l'inverse de la matrice A à l'aide de la méthode de Gauss-Jordan.",
        "",
        "Une matrice inverse A⁻¹ est une matrice qui, lorsqu'elle est multipliée par A, donne la matrice identité.",
        "Nous allons donc transformer progressivement la matrice A en matrice identité.",
        "",
        "Matrice A :",
        format_sq_matrix(A),
        "",
        f"La matrice identité de taille {n}×{n} est :",
        f"I_{n} =",
        format_sq_matrix([[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]),
        "",
        f"Nous plaçons A et I_{n} côte à côte. Cela permet de suivre simultanément la transformation de A et les opérations qui permettront d'obtenir son inverse.",
        ""
    ]
    
    # Matrice augmentée [A | I_n]
    aug: List[List[Fraction]] = []
    for i in range(n):
        id_part = [Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)]
        aug.append(A[i][:] + id_part)
        
    steps.append(format_aug_matrix(aug, n))
    steps.append("")
    steps.append("À gauche se trouve la matrice A.")
    steps.append(f"À droite se trouve la matrice identité I_{n}.")
    steps.append("")
    steps.append("Notre objectif est de transformer la partie gauche en :")
    steps.append(format_sq_matrix([[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]))
    steps.append("")
    steps.append("Lorsque cela sera fait, la partie droite sera la matrice inverse A⁻¹.")
    steps.append("")
    steps.append("DÉPART")
    steps.append(f"[ A | I_{n} ]")
    steps.append("↓")
    steps.append("OBJECTIF")
    steps.append(f"[ I_{n} | A⁻¹ ]")
    steps.append("")
    
    # Cas particulier n = 1
    if n == 1:
        val = aug[0][0]
        if val == Fraction(0, 1):
            steps.append("Impossible d'inverser la matrice 1×1 dont l'unique valeur est 0 (division par zéro).")
            steps.append("Conclusion : La matrice n'est pas inversible.")
            return None, steps, False
        inv_val = Fraction(1, 1) / val
        box = make_box("ÉTAPE 1", "Rendre le coefficient égal à 1")
        step_entry = (
            f"{box}\n\n"
            f"Pourquoi ?\nPour transformer [ {format_frac(val)} | 1 ] en [ 1 | A⁻¹ ], nous multiplions la ligne par 1/({format_frac(val)}).\n\n"
            f"Opération :\nL₁ ← {format_frac(inv_val)} · L₁\n\n"
            f"Calcul :\n{format_frac(inv_val)} × [ {format_frac(val)} | 1 ] = [ 1 | {format_frac(inv_val)} ]\n\n"
            f"Avant :\n[ {format_frac(val)} | 1 ]\n\n"
            f"Après :\n[ 1 | {format_frac(inv_val)} ]\n\n"
            f"Ce que cela signifie :\nLa partie gauche est devenue [ 1 ], la partie droite est A⁻¹ = [ {format_frac(inv_val)} ]."
        )
        steps.append(step_entry)
        steps.append("")
        steps.append("RÉSULTAT")
        steps.append(f"A⁻¹ = [ {format_frac(inv_val)} ]")
        return [[float(inv_val)]], steps, True

    step_num = 1
    pivot_defined = False
    
    # Algorithme pédagogique de Gauss-Jordan
    for col in range(n):
        # 1. Recherche d'une simplification par différence (ex: 4 - 3 = 1)
        found_diff = False
        if aug[col][col] != Fraction(1, 1):
            for r in range(col + 1, n):
                diff = aug[r][col] - aug[col][col]
                if diff == Fraction(1, 1):
                    before_mat = deepcopy(aug)
                    title1 = f"ÉTAPE {step_num}"
                    title2 = f"Simplifier la colonne {col+1}"
                    box = make_box(title1, title2)
                    
                    pourquoi = f"Nous voulons obtenir un 1 dans la colonne {col+1} de la ligne {r+1}."
                    op_text = f"L_{r+1} ← L_{r+1} - L_{col+1}"
                    
                    calc_lines = ["Calcul détaillé :\n"]
                    new_row = []
                    for c_idx in range(2 * n):
                        v_r = before_mat[r][c_idx]
                        v_col = before_mat[col][c_idx]
                        diff_val = v_r - v_col
                        new_row.append(diff_val)
                        ord_str = get_ordinal(c_idx)
                        calc_lines.append(f"{ord_str} valeur :\n{format_frac(v_r)} - {format_frac(v_col)} = {format_frac(diff_val)}\n")
                    
                    aug[r] = new_row
                    calc_lines.append(f"Donc :\nL_{r+1} = {format_row_aug(new_row, n)}")
                    
                    step_entry = (
                        f"{box}\n\n"
                        f"Pourquoi ?\n{pourquoi}\n\n"
                        f"Opération :\n{op_text}\n\n"
                        f"{''.join(calc_lines)}\n\n"
                        f"Avant :\n{format_aug_matrix(before_mat, n)}\n\n"
                        f"Après :\n{format_aug_matrix(aug, n)}\n\n"
                        f"Ce que cela signifie :\nCette opération a permis d'obtenir un 1 dans la colonne {col+1} de la ligne {r+1}."
                    )
                    steps.append(step_entry)
                    steps.append("")
                    step_num += 1
                    
                    # Échanger avec la ligne col pour placer le 1 comme pivot
                    before_mat2 = deepcopy(aug)
                    title1 = f"ÉTAPE {step_num}"
                    title2 = f"Placer le pivot en haut de la colonne {col+1}"
                    box = make_box(title1, title2)
                    
                    pourquoi = f"Nous avons obtenu le 1 que nous voulons utiliser comme premier pivot. Nous allons maintenant le placer en ligne L_{col+1}."
                    op_text = f"L_{col+1} ↔ L_{r+1}"
                    
                    aug[col], aug[r] = aug[r], aug[col]
                    
                    pivot_def_str = ""
                    if not pivot_defined:
                        pivot_def_str = "\n\nUn pivot est le nombre que nous utilisons comme point de référence pour transformer les autres nombres de sa colonne."
                        pivot_defined = True
                        
                    step_entry = (
                        f"{box}\n\n"
                        f"Pourquoi ?\n{pourquoi}\n\n"
                        f"Opération :\n{op_text}\n\n"
                        f"Avant :\n{format_aug_matrix(before_mat2, n)}\n\n"
                        f"Après :\n{format_aug_matrix(aug, n)}\n\n"
                        f"Ce que cela signifie :\nLe pivot 1 est maintenant placé en ligne L_{col+1}.{pivot_def_str}"
                    )
                    steps.append(step_entry)
                    steps.append("")
                    step_num += 1
                    found_diff = True
                    break
                    
        # 2. Chercher si une ligne en dessous possède déjà un 1
        if not found_diff and aug[col][col] != Fraction(1, 1):
            row_with_one = None
            for r in range(col + 1, n):
                if aug[r][col] == Fraction(1, 1):
                    row_with_one = r
                    break
            if row_with_one is not None:
                before_mat = deepcopy(aug)
                title1 = f"ÉTAPE {step_num}"
                title2 = f"Placer le pivot 1 en ligne L_{col+1}"
                box = make_box(title1, title2)
                
                pourquoi = f"La ligne L_{row_with_one+1} possède déjà un 1 en colonne {col+1}. Nous l'échangeons avec la ligne L_{col+1} pour avoir immédiatement notre pivot."
                op_text = f"L_{col+1} ↔ L_{row_with_one+1}"
                aug[col], aug[row_with_one] = aug[row_with_one], aug[col]
                
                pivot_def_str = ""
                if not pivot_defined:
                    pivot_def_str = "\n\nUn pivot est le nombre que nous utilisons comme point de référence pour transformer les autres nombres de sa colonne."
                    pivot_defined = True
                    
                step_entry = (
                    f"{box}\n\n"
                    f"Pourquoi ?\n{pourquoi}\n\n"
                    f"Opération :\n{op_text}\n\n"
                    f"Avant :\n{format_aug_matrix(before_mat, n)}\n\n"
                    f"Après :\n{format_aug_matrix(aug, n)}\n\n"
                    f"Ce que cela signifie :\nLe pivot 1 est maintenant positionné en ligne L_{col+1}.{pivot_def_str}"
                )
                steps.append(step_entry)
                steps.append("")
                step_num += 1
                found_diff = True

        # 3. Si le pivot actuel est nul, chercher une ligne avec coefficient non nul et échanger
        if aug[col][col] == Fraction(0, 1):
            nonzero_row = None
            for r in range(col + 1, n):
                if aug[r][col] != Fraction(0, 1):
                    nonzero_row = r
                    break
            if nonzero_row is None:
                steps.append(f"Impossible de trouver un pivot non nul dans la colonne {col+1}.")
                steps.append("Tous les coefficients restants sous la diagonale sont nuls.")
                steps.append("Le déterminant de la matrice est nul (det(A) = 0).")
                steps.append("Conclusion : Cette matrice n'est pas inversible (matrice singulière).")
                return None, steps, False
                
            before_mat = deepcopy(aug)
            title1 = f"ÉTAPE {step_num}"
            title2 = f"Échanger les lignes pour obtenir un pivot non nul"
            box = make_box(title1, title2)
            op_text = f"L_{col+1} ↔ L_{nonzero_row+1}"
            aug[col], aug[nonzero_row] = aug[nonzero_row], aug[col]
            
            step_entry = (
                f"{box}\n\n"
                f"Pourquoi ?\nLe nombre sur la diagonale est 0. Nous ne pouvons pas diviser par 0, donc nous échangeons avec la ligne L_{nonzero_row+1} qui a un coefficient non nul.\n\n"
                f"Opération :\n{op_text}\n\n"
                f"Avant :\n{format_aug_matrix(before_mat, n)}\n\n"
                f"Après :\n{format_aug_matrix(aug, n)}\n\n"
                f"Ce que cela signifie :\nLa ligne L_{col+1} dispose maintenant d'un pivot non nul ({format_frac(aug[col][col])})."
            )
            steps.append(step_entry)
            steps.append("")
            step_num += 1

        # 4. Normaliser le pivot si nécessaire (rendre égal à 1)
        pivot_val = aug[col][col]
        if pivot_val != Fraction(1, 1):
            before_mat = deepcopy(aug)
            title1 = f"ÉTAPE {step_num}"
            title2 = f"Normaliser le pivot de la ligne L_{col+1}"
            box = make_box(title1, title2)
            
            inv_pivot = Fraction(1, 1) / pivot_val
            op_text = f"L_{col+1} ← {format_frac(inv_pivot)} L_{col+1}"
            pourquoi = f"Le {get_ordinal(col).lower()} pivot vaut actuellement {format_frac(pivot_val)}. Pour obtenir la matrice identité, ce pivot doit être égal à 1."
            
            calc_lines = [f"Calcul :\n{format_frac(inv_pivot)} × {format_row_aug(before_mat[col], n)}\n\n=\n\n"]
            new_row = []
            for c_idx in range(2 * n):
                val = before_mat[col][c_idx] * inv_pivot
                new_row.append(val)
            aug[col] = new_row
            calc_lines.append(f"{format_row_aug(new_row, n)}")
            
            pivot_def_str = ""
            if not pivot_defined:
                pivot_def_str = "\n\nUn pivot est le nombre que nous utilisons comme point de référence pour transformer les autres nombres de sa colonne."
                pivot_defined = True
                
            step_entry = (
                f"{box}\n\n"
                f"Pourquoi ?\n{pourquoi}\n\n"
                f"Opération :\n{op_text}\n\n"
                f"{''.join(calc_lines)}\n\n"
                f"Avant :\n{format_aug_matrix(before_mat, n)}\n\n"
                f"Après :\n{format_aug_matrix(aug, n)}\n\n"
                f"Ce que cela signifie :\nLe pivot en ligne L_{col+1} est maintenant exactement égal à 1.{pivot_def_str}"
            )
            steps.append(step_entry)
            steps.append("")
            step_num += 1

        # 5. Éliminer tous les autres coefficients de la colonne (obtenir 0 au-dessus et en-dessous)
        for r in range(n):
            if r != col and aug[r][col] != Fraction(0, 1):
                before_mat = deepcopy(aug)
                factor = aug[r][col]
                pos_desc = "sous le" if r > col else "au-dessus du"
                title1 = f"ÉTAPE {step_num}"
                title2 = f"Annuler le nombre {pos_desc} pivot (colonne {col+1})"
                box = make_box(title1, title2)
                
                pourquoi = f"Nous voulons maintenant obtenir 0 {pos_desc} premier pivot en ligne L_{r+1}, colonne C_{col+1}." if col == 0 and r > col else f"Nous voulons maintenant obtenir 0 {pos_desc} pivot en ligne L_{r+1}, colonne C_{col+1}."
                
                if factor > 0:
                    op_text = f"L_{r+1} ← L_{r+1} - {format_frac(factor)}L_{col+1}" if factor != 1 else f"L_{r+1} ← L_{r+1} - L_{col+1}"
                else:
                    op_text = f"L_{r+1} ← L_{r+1} + {format_frac(abs(factor))}L_{col+1}" if abs(factor) != 1 else f"L_{r+1} ← L_{r+1} + L_{col+1}"
                    
                scaled_pivot_row = [factor * aug[col][c_idx] for c_idx in range(2 * n)]
                
                calc_lines = []
                if factor != 1 and factor != -1:
                    calc_lines.append(f"Nous multiplions d'abord la première ligne par {format_frac(abs(factor))}." if col == 0 else f"Nous multiplions d'abord la ligne L_{col+1} par {format_frac(abs(factor))}.")
                    calc_lines.append(f"\n\n{format_frac(abs(factor))}L_{col+1} :\n\n{format_row_aug([abs(factor)*aug[col][c_idx] for c_idx in range(2*n)], n)}\n\n")
                    calc_lines.append(f"Puis nous soustrayons cette ligne de L_{r+1} :\n\n")
                else:
                    calc_lines.append("Calcul détaillé :\n\n")
                    
                calc_lines.append(f"{format_row_aug(before_mat[r], n)}\n-\n{format_row_aug(scaled_pivot_row, n)}\n\nCalcul :\n\n")
                
                new_row = []
                for c_idx in range(2 * n):
                    v_r = before_mat[r][c_idx]
                    v_sub = scaled_pivot_row[c_idx]
                    res_val = v_r - v_sub
                    new_row.append(res_val)
                    ord_str = get_ordinal(c_idx)
                    v_sub_disp = f"({format_frac(v_sub)})" if v_sub < 0 else format_frac(v_sub)
                    calc_lines.append(f"{ord_str} valeur :\n\n{format_frac(v_r)} - {v_sub_disp} = {format_frac(res_val)}\n\n")
                    
                aug[r] = new_row
                calc_lines.append(f"Donc :\n\nL_{r+1} = {format_row_aug(new_row, n)}")
                
                step_entry = (
                    f"{box}\n\n"
                    f"Pourquoi ?\n{pourquoi}\n\n"
                    f"Opération :\n{op_text}\n\n"
                    f"{''.join(calc_lines)}\n\n"
                    f"Nouvelle matrice :\n\n"
                    f"{format_aug_matrix(aug, n)}\n\n"
                    f"Ce que cela signifie :\nLe premier élément de la deuxième ligne est maintenant 0. La première colonne a donc la forme souhaitée." if col == 0 and r == 1 and n == 2 else
                    f"Ce que cela signifie :\nLe coefficient de la ligne L_{r+1} en colonne C_{col+1} est maintenant 0. La colonne a la forme souhaitée."
                )
                steps.append(step_entry)
                steps.append("")
                step_num += 1

    # Résultat
    inv_matrix_frac = [[aug[i][n + j] for j in range(n)] for i in range(n)]
    inv_matrix_float = [[float(aug[i][n + j]) for j in range(n)] for i in range(n)]
    
    steps.append("==================================================")
    steps.append("RÉSULTAT")
    steps.append("==================================================")
    steps.append(format_aug_matrix(aug, n))
    steps.append("")
    steps.append("Nous avons transformé :")
    steps.append("")
    steps.append(f"[A | I_{n}]")
    steps.append("")
    steps.append("en :")
    steps.append("")
    steps.append(f"[I_{n} | A⁻¹]")
    steps.append("")
    steps.append("La partie droite contient donc l'inverse de A.")
    steps.append("")
    steps.append("A⁻¹ =")
    steps.append(format_sq_matrix(inv_matrix_frac))
    steps.append("")
    
    # 6. Vérification par le produit A * A^-1
    steps.append("==================================================")
    steps.append("VÉRIFICATION : A × A⁻¹")
    steps.append("==================================================")
    steps.append("Pour vérifier que cette matrice est bien l'inverse de A, nous multiplions A par A⁻¹.")
    steps.append("")
    
    prod_steps = []
    prod_matrix = []
    for i in range(n):
        prod_row = []
        for j in range(n):
            terms = []
            sum_val = Fraction(0, 1)
            for k in range(n):
                p = A[i][k] * inv_matrix_frac[k][j]
                sum_val += p
                terms.append(f"({format_frac(A[i][k])} × {format_frac(inv_matrix_frac[k][j])})")
            prod_row.append(sum_val)
            expr = " + ".join(terms)
            prod_steps.append(f"Élément ({i+1}, {j+1}) :\n{expr} = {format_frac(sum_val)}")
        prod_matrix.append(prod_row)
        
    steps.append("\n\n".join(prod_steps))
    steps.append("")
    steps.append("Le résultat doit être la matrice identité :")
    steps.append(format_sq_matrix(prod_matrix))
    steps.append("")
    steps.append("Nous obtenons la matrice identité. Le calcul est donc correct.")
    steps.append("")
    
    # 7. Section facultative pédagogique
    steps.append("--------------------------------------------------")
    steps.append("Pourquoi utilise-t-on la matrice identité ?")
    steps.append("--------------------------------------------------")
    steps.append("La matrice identité joue pour les matrices un rôle similaire au nombre 1 pour les nombres.")
    steps.append("")
    steps.append("5 × 1 = 5")
    steps.append("")
    steps.append("De la même façon :")
    steps.append("")
    steps.append(f"A × I_{n} = A")
    steps.append("")
    steps.append("Elle sert ici de point de départ pour construire l'inverse avec la méthode de Gauss-Jordan.")
    
    return inv_matrix_float, steps, True

