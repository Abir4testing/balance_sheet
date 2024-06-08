import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

class BalanceSheetGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Balance Sheet Generator")

        self.categories = ["Current Assets", "Fixed Assets", "Current Liabilities", "Long-term Liabilities", "Stockholders' Equity"]
        self.current_assets = 0
        self.fixed_assets = 0
        self.total_assets = 0
        self.current_liabilities = 0
        self.long_term_liabilities = 0
        self.total_liabilities = 0
        self.stockholders_equity = 0
        self.total_equity_liabilities = 0

        self.category_ids = {}  # Dictionary to store category IDs

        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.company_name_label = ttk.Label(self.frame, text="Company Name:")
        self.company_name_label.grid(row=0, column=0, padx=5, pady=5)

        self.company_name_entry = ttk.Entry(self.frame)
        self.company_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.item_label = ttk.Label(self.frame, text="Account Detail:")
        self.item_label.grid(row=1, column=0, padx=5, pady=5)

        self.item_entry = ttk.Entry(self.frame)
        self.item_entry.grid(row=1, column=1, padx=5, pady=5)

        self.amount_label = ttk.Label(self.frame, text="Amount:")
        self.amount_label.grid(row=1, column=2, padx=5, pady=5)

        self.amount_entry = ttk.Entry(self.frame)
        self.amount_entry.grid(row=1, column=3, padx=5, pady=5)

        self.add_button = ttk.Button(self.frame, text="Add", command=self.add_item)
        self.add_button.grid(row=1, column=4, padx=5, pady=5)

        self.sub_button = ttk.Button(self.frame, text="Subtract", command=self.subtract_item)
        self.sub_button.grid(row=1, column=5, padx=5, pady=5)

        self.balance_sheet_label = ttk.Label(self.frame, text="Balance Sheet")
        self.balance_sheet_label.grid(row=2, column=0, columnspan=6, padx=5, pady=5)

        self.tree = ttk.Treeview(self.frame, columns=("Category", "Item", "Amount"), selectmode="extended", height=15)
        self.tree.grid(row=3, column=0, columnspan=6, padx=5, pady=5)

        for category in self.categories:
            category_id = self.tree.insert("", "end", text=category, values=("Total", "", 0))
            self.category_ids[category] = category_id

        self.total_current_assets_label = ttk.Label(self.frame, text="Total Current Assets: {:.2f}".format(self.current_assets))
        self.total_current_assets_label.grid(row=4, column=0, columnspan=6, padx=5, pady=5)

        self.total_fixed_assets_label = ttk.Label(self.frame, text="Total Fixed Assets: {:.2f}".format(self.fixed_assets))
        self.total_fixed_assets_label.grid(row=5, column=0, columnspan=6, padx=5, pady=5)

        self.total_assets_label = ttk.Label(self.frame, text="Total Assets: {:.2f}".format(self.total_assets))
        self.total_assets_label.grid(row=6, column=0, columnspan=6, padx=5, pady=5)

        self.total_current_liabilities_label = ttk.Label(self.frame, text="Total Current Liabilities: {:.2f}".format(self.current_liabilities))
        self.total_current_liabilities_label.grid(row=7, column=0, columnspan=6, padx=5, pady=5)

        self.total_long_term_liabilities_label = ttk.Label(self.frame, text="Total Long-term Liabilities: {:.2f}".format(self.long_term_liabilities))
        self.total_long_term_liabilities_label.grid(row=8, column=0, columnspan=6, padx=5, pady=5)

        self.total_liabilities_label = ttk.Label(self.frame, text="Total Liabilities: {:.2f}".format(self.total_liabilities))
        self.total_liabilities_label.grid(row=9, column=0, columnspan=6, padx=5, pady=5)

        self.total_stockholders_equity_label = ttk.Label(self.frame, text="Total Stockholders' Equity: {:.2f}".format(self.stockholders_equity))
        self.total_stockholders_equity_label.grid(row=10, column=0, columnspan=6, padx=5, pady=5)

        self.total_equity_liabilities_label = ttk.Label(self.frame, text="Total Liabilities & Stockholders' Equity: {:.2f}".format(self.total_equity_liabilities))
        self.total_equity_liabilities_label.grid(row=11, column=0, columnspan=6, padx=5, pady=5)

        self.csv_button = ttk.Button(self.frame, text="Generate CSV", command=self.generate_csv)
        self.csv_button.grid(row=12, column=0, columnspan=6, padx=5, pady=5)

    def add_item(self):
        try:
            category = self.tree.selection()[0]  # Assuming only one category can be selected at a time
        except IndexError:
            messagebox.showerror("Error", "Please select a category.")
            return

        item = self.item_entry.get()
        amount = float(self.amount_entry.get())

        if item.lower().startswith("less"):
            amount *= -1

        self.tree.insert(category, "end", text="", values=(item, amount))

        current_category = self.tree.item(category)["text"]
        if current_category == "Current Assets":
            self.current_assets += amount
            self.update_current_assets_label()
        elif current_category == "Fixed Assets":
            self.fixed_assets += amount
            self.update_fixed_assets_label()
        elif current_category == "Current Liabilities":
            self.current_liabilities += amount
            self.update_current_liabilities_label()
        elif current_category == "Long-term Liabilities":
            self.long_term_liabilities += amount
            self.update_long_term_liabilities_label()
        elif current_category == "Stockholders' Equity":
            self.stockholders_equity += amount
            self.update_stockholders_equity_label()

        self.update_total_assets()
        self.update_total_liabilities()
        self.update_total_equity_liabilities()

    def subtract_item(self):
        try:
            category = self.tree.selection()[0]  # Assuming only one category can be selected at a time
        except IndexError:
            messagebox.showerror("Error", "Please select a category.")
            return

        item = self.item_entry.get()
        amount = float(self.amount_entry.get())

        if not item.lower().startswith("less"):
            item = "Less " + item

        amount *= -1

        self.tree.insert(category, "end", text="", values=(item, amount))

        current_category = self.tree.item(category)["text"]
        if current_category == "Current Assets":
            self.current_assets += amount
            self.update_current_assets_label()
        elif current_category == "Fixed Assets":
            self.fixed_assets += amount
            self.update_fixed_assets_label()
        elif current_category == "Current Liabilities":
            self.current_liabilities += amount
            self.update_current_liabilities_label()
        elif current_category == "Long-term Liabilities":
            self.long_term_liabilities += amount
            self.update_long_term_liabilities_label()
        elif current_category == "Stockholders' Equity":
            self.stockholders_equity += amount
            self.update_stockholders_equity_label()

        self.update_total_assets()
        self.update_total_liabilities()
        self.update_total_equity_liabilities()

    def update_current_assets_label(self):
        self.total_current_assets_label.config(text="Total Current Assets: {:.2f}".format(self.current_assets))

    def update_fixed_assets_label(self):
        self.total_fixed_assets_label.config(text="Total Fixed Assets: {:.2f}".format(self.fixed_assets))

    def update_total_assets(self):
        self.total_assets = self.current_assets + self.fixed_assets
        self.total_assets_label.config(text="Total Assets: {:.2f}".format(self.total_assets))

    def update_current_liabilities_label(self):
        self.total_current_liabilities_label.config(text="Total Current Liabilities: {:.2f}".format(self.current_liabilities))

    def update_long_term_liabilities_label(self):
        self.total_long_term_liabilities_label.config(text="Total Long-term Liabilities: {:.2f}".format(self.long_term_liabilities))

    def update_total_liabilities(self):
        self.total_liabilities = self.current_liabilities + self.long_term_liabilities
        self.total_liabilities_label.config(text="Total Liabilities: {:.2f}".format(self.total_liabilities))

    def update_stockholders_equity_label(self):
        self.total_stockholders_equity_label.config(text="Total Stockholders' Equity: {:.2f}".format(self.stockholders_equity))

    def update_total_equity_liabilities(self):
        self.total_equity_liabilities = self.total_liabilities + self.stockholders_equity
        self.total_equity_liabilities_label.config(text="Total Liabilities & Stockholders' Equity: {:.2f}".format(self.total_equity_liabilities))

    def generate_csv(self):
        company_name = self.company_name_entry.get()
        if not company_name:
            messagebox.showerror("Error", "Please enter the company name.")
            return

        year = datetime.now().year
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"balance_sheet_{date}.csv"

        data = [
            [company_name, year],
            ["Balance Sheet", ""],
            ["", ""],
            ["Assets", ""],
            ["Current Assets", ""]
        ]

        for item in self.tree.get_children(self.category_ids["Current Assets"]):
            values = self.tree.item(item)["values"]
            data.append([values[0], values[1]])

        data.append(["Total Current Assets:", self.current_assets])
        data.append(["", ""])
        data.append(["Fixed Assets", ""])

        for item in self.tree.get_children(self.category_ids["Fixed Assets"]):
            values = self.tree.item(item)["values"]
            data.append([values[0], values[1]])

        data.append(["Total Fixed Assets:", self.fixed_assets])
        data.append(["", ""])
        data.append(["Total Assets:", self.total_assets])
        data.append(["", ""])
        data.append(["Liabilities", ""])
        data.append(["Current Liabilities", ""])

        for item in self.tree.get_children(self.category_ids["Current Liabilities"]):
            values = self.tree.item(item)["values"]
            data.append([values[0], values[1]])

        data.append(["Total Current Liabilities:", self.current_liabilities])
        data.append(["", ""])
        data.append(["Long-term Liabilities", ""])

        for item in self.tree.get_children(self.category_ids["Long-term Liabilities"]):
            values = self.tree.item(item)["values"]
            data.append([values[0], values[1]])

        data.append(["Total Long-term Liabilities:", self.long_term_liabilities])
        data.append(["", ""])
        data.append(["Total Liabilities:", self.total_liabilities])
        data.append(["", ""])
        data.append(["Stockholders' Equity", ""])

        for item in self.tree.get_children(self.category_ids["Stockholders' Equity"]):
            values = self.tree.item(item)["values"]
            data.append([values[0], values[1]])

        data.append(["Total Stockholders' Equity:", self.stockholders_equity])
        data.append(["", ""])
        data.append(["Total Liabilities & Stockholders' Equity:", self.total_equity_liabilities])
        data.append(["", ""])
        data.append(["Balance:", self.total_assets - self.total_equity_liabilities])

        try:
            with open(filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(data)
            messagebox.showinfo("Success", f"CSV file '{filename}' generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate CSV file: {e}")

# Create the Tkinter window
root = tk.Tk()
app = BalanceSheetGenerator(root)
root.mainloop()
