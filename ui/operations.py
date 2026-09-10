"""
Module d'affichage pour les opérations matricielles (A+B, A-B, A*B, A^T).
"""

import customtkinter as ctk
from ui.matrix_input import MatrixInput
from core.matrix_operations import matrix_add, matrix_subtract, matrix_multiply, transpose
from utils.formatter import format_matrix_str
from utils.storage import save_history_item

class OperationsPage(ctk.CTkFrame):
    def __init__(self, master, initial_tab: str = "add", **kwargs):
        super().__init__(master, **kwargs)
        
        title_label = ctk.CTkLabel(self, text="Opérations Matricielles", font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Selector tabs
        self.tab_menu = ctk.CTkSegmentedButton(
            self,
            values=["Addition (A+B)", "Soustraction (A-B)", "Multiplication (A×B)", "Transposée (Aᵀ)"],
            command=self.on_tab_changed
        )
        self.tab_menu.pack(fill="x", padx=20, pady=5)
        
        # Content frame
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Set initial tab
        if initial_tab == "add":
            self.tab_menu.set("Addition (A+B)")
        elif initial_tab == "subtract":
            self.tab_menu.set("Soustraction (A-B)")
        elif initial_tab == "multiply":
            self.tab_menu.set("Multiplication (A×B)")
        else:
            self.tab_menu.set("Transposée (Aᵀ)")
            
        self.render_view()

    def on_tab_changed(self, value):
        self.render_view()

    def render_view(self):
        for child in self.content_frame.winfo_children():
            child.destroy()
            
        mode = self.tab_menu.get()
        
        if "Transposée" in mode:
            # Single matrix input
            self.mat_a = MatrixInput(self.content_frame, title="Matrice A")
            self.mat_a.pack(fill="x", pady=10)
            
            btn = ctk.CTkButton(
                self.content_frame, text="Calculer la Transposée (Aᵀ)",
                command=self.calculate_transpose, fg_color="#2563EB", height=38, font=ctk.CTkFont(weight="bold")
            )
            btn.pack(fill="x", pady=10)
            
        else:
            # Dual matrix inputs
            grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            grid.pack(fill="x", pady=10)
            grid.columnconfigure(0, weight=1)
            grid.columnconfigure(1, weight=1)
            
            self.mat_a = MatrixInput(grid, title="Matrice A", default_rows=2, default_cols=3 if "Multiplication" in mode else 2)
            self.mat_a.grid(row=0, column=0, padx=5, sticky="nsew")
            
            self.mat_b = MatrixInput(grid, title="Matrice B", default_rows=3 if "Multiplication" in mode else 2, default_cols=2)
            self.mat_b.grid(row=0, column=1, padx=5, sticky="nsew")
            
            btn_text = f"Calculer {mode}"
            btn = ctk.CTkButton(
                self.content_frame, text=btn_text,
                command=self.calculate_binary, fg_color="#2563EB", height=38, font=ctk.CTkFont(weight="bold")
            )
            btn.pack(fill="x", pady=10)
            
        # Result output frame
        self.result_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.result_frame.pack(fill="both", expand=True, pady=10)
        
        self.result_label = ctk.CTkLabel(self.result_frame, text="Le résultat s'affichera ici...", font=ctk.CTkFont(size=14))
        self.result_label.pack(padx=15, pady=15)

    def calculate_binary(self):
        try:
            A = self.mat_a.get_matrix_values()
            B = self.mat_b.get_matrix_values()
            mode = self.tab_menu.get()
            
            if "Addition" in mode:
                res, steps = matrix_add(A, B)
                op_name = "Addition (A + B)"
            elif "Soustraction" in mode:
                res, steps = matrix_subtract(A, B)
                op_name = "Soustraction (A - B)"
            else:
                res, steps = matrix_multiply(A, B)
                op_name = "Multiplication (A × B)"
                
            save_history_item(op_name, {"A": A, "B": B}, res, steps)
            self.show_result(op_name, res, steps)
            
        except Exception as e:
            self.show_error(str(e))

    def calculate_transpose(self):
        try:
            A = self.mat_a.get_matrix_values()
            res, steps = transpose(A)
            save_history_item("Transposée (Aᵀ)", {"A": A}, res, steps)
            self.show_result("Transposée Aᵀ", res, steps)
        except Exception as e:
            self.show_error(str(e))

    def show_result(self, title: str, matrix: list, steps: list):
        for child in self.result_frame.winfo_children():
            child.destroy()
            
        ctk.CTkLabel(self.result_frame, text=f"Résultat : {title}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#10B981").pack(anchor="w", padx=15, pady=(15, 5))
        
        # Display formatted matrix
        mat_str = format_matrix_str(matrix)
        textbox = ctk.CTkTextbox(self.result_frame, height=100, font=ctk.CTkFont(family="monospace", size=13))
        textbox.pack(fill="x", padx=15, pady=5)
        textbox.insert("1.0", mat_str)
        textbox.configure(state="disabled")
        
        # Steps
        ctk.CTkLabel(self.result_frame, text="Étapes du calcul :", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        steps_box = ctk.CTkTextbox(self.result_frame, height=150, font=ctk.CTkFont(family="monospace", size=12))
        steps_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        steps_box.insert("1.0", "\n".join(steps))
        steps_box.configure(state="disabled")

    def show_error(self, message: str):
        for child in self.result_frame.winfo_children():
            child.destroy()
        ctk.CTkLabel(self.result_frame, text="Erreur :", font=ctk.CTkFont(size=16, weight="bold"), text_color="#EF4444").pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(self.result_frame, text=message, font=ctk.CTkFont(size=13), text_color="#EF4444", wraplength=600, justify="left").pack(anchor="w", padx=15, pady=(0, 15))
