import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# ----- Setup figure -----
fig = plt.figure(figsize=(12, 6))

# Classical particle subplot
ax1 = fig.add_subplot(121)
particle_dot, = ax1.plot([], [], 'ro', markersize=14)
ax1.set_xlim(-0.5, 1.5)
ax1.set_ylim(-0.5, 0.5)
ax1.set_xticks([0, 1])
ax1.set_xticklabels(["State 0", "State 1"])
ax1.set_yticks([])
ax1.set_title("Classical Particle (Bit)", fontsize=12)

# Qubit subplot (Bloch Sphere)
ax2 = fig.add_subplot(122, projection="3d")
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(0, np.pi, 30)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax2.plot_wireframe(x, y, z, color='lightgray', linewidth=0.5)

# Initial qubit arrow
qubit_arrow = ax2.quiver(0, 0, 0, 0, 0, 1, color="blue", linewidth=2)

ax2.set_title("Qubit (Bloch Sphere)", fontsize=12)
ax2.set_xlim([-1, 1])
ax2.set_ylim([-1, 1])
ax2.set_zlim([-1, 1])
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_zlabel("Z")

# ----- Update function for animation -----
def update(frame):
    global qubit_arrow

    # --- Classical Particle ---
    pos = 0 if frame % 60 < 30 else 1  # alternate between 0 and 1
    particle_dot.set_data([pos], [0])

    # --- Qubit Arrow (rotating vector) ---
    theta = frame * 0.05   # polar angle (slow rotation)
    phi = frame * 0.07     # azimuthal angle

    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    # Change color smoothly (RGB based on angles)
    color = (0.5 + 0.5 * np.cos(phi),
             0.5 + 0.5 * np.sin(theta),
             0.5 + 0.5 * np.sin(phi))

    # Remove old arrow and draw new one
    qubit_arrow.remove()
    qubit_arrow = ax2.quiver(0, 0, 0, x, y, z, color=color, linewidth=2)

    return particle_dot, qubit_arrow

# ----- Run Animation -----
ani = FuncAnimation(fig, update, frames=300, interval=80, blit=False)

plt.tight_layout()
plt.show()
