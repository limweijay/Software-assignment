import tkinter as tk
from tkinter import ttk, messagebox
from recipe_module import RecipesPage
from substitute_module import SubstitutePage
from shopping_module import ShoppingPage

MENU_BG = "#D6E3F5"
MENU_TITLE_BG = "#87A7ED"
PRIMARY = "#6F82EF"
HOVER_BG = "#D1DAE8"
BG_LIGHT = "#F7F9FC"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recipe & Nutrition Assistant")
        self.geometry("1000x600")
        self.configure(bg=BG_LIGHT)
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.main_frame = tk.Frame(self, bg=BG_LIGHT)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.create_left_menu()
        self.create_right_pages()
        self.show_page("recipes")

    # LEFT MENU 
    def create_left_menu(self):
        self.menu_frame = tk.Frame(self.main_frame, width=220, bg=MENU_BG)
        self.menu_frame.grid(row=0, column=0, sticky="ns")
        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.menu_frame.grid_propagate(False)

        tk.Label(self.menu_frame, text=" MENU ",font=("Segoe UI", 20, "bold"),fg="#1B4CC8", height=2, bg=MENU_TITLE_BG).pack(fill="x")
        self.create_menu_item("🍳 Recipes Manager", "recipes")
        self.create_menu_item("🔄 Ingredient", "substitutes")
        self.create_menu_item("🛒 Shopping List", "shopping")

    def create_menu_item(self, text, target_page):
        lbl = tk.Label(self.menu_frame, text=" " + text,font=("Segoe UI", 14, "bold"),fg="#2C3E50", bg=MENU_BG, anchor="w",cursor="hand2", padx=20, pady=15)
        lbl.pack(fill="x", pady=3)
        lbl.bind("<Enter>", lambda e, L=lbl: L.config(bg=HOVER_BG))
        lbl.bind("<Leave>", lambda e, L=lbl: L.config(bg=MENU_BG))
        lbl.bind("<Button-1>", lambda e: self.show_page(target_page))

    # RIGHT SIDE
    def create_right_pages(self):
        self.content = tk.Frame(self.main_frame, bg=BG_LIGHT)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.pages = {"recipes": RecipesPage(self.content),"substitutes": SubstitutePage(self.content),"shopping": ShoppingPage(self.content)}

    def show_page(self, name):
        if name == "shopping":
            self.pages["shopping"].destroy()
            self.pages["shopping"] = ShoppingPage(self.content)

        for p in self.pages.values():
            p.pack_forget()

        self.pages[name].pack(fill="both", expand=True)

if __name__ == "__main__":
    App().mainloop()