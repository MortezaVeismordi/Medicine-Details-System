import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

file_path = 'Preprocessed_Medicine_Details.csv' 
medicine_data = pd.read_csv(file_path)


def search_medicine():
    medicine_name = combobox.get().strip()
    if not medicine_name:
        messagebox.showerror("Error", "Please enter a medicine name")
        return

    results = medicine_data[medicine_data['Medicine Name'].str.contains(medicine_name, case=False, na=False)]
    if not results.empty:
        result = results.iloc[0]  
        medicine_name_label.config(text=result['Medicine Name'])
        composition_label.config(text=result['Composition'])
        uses_label.config(text=result['Uses'])
        side_effects_label.config(text=result['Side_effects'])
        manufacturer_label.config(text=result['Manufacturer'])
        reviews_label.config(
            text=f"Excellent: {result['Excellent Review %']}% | Average: {result['Average Review %']}% | Poor: {result['Poor Review %']}%"
        )
    else:
        messagebox.showinfo("Result", "No Medicine Found")

def update_combobox(event):
    typed_text = combobox.get().strip()
    if typed_text:
        filtered_names = medicine_data[medicine_data['Medicine Name']
                                       .str.contains(typed_text, case=False, na=False)]['Medicine Name'].tolist()
        combobox['values'] = filtered_names
    else:
        combobox['values'] = medicine_names

def reset_search():
    combobox.set("")
    medicine_name_label.config(text="")
    composition_label.config(text="")
    uses_label.config(text="")
    side_effects_label.config(text="")
    manufacturer_label.config(text="")
    reviews_label.config(text="")
    combobox['values'] = medicine_names

root = tk.Tk()
root.title("Medicine Database Search")
root.geometry("600x700")

title_label = tk.Label(root, text="Medicine Database Search", font=("Arial", 16, "bold"), pady=10)
title_label.pack()

entry_label = tk.Label(root, text="Enter Medicine Name:", font=("Arial", 12))
entry_label.pack(pady=5)

combobox = ttk.Combobox(root, font=("Arial", 12), width=40)
combobox.pack(pady=5)

medicine_names = medicine_data['Medicine Name'].dropna().tolist()
combobox['values'] = medicine_names
combobox.set("Choose a Medicine or Enter a Name ...")
combobox.bind('<KeyRelease>', update_combobox)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

search_button = tk.Button(button_frame, text="Search", font=("Arial", 12), command=search_medicine)
search_button.grid(row=0, column=0, padx=10)

reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 12), command=reset_search)
reset_button.grid(row=0, column=1, padx=10)

info_frame = tk.Frame(root)
info_frame.pack(pady=10)

medicine_name_frame = ttk.LabelFrame(root, text="Medicine Name", style="Custom.TLabelframe")
medicine_name_frame.pack(fill="x", pady=5)
medicine_name_label = tk.Label(medicine_name_frame, text="", font=("Arial", 12), anchor="w")
medicine_name_label.pack(fill="x", padx=10, pady=5)

composition_frame = ttk.LabelFrame(info_frame, text="Composition", style="Custom.TLabelframe")
composition_frame.pack(fill="x", pady=5)
composition_label = tk.Label(composition_frame, text="", font=("Arial", 12), anchor="w")
composition_label.pack(fill="x", padx=10, pady=5)

uses_frame = ttk.LabelFrame(info_frame, text="Uses", style="Custom.TLabelframe")
uses_frame.pack(fill="x", pady=5)
uses_label = tk.Label(uses_frame, text="", font=("Arial", 12), anchor="w")
uses_label.pack(fill="x", padx=10, pady=5)

side_effects_frame = ttk.LabelFrame(info_frame, text="Side Effects", style="Custom.TLabelframe")
side_effects_frame.pack(fill="x", pady=5)
side_effects_label = tk.Label(side_effects_frame, text="", font=("Arial", 12), anchor="w")
side_effects_label.pack(fill="x", padx=10, pady=5)

manufacturer_frame = ttk.LabelFrame(info_frame, text="Manufacturer", style="Custom.TLabelframe")
manufacturer_frame.pack(fill="x", pady=5)
manufacturer_label = tk.Label(manufacturer_frame, text="", font=("Arial", 12), anchor="w")
manufacturer_label.pack(fill="x", padx=10, pady=5)

reviews_frame = ttk.LabelFrame(info_frame, text="Reviews", style="Custom.TLabelframe")
reviews_frame.pack(fill="x", pady=5)
reviews_label = tk.Label(reviews_frame, text="", font=("Arial", 12), anchor="w")
reviews_label.pack(fill="x", padx=10, pady=5)

root.mainloop()