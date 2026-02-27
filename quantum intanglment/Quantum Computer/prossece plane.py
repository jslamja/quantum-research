import matplotlib.pyplot as plt
import numpy as np

# ==========================
# PARAMETERS
# ==========================
num_qubits = 5
rows = 1
cols = num_qubits
x = np.arange(cols)
y = np.zeros_like(x)

# ==========================
# CREATE FIGURE
# ==========================
plt.figure(figsize=(10,3))

# رسم الكيوبتات
for i in range(num_qubits):
    plt.scatter(x[i], y[i], s=500, color='skyblue')
    plt.text(x[i], y[i]+0.1, f'Q{i+1}', ha='center', fontsize=12)

# رسم خطوط التشابك بين الكيوبتات
for i in range(num_qubits-1):
    plt.plot([x[i], x[i+1]], [y[i], y[i+1]], 'k--', alpha=0.5)

# رسم مربعات التحكم (مثلاً مجال مغناطيسي خارجي)
for i in range(num_qubits):
    plt.gca().add_patch(plt.Rectangle((x[i]-0.25, y[i]-0.4), 0.5, 0.1, color='red', alpha=0.5))
    plt.text(x[i], y[i]-0.35, 'B_ext', ha='center', fontsize=9, color='white')

plt.title('Simplified Trapped Ion Quantum Processor Layout')
plt.axis('off')
plt.ylim(-1, 0.5)
plt.show()
