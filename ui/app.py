"""
Application principale CustomTkinter MATRICAL.
Contient la barre latérale de navigation, la gestion des vues et le basculement de thème.
"""

import customtkinter as ctk
from ui.home import HomePage
from ui.operations import OperationsPage
from ui.solver_ui import SingleMatrixPage, SystemSolverPage
from ui.history import HistoryPage
from ui.help import HelpPage

# Configuration du thème CustomTkinter par défaut
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MatrixCalcApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("MATRICAL - Calculatrice & Solveur Matriciel")
        self.geometry("1100 x 700")
        self.minsize(900, 600)
        
        # Grid layout 1x2 (Sidebar + Main View)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1)
        
        # App Title in Sidebar
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="MATRICAL",
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#2563EB"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        self.sub_logo = ctk.CTkLabel(
            self.sidebar_frame, text="Solveur & Calculatrice",
            font=ctk.CTkFont(size=12), text_color="gray"
        )
        self.sub_logo.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Navigation Buttons
        self.nav_buttons = {}
        nav_items = [
            ("Accueil", "home"),
            ("Opérations (+, -, ×)", "operations"),
            ("Déterminant", "determinant"),
            ("Matrice Inverse", "inverse"),
            ("Système d'Équations", "solver"),
            ("Historique", "history"),
            ("Aide & Theorie", "help")
        ]
        
        for idx, (label, page_id) in enumerate(nav_items, start=2):
            btn = ctk.CTkButton(
                self.sidebar_frame, text=label,
                corner_radius=8, height=36,
                border_spacing=10, fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                command=lambda p=page_id: self.navigate_to(p)
            )
            btn.grid(row=idx, column=0, padx=15, pady=4, sticky="ew")
            self.nav_buttons[page_id] = btn
            
        # Dark/Light Theme Switcher at bottom
        self.theme_label = ctk.CTkLabel(self.sidebar_frame, text="Thème de l'interface :", font=ctk.CTkFont(size=12))
        self.theme_label.grid(row=10, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.theme_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=["Sombre", "Clair", "Système"],
            command=self.change_theme
        )
        self.theme_menu.grid(row=11, column=0, padx=20, pady=(5, 20), sticky="ew")
        
        # Container for main views
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        self.pages = {}
        self.current_page = None
        
        # Load initial page
        self.navigate_to("home")

    def navigate_to(self, page_id: str, sub_param: str = None):
        # Update button highlights
        for key, btn in self.nav_buttons.items():
            if key == page_id:
                btn.configure(fg_color=("#3B82F6", "#2563EB"), text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))
                
        # Hide current page
        if self.current_page:
            self.current_page.grid_forget()
            
        # Create or retrieve page
        if page_id == "home":
            page = HomePage(self.main_container, navigate_callback=self.navigate_to)
        elif page_id == "operations":
            page = OperationsPage(self.main_container, initial_tab=sub_param or "add")
        elif page_id == "determinant":
            page = SingleMatrixPage(self.main_container, mode="determinant")
        elif page_id == "inverse":
            page = SingleMatrixPage(self.main_container, mode="inverse")
        elif page_id == "solver":
            page = SystemSolverPage(self.main_container)
        elif page_id == "history":
            page = HistoryPage(self.main_container)
        elif page_id == "help":
            page = HelpPage(self.main_container)
        else:
            page = HomePage(self.main_container, navigate_callback=self.navigate_to)
            
        page.grid(row=0, column=0, sticky="nsew")
        self.current_page = page

    def change_theme(self, new_theme: str):
        if new_theme == "Sombre":
            ctk.set_appearance_mode("Dark")
        elif new_theme == "Clair":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("System")
