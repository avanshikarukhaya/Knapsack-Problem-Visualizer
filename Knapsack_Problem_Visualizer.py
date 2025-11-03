import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def knapsack(weights, values, capacity):
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]
    selected.reverse()
    return dp[n][capacity], selected


def calculate_knapsack():
    try:
        weights = list(map(int, weight_entry.get().split(',')))
        values = list(map(int, value_entry.get().split(',')))
        capacity = int(capacity_entry.get())

        if len(weights) != len(values):
            messagebox.showerror("Input Error", "Weights and values must have the same number of items!")
            return

        max_value, selected_items = knapsack(weights, values, capacity)
        result_label.config(text=f"Maximum Value: {max_value}\nSelected Items: {selected_items}")

        plot_chart(values, selected_items)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integers separated by commas.")


def plot_chart(values, selected_items):
    for widget in chart_frame.winfo_children():
        widget.destroy()

    labels = [f"Item {i+1}" for i in range(len(values))]
    selected_values = [values[i] if i in selected_items else 0 for i in range(len(values))]

    fig, ax = plt.subplots(figsize=(5, 3.5))
    bar_width = 0.4

    ax.bar(labels, values, color='lightgray', width=bar_width, label='Not Selected')
    ax.bar(labels, selected_values, color='teal', width=bar_width, label='Selected Items')

    ax.set_title("Knapsack Item Selection", fontsize=14, fontweight='bold')
    ax.set_xlabel("Items", fontsize=12)
    ax.set_ylabel("Values", fontsize=12)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


root = tk.Tk()
root.title("Knapsack Problem Visualizer")
root.geometry("650x550")
root.config(bg="#f0f8ff")

title = tk.Label(root, text="0/1 Knapsack Problem Visualizer", font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#003366")
title.pack(pady=10)

tk.Label(root, text="Enter Weights (comma-separated):", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
weight_entry = tk.Entry(root, width=40, font=("Arial", 12))
weight_entry.pack(pady=5)

tk.Label(root, text="Enter Values (comma-separated):", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
value_entry = tk.Entry(root, width=40, font=("Arial", 12))
value_entry.pack(pady=5)

tk.Label(root, text="Enter Knapsack Capacity:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
capacity_entry = tk.Entry(root, width=20, font=("Arial", 12))
capacity_entry.pack(pady=5)

tk.Button(root, text="Calculate & Show Chart", font=("Arial", 12, "bold"),
          bg="#007acc", fg="white", command=calculate_knapsack).pack(pady=15)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="#003366")
result_label.pack(pady=10)

chart_frame = tk.Frame(root, bg="#f0f8ff")
chart_frame.pack(pady=10)

root.mainloop()
