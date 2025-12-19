# Recipe & Nutrition Assistant

## Group Members
- Member 1: Lim Wei Jay
- Member 2: Tan Jia Yii
- Member 3: Yap Xuan Yuan

## Project Description
Recipe & Nutrition Assistant is a Python-based desktop application developed using Tkinter.
The system helps users manage recipes, calculate total calories, find ingredient substitutes,
and generate a shopping list based on selected recipes.

This project is developed as part of a group assignment and focuses on GUI design,
file handling, and basic data processing.

---

## Features

### 1. Recipes Manager
- Add new recipes with ingredients, quantity, unit, and calories
- Automatically calculate total calories per recipe
- View recipe details in a separate window
- Edit existing recipes
- Delete recipes
- Store recipe data locally using JSON file

### 2. Ingredient Substitutes
- Select ingredient categories
- Search for substitute ingredients
- Display alternative ingredients using stored JSON data

### 3. Shopping List Generator
- Select multiple recipes
- Combine ingredients from selected recipes
- Calculate total required quantity for each ingredient
- Generate a list of ingredients not yet bought

---

## Technologies Used
- Programming Language: Python 3
- GUI Library: Tkinter
- Data Storage: JSON files
- Platform: Windows

---

## File Structure

---

## Description of Main Files

### main.py
- Entry point of the application
- Handles main window layout and navigation menu
- Switches between different pages (Recipes, Substitutes, Shopping List)

### recipe_module.py
- Manages recipe creation, editing, viewing, and deletion
- Validates user input
- Calculates total calories
- Stores and loads recipe data using `recipes.json`

### substitute_module.py
- Handles ingredient substitute searching
- Loads substitute data from `substitutes.json`
- Allows category-based ingredient selection

### shopping_module.py
- Generates shopping list based on selected recipes
- Combines ingredient quantities automatically
- Displays missing ingredients in a separate window

---

## How to Run the Program

1. Make sure **Python 3** is installed on your computer.
2. Open the `Source Code` folder.
3. Run the application using the command:
   ```bash
   python main.py
