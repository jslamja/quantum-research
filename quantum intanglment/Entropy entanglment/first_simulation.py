import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# إعداد الشكل
fig = plt.figure(figsize=(12, 8), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.grid(False)

# معلمات المحاكاة
N = 50  # عدد الجسيمات
t_c = 5  # الزمن الحرج
total_time = 10  # الزمن الكلي

# تهيئة الجسيمات
np.random.seed(42)
pos = np.random.uniform(-2, 2, (N, 3))
vel = np.random.normal(0, 0.05, (N, 3))

# دالة التحديث
def update(frame):
    t = frame * total_time / 100
    
    ax.clear()
    ax.set_axis_off()
    
    # حساب الإنتروبيا
    S = min(1.0 * t, 5.0) if t < t_c else 5.0
    
    # تحريك الجسيمات
    if t < t_c:
        vel[:] += np.random.normal(0, 0.01, (N, 3))
    else:
        vel[:] += np.random.normal(0, 0.005, (N, 3))
    
    pos[:] += vel
    
    # تحديد الألوان حسب الإنتروبيا
    colors = plt.cm.plasma(np.linspace(0, S/5, N))
    
    # رسم الجسيمات
    ax.scatter(pos[:,0], pos[:,1], pos[:,2], c=colors, s=30, alpha=0.8)
    
    # إضافة النصوص
    ax.text2D(0.05, 0.95, f"Time: {t:.2f}", transform=ax.transAxes, color='white')
    ax.text2D(0.05, 0.90, f"Entropy: {S:.2f}", transform=ax.transAxes, color='white')
    
    return ax,

# إنشاء التحريك
ani = FuncAnimation(fig, update, frames=100, interval=50, blit=False)

plt.tight_layout()
plt.show()