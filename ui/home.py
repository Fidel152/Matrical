"""
Page d'accueil de l'application MATRICAL avec cartes raccourcis.
"""

import customtkinter as ctk

class HomePage(ctk.CTkFrame):
    def __init__(self, master, navigate_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.navigate_callback = navigate_callback
        
        # En-tête principal
        title_label = ctk.CTkLabel(
            self, text="MATRICAL", font=ctk.CTkFont(size=28, weight="bold"), text_color="#2563EB"
        )
        title_label.pack(anchor="w", padx=30, pady=(30, 5))
        
        subtitle_label = ctk.CTkLabel(
            self, text="Calculatrice matricielle & solveur de systèmes d'équations",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        subtitle_label.pack(anchor="w", padx=30, pady=(0, 10))
        
        desc_label = ctk.CTkLabel(
            self,
            text="Effectuez des opérations matricielles et résolvez des systèmes d'équations linéaires étape par étape avec des explications algorithmiques détaillées.",
            font=ctk.CTkFont(size=13),
            wraplength=700,
            justify="left"
        )
        desc_label.pack(anchor="w", padx=30, pady=(0, 25))
        
        # Grille de cartes de fonctionnalités
        cards_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        cards_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        features = [
            ("Addition & Soustraction", "Additionnez ou soustrayez deux matrices de mêmes dimensions.", "operations", "add"),
            ("Multiplication", "Multipliez deux matrices compatibles (colonnes A = lignes B).", "operations", "multiply"),
            ("Transposée", "Intervertissez les lignes et colonnes d'une matrice.", "operations", "transpose"),
            ("Déterminant", "Calculez le déterminant d'une matrice carrée par élimination.", "determinant", None),
            ("Matrice Inverse", "Calculez l'inverse A⁻¹ par la méthode de Gauss-Jordan [A|I].", "inverse", None),
            ("Système d'Équations", "Résolvez AX = B et détectez l'unicité ou l'incompatibilité.", "solver", None),
            ("Guide & Aide", "Consultez les explications théoriques et les définitions mathématiques.", "help", None),
        ]
        
        grid_cols = 2
        for idx, (title, desc, page_id, sub_tab) in enumerate(features):
            row = idx // grid_cols
            col = idx % grid_cols
            
            card = ctk.CTkFrame(cards_frame, corner_radius=12, border_width=1, border_color="#3B82F6")
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))
            ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=12), wraplength=280, justify="left").pack(anchor="w", padx=15, pady=(0, 15))
            
            btn = ctk.CTkButton(
                card, text="Accéder →",
                command=lambda p=page_id, s=sub_tab: self.navigate_callback(p, s),
                fg_color="#2563EB", hover_color="#1D4ED8", width=100
            )
            btn.pack(anchor="e", padx=15, pady=(0, 15))
            
        for i in range(grid_cols):
            cards_frame.columnconfigure(i, weight=1)
