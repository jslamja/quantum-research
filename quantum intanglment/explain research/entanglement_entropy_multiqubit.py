import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import unitary_group
from scipy.linalg import eigh
import tkinter as tk
from tkinter import ttk

# ----------------- Utility functions -----------------
def kron_n(ops):
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out

def partial_trace(rho, sys_dims, keep):
    dims = sys_dims
    N = len(dims)
    shape = dims + dims
    rho_tensor = rho.reshape(shape)
    keep = list(keep)
    trace_out = [i for i in range(N) if i not in keep]
    perm = keep + trace_out + [i + N for i in keep] + [i + N for i in trace_out]
    rho_perm = np.transpose(rho_tensor, perm)
    d_keep = int(np.prod([dims[i] for i in keep])) if keep else 1
    d_trace = int(np.prod([dims[i] for i in trace_out])) if trace_out else 1
    rho_perm = rho_perm.reshape((d_keep, d_trace, d_keep, d_trace))
    rho_red = np.zeros((d_keep, d_keep), dtype=complex)
    for i in range(d_trace):
        rho_red += rho_perm[:, i, :, i]
    return rho_red

def von_neumann_entropy(rho, base=2):
    vals = np.real(eigh(rho, eigvals_only=True))
    vals = np.clip(vals, 0, 1)
    nz = vals[vals > 1e-12]
    if len(nz) == 0:
        return 0.0
    return -np.sum(nz * np.log(nz) / np.log(base))

# ----------------- State constructors -----------------
zero = np.array([1,0], dtype=complex)
one  = np.array([0,1], dtype=complex)

def product_state(bitstring):
    vecs = [zero if b==0 else one for b in bitstring]
    return kron_n(vecs)

def ghz_state(N):
    psi0 = product_state([0]*N)
    psi1 = product_state([1]*N)
    return (psi0 + psi1)/np.sqrt(2)

def w_state(N):
    states = []
    for i in range(N):
        b = [0]*N
        b[i] = 1
        states.append(product_state(b))
    psi = sum(states)
    return psi/np.linalg.norm(psi)

def random_haar_state(N):
    dim = 2**N
    U = unitary_group.rvs(dim)
    return U[:,0]

def entropies_for_state(psi, N, step=1):
    rho = np.outer(psi, psi.conj())
    dims = [2]*N
    entropies = []
    ks = list(range(1, N//2 + 1, step))
    for k in ks:
        keep = list(range(k))
        rhoA = partial_trace(rho, dims, keep)
        entropies.append(von_neumann_entropy(rhoA))
    return ks, entropies

# ----------------- Tkinter GUI -----------------
class EntanglementComparisonGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualize Entanglement Entropy")
        
        # أربع فئات حسب عدد الجسيمات (خفض N الكبير لتجنب توقف)
        self.N_list = [3, 6, 12, 14]  # آخر فئة 14 بدل 18
        self.N_labels = [
            "Few particles (<4)",
            "Moderate particles (4-8)",
            "Many particles (8-16)",
            "Very large system (>12)"
        ]
        
        self.states = ["Product |000...>", "GHZ", "W", "Random Haar"]
        
        # Figure
        self.fig, self.ax = plt.subplots(figsize=(7,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()
        
        # ComboBox لاختيار الفئة
        self.combo = ttk.Combobox(master, values=self.N_labels, state="readonly")
        self.combo.current(0)
        self.combo.pack(pady=10)
        self.combo.bind("<<ComboboxSelected>>", self.update_plot)
        
        # نص أسفل الرسم لتوضيح الملاحظات
        self.note_label = tk.Label(master, text="", justify=tk.LEFT, wraplength=700)
        self.note_label.pack(pady=10)
        
        self.plot_current(0)
    
    def plot_current(self, index):
        self.ax.clear()
        N = self.N_list[index]
        label = self.N_labels[index]
        step = 1 if N <=8 else 2  # تسريع للأنظمة الكبيرة
        
        for state_name in self.states:
            if state_name == "Product |000...>":
                psi = product_state([0]*N)
            elif state_name == "GHZ":
                psi = ghz_state(N)
            elif state_name == "W":
                psi = w_state(N)
            elif state_name == "Random Haar":
                psi = random_haar_state(N)
            ks, ents = entropies_for_state(psi, N, step=step)
            self.ax.plot(ks, ents, marker='o', label=state_name)
        
        self.ax.set_xlabel("Subsystem size k (first k qubits)")
        self.ax.set_ylabel("Von Neumann Entropy S(ρ_A) (ebits)")
        self.ax.set_title(f"Entanglement Entropy | {label} | N={N}")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()
        
        # إضافة ملاحظات أسفل الرسم
        note_text = f"Symbols explanation:\n"
        note_text += "  S(ρ_A): Von Neumann entropy of subsystem A\n"
        note_text += "  k: number of qubits in the subsystem\n"
        note_text += "States:\n"
        note_text += "  Product: unentangled state |000...>\n"
        note_text += "  GHZ: maximally entangled state (|00..0> + |11..1>)/√2\n"
        note_text += "  W: single-excitation symmetric superposition\n"
        note_text += "  Random Haar: random pure state\n\n"
        note_text += f"Observation:\n"
        note_text += "  - As N increases, entanglement entropy grows and differences between states become more pronounced.\n"
        note_text += "  - Product state remains low entropy, GHZ quickly reaches high entropy for small subsystems.\n"
        note_text += "  - W and Random Haar show intermediate behavior.\n"
        note_text += f"  - Current system size category: {label}\n"
        self.note_label.config(text=note_text)
    
    def update_plot(self, event):
        index = self.combo.current()
        self.plot_current(index)

# ----------------- Main -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EntanglementComparisonGUI(root)
    root.mainloop()
