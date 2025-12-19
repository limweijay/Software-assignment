import tkinter as tk
from tkinter import ttk, messagebox
import json, os

# =====================================================
# Global UI constants
# =====================================================
BG_LIGHT = "#F7F9FC"
PRIMARY = "#6F82EF"
RECIPE_FILE = "recipes.json"

# =====================================================
# Reusable modern-style button
# =====================================================
def modern_button(parent, text, command, width=16):
    btn = tk.Button(parent, text=text, command=command, width=width,
                    bg=PRIMARY, fg="white", activebackground="#5B6EDC",
                    activeforeground="white", relief="flat",
                    font=("Segoe UI", 10, "bold"), cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg="#5B6EDC"))
    btn.bind("<Leave>", lambda e: btn.config(bg=PRIMARY))
    return btn

# =====================================================
# ScrollableFrame
# =====================================================
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, width=200, height=200, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self, bg=BG_LIGHT, highlightthickness=0,
                           width=width, height=height)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

# =====================================================
# Shopping Page
# =====================================================
class ShoppingPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_LIGHT)

        tk.Label(self, text="Shopping List Generator", bg=BG_LIGHT,
                 fg=PRIMARY, font=("Segoe UI", 22, "bold")).pack(pady=15)

        main = tk.Frame(self, bg=BG_LIGHT)
        main.pack(fill="both", expand=True, padx=40, pady=10)

        # Left panel
        left_frame = tk.Frame(main, bg=BG_LIGHT)
        left_frame.pack(side="left", fill="y", padx=(0, 40))

        tk.Label(left_frame, text="Select Recipes",
                 font=("Segoe UI", 14, "bold"),
                 bg=BG_LIGHT, fg="#2C3E50").pack(anchor="w", pady=5)

        scroll_left = ScrollableFrame(left_frame, width=220, height=300)
        scroll_left.pack()

        self.recipe_vars = {}
        self.load_recipes()

        for recipe in self.recipes:
            var = tk.BooleanVar()
            ttk.Checkbutton(scroll_left.scrollable_frame,
                            text=recipe["name"], variable=var).pack(anchor="w")
            self.recipe_vars[recipe["name"]] = var

        modern_button(left_frame, "Select Recipes",
                      self.select_recipes, 16).pack(pady=15)

        # Right panel
        right_frame = tk.Frame(main, bg=BG_LIGHT)
        right_frame.pack(side="left", fill="both", expand=True)

        tk.Label(right_frame, text="Selected Recipes:",
                 font=("Segoe UI", 13, "bold"),
                 bg=BG_LIGHT, fg="#2C3E50").pack(anchor="w")

        self.selected_box = tk.Text(right_frame, height=6,
                                    font=("Segoe UI", 11))
        self.selected_box.pack(fill="x", pady=6)
        self.selected_box.config(state="disabled")

        tk.Label(right_frame, text="Ingredients Not Yet Bought:",
                 font=("Segoe UI", 13, "bold"),
                 bg=BG_LIGHT, fg="#2C3E50").pack(anchor="w", pady=(10, 5))

        scroll_ing = ScrollableFrame(right_frame, width=350, height=215)
        scroll_ing.pack(fill="x", pady=5, anchor="n")

        self.ing_frame = scroll_ing.scrollable_frame
        self.ing_vars, self.combined_ings = {}, {}

        modern_button(right_frame, "Generate Shopping List",
                      self.generate_missing, width=23).pack(pady=20)

    # =====================================================
    # Load recipes
    # =====================================================
    def load_recipes(self):
        if os.path.exists(RECIPE_FILE):
            try:
                with open(RECIPE_FILE, "r", encoding="utf-8") as f:
                    self.recipes = json.load(f)
            except Exception:
                self.recipes = []
        else:
            self.recipes = []

    # =====================================================
    # Select recipes
    # =====================================================
    def select_recipes(self):
        selected = [n for n, v in self.recipe_vars.items() if v.get()]
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one recipe.")
            return

        self.selected_box.config(state="normal")
        self.selected_box.delete("1.0", "end")
        for name in selected:
            self.selected_box.insert("end", f"- {name}\n")
        self.selected_box.config(state="disabled")

        self.build_ingredient_list(selected)

    # =====================================================
    # Merge ingredients
    # =====================================================
    def build_ingredient_list(self, selected_recipes):
        for w in self.ing_frame.winfo_children(): w.destroy()
        self.ing_vars.clear()
        self.combined_ings.clear()

        for recipe in self.recipes:
            if recipe["name"] not in selected_recipes: continue
            for ing in recipe.get("ingredients", []):
                name, unit = ing.get("name", "").strip(), ing.get("unit", "").strip()
                try: qty = float(ing.get("qty", 0))
                except Exception: qty = 0.0
                key = f"{name} ({unit})"
                self.combined_ings[key] = self.combined_ings.get(key, 0) + qty

        for key in sorted(self.combined_ings, key=str.lower):
            text = f"{key}: {self.combined_ings[key]}"
            var = tk.BooleanVar()
            ttk.Checkbutton(self.ing_frame,
                            text=text, variable=var).pack(anchor="w", pady=2)
            self.ing_vars[text] = var

    # =====================================================
    # Generate shopping list
    # =====================================================
    def generate_missing(self):
        missing = {}
        for text, var in self.ing_vars.items():
            if var.get():
                parts = text.split(":")
                missing[parts[0].strip()] = ":".join(parts[1:]).strip() if len(parts) >= 2 else ""

        if not missing:
            messagebox.showwarning("Warning", "No ingredients selected.")
            return

        win = tk.Toplevel(self)
        win.title("Missing Ingredients")
        win.geometry("420x400")
        win.config(bg=BG_LIGHT)
        win.grab_set()

        tk.Label(win, text="Missing Ingredients:",
                 font=("Segoe UI", 18, "bold"),
                 bg=BG_LIGHT).pack(pady=10)

        box = tk.Text(win, width=45, height=10,
                      font=("Segoe UI", 12))
        box.pack(pady=5, padx=10, fill="both", expand=True)

        for name, qty in missing.items():
            box.insert("end", f"- {name}: {qty}\n")

        box.config(state="disabled")
        modern_button(win, "Close", win.destroy).pack(pady=10)