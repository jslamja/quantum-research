import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)

# ============ General Settings ============
FPS = 30
DURATION_SEC = 12
FRAMES = FPS * DURATION_SEC
INTERVAL_MS = 1000 / FPS
np.random.seed(42)

# Enable this to save the animation as GIF (requires pillow)
SAVE_GIF = False
GIF_NAME = "bit_vs_qubit.gif"

# ============ Figure Layout ============
plt.rcParams["figure.figsize"] = (12, 5)
plt.rcParams["figure.dpi"] = 120

fig = plt.figure()
ax_bit = fig.add_subplot(1, 2, 1)            # Classical bit (2D)
ax_bloch = fig.add_subplot(1, 2, 2, projection='3d')  # Bloch sphere (3D)

fig.suptitle("Classical Bit vs Qubit (Bloch Sphere)", fontsize=14, y=0.98)

# ============ Classical Bit Panel ============
ax_bit.set_xlim(-0.2, 1.2)
ax_bit.set_ylim(-0.2, 1.2)
ax_bit.set_aspect('equal', adjustable='box')
ax_bit.axis('off')

# Two boxes for states 0 and 1
rect0 = plt.Rectangle((0.0, 0.2), 0.45, 0.6, fill=False, linewidth=2)
rect1 = plt.Rectangle((0.55, 0.2), 0.45, 0.6, fill=False, linewidth=2)
ax_bit.add_patch(rect0)
ax_bit.add_patch(rect1)
ax_bit.text(0.225, 0.85, "0", ha='center', va='center', fontsize=16)
ax_bit.text(0.775, 0.85, "1", ha='center', va='center', fontsize=16)

# Moving dot ("coin flip")
coin_dot, = ax_bit.plot([0.5], [0.5], 'o', markersize=10)

# Text labels
ax_bit.text(0.5, 1.05, "Classical Bit", ha='center', va='center', fontsize=12, transform=ax_bit.transAxes)
bit_state_txt = ax_bit.text(0.5, 0.08, "", ha='center', va='center', fontsize=10, transform=ax_bit.transAxes)

# Measurement schedule for the classical bit
measure_period = 4.0   # every 4 seconds
collapse_window = 1.5  # during first 1.5s, the coin "spins"
meas_outcome = None    # None while spinning, then 0 or 1

# ============ Bloch Sphere ============
# Wireframe sphere
u = np.linspace(0, 2*np.pi, 40)
v = np.linspace(0, np.pi, 20)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones_like(u), np.cos(v))
ax_bloch.plot_wireframe(x, y, z, linewidth=0.4, alpha=0.5)

# Axes
ax_bloch.quiver(0, 0, 0, 1.0, 0, 0, length=1.0, arrow_length_ratio=0.1, linewidth=1)
ax_bloch.quiver(0, 0, 0, 0, 1.0, 0, length=1.0, arrow_length_ratio=0.1, linewidth=1)
ax_bloch.quiver(0, 0, 0, 0, 0, 1.0, length=1.0, arrow_length_ratio=0.1, linewidth=1)
ax_bloch.text(1.1, 0, 0, 'X')
ax_bloch.text(0, 1.1, 0, 'Y')
ax_bloch.text(0, 0, 1.1, 'Z')

# State vector (qubit) — starts at |0>
state_vec = ax_bloch.quiver(0, 0, 0, 0, 0, 1, length=1.0, arrow_length_ratio=0.15, linewidth=3)

# Labels |0> and |1>
ax_bloch.text(0, 0, 1.15, r"|0⟩", ha='center', va='center', fontsize=12)
ax_bloch.text(0, 0, -1.2, r"|1⟩", ha='center', va='center', fontsize=12)

ax_bloch.set_box_aspect([1, 1, 1])
ax_bloch.set_xlim([-1.2, 1.2])
ax_bloch.set_ylim([-1.2, 1.2])
ax_bloch.set_zlim([-1.2, 1.2])
ax_bloch.set_title("Qubit on the Bloch Sphere", pad=10, fontsize=12)
ax_bloch.set_xticks([])
ax_bloch.set_yticks([])
ax_bloch.set_zticks([])

# Text showing probabilities
bloch_prob_txt = ax_bloch.text2D(0.05, 0.92, "", transform=ax_bloch.transAxes, fontsize=10)

# Helper: Bloch vector
def bloch_vector(theta, phi):
    # |ψ⟩ = cos(θ/2)|0⟩ + e^{iφ} sin(θ/2)|1⟩
    # Bloch coordinates: (x, y, z) = (sinθ cosφ, sinθ sinφ, cosθ)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return x, y, z

# Motion for the classical "coin"
def bit_coin_motion(t_in_period):
    x = 0.5 + 0.45 * np.sin(2*np.pi * 1.3 * t_in_period)  # horizontal oscillation
    y = 0.5 + 0.20 * np.sin(2*np.pi * 3.7 * t_in_period)  # vertical wobble
    return x, y

def update(frame):
    global meas_outcome, state_vec

    # ---- Classical Bit ----
    t = frame / FPS
    t_in_period = t % measure_period

    ax_bit.patches[0].set_linewidth(2)
    ax_bit.patches[1].set_linewidth(2)

    if t_in_period < collapse_window:
        # "Spinning" phase
        meas_outcome = None
        x, y = bit_coin_motion(t_in_period / collapse_window)
        coin_dot.set_data([x], [y])
        bit_state_txt.set_text("Coin is spinning — no measurement yet")
    else:
        # Measurement
        if meas_outcome is None:
            meas_outcome = np.random.choice([0, 1], p=[0.5, 0.5])

        if meas_outcome == 0:
            coin_dot.set_data([0.225], [0.5])
            ax_bit.patches[0].set_linewidth(4)
            bit_state_txt.set_text("Measurement result: 0")
        else:
            coin_dot.set_data([0.775], [0.5])
            ax_bit.patches[1].set_linewidth(4)
            bit_state_txt.set_text("Measurement result: 1")

    # ---- Qubit on Bloch Sphere ----
    # θ oscillates, φ rotates
    theta = (np.pi/2) * (1 + np.sin(2*np.pi * (t / 6.0)))
    phi = 2*np.pi * (t / 5.0)

    vx, vy, vz = bloch_vector(theta, phi)

    # Replace the old state vector
    state_vec.remove()
    state_vec = ax_bloch.quiver(0, 0, 0, vx, vy, vz, length=1.0, arrow_length_ratio=0.15, linewidth=3)

    # Probabilities: P(0)=cos²(θ/2), P(1)=sin²(θ/2)
    p0 = np.cos(theta/2.0)**2
    p1 = 1.0 - p0
    bloch_prob_txt.set_text(f"P(|0⟩) = {p0:.2f},  P(|1⟩) = {p1:.2f}")

    return coin_dot, state_vec

# Create animation
anim = FuncAnimation(fig, update, frames=FRAMES, interval=INTERVAL_MS, blit=False)

# Optional: save as GIF
if SAVE_GIF:
    try:
        from matplotlib.animation import PillowWriter
        anim.save(GIF_NAME, writer=PillowWriter(fps=FPS))
        print(f"Saved animation to {GIF_NAME}")
    except Exception as e:
        print("Failed to save GIF. Install pillow. Error:", e)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
