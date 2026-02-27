import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# System parameters
v_E = 1.0                # Base entanglement velocity
t_c = 5.0                # Critical time (saturation time)
S_max = 5.0              # Maximum entropy
N = 1000                 # Number of time points
fluctuation_strength = 0.15  # Quantum fluctuation strength

# Time array with finer resolution near t_c
t = np.linspace(0, 10, N)

# Base entropy function
def base_entropy(t):
    return np.where(t < t_c, v_E * t, S_max)

# Add realistic effects
def realistic_entropy(t):
    # 1. Initial quadratic growth (before linear regime)
    quadratic_region = (t < 0.2*t_c)
    S = np.where(quadratic_region, v_E*(t**2)/(0.2*t_c), base_entropy(t))
    
    # 2. Finite-size rounding near saturation
    saturation_region = (t > 0.8*t_c) & (t < 1.2*t_c)
    S = np.where(saturation_region, S_max - (S_max - v_E*t)*np.exp(-(t-0.8*t_c)/(0.1*t_c)), S)
    
    # 3. Add quantum fluctuations
    fluctuations = fluctuation_strength*np.random.normal(0, 0.1, len(t))
    S += fluctuations
    
    # 4. Smooth the curve (emulating collective effects)
    S = savgol_filter(S, window_length=51, polyorder=3)
    
    # 5. Final saturation with small thermal fluctuations
    S[t > 1.5*t_c] = S_max + 0.02*np.random.normal(0, 1, np.sum(t > 1.5*t_c))
    
    return S

# Generate entropy data
S = realistic_entropy(t)

# Create the plot
plt.figure(figsize=(12, 7))

# Plot entropy curve with realistic effects
plt.plot(t, S, 'b-', linewidth=2, label='Simulated S(t)')
plt.plot(t, base_entropy(t), 'k--', alpha=0.5, linewidth=1.5, label='Theoretical S(t)')

# Add guide lines and annotations
plt.axvline(t_c, color='r', linestyle='--', alpha=0.5)
plt.axhline(S_max, color='g', linestyle='--', alpha=0.5)

# Mark critical point
plt.plot(t_c, S_max, 'ro', markersize=8)

# Add annotations with LaTeX
plt.text(t_c + 0.2, 0.8, r'$t_c$ (scrambling time)', fontsize=12, color='r')
plt.text(0.3, S_max + 0.1, r'$S_{max}$ (Page value)', fontsize=12, color='g')
plt.text(1.5, 2.5, r'$S(t) \approx v_E t$', fontsize=14, bbox=dict(facecolor='white', alpha=0.8))
plt.text(7.5, 4.7, 'Saturation with\nthermal fluctuations', fontsize=12, 
         bbox=dict(facecolor='white', alpha=0.8))

# Highlight physical effects
plt.axvspan(0, 0.2*t_c, color='yellow', alpha=0.1, label='Initial quadratic growth')
plt.axvspan(0.8*t_c, 1.2*t_c, color='orange', alpha=0.1, label='Finite-size rounding')

# Axis labels and title
plt.xlabel('Time (t)', fontsize=14)
plt.ylabel('Entanglement Entropy S(t)', fontsize=14)
plt.title('Realistic Simulation of Entanglement Entropy Evolution\nin a Closed Quantum System', fontsize=16)

# Legend and grid
plt.legend(fontsize=12, loc='lower right')
plt.grid(True, linestyle='--', alpha=0.6)

# Set limits and save
plt.xlim(0, 10)
plt.ylim(0, 5.5)
plt.tight_layout()
plt.savefig('realistic_entropy_evolution.png', dpi=300, bbox_inches='tight')
plt.show()