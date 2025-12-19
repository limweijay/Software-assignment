import tkinter as tk
from tkinter import ttk, messagebox
import json, os

# Unified colors
BG_LIGHT = "#F7F9FC"
PRIMARY = "#6F82EF"

SUB_FILE = "substitutes.json"

# ==================== Unified Button Style ======================
def modern_button(parent, text, command, width=16):
    btn = tk.Button(parent, text=text, command=command, width=width,bg=PRIMARY, fg="white",activebackground="#5B6EDC", activeforeground="white",relief="flat", font=("Segoe UI", 11, "bold"),cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg="#5B6EDC"))
    btn.bind("<Leave>", lambda e: btn.config(bg=PRIMARY))
    return btn

# ==================== Substitute Page ===========================
class SubstitutePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_LIGHT)

        # Load JSON
        self.subs = self.load_json()
        self.categories = self.build_categories()

        # ======================== TITLE ============================
        tk.Label(self, text="Ingredient Substitutes",font=("Segoe UI", 22, "bold"),bg=BG_LIGHT, fg=PRIMARY).pack(pady=15)

        # Main layout frame
        main = tk.Frame(self, bg=BG_LIGHT)
        main.pack(padx=40, pady=10, anchor="nw")

        # ======================== CATEGORY =========================
        tk.Label(main, text="Select Category:",font=("Segoe UI", 13, "bold"),bg=BG_LIGHT, fg="#2C3E50").grid(row=0, column=0, pady=10, sticky="w")

        self.category_cb = ttk.Combobox(main, state="readonly", width=28,values=list(self.categories.keys()))
        self.category_cb.grid(row=0, column=1, padx=10)
        self.category_cb.bind("<<ComboboxSelected>>", self.update_ingredients)

        # ======================== INGREDIENT ========================
        tk.Label(main, text="Select Missing Ingredient:",font=("Segoe UI", 13, "bold"),bg=BG_LIGHT, fg="#2C3E50").grid(row=1, column=0, pady=10, sticky="w")

        self.ing_cb = ttk.Combobox(main, state="readonly", width=28)
        self.ing_cb.grid(row=1, column=1, padx=10)

        tk.Label(main,text="# Select category first then ingredient",font=("Segoe UI", 9, "italic"),bg=BG_LIGHT,fg="#7F8C8D").grid(row=2, column=1, sticky="w", padx=10)

        # ======================== SEARCH BUTTON =====================
        modern_button(main, "Searching", self.find_substitute, 18).grid(row=3, column=1, pady=18, padx=24, sticky="w")

        # ======================== RESULT LABEL ======================
        tk.Label(self, text="Replacement Suggestion:",font=("Segoe UI", 14, "bold"),bg=BG_LIGHT, fg="#2C3E50").pack(anchor="w", padx=40, pady=(15, 5))

        # ======================== RESULT BOX ========================
        self.result_box = tk.Text(self, width=70, height=10, wrap="word",font=("Segoe UI", 12), bg="white")
        self.result_box.pack(padx=40, pady=5)
        self.result_box.config(state="disabled")

    # ================== Load JSON ====================
    def load_json(self):
        if os.path.exists(SUB_FILE):
            try:
                with open(SUB_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                messagebox.showerror("Error", "Failed to read JSON file.")
                return {}
        else:
            messagebox.showerror("Error", f"JSON file '{SUB_FILE}' not found.")
            return {}

    # ================== Build Category List ====================
    def build_categories(self):
        categories = {}

        for ing, data in self.subs.items():
            cat = data.get("category", "Others")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ing)

        return categories

    # ================== Update Ingredient After Category Change ====================
    def update_ingredients(self, event):
        cat = self.category_cb.get()
        ingredients = self.categories.get(cat, [])
        self.ing_cb["values"] = ingredients
        self.ing_cb.set("")

    # ================== Search Button ====================
    def find_substitute(self):
        ing = self.ing_cb.get().strip().lower()

        if not ing:
            messagebox.showwarning("Warning", "Please select an ingredient.")
            return

        if ing not in self.subs:
            self.display_result(f"No substitute found for '{ing}'.")
            return

        text = f"Ingredient: {ing}\n\nSubstitutes:\n"
        for s in self.subs[ing]["subs"]:
            text += f"- {s}\n"

        self.display_result(text)

    # ================== Display ====================
    def display_result(self, text):
        self.result_box.config(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", text)
        self.result_box.config(state="disabled")