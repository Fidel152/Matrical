"""
Page de guide pédagogique et aide théorique sur les matrices.
"""

import customtkinter as ctk

class HelpPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        ctk.CTkLabel(self, text="Guide Pédagogique & Aide Théorique", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))
        
        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        sections = [
            ("1. Qu'est-ce qu'une matrice ?",
             "Une matrice de dimension m × n est un tableau rectangulaire de nombres disposés en m lignes et n colonnes.\n"
             "Exemple d'une matrice 2 × 3 :\n"
             "[ 1   2   3 ]\n"
             "[ 4   5   6 ]"),
             
            ("2. Addition et Soustraction",
             "Deux matrices ne peuvent être additionnées ou soustraites que si elles ont EXACTEMENT les mêmes dimensions (m × n).\n"
             "L'opération s'effectue élément par élément :\n"
             "C[i][j] = A[i][j] + B[i][j]\n"
             "C[i][j] = A[i][j] - B[i][j]"),
             
            ("3. Multiplication Matricielle (A × B)",
             "La multiplication A × B n'est possible que si le nombre de COLONNES de A est égal au nombre de LIGNES de B.\n"
             "Si A est de taille (m × p) et B de taille (p × n), le résultat C sera de taille (m × n).\n"
             "Calcul du terme C[i][j] : Produit scalaire de la ligne i de A et de la colonne j de B :\n"
             "C[i][j] = A[i][0]·B[0][j] + A[i][1]·B[1][j] + ... + A[i][p-1]·B[p-1][j]"),
             
            ("4. Transposée d'une matrice (Aᵀ)",
             "La transposée consiste à échanger les lignes et les colonnes d'une matrice.\n"
             "Aᵀ[j][i] = A[i][j]. Une matrice (m × n) devient une matrice (n × m)."),
             
            ("5. Déterminant Det(A)",
             "Le déterminant est un nombre associé à une matrice CARRÉE (n × n).\n"
             "- Pour 2 × 2 : det([a b | c d]) = a·d - b·c.\n"
             "- Pour n × n : On applique l'élimination de Gauss pour réduire la matrice en forme triangulaire supérieure.\n"
             "Le déterminant est alors égal au produit des éléments diagonaux (corrigé du signe selon les échanges de lignes)."),
             
            ("6. Matrice Inverse (A⁻¹)",
             "Une matrice carrée A est inversible si et seulement si son déterminant est NON NUL (det(A) ≠ 0).\n"
             "Propriété : A · A⁻¹ = A⁻¹ · A = I (Matrice Identité).\n"
             "Méthode de Gauss-Jordan : On forme la matrice augmentée [A | I] et on applique des opérations sur les lignes jusqu'à obtenir [I | A⁻¹]."),
             
            ("7. Opérations Élémentaires sur les Lignes",
             "Les 3 opérations autorisées sur les lignes d'une matrice sont :\n"
             "• E1 : Échanger deux lignes (Li ↔ Lj)\n"
             "• E2 : Multiplier une ligne par un nombre non nul (Li ← k·Li)\n"
             "• E3 : Ajouter à une ligne un multiple d'une autre ligne (Li ← Li + k·Lj)"),
             
            ("8. Formes Échelonnées (REF et RREF)",
             "• Forme Échelonnée (REF) : Tous les éléments sous les pivots sont nuls.\n"
             "• Forme Échelonnée Réduite (RREF) : Les pivots valent 1 et sont les seuls éléments non nuls de leur colonne."),
             
            ("9. Systèmes d'Équations Linéaires (AX = B)",
             "Un système linéaire peut s'écrire sous forme matricielle A X = B.\n"
             "En appliquant la méthode de Gauss-Jordan sur la matrice augmentée [A | B], on distingue 3 cas :\n"
             "1. Solution unique : Rang(A) = nombre d'inconnues.\n"
             "2. Infinité de solutions : Le système est compatible mais comporte des variables libres.\n"
             "3. Aucune solution : Une ligne absurde de la forme [0 0 ... 0 | k] avec k ≠ 0 est obtenue.")
        ]
        
        for title, content in sections:
            card = ctk.CTkFrame(scroll, corner_radius=10, border_width=1, border_color="#3B82F6")
            card.pack(fill="x", pady=8, padx=5)
            
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold"), text_color="#2563EB").pack(anchor="w", padx=15, pady=(15, 5))
            ctk.CTkLabel(card, text=content, font=ctk.CTkFont(size=13), justify="left", wraplength=650).pack(anchor="w", padx=15, pady=(0, 15))
