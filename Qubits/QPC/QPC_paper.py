import tkinter as tk
import random

# إعداد النافذة
root = tk.Tk()
root.title("Quantum Chip Visualization")
root.geometry("1200x700")
root.configure(bg="#0b0f1a")

canvas = tk.Canvas(root, width=1100, height=600, bg="#0b0f1a", highlightthickness=0)
canvas.pack(pady=20)

# رسم الرقاقة
chip_x1, chip_y1 = 100, 100
chip_x2, chip_y2 = 1000, 500

canvas.create_rectangle(
    chip_x1, chip_y1, chip_x2, chip_y2,
    fill="#1e1e2f", outline="#888", width=3
)

canvas.create_text(
    550, 70,
    text="Superconducting Quantum Chip (50 Qubits)",
    fill="white",
    font=("Arial", 18, "bold")
)

qubits = []

# إعداد الشبكة
rows, cols = 5, 10
qx_spacing = (chip_x2 - chip_x1) // (cols + 1)
qy_spacing = (chip_y2 - chip_y1) // (rows + 1)

def toggle_qubit(qubit):
    state = random.choice([0, 1])
    color = "green" if state == 0 else "red"
    canvas.itemconfig(qubit["glow"], fill=color)

# رسم الكيوبتات
for r in range(rows):
    for c in range(cols):
        cx = chip_x1 + (c + 1) * qx_spacing
        cy = chip_y1 + (r + 1) * qy_spacing

        # جسم الكيوبت
        body = canvas.create_rectangle(
            cx - 25, cy - 15, cx + 25, cy + 15,
            fill="#c9a227", outline="#ffd700"
        )

        # حلقتان (∞)
        canvas.create_oval(cx - 18, cy - 10, cx - 2, cy + 10, outline="black", width=2)
        canvas.create_oval(cx + 2, cy - 10, cx + 18, cy + 10, outline="black", width=2)

        # النقطة الكمومية
        glow = canvas.create_oval(
            cx - 5, cy - 5, cx + 5, cy + 5,
            fill="blue", outline=""
        )

        # جهاز القراءة
        canvas.create_oval(
            cx + 30, cy - 5, cx + 40, cy + 5,
            fill="#00ffff"
        )

        # سلك التحكم
        canvas.create_line(
            cx, chip_y1 - 40, cx, cy - 15,
            fill="#aaaaaa", width=1
        )

        qubit = {"body": body, "glow": glow}
        canvas.tag_bind(body, "<Button-1>", lambda e, q=qubit: toggle_qubit(q))
        canvas.tag_bind(glow, "<Button-1>", lambda e, q=qubit: toggle_qubit(q))

        qubits.append(qubit)

# شرح
canvas.create_text(
    550, 540,
    text="Click on any qubit to simulate measurement (green=|0⟩, red=|1⟩)",
    fill="#cccccc",
    font=("Arial", 12)
)

root.mainloop()
