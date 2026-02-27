import matplotlib.pyplot as plt
import numpy as np

# ==========================
# PARAMETERS
# ==========================
num_qubits = 5       # عدد الكيوبتات (الأيونات)
ion_spacing = 1.0    # المسافة بين الأيونات

# مواقع الأيونات على خط مستقيم
x = np.arange(num_qubits) * ion_spacing
y = np.zeros_like(x)

# المرحلة phi للتحكم بالمجال المغناطيسي
phi = np.pi / 3  # مثال زاوية

# ==========================
# PLOT IONS
# ==========================
plt.figure(figsize=(10,4))
plt.scatter(x, y, s=300, c='skyblue', label='Qubits (Ions)')
for i, xi in enumerate(x):
    plt.text(xi, y[i]+0.1, f'Q{i+1}', ha='center', fontsize=12)

# ==========================
# PLOT CONTROL MAGNETIC FIELD
# ==========================
# رسم سهم يمثل المجال المغناطيسي وتأثير الطور
for xi in x:
    plt.arrow(xi, -0.3, 0.0, 0.2*np.cos(phi), head_width=0.1, head_length=0.05, color='r')

plt.text(-0.5, -0.3, 'B_ext', color='r', fontsize=12)

# ==========================
# PLOT CONNECTIONS (Entanglement)
# ==========================
# رسم خطوط بين الأيونات تمثل التشابك
for i in range(num_qubits-1):
    plt.plot([x[i], x[i+1]], [y[i], y[i+1]], 'k--', alpha=0.5)

# ==========================
# FINAL TOUCHES
# ==========================
plt.title('Trapped Ion Quantum Processor with External Magnetic Field Control (phi)')
plt.ylim(-0.5, 0.5)
plt.axis('off')
plt.legend()
plt.show()
