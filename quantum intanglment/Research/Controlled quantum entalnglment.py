import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
v0 = 1.0           # v_E^(0)
Delta_v = 0.5      # Delta v
S_max = 10         # S_max
kappa0 = 0.3       # kappa_0
beta = 0.5         # beta
phi_values = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]  # control parameter phi
t = np.linspace(0, 20, 1000)  # time array
# -----------------------------

plt.figure(figsize=(8,5))

for phi in phi_values:
    # Compute phi-dependent parameters
    vE_phi = v0 - Delta_v * np.cos(phi)
    t_c = S_max / vE_phi
    kappa_phi = kappa0 * (1 + beta * np.cos(phi))
    
    # Compute S(t) using piecewise definition
    S = np.where(t <= t_c,
                 vE_phi * t,
                 S_max + vE_phi * (t - t_c) * np.exp(-kappa_phi * (t - t_c))
                )
    
    plt.plot(t, S, label=f'$\phi = {phi:.2f}$ rad')

# Plot formatting
plt.xlabel('Time $t$', fontsize=12)
plt.ylabel('Entanglement Entropy $S(t, \phi)$', fontsize=12)
plt.title('Controlled Entanglement Entropy Growth', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()
