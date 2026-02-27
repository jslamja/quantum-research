import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, Polygon, Wedge, Ellipse
import matplotlib.patheffects as pe
from matplotlib.collections import LineCollection, PatchCollection

# إنشاء الشكل
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Trapped Ion Qubit System', fontsize=20, fontweight='bold', color='#7d3c98')

# ========== لوحة المصيدة الأيونية ==========
ax1.set_xlim(-3, 3)
ax1.set_ylim(-2, 2)
ax1.set_aspect('equal')
ax1.set_facecolor('#1a1a2e')
ax1.set_title('Ion Trap Configuration', fontsize=14, fontweight='bold', color='#9b59b6')
ax1.axis('off')

# رسم مصيدة بول (Paul Trap)
# الأقطاب الكهربائية
electrode1 = Ellipse((-1.5, 0), 1.0, 0.5, angle=0, 
                     facecolor='#8e44ad', alpha=0.3, edgecolor='#9b59b6', linewidth=2)
electrode2 = Ellipse((1.5, 0), 1.0, 0.5, angle=0,
                     facecolor='#8e44ad', alpha=0.3, edgecolor='#9b59b6', linewidth=2)
electrode3 = Ellipse((0, 1.0), 2.0, 0.5, angle=90,
                     facecolor='#8e44ad', alpha=0.3, edgecolor='#9b59b6', linewidth=2)
electrode4 = Ellipse((0, -1.0), 2.0, 0.5, angle=90,
                     facecolor='#8e44ad', alpha=0.3, edgecolor='#9b59b6', linewidth=2)

ax1.add_patch(electrode1)
ax1.add_patch(electrode2)
ax1.add_patch(electrode3)
ax1.add_patch(electrode4)

# إضافة تسميات للأقطاب
ax1.text(-1.5, 0.4, '+V', ha='center', va='center', fontsize=10, 
         fontweight='bold', color='#e74c3c')
ax1.text(1.5, 0.4, '+V', ha='center', va='center', fontsize=10,
         fontweight='bold', color='#e74c3c')
ax1.text(0.4, 1.0, '-V', ha='center', va='center', fontsize=10,
         fontweight='bold', color='#3498db')
ax1.text(0.4, -1.0, '-V', ha='center', va='center', fontsize=10,
         fontweight='bold', color='#3498db')

# رسم خطوط المجال الكهربائي
field_lines = []
for angle in np.linspace(0, 2*np.pi, 12, endpoint=False):
    x_start = 2.0 * np.cos(angle)
    y_start = 1.2 * np.sin(angle)
    x_end = 0.5 * np.cos(angle)
    y_end = 0.3 * np.sin(angle)
    line, = ax1.plot([x_start, x_end], [y_start, y_end], 
                     color='#5dade2', alpha=0.4, linewidth=1)
    field_lines.append(line)

# إنشاء الأيونات
ions = []
ion_positions = np.linspace(-1.0, 1.0, 5)
ion_colors = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6']
ion_elements = ['Ca⁺', 'Sr⁺', 'Ba⁺', 'Yb⁺', 'Mg⁺']

for i, (x, color, element) in enumerate(zip(ion_positions, ion_colors, ion_elements)):
    ion = Circle((x, 0), 0.1, facecolor=color, edgecolor='white', linewidth=1.5)
    ax1.add_patch(ion)
    
    # إضافة تسمية العنصر
    ax1.text(x, 0.2, element, ha='center', va='center', fontsize=9,
             fontweight='bold', color=color)
    
    ions.append({
        'patch': ion,
        'x': x,
        'y': 0,
        'phase': i * 0.5,
        'amplitude': 0.05 + np.random.random() * 0.1,
        'color': color,
        'vibration_mode': np.random.choice(['axial', 'radial'])
    })

# حزم الليزر
lasers = []
laser_directions = [
    [(2.5, 0.5), (ion_positions[0], 0.1)],      # من اليمين إلى الأيون الأول
    [(-2.5, -0.5), (ion_positions[-1], -0.1)],  # من اليسار إلى الأيون الأخير
    [(0, 2.5), (0, 0.1)],                       # من الأعلى
    [(0, -2.5), (0, -0.1)]                      # من الأسفل
]

for i, (start, end) in enumerate(laser_directions):
    laser, = ax1.plot([], [], color='#f1c40f', linewidth=3, alpha=0.6)
    lasers.append(laser)
    
    # مصادر الليزر
    source = Wedge(start, 0.2, 0, 360, facecolor='#f1c40f', alpha=0.8)
    ax1.add_patch(source)
    ax1.text(start[0], start[1], f"L{i+1}", ha='center', va='center',
             fontsize=8, fontweight='bold', color='black')

# مستشعرات الكشف
detectors = [
    Circle((2.2, 1.0), 0.15, facecolor='#2ecc71', alpha=0.6),
    Circle((-2.2, -1.0), 0.15, facecolor='#2ecc71', alpha=0.6)
]

for detector in detectors:
    ax1.add_patch(detector)
    ax1.text(detector.center[0], detector.center[1], 'D', ha='center', va='center',
             fontsize=9, fontweight='bold', color='white')

# إضافة خطوط توصيل كهربائية
for x in [-1.5, 1.5, 0]:
    ax1.plot([x, x], [2, 2.5], 'gray', linewidth=1, alpha=0.5)
    ax1.plot([x, x], [-2, -2.5], 'gray', linewidth=1, alpha=0.5)

# ========== لوحة المعلومات والبيانات ==========
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_facecolor('#2c3e50')
ax2.set_title('Ion Trap Specifications', fontsize=14, fontweight='bold', color='#e74c3c')
ax2.axis('off')

# العنوان
ax2.text(0.5, 0.95, 'TRAPPED ION QUBIT', ha='center', va='center',
         fontsize=16, fontweight='bold', color='#9b59b6',
         path_effects=[pe.withStroke(linewidth=2, foreground='white')])

# بيانات الأداء
metrics = [
    ("Operating Temperature", "Room Temperature\n(Cooled ions)", "#5dade2"),
    ("Trap Frequency (Axial)", "1-10 MHz", "#3498db"),
    ("Trap Frequency (Radial)", "3-30 MHz", "#2980b9"),
    ("Coherence Time (T₂)", "1-10 seconds", "#2ecc71"),
    ("Gate Time", "1-100 μs", "#e74c3c"),
    ("State Detection Fidelity", ">99.9%", "#f39c12"),
    ("Single Qubit Fidelity", "99.99%", "#9b59b6"),
    ("Two Qubit Fidelity", "99.9%", "#1abc9c"),
    ("Laser Wavelength", "369-674 nm", "#e67e22"),
    ("Ion-Ion Distance", "3-10 μm", "#95a5a6")
]

# رسم المترجات
for i, (name, value, color) in enumerate(metrics):
    y_pos = 0.9 - i * 0.09
    ax2.text(0.05, y_pos, f"{name}:", ha='left', va='center',
             fontsize=10, fontweight='bold', color='#ecf0f1')
    ax2.text(0.55, y_pos, value, ha='left', va='center',
             fontsize=10, fontweight='bold', color=color)

# رسم مخطط مستويات الطاقة
ax2.text(0.5, 0.15, 'Energy Level Diagram', ha='center', va='center',
         fontsize=12, fontweight='bold', color='#f1c40f')

# مستويات الطاقة
energy_levels = [0, 0.3, 0.6, 0.9]
level_colors = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
level_names = ['Ground State', 'Metastable', 'Excited', 'Rydberg']

for i, (level, color, name) in enumerate(zip(energy_levels, level_colors, level_names)):
    ax2.plot([0.1, 0.9], [level, level], color=color, linewidth=3)
    ax2.text(0.92, level, name, ha='left', va='center', fontsize=9, color=color)
    
    # انتقالات الليزر
    if i < len(energy_levels) - 1:
        ax2.arrow(0.5, level, 0, energy_levels[i+1] - level - 0.02,
                  head_width=0.02, head_length=0.02, fc='#f1c40f', ec='#f1c40f')

# وظيفة تحديث الرسوم المتحركة
def update(frame):
    # تحديث حركة الأيونات
    for ion in ions:
        ion['phase'] += 0.05
        
        if ion['vibration_mode'] == 'axial':
            # اهتزاز محوري (على طول السلسلة)
            displacement = ion['amplitude'] * np.sin(ion['phase'])
            ion['patch'].center = (ion['x'] + displacement, ion['y'])
        else:
            # اهتزاز شعاعي (عمودي على السلسلة)
            displacement = ion['amplitude'] * np.sin(ion['phase'])
            ion['patch'].center = (ion['x'], displacement)
        
        # تأثير النبض
        pulse = 0.6 + 0.4 * np.sin(ion['phase'] * 2)
        ion['patch'].set_alpha(pulse)
        
        # تغيير لون خفيف
        r, g, b = int(ion['color'][1:3], 16), int(ion['color'][3:5], 16), int(ion['color'][5:7], 16)
        new_color = (r/255, g/255, b/255, pulse)
        ion['patch'].set_facecolor(new_color)
    
    # تحديث حزم الليزر
    for i, laser in enumerate(lasers):
        phase = frame * 0.05 + i * 0.5
        alpha = 0.4 + 0.3 * np.sin(phase)
        laser.set_alpha(alpha)
        
        start, end = laser_directions[i]
        # تحريك نقطة النهاية
        if i == 0:
            end = (ion_positions[0] + 0.1 * np.sin(frame * 0.1), 
                   0.1 + 0.05 * np.sin(frame * 0.08))
        elif i == 1:
            end = (ion_positions[-1] + 0.1 * np.sin(frame * 0.12),
                   -0.1 + 0.05 * np.sin(frame * 0.09))
        
        laser.set_data([start[0], end[0]], [start[1], end[1]])
        
        # تأثير الانتشار
        if np.random.random() < 0.1:
            ax1.plot([start[0], end[0]], [start[1], end[1]], 
                    color='#f1c40f', linewidth=1, alpha=0.2)
    
    # تحديث خطوط المجال الكهربائي
    for i, line in enumerate(field_lines):
        phase = frame * 0.02 + i * 0.2
        alpha = 0.3 + 0.2 * np.sin(phase)
        line.set_alpha(alpha)
        
        # تغيير اللون قليلاً
        color_val = 0.5 + 0.5 * np.sin(phase)
        line.set_color((0.35, 0.7, 0.9, alpha))
    
    # تحديث مستشعرات الكشف
    for detector in detectors:
        pulse = 0.5 + 0.5 * np.sin(frame * 0.08)
        detector.set_alpha(0.4 + 0.3 * pulse)
        
        # كشف عشوائي للأيونات
        if np.random.random() < 0.05:
            flash = Circle(detector.center, detector.radius * 1.5,
                          facecolor='none', edgecolor='#2ecc71', linewidth=2, alpha=0.5)
            ax1.add_patch(flash)
            # إزالة الوميض بعد فترة
            fig.canvas.draw_idle()
    
    # تحديث أقطاب المصيدة
    pulse = 0.5 + 0.5 * np.sin(frame * 0.03)
    for electrode in [electrode1, electrode2, electrode3, electrode4]:
        electrode.set_alpha(0.2 + 0.2 * pulse)
    
    return ions + lasers + field_lines

# إنشاء الرسوم المتحركة
ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=False)

# إضافة وصف
fig.text(0.02, 0.02,
         "Trapped Ion Qubits: Atomic ions confined in electromagnetic traps, controlled by lasers\n"
         "Key Features: Long coherence times, high fidelity, individual addressability",
         fontsize=10, color='#7f8c8d', style='italic')

plt.tight_layout()
plt.show()