import tkinter as tk
from tkinter import ttk
import pandas as pd

def load_csv_data():
    # Load CSV data using pandas
    file_path = "Twitter_Account_info.csv"  # Replace with your CSV file path
    data = pd.read_csv(file_path)

    # Create the Tkinter window
    root = tk.Tk()
    root.title("CSV Data Display")

    # Create a treeview widget (Data Grid)
    tree = ttk.Treeview(root)

    # Set up columns
    tree["columns"] = list(data.columns)
    tree["show"] = "headings"

    # Add columns to the treeview
    for col in tree["columns"]:
        tree.heading(col, text=col)

    # Insert data into the treeview
    for i, row in data.iterrows():
        tree.insert("", "end", values=list(row))

    # Add treeview to window and pack it
    tree.pack()

    # Run the Tkinter main loop
    root.mainloop()

# Call the function to load and display CSV data
load_csv_data()
