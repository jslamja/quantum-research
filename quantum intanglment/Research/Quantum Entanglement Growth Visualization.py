"""
Quantum Entanglement Growth Visualization — Interactive GUI
-----------------------------------------------------------
A teaching-oriented simulator that animates entanglement entropy growth S_A(t)
for a 1D chain after a quench. It shows:
  • Top panel: a chain of N sites; region A (first L_A sites) is shaded.
    A pair of light-cone fronts (speed v) emanate from the center, indicating
    the causal spread. Color intensity in region A reflects normalized S_A(t)/S_max.
  • Bottom panel: real-time plot of S_A(t) vs time with saturation.

Controls:
  - Play / Pause / Reset
  - Sliders for L_A, v (Lieb-Robinson), v_E (entanglement velocity), gamma (decoherence),
    and dt (simulation step). Mode: Global Quench or Local Quench.

Physics model (simplified, pedagogical):
  S_A(t) = s * min( (2*v_E/gamma)*(1 - exp(-gamma*t))  if gamma>0 else  2*v_E*t , L_A )
  where s=1 bit per entangled pair (unitless here). Saturates at S_max = L_A.

Requirements: Python 3, tkinter, matplotlib, numpy
Run: python entanglement_gui.py
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class EntanglementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Entanglement Growth Visualization")
        self.root.geometry("1100x700")

        # --- State ---
        self.N = 60                 # number of sites
        self.a = 1.0                # lattice spacing (arb. units)
        self.t = 0.0
        self.playing = False
        self.t_data = []
        self.S_data = []

        # --- UI Frames ---
        self.frame_controls = ttk.Frame(root, padding=8)
        self.frame_controls.pack(side=tk.LEFT, fill=tk.Y)

        self.frame_plot = ttk.Frame(root)
        self.frame_plot.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Matplotlib Figure ---
        self.fig = Figure(figsize=(7.8, 5.6), dpi=100)
        self.ax_chain = self.fig.add_subplot(2, 1, 1)
        self.ax_S = self.fig.add_subplot(2, 1, 2)
        self.fig.tight_layout(pad=3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # --- Controls ---
        self._build_controls()

        # --- Precompute chain coordinates ---
        self.x_sites = np.arange(self.N) * self.a
        self.center_x = (self.N - 1) * self.a / 2

        # --- Artists initialization ---
        self._init_chain_plot()
        self._init_S_plot()

        # --- Main loop ---
        self._tick()

    # ===================== Controls =====================
    def _build_controls(self):
        title = ttk.Label(self.frame_controls, text="Controls", font=("Segoe UI", 14, "bold"))
        title.pack(anchor=tk.W, pady=(0, 8))

        # Region size L_A
        ttk.Label(self.frame_controls, text="Region A size L_A").pack(anchor=tk.W)
        self.L_A_var = tk.IntVar(value=12)
        s_la = ttk.Scale(self.frame_controls, from_=2, to=self.N//2, orient=tk.HORIZONTAL,
                         command=lambda e: None, variable=self.L_A_var)
        s_la.pack(fill=tk.X, pady=4)

        # v (LR speed)
        ttk.Label(self.frame_controls, text="Causal speed v").pack(anchor=tk.W)
        self.v_var = tk.DoubleVar(value=2.0)
        s_v = ttk.Scale(self.frame_controls, from_=0.2, to=5.0, orient=tk.HORIZONTAL,
                        command=lambda e: None, variable=self.v_var)
        s_v.pack(fill=tk.X, pady=4)

        # v_E (entanglement velocity)
        ttk.Label(self.frame_controls, text="Entanglement velocity v_E").pack(anchor=tk.W)
        self.vE_var = tk.DoubleVar(value=1.0)
        s_ve = ttk.Scale(self.frame_controls, from_=0.1, to=3.0, orient=tk.HORIZONTAL,
                         command=lambda e: None, variable=self.vE_var)
        s_ve.pack(fill=tk.X, pady=4)

        # gamma (decoherence)
        ttk.Label(self.frame_controls, text="Decoherence rate γ").pack(anchor=tk.W)
        self.gamma_var = tk.DoubleVar(value=0.10)
        s_g = ttk.Scale(self.frame_controls, from_=0.0, to=1.0, orient=tk.HORIZONTAL,
                        command=lambda e: None, variable=self.gamma_var)
        s_g.pack(fill=tk.X, pady=4)

        # dt (step)
        ttk.Label(self.frame_controls, text="Time step dt").pack(anchor=tk.W)
        self.dt_var = tk.DoubleVar(value=0.05)
        s_dt = ttk.Scale(self.frame_controls, from_=0.005, to=0.20, orient=tk.HORIZONTAL,
                         command=lambda e: None, variable=self.dt_var)
        s_dt.pack(fill=tk.X, pady=4)

        # Mode
        ttk.Label(self.frame_controls, text="Quench mode").pack(anchor=tk.W)
        self.mode_var = tk.StringVar(value="Global quench")
        mode_box = ttk.Combobox(self.frame_controls, textvariable=self.mode_var, state="readonly",
                                values=["Global quench", "Local quench"])
        mode_box.pack(fill=tk.X, pady=6)

        # Buttons
        btns = ttk.Frame(self.frame_controls)
        btns.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(btns, text="Play", command=self._play).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(btns, text="Pause", command=self._pause).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)
        ttk.Button(btns, text="Reset", command=self._reset).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Legend / explanation
        expl = (
            "Model:\n"
            "S_A(t) grows with rate v_E and saturates at S_max = L_A.\n"
            "γ>0 slows growth (mimics decoherence).\n"
            "Top: chain, shaded A; moving lines: causal fronts v.\n"
            "Bottom: S_A(t) with current time marker."
        )
        ttk.Label(self.frame_controls, text=expl, wraplength=280, justify=tk.LEFT).pack(anchor=tk.W, pady=10)

    def _play(self):
        self.playing = True

    def _pause(self):
        self.playing = False

    def _reset(self):
        self.playing = False
        self.t = 0.0
        self.t_data.clear()
        self.S_data.clear()
        self._redraw_all()

    # ===================== Plot setup =====================
    def _init_chain_plot(self):
        ax = self.ax_chain
        ax.clear()
        ax.set_title("1D Chain & Causal Spread")
        ax.set_xlim(-1, self.x_sites[-1] + 1)
        ax.set_ylim(-1.5, 1.5)
        ax.get_yaxis().set_visible(False)
        ax.set_xlabel("site index")

        # region A background (updated in redraw)
        self.regionA_patch = None

        # sites scatter
        self.sites_scatter = ax.scatter(self.x_sites, np.zeros_like(self.x_sites), s=40, zorder=3)

        # causal fronts
        self.front_left = ax.axvline(self.center_x, linestyle='--', linewidth=1.5)
        self.front_right = ax.axvline(self.center_x, linestyle='--', linewidth=1.5)

        # text annotations
        self.lbl_t = ax.text(0.01, 0.90, "t = 0.00", transform=ax.transAxes)
        self.lbl_S = ax.text(0.01, 0.80, "S_A = 0.00", transform=ax.transAxes)

    def _init_S_plot(self):
        ax = self.ax_S
        ax.clear()
        ax.set_title("Entanglement Entropy S_A(t)")
        ax.set_xlabel("time t")
        ax.set_ylabel("S_A (arb. units)")
        self.S_line, = ax.plot([], [], lw=2)
        self.S_marker, = ax.plot([], [], 'o')
        ax.grid(True, alpha=0.3)

    # ===================== Physics helpers =====================
    def S_of_t(self, t, L_A, vE, gamma):
        s_per_pair = 1.0
        S_max = s_per_pair * L_A
        if gamma > 1e-9:
            raw = (2.0 * vE / gamma) * (1.0 - np.exp(-gamma * t))
        else:
            raw = 2.0 * vE * t
        return float(min(raw * s_per_pair, S_max))

    def front_positions(self, t, v, mode):
        if mode == "Local quench":
            # single-sided cone (e.g., local perturbation traveling right)
            xR = self.center_x + v * t
            xL = self.center_x
        else:
            # global quench: symmetric cones
            xR = self.center_x + v * t
            xL = self.center_x - v * t
        return max(-10, xL), min(self.x_sites[-1] + 10, xR)

    # ===================== Redraw =====================
    def _redraw_all(self):
        # Read controls
        L_A = int(self.L_A_var.get())
        v = float(self.v_var.get())
        vE = float(self.vE_var.get())
        gamma = float(self.gamma_var.get())
        dt = float(self.dt_var.get())
        mode = self.mode_var.get()

        # Update region A patch
        ax = self.ax_chain
        if self.regionA_patch is not None:
            self.regionA_patch.remove()
        x0 = -0.5
        x1 = (L_A - 0.5) * self.a
        self.regionA_patch = ax.axvspan(x0, x1, alpha=0.15, zorder=1)

        # Update causal fronts
        xL, xR = self.front_positions(self.t, v, mode)
        self.front_left.set_xdata([xL, xL])
        self.front_right.set_xdata([xR, xR])

        # Update labels
        Sval = self.S_of_t(self.t, L_A, vE, gamma)
        self.lbl_t.set_text(f"t = {self.t:.2f}")
        self.lbl_S.set_text(f"S_A = {Sval:.2f}  (S_max={L_A})")

        # Color intensity in region A ~ S/S_max
        intensity = 0.1 + 0.6 * (Sval / max(1e-9, L_A))
        self.sites_scatter.set_color([ (0.2, 0.2, 0.2) for _ in range(self.N) ])
        # highlight region A with intensity using RGBA alpha
        colors = []
        for i in range(self.N):
            if i < L_A:
                colors.append((0.1, 0.5, 0.9, min(1.0, intensity)))
            else:
                colors.append((0.2, 0.2, 0.2, 1.0))
        self.sites_scatter.set_facecolor(colors)

        # Update S(t) plot
        self.ax_S.relim()
        self.ax_S.autoscale_view()
        if len(self.t_data) == 0 or self.t > self.t_data[-1]:
            self.t_data.append(self.t)
            self.S_data.append(Sval)
        self.S_line.set_data(self.t_data, self.S_data)
        self.S_marker.set_data([self.t], [Sval])

        # Dynamic y-limit to include S_max
        ymin, ymax = self.ax_S.get_ylim()
        target = max(ymax, max(self.S_data + [L_A]) * 1.05 if self.S_data else L_A * 1.1)
        if target > ymax:
            self.ax_S.set_ylim(ymin, target)

        # Draw
        self.canvas.draw_idle()

    # ===================== Main loop tick =====================
    def _tick(self):
        if self.playing:
            dt = float(self.dt_var.get())
            # Stop if fully saturated for a while
            L_A = int(self.L_A_var.get())
            vE = float(self.vE_var.get())
            gamma = float(self.gamma_var.get())
            Sval = self.S_of_t(self.t, L_A, vE, gamma)
            if Sval >= L_A - 1e-3 and self.t > 0.5:
                self.playing = False
            else:
                self.t += dt
        self._redraw_all()
        # schedule next tick
        self.root.after(33, self._tick)  # ~30 FPS


def main():
    root = tk.Tk()
    # Use modern ttk theme if available
    try:
        from tkinter import ttk
        s = ttk.Style()
        if "vista" in s.theme_names():
            s.theme_use("vista")
        elif "clam" in s.theme_names():
            s.theme_use("clam")
    except Exception:
        pass
    app = EntanglementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
