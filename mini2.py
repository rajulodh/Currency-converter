import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
import heapq


class CurrencyConverter:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.add_sample_currencies()

    def add_sample_currencies(self):
        self.graph.add_weighted_edges_from([
            ("USD", "INR", 82.0),
            ("INR", "USD", 0.012),
            ("USD", "EUR", 0.91),
            ("EUR", "USD", 1.1),
            ("INR", "EUR", 0.011),
            ("EUR", "INR", 90.0),
            ("USD", "GBP", 0.76),
            ("GBP", "USD", 1.32),
            ("INR", "GBP", 0.0092),
            ("GBP", "INR", 109.0),
            ("EUR", "GBP", 0.84),
            ("GBP", "EUR", 1.19),
        ])

    def dijkstra(self, source, target):
        queue = [(0, source, [])]
        visited = set()

        while queue:
            (cost, node, path) = heapq.heappop(queue)

            if node in visited:
                continue

            path = path + [node]
            visited.add(node)

            if node == target:
                return path, cost

            for neighbor in self.graph.neighbors(node):
                if neighbor not in visited:
                    total_cost = cost + self.graph[node][neighbor]['weight']
                    heapq.heappush(queue, (total_cost, neighbor, path))

        return None, float('inf')


converter = CurrencyConverter()



def convert_currency():
    try:
        source = from_currency_combobox.get()
        target = to_currency_combobox.get()

        if source == target:
            messagebox.showerror("Error", "Source and target currencies must be different")
            return

        path, cost = converter.dijkstra(source, target)
        amount = float(amount_entry.get())
        converted_amount = amount * cost
        result_label.config(text=f"Conversion Path: {' -> '.join(path)}\nConverted Amount: {converted_amount:.2f} {target}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Currency Converter Application")
root.geometry("400x300")
root.configure(bg="#1e1e2e")

style = ttk.Style()
style.theme_use("clam")

header = tk.Label(root, text="Currency Converter", bg="#1e1e2e", fg="white", font=("Arial", 18, "bold"))
header.pack(pady=10)

currencies = ["USD", "INR", "EUR", "GBP"]

from_currency_combobox = ttk.Combobox(root, values=currencies, font=("Arial", 12))
from_currency_combobox.set("USD")
from_currency_combobox.pack(pady=5)

to_currency_combobox = ttk.Combobox(root, values=currencies, font=("Arial", 12))
to_currency_combobox.set("INR")
to_currency_combobox.pack(pady=5)

amount_entry = tk.Entry(root, font=("Arial", 12))
amount_entry.insert(0, "Enter Amount")
amount_entry.pack(pady=5)

convert_button = tk.Button(root, text="Convert", command=convert_currency, bg="#007acc", fg="white", font=("Arial", 12), relief="raised")
convert_button.pack(pady=10)

result_label = tk.Label(root, text="", bg="#1e1e2e", fg="white", font=("Arial", 12))
result_label.pack(pady=5)

root.mainloop()
