"""
Module d'interface pour le solveur de systèmes d'équations, déterminant, inverse et formes échelonnées.
"""

import customtkinter as ctk
from ui.matrix_input import MatrixInput
from core.determinant import determinant
from core.inverse import inverse
from core.gaussian import row_echelon, rref
from core.matrix_operations import identity_matrix
from core.solver import solve_system
from utils.formatter import format_matrix_str, format_number
from utils.storage import save_history_item

class SingleMatrixPage(ctk.CTkFrame):
    """Page réutilisable pour Déterminant et Inverse."""
    def __init__(self, master, mode: str = "determinant", **kwargs):
        super().__init__(master, **kwargs)
        self.mode = mode
        
        titles = {
            "determinant": "Calcul du Déterminant Det(A)",
            "inverse": "Calcul de la Matrice Inverse (A⁻¹)"
        }
        
        ctk.CTkLabel(self, text=titles.get(mode, "Calcul Matriciel"), font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))
        
        self.content = ctk.CTkScrollableFrame(self)
        self.content.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.mat_input = MatrixInput(self.content, title="Matrice A", default_rows=3, default_cols=3)
        self.mat_input.pack(fill="x", pady=10)
        
        if mode == "determinant":
            btn_text = "Calculer le Déterminant Det(A)"
        else:
            btn_text = "Calculer l'Inverse A⁻¹"
            
        ctk.CTkButton(self.content, text=btn_text, command=lambda: self.calculate(mode), fg_color="#2563EB", height=38, font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=10)
            
        self.result_frame = ctk.CTkFrame(self.content, corner_radius=10)
        self.result_frame.pack(fill="both", expand=True, pady=10)
        self.clear_results()

    def clear_results(self):
        for child in self.result_frame.winfo_children():
            child.destroy()
        ctk.CTkLabel(self.result_frame, text="Le résultat s'affichera ici...").pack(padx=15, pady=15)

    def calculate(self, calc_type: str):
        self.clear_results()
        try:
            A = self.mat_input.get_matrix_values()
            
            if calc_type == "determinant":
                det_val, steps = determinant(A)
                save_history_item("Déterminant Det(A)", {"A": A}, det_val, steps)
                self.show_single_val("Déterminant Det(A)", f"Det(A) = {format_number(det_val)}", steps)
                
            elif calc_type == "inverse":
                inv, steps, is_inv = inverse(A)
                save_history_item("Matrice Inverse A⁻¹", {"A": A}, inv, steps)
                if not is_inv:
                    self.show_error("Cette matrice n'est pas inversible (Déterminant nul).")
                else:
                    self.show_matrix_val("Matrice Inverse A⁻¹", inv, steps)
                    
            elif calc_type == "identity":
                n = len(A)
                I_mat, steps = identity_matrix(n)
                save_history_item(f"Matrice Identité (I_{n})", {"n": n}, I_mat, steps)
                self.show_matrix_val(f"Matrice Identité I_{n}", I_mat, steps)
                
        except Exception as e:
            self.show_error(str(e))

    def show_single_val(self, title: str, main_val: str, steps: list):
        for child in self.result_frame.winfo_children():
            child.destroy()
        ctk.CTkLabel(self.result_frame, text=title, font=ctk.CTkFont(size=16, weight="bold"), text_color="#10B981").pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(self.result_frame, text=main_val, font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=15, pady=10)
        
        ctk.CTkLabel(self.result_frame, text="Étapes :", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        box = ctk.CTkTextbox(self.result_frame, height=180, font=ctk.CTkFont(family="monospace", size=12))
        box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        box.insert("1.0", "\n".join(steps))
        box.configure(state="disabled")

    def show_matrix_val(self, title: str, matrix: list, steps: list):
        for child in self.result_frame.winfo_children():
            child.destroy()
        ctk.CTkLabel(self.result_frame, text=title, font=ctk.CTkFont(size=16, weight="bold"), text_color="#10B981").pack(anchor="w", padx=15, pady=(15, 5))
        
        mat_str = format_matrix_str(matrix)
        textbox = ctk.CTkTextbox(self.result_frame, height=120, font=ctk.CTkFont(family="monospace", size=13))
        textbox.pack(fill="x", padx=15, pady=5)
        textbox.insert("1.0", mat_str)
        textbox.configure(state="disabled")
        
        ctk.CTkLabel(self.result_frame, text="Étapes détaillées :", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        box = ctk.CTkTextbox(self.result_frame, height=200, font=ctk.CTkFont(family="monospace", size=12))
        box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        box.insert("1.0", "\n".join(steps) if isinstance(steps[0], str) else "\n".join(str(s) for s in steps))
        box.configure(state="disabled")

    def show_error(self, message: str):
        for child in self.result_frame.winfo_children():
            child.destroy()
        ctk.CTkLabel(self.result_frame, text="Erreur :", font=ctk.CTkFont(size=16, weight="bold"), text_color="#EF4444").pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(self.result_frame, text=message, font=ctk.CTkFont(size=13), text_color="#EF4444", wraplength=600, justify="left").pack(anchor="w", padx=15, pady=(0, 15))


class SystemSolverPage(ctk.CTkFrame):
    """Page de résolution de systèmes d'équations linéaires AX = B."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        ctk.CTkLabel(self, text="Solveur de Systèmes d'Équations Linéaires", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))
        
        self.content = ctk.CTkScrollableFrame(self)
        self.content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Dimensions selector
        dim_frame = ctk.CTkFrame(self.content)
        dim_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(dim_frame, text="Nombre d'inconnues / équations :", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=10)
        self.size_var = ctk.StringVar(value="3")
        self.size_menu = ctk.CTkOptionMenu(dim_frame, values=["2", "3", "4", "5"], variable=self.size_var, command=self.generate_system_grid, width=70)
        self.size_menu.pack(side="left", padx=10, pady=10)
        
        self.grid_frame = ctk.CTkFrame(self.content)
        self.grid_frame.pack(fill="x", pady=10)
        
        btn_solve = ctk.CTkButton(self.content, text="Résoudre par la Méthode de Gauss-Jordan", command=self.solve, fg_color="#2563EB", height=38, font=ctk.CTkFont(weight="bold"))
        btn_solve.pack(fill="x", pady=10)
        
        self.result_frame = ctk.CTkFrame(self.content, corner_radius=10)
        self.result_frame.pack(fill="both", expand=True, pady=10)
        
        self.entries_a = []
        self.entries_b = []
        self.generate_system_grid("3")

    def generate_system_grid(self, size_str: str):
        for child in self.grid_frame.winfo_children():
            child.destroy()
            
        n = int(size_str)
        var_names = ["x", "y", "z", "t", "w"][:n]
        
        self.entries_a = []
        self.entries_b = []
        
        for i in range(n):
            row_frame = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(row_frame, text=f"Éq {i+1} :", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))
            
            row_a = []
            for j in range(n):
                entry_a = ctk.CTkEntry(row_frame, width=50, justify="center", placeholder_text="1" if i==j else "0")
                entry_a.pack(side="left", padx=2)
                row_a.append(entry_a)
                
                var_label = f"{var_names[j]} +" if j < n-1 else f"{var_names[j]} ="
                ctk.CTkLabel(row_frame, text=var_label).pack(side="left", padx=2)
                
            self.entries_a.append(row_a)
            
            entry_b = ctk.CTkEntry(row_frame, width=60, justify="center", placeholder_text="0")
            entry_b.pack(side="left", padx=(5, 0))
            self.entries_b.append(entry_b)

    def solve(self):
        try:
            n = int(self.size_var.get())
            A = []
            B = []
            
            for i in range(n):
                row_a = []
                for j in range(n):
                    val_str = self.entries_a[i][j].get().strip().replace(',', '.')
                    row_a.append(float(val_str) if val_str else 0.0)
                A.append(row_a)
                
                b_str = self.entries_b[i].get().strip().replace(',', '.')
                B.append(float(b_str) if b_str else 0.0)
                
            sol_type, vec, aug_final, steps, explanation = solve_system(A, B)
            save_history_item("Résolution Système AX = B", {"A": A, "B": B}, {"type": sol_type, "vector": vec}, [s["description"] for s in steps])
            
            self.show_system_result(sol_type, vec, steps, explanation, n)
            
        except Exception as e:
            self.show_error(str(e))

    def show_system_result(self, sol_type: str, vec: list, steps: list, explanation: str, n: int):
        for child in self.result_frame.winfo_children():
            child.destroy()
            
        colors = {"UNIQUE": "#10B981", "INFINITE": "#F59E0B", "NONE": "#EF4444"}
        color = colors.get(sol_type, "#2563EB")
        
        ctk.CTkLabel(self.result_frame, text="Résultat de la Résolution :", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(self.result_frame, text=explanation, font=ctk.CTkFont(size=15, weight="bold"), text_color=color, wraplength=600, justify="left").pack(anchor="w", padx=15, pady=5)
        
        if sol_type == "UNIQUE" and vec:
            var_names = ["x", "y", "z", "t", "w"][:n]
            sol_box = ctk.CTkFrame(self.result_frame, fg_color="#1E293B" if ctk.get_appearance_mode() == "Dark" else "#F1F5F9")
            sol_box.pack(fill="x", padx=15, pady=10)
            
            for var, val in zip(var_names, vec):
                ctk.CTkLabel(sol_box, text=f"{var} = {format_number(val)}", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, pady=10)
                
        # Resolution steps
        ctk.CTkLabel(self.result_frame, text="Étapes d'Élimination de Gauss-Jordan :", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        
        steps_box = ctk.CTkTextbox(self.result_frame, height=220, font=ctk.CTkFont(family="monospace", size=12))
        steps_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        step_str_lines = []
        for s in steps:
            step_str_lines.append(f"Étape {s['step']} : {s['operation']}")
            step_str_lines.append(s['description'])
            if 'formatted' in s:
                step_str_lines.append(s['formatted'])
            step_str_lines.append("-" * 40)
            
        steps_box.insert("1.0", "\n".join(step_str_lines))
        steps_box.configure(state="disabled")

    def show_error(self, message: str):
        for child in self.result_frame.winfo_children():
            child.destroy()
        ctk.CTkLabel(self.result_frame, text="Erreur :", font=ctk.CTkFont(size=16, weight="bold"), text_color="#EF4444").pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(self.result_frame, text=message, font=ctk.CTkFont(size=13), text_color="#EF4444", wraplength=600, justify="left").pack(anchor="w", padx=15, pady=(0, 15))
