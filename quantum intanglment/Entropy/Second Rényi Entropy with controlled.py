import numpy as np
import matplotlib.pyplot as plt

# ===============================
# Parameters for the simulation
# ===============================
v_E0 = 1.0           # Natural entanglement growth rate (v_E^(0))
Delta_v = 0.6        # Amplitude of control
phi_ctrl_values = [0, np.pi/4, np.pi/2]  # Control phases
t = np.linspace(0, 5, 200)  # Time array

# Function to compute controlled growth rate
def vE_controlled(v_E0, Delta_v, phi_ctrl):
    return v_E0 - Delta_v * np.cos(phi_ctrl)

# ===============================
# Compute S2(t) for natural and controlled cases
# S2(t) ~ v_E * t  (linear approximation for simplicity)
# ===============================
S2_natural = v_E0 * t

plt.figure(figsize=(9,6))
plt.plot(t, S2_natural, label=r"Natural growth $v_E^{(0)} t$", color='black', linewidth=2)

colors = ['red', 'blue', 'green']
for i, phi in enumerate(phi_ctrl_values):
    vE_c = vE_controlled(v_E0, Delta_v, phi)
    S2_controlled = vE_c * t
    plt.plot(t, S2_controlled, linestyle='--', color=colors[i],
             label=fr"Controlled growth $\phi_{{ctrl}}={phi:.2f}$, $v_E={vE_c:.2f}$")

# ===============================
# Add equations on the plot
# ===============================
plt.text(0.1, max(S2_natural)*0.9, 
         r"$S_2(t) \sim v_E \cdot t$" "\n"
         r"$v_E^{\rm controlled} = v_E^{(0)} - \Delta v \cos(\phi_{\rm ctrl})$" "\n"
         r"$v_E$: entanglement growth rate"
         , fontsize=11, bbox=dict(facecolor='white', alpha=0.7))

plt.xlabel("Time t")
plt.ylabel("Second Rényi Entropy S2(t)")
plt.title("Controlled vs Natural Growth of Second Rényi Entropy")
plt.legend()
plt.grid(True)
plt.show()
