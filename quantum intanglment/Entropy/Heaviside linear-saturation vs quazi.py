import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
t_max = 10.0      # أقصى وقت
dt = 0.01         # خطوة زمنية
t = np.arange(0, t_max, dt)

# --- Heaviside segmented linear model ---
v_E = 1.0
S_max = 5.0
t_c = S_max / v_E

S_heaviside = v_E * t * (t < t_c) + S_max * (t >= t_c)

# --- Simplified quasiparticle model ---
# نأخذ توزيع ثابت f(p',p'')=1 وسرعات ثابتة v(p)=v_max
v_max = 1.0
ell = S_max  # طول النظام يتوافق مع S_max لتقريب التشبع
S_qp = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < ell / (2 * v_max):
        S_qp[i] = 2 * v_max * ti  # linear growth
    else:
        S_qp[i] = ell               # saturation

# --- Plot comparison ---
plt.figure(figsize=(8,5))
plt.plot(t, S_heaviside, label="Heaviside Linear-Saturation", lw=2)
plt.plot(t, S_qp, label="Simplified Quasiparticle Model", lw=2, linestyle='--')
plt.axvline(x=t_c, color='gray', linestyle=':', label="Saturation time t_c")
plt.xlabel("Time")
plt.ylabel("Entanglement Entropy S(t)")
plt.title("Comparison of Entanglement Entropy Models")
plt.legend()
plt.grid(True)
plt.show()
