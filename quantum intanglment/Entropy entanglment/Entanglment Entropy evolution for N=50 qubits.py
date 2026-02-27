import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# -------------------------
# Physical parameters
# -------------------------
N_qubits = 50           # total number of qubits
v_E = 0.3               # entanglement velocity (chosen realistically < 1)
S_max = (N_qubits / 2) * np.log(2)   # Page value
t_c = N_qubits / v_E    # scrambling/saturation time estimate
fluctuation_strength = 0.05
N_points = 2000

# Time array
t = np.linspace(0, 2*t_c, N_points)

# Base entropy
def base_entropy(t):
    return np.where(t < t_c, v_E * t, S_max)

# More realistic entropy
def realistic_entropy(t):
    # Initial quadratic growth
    quadratic_region = (t < 0.2*t_c)
    S = np.where(quadratic_region, v_E*(t**2)/(0.2*t_c), base_entropy(t))

    # Finite-size rounding
    saturation_region = (t > 0.8*t_c) & (t < 1.2*t_c)
    S = np.where(saturation_region, 
                 S_max - (S_max - v_E*t)*np.exp(-(t-0.8*t_c)/(0.1*t_c)), S)

    # Fluctuations
    fluctuations = fluctuation_strength*np.random.normal(0, 0.2, len(t))
    S += fluctuations

    # Smooth
    S = savgol_filter(S, window_length=101, polyorder=3)

    # Final saturation with thermal wiggles
    S[t > 1.5*t_c] = S_max + 0.02*np.random.normal(0, 1, np.sum(t > 1.5*t_c))

    return S

# Generate entropy curve
S = realistic_entropy(t)

# Plot
plt.figure(figsize=(12, 7))
plt.plot(t, S, 'b-', linewidth=2, label='Simulated $S(t)$')
plt.plot(t, base_entropy(t), 'k--', linewidth=1.5, alpha=0.6, label='Theoretical model')

plt.axvline(t_c, color='r', linestyle='--', alpha=0.6, label='$t_c$')
plt.axhline(S_max, color='g', linestyle='--', alpha=0.6, label='$S_{max}$')

plt.xlabel('Time (t)', fontsize=14)
plt.ylabel('Entanglement Entropy $S(t)$', fontsize=14)
plt.title(f'Entanglement Entropy Evolution for N={N_qubits} qubits', fontsize=16)

plt.legend(fontsize=12, loc='lower right')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('page_entropy_evolution.png', dpi=300)
plt.show()
