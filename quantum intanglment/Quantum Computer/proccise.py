import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ==========================
# PARAMETERS
# ==========================
num_qubits = 5
ion_spacing = 1.0
x = np.arange(num_qubits) * ion_spacing
y = np.zeros_like(x)

# ==========================
# FUNCTION TO DRAW
# ==========================
def draw_plot(phi):
    fig.clear()
    ax = fig.add_subplot(111)
    ax.scatter(x, y, s=300, c='skyblue', label='Qubits (Ions)')
    for i, xi in enumerate(x):
        ax.text(xi, y[i]+0.1, f'Q{i+1}', ha='center', fontsize=12)

    for xi in x:
        ax.arrow(xi, -0.3, 0.0, 0.2*np.cos(phi), head_width=0.1, head_length=0.05, color='r')
    for i in range(num_qubits-1):
        ax.plot([x[i], x[i+1]], [y[i], y[i+1]], 'k--', alpha=0.5)

    ax.set_title(f'Trapped Ion Processor - phi = {phi:.2f} rad')
    ax.set_ylim(-0.5, 0.5)
    ax.axis('off')
    canvas.draw()

# ==========================
# TKINTER GUI
# ==========================
root = tk.Tk()
root.title("Trapped Ion Quantum Processor Control")

fig = Figure(figsize=(10,4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Slider to control phi
def update(val):
    phi = slider.get()
    draw_plot(phi)

slider = tk.Scale(root, from_=0, to=2*np.pi, resolution=0.05, orient=tk.HORIZONTAL, label="phi (rad)", length=500, command=lambda x: update(x))
slider.pack()

draw_plot(0)  # initial plot
root.mainloop()
