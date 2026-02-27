import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, Polygon, FancyArrow
import matplotlib.patheffects as pe

# إنشاء الشكل
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Superconducting Qubit System', fontsize=20, fontweight='bold', color='#1a5276')

# ========== لوحة الدائرة الكهربائية ==========
ax1.set_xlim(-3, 3)
ax1.set_ylim(-2, 2)
ax1.set_aspect('equal')
ax1.set_facecolor('#0d1b2a')
ax1.set_title('Electrical Circuit Schematic', fontsize=14, fontweight='bold', color='#3498db')
ax1.axis('off')

# رسم دائرة التبريد
cooling_circle = Circle((0, 1.5), 0.8, facecolor='none', edgecolor='#5dade2', 
                        linewidth=3, linestyle='--', alpha=0.7)
ax1.add_patch(cooling_circle)

# إضافة نص درجة الحرارة
temp_text = ax1.text(0, 1.5, "10 mK", ha='center', va='center', fontsize=11,
                     fontweight='bold', color='#5dade2',
                     path_effects=[pe.withStroke(linewidth=3, foreground='black')])

# رسم مقياس حرارة
thermometer_base = Rectangle((-0.2, 0.2), 0.4, 1.6, facecolor='#34495e', edgecolor='#7f8c8d')
ax1.add_patch(thermometer_base)
thermometer_mercury = Rectangle((-0.15, 0.3), 0.3, 0.4, facecolor='#3498db', alpha=0.8)
ax1.add_patch(thermometer_mercury)

# عناصر الدائرة الكهربائية
# Josephson Junction (X symbol)
jj_x = [(-0.8, 0), (-0.4, 0)]
jj_y = [(-0.8, -0.3), (-0.4, 0.3)]
ax1.plot([-0.8, -0.4], [0, 0], 'w-', linewidth=2)
ax1.plot([-0.6, -0.6], [-0.3, 0.3], 'w-', linewidth=2)

# Capacitor (parallel lines)
cap_x = [(-0.2, -0.2), (0.2, 0.2)]
cap_y = [(-0.8, -0.3), (-0.8, 0.3)]
ax1.plot([-0.2, -0.2], [-0.8, -0.3], 'w-', linewidth=2)
ax1.plot([0.2, 0.2], [-0.8, 0.3], 'w-', linewidth=2)
ax1.plot([-0.2, 0.2], [-0.55, -0.55], 'w-', linewidth=1, alpha=0.5)

# Inductor (spiral)
theta = np.linspace(0, 6 * np.pi, 200)
inductor_x = 1.0 + 0.15 * np.cos(theta)
inductor_y = 0.0 + 0.15 * theta / (6 * np.pi) - 0.4
ax1.plot(inductor_x, inductor_y, 'w-', linewidth=2)

# Connecting wires
wire_points = [
    [(-1.5, 0), (-0.8, 0)],
    [(-0.4, 0), (-0.2, 0)],
    [(0.2, 0), (0.8, 0)],
    [(0.8, 0), (1.5, 0)],
    [(-0.6, -0.3), (-0.6, -1.0)],
    [(-0.6, 0.3), (-0.6, 1.0)]
]

for start, end in wire_points:
    ax1.plot([start[0], end[0]], [start[1], end[1]], 'w-', linewidth=1, alpha=0.7)

# إضافة تسميات
labels = [
    ("Josephson\nJunction", -0.6, 0),
    ("Capacitor", 0, -0.6),
    ("Inductor", 1.0, -0.4),
    ("Superconducting\nWires", 0, 0.8)
]

for text, x, y in labels:
    ax1.text(x, y, text, ha='center', va='center', fontsize=9, color='#85c1e9',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e3a5f', alpha=0.7))

# جسيمات الإلكترون المتحركة
electrons = []
for i in range(8):
    electron = Circle((0, 0), 0.05, facecolor='#e74c3c')
    ax1.add_patch(electron)
    electrons.append({
        'patch': electron,
        'pos': i * 0.125,
        'path': np.random.choice([0, 1]),
        'speed': 0.02 + np.random.random() * 0.01
    })

# إشارة التردد الراديوي
frequency_signal, = ax1.plot([], [], 'y-', linewidth=2, alpha=0.7)

# ========== لوحة المعلومات والبيانات ==========
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_facecolor('#1c2833')
ax2.set_title('Performance Metrics & Specifications', fontsize=14, fontweight='bold', color='#2ecc71')
ax2.axis('off')

# العنوان
ax2.text(0.5, 0.95, 'SUPERCONDUCTING QUBIT', ha='center', va='center', 
         fontsize=16, fontweight='bold', color='#3498db',
         path_effects=[pe.withStroke(linewidth=2, foreground='white')])

# بيانات الأداء
metrics = [
    ("Temperature", "10-20 mK", "#5dade2"),
    ("Frequency", "4-8 GHz", "#3498db"),
    ("Coherence Time (T₁)", "50-100 μs", "#2ecc71"),
    ("Gate Time", "10-50 ns", "#e74c3c"),
    ("Readout Time", "100-500 ns", "#f39c12"),
    ("Typical Fidelity", "99.5-99.9%", "#9b59b6"),
    ("Qubit-Qubit Coupling", "10-100 MHz", "#1abc9c"),
    ("Anharmonicity", "200-300 MHz", "#e67e22")
]

# رسم المترجات
for i, (name, value, color) in enumerate(metrics):
    y_pos = 0.85 - i * 0.1
    ax2.text(0.1, y_pos, f"{name}:", ha='left', va='center', 
             fontsize=11, fontweight='bold', color='#ecf0f1')
    ax2.text(0.6, y_pos, value, ha='left', va='center', 
             fontsize=11, fontweight='bold', color=color)
    
    # رسم شريط التقدم
    if 'μs' in value or 'ns' in value or 'GHz' in value or '%' in value:
        progress = 0
        if 'μs' in value:
            val = float(value.split('-')[0])
            progress = min(val / 100, 1)
        elif 'ns' in value:
            val = float(value.split('-')[0])
            progress = min(val / 50, 1)
        elif 'GHz' in value:
            val = float(value.split('-')[0])
            progress = min(val / 8, 1)
        elif '%' in value:
            val = float(value.split('-')[0].replace('%', ''))
            progress = min((val - 99) / 1, 1)
        
        bar = Rectangle((0.8, y_pos - 0.02), 0.15 * progress, 0.04, 
                        facecolor=color, alpha=0.7)
        ax2.add_patch(bar)

# رسم مخطط الأداء
performance_x = [0.1, 0.3, 0.5, 0.7, 0.9]
performance_y = [0.15, 0.25, 0.35, 0.45, 0.55]
performance_values = [0.7, 0.9, 0.8, 0.85, 0.95]

ax2.text(0.5, 0.65, 'Performance Metrics', ha='center', va='center',
         fontsize=12, fontweight='bold', color='#f1c40f')

for i, (x, y, val) in enumerate(zip(performance_x, performance_y, performance_values)):
    circle = Circle((x, y), 0.04, facecolor='#3498db', alpha=val)
    ax2.add_patch(circle)
    ax2.text(x, y, f"{int(val*100)}%", ha='center', va='center', 
             fontsize=8, color='white', fontweight='bold')

# وظيفة تحديث الرسوم المتحركة
def update(frame):
    global thermometer_mercury
    
    # تحديث جسيمات الإلكترون
    for electron in electrons:
        electron['pos'] = (electron['pos'] + electron['speed']) % 1
        
        # المسارات المختلفة في الدائرة
        if electron['path'] == 0:
            # المسار العلوي
            if electron['pos'] < 0.25:
                x = -1.5 + electron['pos'] * 6
                y = 0
            elif electron['pos'] < 0.5:
                x = -0.6
                y = -0.3 - (electron['pos'] - 0.25) * 4 * 0.7
            else:
                x = -1.5 + (electron['pos'] - 0.5) * 6
                y = -1.0
        else:
            # المسار السفلي
            if electron['pos'] < 0.25:
                x = -1.5 + electron['pos'] * 6
                y = 0
            elif electron['pos'] < 0.5:
                x = 0
                y = (electron['pos'] - 0.25) * 4 * 0.8 - 0.4
            else:
                x = -1.5 + (electron['pos'] - 0.5) * 6
                y = 1.0
        
        electron['patch'].center = (x, y)
        
        # تغيير المسار عشوائياً
        if np.random.random() < 0.005:
            electron['path'] = 1 - electron['path']
    
    # تحديث إشارة التردد
    t = np.linspace(-2, 2, 100)
    freq_signal = 0.5 * np.sin(2 * np.pi * 2 * t + frame * 0.1)
    frequency_signal.set_data(t, freq_signal + 1.2)
    
    # تحديث مقياس الحرارة
    pulse = 0.5 + 0.5 * np.sin(frame * 0.05)
    thermometer_mercury.set_height(0.3 + 0.2 * pulse)
    thermometer_mercury.set_alpha(0.6 + 0.4 * pulse)
    
    # تحديث نص درجة الحرارة
    temp_val = 10 + 2 * np.sin(frame * 0.03)
    temp_text.set_text(f"{temp_val:.1f} mK")
    
    # تغيير لون الدائرة الباردة
    cooling_circle.set_edgecolor((0.35, 0.7, 0.9, 0.5 + 0.3 * pulse))
    
    return electrons + [frequency_signal, thermometer_mercury, temp_text, cooling_circle]

# إنشاء الرسوم المتحركة
ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=False)

# إضافة وصف
fig.text(0.02, 0.02, 
         "Superconducting Qubits: Josephson junction-based circuits operating at millikelvin temperatures\n"
         "Key Features: Fast gate operations, good scalability, requires cryogenic cooling",
         fontsize=10, color='#7f8c8d', style='italic')

plt.tight_layout()
plt.show()