"""
Composant réutilisable CustomTkinter de saisie de matrice.
Génère une grille dynamique de champs numériques selon les dimensions demandées.
"""

import customtkinter as ctk
from typing import List, Optional

class MatrixInput(ctk.CTkFrame):
    def __init__(self, master, title: str = "Matrice", default_rows: int = 2, default_cols: int = 2, **kwargs):
        super().__init__(master, **kwargs)
        self.title = title
        self.entries: List[List[ctk.CTkEntry]] = []
        
        # En-tête
        self.header_label = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        self.header_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Contrôles de dimensions
        dim_frame = ctk.CTkFrame(self, fg_color="transparent")
        dim_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(dim_frame, text="Lignes:").pack(side="left", padx=(0, 5))
        self.rows_spin = ctk.CTkOptionMenu(dim_frame, values=["1", "2", "3", "4", "5", "6"], width=60)
        self.rows_spin.set(str(default_rows))
        self.rows_spin.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(dim_frame, text="Colonnes:").pack(side="left", padx=(0, 5))
        self.cols_spin = ctk.CTkOptionMenu(dim_frame, values=["1", "2", "3", "4", "5", "6"], width=60)
        self.cols_spin.set(str(default_cols))
        self.cols_spin.pack(side="left", padx=(0, 15))
        
        self.btn_generate = ctk.CTkButton(
            dim_frame, text="Générer la grille", command=self.generate_grid, width=120, fg_color="#2563EB", hover_color="#1D4ED8"
        )
        self.btn_generate.pack(side="left")
        
        # Zone de grille
        self.grid_frame = ctk.CTkScrollableFrame(self, height=180)
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.generate_grid()

    def generate_grid(self):
        """Génère dynamiquement les champs d'entrée selon les dimensions sélectionnées."""
        for child in self.grid_frame.winfo_children():
            child.destroy()
            
        self.entries = []
        rows = int(self.rows_spin.get())
        cols = int(self.cols_spin.get())
        
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ctk.CTkEntry(self.grid_frame, width=65, justify="center", placeholder_text="0")
                entry.grid(row=i, column=j, padx=4, pady=4)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def get_matrix_values(self) -> List[List[float]]:
        """Extrait et valide les valeurs saisies dans la grille."""
        matrix = []
        for i, row in enumerate(self.entries):
            matrix_row = []
            for j, entry in enumerate(row):
                val_str = entry.get().strip().replace(',', '.')
                if not val_str:
                    val_str = "0"
                try:
                    val = float(val_str)
                    matrix_row.append(val)
                except ValueError:
                    raise ValueError(f"Valeur non numérique '{entry.get()}' à la position ({i+1}, {j+1}) dans {self.title}.")
            matrix.append(matrix_row)
        return matrix

    def set_matrix_values(self, matrix: List[List[float]]):
        """Remplit la grille avec les valeurs fournies."""
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0
        
        self.rows_spin.set(str(rows))
        self.cols_spin.set(str(cols))
        self.generate_grid()
        
        for i in range(rows):
            for j in range(cols):
                self.entries[i][j].delete(0, "end")
                self.entries[i][j].insert(0, str(matrix[i][j]))
