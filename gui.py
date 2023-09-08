import tkinter as tk
from tkinter import ttk

class Window:
    tree = None
    refresh_button = None
    
    def __init__(self, root, df):
        self.root = root
        self.root.title("RSI Stock Screener")
        self.root.resizable(False, False)
        self.tree = ttk.Treeview(root)
        
        # Add a Scrollbar
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Hide the Treeview's index column
        self.tree["show"] = "headings"
        self.tree.pack()

        # Add a Refresh button
        self.refresh_button = tk.Button(root, text="Refresh", command=self.insert_data(df))
        self.refresh_button.pack()

        self.insert_data(df)
        
    def insert_data(self, df):
        """
        Insert data from a DataFrame into a Tkinter Treeview widget.
    
        Parameters:
        - df (pd.DataFrame): The DataFrame containing the data to be inserted.
        """
        
        self.tree.delete(*self.tree.get_children())
  
        # Convert DataFrame columns to numeric IDs
        col_ids = range(len(df.columns))
        self.tree["columns"] = col_ids

        # Configure column headings
        for col, col_id in zip(df.columns, col_ids):
            self.tree.heading(col_id, text=col)
            #self.tree.column(col_id, width=100) 

        # Insert data from the DataFrame into the Treeview
        for i, row in df.iterrows():
            values = [row[col] for col in df.columns]
            self.tree.insert("", i, values=values)

  
