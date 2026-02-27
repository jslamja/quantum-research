"""
Explaining v_E — Entanglement Entropy Growth Rate (Python)
---------------------------------------------------------
This script visualizes how the entanglement-entropy growth rate v_E controls the
speed at which S_A(t) increases and saturates at S_max = L_A.

Two views are provided:
  1) Static comparison of S_A(t) for multiple v_E values (with optional decoherence gamma).
  2) An animation with a causal front (speed v) and a live S_A(t) marker showing growth.

Model (pedagogical):
  If gamma == 0:   S_A(t) = min( 2 * v_E * t, L_A )
  If gamma > 0:    S_A(t) = min( (2*v_E/gamma) * (1 - exp(-gamma*t)), L_A )

Dependencies: numpy, matplotlib
Run: python explain_vE.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ===================== Parameters =====================
L_A = 12.0        # size/capacity of region A (sets S_max)
vs = [0.5, 1.0, 2.0]  # three example entanglement velocities v_E
v_causal = 2.0    # causal/Lieb-Robinson-like speed for fronts in the animation
Gamma = 0.0       # set to e.g. 0.15 to show saturation slowdown from decoherence
T_max = 10.0
N_t = 400

# ===================== Model =====================
def S_of_t(t, vE, L_A=L_A, gamma=Gamma):
    if gamma > 1e-12:
        raw = (2.0 * vE / gamma) * (1.0 - np.exp(-gamma * t))
    else:
        raw = 2.0 * vE * t
    return np.minimum(raw, L_A)

# ===================== Figure layout =====================
fig = plt.figure(figsize=(10, 6))
gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1.0], width_ratios=[3, 2], hspace=0.55, wspace=0.35)

ax_anim = fig.add_subplot(gs[0, 0])
ax_curve = fig.add_subplot(gs[1, 0])
ax_explain = fig.add_subplot(gs[:, 1])

# ===================== Panel 1: Animation =====================
# A simple 1D chain visual with a shaded region A and moving fronts.
N_sites = 60
x = np.arange(N_sites)
center = (N_sites - 1) / 2

ax_anim.set_title("Causal Spread & Entanglement Growth")
ax_anim.set_xlim(-1, N_sites)
ax_anim.set_ylim(-1.5, 1.5)
ax_anim.get_yaxis().set_visible(False)
ax_anim.set_xlabel("Site index (Region A = shaded)")

regionA = ax_anim.axvspan(-0.5, L_A - 0.5, alpha=0.15)
pts = ax_anim.scatter(x, np.zeros_like(x), s=30)

left_line = ax_anim.axvline(center, linestyle='--', linewidth=1.25)
right_line = ax_anim.axvline(center, linestyle='--', linewidth=1.25)

lbl_t = ax_anim.text(0.02, 0.88, "t = 0.00", transform=ax_anim.transAxes)
lbl_S = ax_anim.text(0.02, 0.78, "S_A = 0.00", transform=ax_anim.transAxes)

# we'll animate the case v_E = vs[1] as the "representative" run
vE_anim = vs[1]

t_grid = np.linspace(0, T_max, N_t)
S_series = S_of_t(t_grid, vE_anim)

# ===================== Panel 2: S_A(t) curves =====================
ax_curve.set_title("Entanglement Entropy S_A(t) for different v_E")
ax_curve.set_xlabel("time t")
ax_curve.set_ylabel("S_A (arb. units)")
ax_curve.grid(True, alpha=0.3)

for vE in vs:
    S_vals = S_of_t(t_grid, vE)
    ax_curve.plot(t_grid, S_vals, label=f"v_E = {vE}")

ax_curve.axhline(L_A, linestyle=':', linewidth=1)
ax_curve.text(T_max*0.98, L_A*1.01, r"$S_{max}=L_A$", ha='right', va='bottom')
ax_curve.legend(title="Growth rate v_E")

# Marker that follows the animated run
(line_marker,) = ax_curve.plot([], [], 'o')

# ===================== Panel 3: Explanation =====================
ax_explain.axis('off')
explain_text = (
    r"$\\textbf{Key idea:}$ The parameter $v_E$ sets the $\\textbf{speed}$ at which entanglement entropy grows.\\n"
    r"$\\;$• For $\\gamma=0$, $S_A(t) = \\min(2 v_E t, L_A)$: slope $2 v_E$ until saturating at $L_A$.\\n"
    r"$\\;$• For $\\gamma>0$, $S_A(t) = \\min(\\frac{2 v_E}{\\gamma}(1-e^{-\\gamma t}), L_A)$: initial slope $2 v_E$, then exponential saturation.\\n"
    r"$\\;$• Bigger $v_E$ ⇒ faster rise, earlier saturation. Smaller $v_E$ ⇒ slower information spread.\\n"
    r"$\\;$• $v_E$ is a $\\textit{growth-rate indicator}$ for how quickly quantum information propagates into region $A$."
)
ax_explain.text(0.02, 0.98, explain_text, va='top', ha='left', fontsize=11, family='monospace')

# ===================== Animation function =====================
def init_anim():
    left_line.set_xdata([center, center])
    right_line.set_xdata([center, center])
    lbl_t.set_text("t = 0.00")
    lbl_S.set_text("S_A = 0.00")
    line_marker.set_data([], [])
    return left_line, right_line, lbl_t, lbl_S, line_marker


def update(frame):
    t = t_grid[frame]
    # move fronts
    xR = center + v_causal * t
    xL = center - v_causal * t
    left_line.set_xdata([xL, xL])
    right_line.set_xdata([xR, xR])

    # compute S(t)
    S_val = S_series[frame]
    lbl_t.set_text(f"t = {t:.2f}")
    lbl_S.set_text(f"S_A = {S_val:.2f}  (S_max={L_A:.0f})")

    # update marker on S(t) plot
    line_marker.set_data([t], [S_val])
    return left_line, right_line, lbl_t, lbl_S, line_marker


ani = FuncAnimation(fig, update, frames=N_t, init_func=init_anim, interval=25, blit=False, repeat=True)

if __name__ == "__main__":
    plt.show()
