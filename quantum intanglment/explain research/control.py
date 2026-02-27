import numpy as np
import matplotlib.pyplot as plt

# ==========================
# PARAMETERS (user-defined)
# ==========================
S_max = 10.0          # الحد الأقصى للانتروبيا
v_E0 = 1.0            # معدل النمو الأساسي
Delta_v = 0.5         # تعديل التحكم في النمو
kappa0 = 0.8          # معدل الانحدار بعد التشبع
beta = 0.3            # قوة تأثير التحكم بعد التشبع

# اختيار قيم مختلفة للطور φ لتوضيح التحكم
phi_values = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
colors = ['r','g','b','c','m']

# ==========================
# TIME ARRAY
# ==========================
t = np.linspace(0, 20, 1000)  # الزمن من 0 إلى 20 وحدات زمنية

# ==========================
# FUNCTION DEFINITIONS
# ==========================
def v_E_ctrl(phi):
    """معدل النمو المتحكم به"""
    return v_E0 - Delta_v * np.cos(phi)

def t_c(phi):
    """زمن التشبع المتأثر بالطور"""
    return S_max / v_E_ctrl(phi)

def kappa(phi):
    """ثابت الانحدار بعد التشبع"""
    return kappa0 * (1 + beta * np.cos(phi))

def S(t, phi):
    """الانتروبيا مع التحكم"""
    S_array = np.zeros_like(t)
    tc = t_c(phi)
    kap = kappa(phi)
    for i, ti in enumerate(t):
        if ti <= tc:
            S_array[i] = v_E_ctrl(phi) * ti
        else:
            S_array[i] = S_max + v_E_ctrl(phi) * (ti - tc) * np.exp(-kap * (ti - tc))
    return S_array

# ==========================
# PLOTTING
# ==========================
plt.figure(figsize=(10,6))
for phi, color in zip(phi_values, colors):
    plt.plot(t, S(t, phi), color=color, label=f'phi = {phi:.2f} rad')

plt.axhline(S_max, color='k', linestyle='--', label='S_max (saturation)')
plt.xlabel('Time')
plt.ylabel('Entanglement Entropy S(t, phi)')
plt.title('Controlled Entanglement Dynamics')
plt.legend()
plt.grid(True)
plt.show()
