"""
Page d'historique des calculs enregistrés.
"""

import customtkinter as ctk
from utils.storage import load_history, clear_history
from utils.formatter import format_matrix_str, format_number

class HistoryPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(header, text="Historique des Calculs", font=ctk.CTkFont(size=22, weight="bold")).pack(side="left")
        
        btn_clear = ctk.CTkButton(
            header, text="Effacer l'historique", command=self.clear_all,
            fg_color="#EF4444", hover_color="#DC2626", width=140
        )
        btn_clear.pack(side="right")
        
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.refresh()

    def refresh(self):
        for child in self.scroll_frame.winfo_children():
            child.destroy()
            
        history = load_history()
        
        if not history:
            ctk.CTkLabel(
                self.scroll_frame, text="Aucun calcul enregistré dans l'historique.",
                font=ctk.CTkFont(size=14), text_color="gray"
            ).pack(pady=40)
            return
            
        for item in history:
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=10, border_width=1, border_color="#3B82F6")
            card.pack(fill="x", pady=8, padx=5)
            
            top_bar = ctk.CTkFrame(card, fg_color="transparent")
            top_bar.pack(fill="x", padx=15, pady=(10, 5))
            
            ctk.CTkLabel(top_bar, text=item["operation"], font=ctk.CTkFont(size=15, weight="bold"), text_color="#2563EB").pack(side="left")
            ctk.CTkLabel(top_bar, text=item.get("timestamp", ""), font=ctk.CTkFont(size=12), text_color="gray").pack(side="right")
            
            # Format result text
            res = item.get("result")
            steps = item.get("steps", [])
            
            if isinstance(res, list):
                res_str = "RÉSULTAT :\n" + format_matrix_str(res)
            elif isinstance(res, (int, float)):
                res_str = f"RÉSULTAT : {format_number(res)}"
            else:
                res_str = f"RÉSULTAT : {res}"

            if steps:
                res_str += "\n\n--- DÉTAILS DU CALCUL ---\n"
                for st in steps:
                    if isinstance(st, dict):
                        res_str += f"• Étape {st.get('step', '')}: {st.get('operation', '')}\n  {st.get('description', '')}\n"
                    else:
                        res_str += f"• {st}\n"
                
            txt = ctk.CTkTextbox(card, height=120, font=ctk.CTkFont(family="monospace", size=11))
            txt.pack(fill="x", padx=15, pady=(0, 10))
            txt.insert("1.0", res_str)
            txt.configure(state="disabled")

    def clear_all(self):
        clear_history()
        self.refresh()
