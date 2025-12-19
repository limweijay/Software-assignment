import tkinter as tk
from tkinter import ttk, messagebox
import json, os, re

BG_LIGHT = "#F7F9FC"
RECIPE_FILE = "recipes.json"
PRIMARY = "#6F82EF"

def modern_button(parent, text, command, width=12):
    btn = tk.Button(parent, text=text, command=command, width=width,bg=PRIMARY, fg="white",activebackground="#5B6EDC", activeforeground="white",relief="flat", font=("Segoe UI", 10, "bold"))
    btn.bind("<Enter>", lambda e: btn.config(bg="#5B6EDC"))
    btn.bind("<Leave>", lambda e: btn.config(bg=PRIMARY))
    return btn

class RecipesPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_LIGHT)
        self.editing_index = None
        self.load_recipes()
        tk.Label(self, text="Recipes Manager",font=("Segoe UI", 20, "bold"),bg=BG_LIGHT, fg=PRIMARY).pack(pady=10)
        main = tk.Frame(self, bg=BG_LIGHT)
        main.pack(fill="both", expand=True, padx=40, pady=20)

        # Input Rows
        def make_row(label, attr, placeholder):
            f = tk.Frame(main, bg=BG_LIGHT)
            f.pack(fill="x", pady=10)
            tk.Label(f, text=label, width=20,bg=BG_LIGHT, fg="#2C3E50",font=("Segoe UI", 12, "bold")).pack(side="left")
            entry = ttk.Entry(f, width=70, font=("Segoe UI", 12))
            entry.pack(side="left")
            self.add_placeholder(entry, placeholder)
            setattr(self, attr, entry)

        make_row("Recipe Name                   :", "recipe_name", "e.g: Fried Rice")
        make_row("Ingredients Name          :", "ing_text", "e.g: egg ; rice ; carrot")
        make_row("Quantity                            :", "qty_text", "e.g: 2(pcs) ; 200(g) ; 50(g)")
        make_row("Calories per ingredient :", "cal_text", "e.g: 70 ; 300 ; 41")

        # Add Button
        btn_area = tk.Frame(main, bg=BG_LIGHT)
        btn_area.pack(fill="x", pady=5)
        self.add_btn = modern_button(btn_area, "Add Recipe", self.on_add_or_save, width=14)
        self.add_btn.pack()

        # Recipe List
        box = tk.Frame(main, bg=BG_LIGHT)
        box.pack(fill="both", expand=True, pady=(10, 5))

        tk.Label(box, text="Recipe",font=("Segoe UI", 14, "bold"),bg=BG_LIGHT, fg=PRIMARY).pack(anchor="w")

        self.recipe_list = tk.Listbox(box, width=70, height=7,font=("Segoe UI", 12))
        self.recipe_list.pack(pady=5, fill="x")

        # Edit,View and Delete buttons
        btns = tk.Frame(box, bg=BG_LIGHT)
        btns.pack(pady=10)

        self.edit_btn = modern_button(btns, "Edit", self.start_edit)
        self.view_btn = modern_button(btns, "View", self.view_recipe)
        self.delete_btn = modern_button(btns, "Delete", self.delete_recipe)

        self.edit_btn.pack(side="left", padx=10)
        self.view_btn.pack(side="left", padx=10)
        self.delete_btn.pack(side="left", padx=10)

        #cancel button after ckick edit button
        self.cancel_btn = modern_button(btn_area, "Cancel", self.cancel_edit)
        self.refresh_recipe_list()

    # logic for placeholder
    def add_placeholder(self, entry, text):
        entry.insert(0, text)
        entry.config(foreground="gray")

        def on_focus_in(e):
            if entry.get() == text:
                entry.delete(0, "end")
                entry.config(foreground="black")

        def on_focus_out(e):
            if entry.get().strip() == "":
                entry.insert(0, text)
                entry.config(foreground="gray")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # Utility to restore all placeholders
    def restore_all_placeholders(self):
        self.recipe_name.delete(0, "end")
        self.ing_text.delete(0, "end")
        self.qty_text.delete(0, "end")
        self.cal_text.delete(0, "end")

        self.add_placeholder(self.recipe_name, "e.g: Fried Rice")
        self.add_placeholder(self.ing_text, "e.g: egg ; rice ; carrot")
        self.add_placeholder(self.qty_text, "e.g: 2(pcs) ; 200(g) ; 50(g)")
        self.add_placeholder(self.cal_text, "e.g: 70 ; 300 ; 41")

    # Add / Save Switch
    def on_add_or_save(self):
        if self.editing_index is None:
            self.add_recipe()
        else:
            self.save_edit()

    # User input format
    def parse_ingredients(self, ing_raw, qty_raw, cal_raw):
        names = [n.strip() for n in ing_raw.split(";") if n.strip()]
        qtys = [q.strip() for q in qty_raw.split(";") if q.strip()]
        cals = [c.strip() for c in cal_raw.split(";") if c.strip()]

        if not (len(names) == len(qtys) == len(cals)):
            return None, "Ingredient count mismatch"

        ingredients = []
        total = 0

        for name, qty_str, cal_str in zip(names, qtys, cals):
            match = re.match(r"^\s*([\d.]+)\s*\((.*?)\)\s*$", qty_str)
            if not match:
                return None, f"Invalid quantity format: {qty_str}"

            qty = float(match.group(1))
            unit = match.group(2)

            try:
                kcal = float(cal_str)
            except:
                return None, f"Invalid calorie: {cal_str}"

            ingredients.append({"name": name, "qty": qty, "unit": unit, "kcal": kcal})
            total += kcal

        return {"ingredients": ingredients, "total": total}, None

    # Add Recipe
    def add_recipe(self):
        name = self.recipe_name.get().strip()
        ing_raw = self.ing_text.get().strip()
        qty_raw = self.qty_text.get().strip()
        cal_raw = self.cal_text.get().strip()

        if name.startswith("e.g"):
            messagebox.showwarning("Warning", "Please enter actual recipe name.")
            return

        data, err = self.parse_ingredients(ing_raw, qty_raw, cal_raw)
        if err:
            messagebox.showwarning("Error", err)
            return

        # Duplicate check
        if any(r["name"].lower() == name.lower() for r in self.recipes):
            messagebox.showwarning("Error", "Recipe already exists.")
            return

        self.recipes.append({"name": name,"ingredients": data["ingredients"],"total_cal": data["total"]})
        self.save_recipes()
        self.refresh_recipe_list()

        messagebox.showinfo("Success", f"Recipe '{name}' added!")
        self.restore_all_placeholders()

    # View Recipe
    def view_recipe(self):
        sel = self.recipe_list.curselection()
        if not sel:
            return messagebox.showwarning("Warning", "Select a recipe to view.")

        recipe = self.recipes[sel[0]]

        win = tk.Toplevel(self)
        win.title(recipe["name"])
        win.geometry("450x400")
        win.configure(bg=BG_LIGHT)
        win.grab_set()

        tk.Label(win, text=recipe["name"],font=("Segoe UI", 18, "bold"),bg=BG_LIGHT).pack(pady=10)

        frame = tk.Frame(win, bg=BG_LIGHT)
        frame.pack(pady=5)

        tk.Label(frame, text="Ingredients:",font=("Segoe UI", 14, "bold"),bg=BG_LIGHT).pack(anchor="w")

        for ing in recipe["ingredients"]:
            line = f"- {ing['name']} : {ing['qty']}({ing['unit']}) - {ing['kcal']} kcal"
            tk.Label(frame, text=line, font=("Segoe UI", 12), bg=BG_LIGHT).pack(anchor="w")

        tk.Label(win, text=f"Total Calories: {recipe['total_cal']} kcal",font=("Segoe UI", 14, "bold"), bg=BG_LIGHT).pack(pady=10)

        modern_button(win, "Close", win.destroy).pack(pady=15)

    # Delete Recipe
    def delete_recipe(self):
        sel = self.recipe_list.curselection()
        if not sel:
            return messagebox.showwarning("Warning", "Select a recipe to delete.")

        name = self.recipe_list.get(sel[0])

        if not messagebox.askyesno("Confirm", f"Delete recipe '{name}'?"):
            return

        self.recipes = [r for r in self.recipes if r["name"] != name]
        self.save_recipes()
        self.refresh_recipe_list()
        messagebox.showinfo("Success", f"Deleted '{name}'")

        if self.editing_index is not None:
            self.cancel_edit()

    # Edit recipe
    def start_edit(self):
        sel = self.recipe_list.curselection()
        if not sel:
            return messagebox.showwarning("Warning", "Select a recipe to edit.")

        idx = sel[0]
        recipe = self.recipes[idx]

        self.recipe_name.delete(0, "end")
        self.recipe_name.insert(0, recipe["name"])

        names = [ing["name"] for ing in recipe["ingredients"]]
        qtys = [f"{ing['qty']}({ing['unit']})" for ing in recipe["ingredients"]]
        cals = [str(ing["kcal"]) for ing in recipe["ingredients"]]

        self.ing_text.delete(0, "end")
        self.ing_text.insert(0, " ; ".join(names))
        self.qty_text.delete(0, "end")
        self.qty_text.insert(0, " ; ".join(qtys))
        self.cal_text.delete(0, "end")
        self.cal_text.insert(0, " ; ".join(cals))

        self.editing_index = idx
        self.add_btn.config(text="Save Changes")
        self.cancel_btn.pack(anchor="center", pady=(6, 0))

    # Save Edit
    def save_edit(self):
        if self.editing_index is None:
            return

        name = self.recipe_name.get().strip()
        ing_raw = self.ing_text.get().strip()
        qty_raw = self.qty_text.get().strip()
        cal_raw = self.cal_text.get().strip()

        data, err = self.parse_ingredients(ing_raw, qty_raw, cal_raw)
        if err:
            messagebox.showwarning("Error", err)
            return

        for idx, r in enumerate(self.recipes):
            if idx != self.editing_index and r["name"].lower() == name.lower():
                return messagebox.showwarning("Error", "Another recipe has this name.")

        self.recipes[self.editing_index] = {"name": name,"ingredients": data["ingredients"],"total_cal": data["total"]}

        self.save_recipes()
        self.refresh_recipe_list()
        messagebox.showinfo("Success", f"Recipe '{name}' updated!")
        self.cancel_edit()

    # Cancel Edit
    def cancel_edit(self):
        self.editing_index = None
        self.add_btn.config(text="Add Recipe")
        self.cancel_btn.pack_forget()
        self.restore_all_placeholders()

    # JSON File input and output
    def load_recipes(self):
        if os.path.exists(RECIPE_FILE):
            self.recipes = json.load(open(RECIPE_FILE, "r", encoding="utf-8"))
        else:
            self.recipes = []

    def save_recipes(self):
        json.dump(self.recipes, open(RECIPE_FILE, "w",encoding="utf-8"),ensure_ascii=False, indent=2)

    # Refresh Recipe List
    def refresh_recipe_list(self):
        self.recipe_list.delete(0, "end")
        for r in self.recipes:
            self.recipe_list.insert("end", r["name"])