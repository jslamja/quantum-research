import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ----- Setup figure -----
fig = plt.figure(figsize=(14, 6))

# Classical particles subplot
ax1 = fig.add_subplot(121)
N_particles = 20
particle_dots, = ax1.plot([], [], 'ro', markersize=8, linestyle="None")
ax1.set_xlim(-0.5, 1.5)
ax1.set_ylim(-0.5, N_particles/2 + 1)
ax1.set_xticks([0, 1])
ax1.set_xticklabels(["State 0", "State 1"])
ax1.set_title("Many Classical Particles (Bits)", fontsize=12)
ax1.set_yticks([])

# Qubits subplot
ax2 = fig.add_subplot(122, projection="3d")
N_qubits = 20
theta = np.linspace(0, np.pi, N_qubits)
phi = np.linspace(0, 2*np.pi, N_qubits)
qubit_arrows = []

# Distribute qubits in a circle layout for clarity
for i in range(N_qubits):
    # initial direction along z-axis
    arrow = ax2.quiver(0, 0, 0, 0, 0, 1, color="blue", linewidth=1)
    qubit_arrows.append(arrow)

ax2.set_title("Many Qubits (Bloch Sphere States)", fontsize=12)
ax2.set_xlim([-1, 1])
ax2.set_ylim([-1, 1])
ax2.set_zlim([-1, 1])
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_zlabel("Z")

# ----- Update function -----
def update(frame):
    global qubit_arrows

    # --- Classical Particles ---
    positions_x = []
    positions_y = []
    for i in range(N_particles):
        pos = 0 if (frame // 30 + i) % 2 == 0 else 1
        positions_x.append(pos)
        positions_y.append(i/2)
    particle_dots.set_data(positions_x, positions_y)

    # --- Qubits ---
    for i, arrow in enumerate(qubit_arrows):
        arrow.remove()

    qubit_arrows.clear()

    for i in range(N_qubits):
        th = 0.05*frame + i*0.2
        ph = 0.07*frame + i*0.3

        x = np.sin(th) * np.cos(ph)
        y = np.sin(th) * np.sin(ph)
        z = np.cos(th)

        color = (0.5+0.5*np.cos(ph),
                 0.5+0.5*np.sin(th),
                 0.5+0.5*np.sin(ph))

        arrow = ax2.quiver(0, 0, 0, x, y, z, color=color, linewidth=1)
        qubit_arrows.append(arrow)

    return particle_dots, qubit_arrows

# ----- Run Animation -----
ani = FuncAnimation(fig, update, frames=300, interval=80, blit=False)

plt.tight_layout()
plt.show()
