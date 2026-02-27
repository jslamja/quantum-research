import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches

# =============================================
# Quantum Information Spread Simulation
# Visualizes how quantum information propagates 
# through a system of qubits over time
# =============================================

# System parameters
N = 10  # Number of qubits in each dimension
v_E = 0.8  # Quantum information speed (light cone slope)
t_c = 5.0  # Critical saturation time
S_max = 10.0  # Maximum entanglement entropy

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={'width_ratios': [2, 1]})
fig.suptitle('Quantum Information Propagation in Qubit Array', fontsize=16, y=0.98)
plt.subplots_adjust(wspace=0.25)

# Initialize qubit array
qubits = np.zeros((N, N))
qubits[N//2, N//2] = 1  # Start with center qubit "excited"

# Initialize entanglement entropy matrix
entropy = np.zeros((N, N))

# Custom color map for visualization
colors = [(0, 0, 0.5), (0, 0.5, 1), (0, 1, 1), (1, 1, 0), (1, 0.5, 0), (1, 0, 0)]
cmap = LinearSegmentedColormap.from_list('quantum_cmap', colors, N=256)

# =============================================
# Qubit Array Visualization (Left Panel)
# =============================================
qubit_plot = ax1.imshow(qubits, cmap='binary', vmin=0, vmax=1, interpolation='nearest')
entropy_plot = ax1.imshow(entropy, cmap=cmap, alpha=0.7, vmin=0, vmax=S_max, interpolation='nearest')

# Add grid lines to show qubit boundaries
ax1.grid(which='major', color='gray', linestyle='-', linewidth=1, alpha=0.3)
ax1.set_xticks(np.arange(-0.5, N, 1))
ax1.set_yticks(np.arange(-0.5, N, 1))
ax1.set_xticklabels([])
ax1.set_yticklabels([])
ax1.set_title('Qubit Array: Information Spread', fontsize=14)

# Add explanatory annotations
ax1.text(0.02, 0.95, 'White = Active qubit\nColor = Entanglement strength', 
         transform=ax1.transAxes, fontsize=10, color='white',
         bbox=dict(facecolor='black', alpha=0.7))

# Add initial state annotation
init_note = ax1.text(N//2-0.5, N//2-1.5, 'Initial excited qubit', 
                    color='white', fontsize=9, ha='center')

# =============================================
# Entropy Growth Curve (Right Panel)
# =============================================
time_points = []
entropy_points = []
line, = ax2.plot([], [], 'b-', linewidth=2)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, S_max * 1.1)
ax2.set_xlabel('Time', fontsize=12)
ax2.set_ylabel('Entanglement Entropy', fontsize=12)
ax2.set_title('Entropy Growth Dynamics', fontsize=14)
ax2.grid(True, linestyle='--', alpha=0.7)

# Add critical lines and labels
ax2.axvline(t_c, color='r', linestyle='--', alpha=0.5)
ax2.axhline(S_max, color='g', linestyle='--', alpha=0.5)
ax2.text(t_c + 0.1, 0.5, 'Saturation Time (t_c)', color='r', fontsize=10)
ax2.text(0.5, S_max + 0.2, 'Max Entropy (S_max)', color='g', fontsize=10)

# Add phase indicators
linear_patch = patches.Rectangle((0.05, 0.7), 0.4, 0.2, transform=ax2.transAxes, 
                               facecolor='blue', alpha=0.1)
saturation_patch = patches.Rectangle((0.55, 0.7), 0.4, 0.2, transform=ax2.transAxes,
                                   facecolor='red', alpha=0.1)
ax2.add_patch(linear_patch)
ax2.add_patch(saturation_patch)
ax2.text(0.25, 0.8, 'Linear Growth', transform=ax2.transAxes, 
        ha='center', fontsize=10)
ax2.text(0.75, 0.8, 'Saturation', transform=ax2.transAxes,
        ha='center', fontsize=10)

# Add colorbar for entanglement strength
cbar = fig.colorbar(entropy_plot, ax=ax1, shrink=0.8)
cbar.set_label('Entanglement Strength', fontsize=10)

# Time and entropy display
time_text = ax1.text(0.02, 0.85, 'Time: 0.00', transform=ax1.transAxes, 
                    fontsize=11, color='white', bbox=dict(facecolor='black', alpha=0.7))
entropy_text = ax1.text(0.02, 0.80, 'Entropy: 0.00', transform=ax1.transAxes,
                       fontsize=11, color='white', bbox=dict(facecolor='black', alpha=0.7))

# =============================================
# Animation Update Function
# =============================================
def update(frame):
    t = frame * 0.2  # Real time
    
    # Calculate total entropy
    if t < t_c:
        total_entropy = min(v_E * t, S_max)
        phase = "Linear Growth Phase"
    else:
        total_entropy = S_max
        phase = "Saturation Phase"
    
    # Update information spread
    if t < t_c:
        # Linear growth phase - information spreads outward
        radius = int(v_E * t * 2)  # Information front radius
        
        # Update qubit states within light cone
        for i in range(N):
            for j in range(N):
                distance = np.sqrt((i - N//2)**2 + (j - N//2)**2)
                if distance <= radius:
                    qubits[i, j] = min(1.0, distance / (radius + 1e-5))
                    entropy[i, j] = total_entropy * (1 - distance/(radius + 1e-5))
        
        # Update information front annotation
        if hasattr(update, 'front_note'):
            update.front_note.remove()
        update.front_note = ax1.text(N//2, N//2+radius+0.7, 'Information Front', 
                                    color='yellow', ha='center', fontsize=9)
    else:
        # Saturation phase - system fully entangled
        for i in range(N):
            for j in range(N):
                distance = np.sqrt((i - N//2)**2 + (j - N//2)**2)
                qubits[i, j] = 1.0
                # Small thermal fluctuations
                entropy[i, j] = S_max * (0.95 + 0.1 * np.sin(t + i + j))
    
    # Update plots
    qubit_plot.set_data(qubits)
    entropy_plot.set_data(entropy)
    
    # Update entropy curve
    time_points.append(t)
    entropy_points.append(total_entropy)
    line.set_data(time_points, entropy_points)
    
    # Update annotations
    time_text.set_text(f'Time: {t:.2f}\nPhase: {phase}')
    entropy_text.set_text(f'Entropy: {total_entropy:.2f}')
    
    # Remove initial note after first frame
    if frame == 1:
        init_note.remove()
    
    return qubit_plot, entropy_plot, line, time_text, entropy_text

# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=100, blit=False)

plt.tight_layout()
plt.show()