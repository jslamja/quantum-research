import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, Wedge
import matplotlib.patheffects as pe

# =========================
# إعداد الشكل
# =========================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle("Photon Qubit – Optical Interferometer",
             fontsize=20, fontweight="bold", color="#2ecc71")

# =========================
# اللوحة اليسرى: الدائرة البصرية
# =========================
ax1.set_xlim(-3, 3)
ax1.set_ylim(-2, 2)
ax1.set_aspect("equal")
ax1.set_facecolor("#0d1b2a")
ax1.axis("off")

# المصدر
source = Wedge((-2.5, 0), 0.3, 45, 315,
               facecolor="#f1c40f", alpha=0.9)
ax1.add_patch(source)
ax1.text(-2.5, 0, "S", ha="center", va="center",
         fontsize=12, fontweight="bold", color="black")

# Beam Splitter
beam_splitter = Rectangle(
    (-0.1, -0.5), 0.15, 1.0, angle=45,
    facecolor=(1, 1, 1, 0.6),
    edgecolor="white", linewidth=2
)
ax1.add_patch(beam_splitter)
ax1.text(-0.3, 0, "BS", color="white", fontsize=10)

# المرايا
mirrors = [
    Rectangle((-1.5, 1.2), 0.12, 0.3, angle=45, color="silver"),
    Rectangle((1.0, 1.2), 0.12, 0.3, angle=45, color="silver"),
    Rectangle((1.0, -1.2), 0.12, 0.3, angle=45, color="silver"),
]
for m in mirrors:
    ax1.add_patch(m)

# الكواشف
detectors = [
    Circle((2.5, 1.2), 0.18, facecolor="#2ecc71", alpha=0.6),
    Circle((2.5, -1.2), 0.18, facecolor="#2ecc71", alpha=0.6)
]
for d in detectors:
    ax1.add_patch(d)
    ax1.text(d.center[0], d.center[1], "D",
             ha="center", va="center",
             fontsize=10, fontweight="bold", color="white")

# المسارات (مرسومة فقط)
ax1.plot([-2.2, -0.2, 2.4], [0, 0.9, 1.2], "w--", alpha=0.3)
ax1.plot([-2.2, -0.2, 2.4], [0, -0.9, -1.2], "w--", alpha=0.3)

# =========================
# الفوتونات
# =========================
photon_colors = {
    "H": "#e74c3c",
    "V": "#3498db",
}

photons = []
N = 6

for i in range(N):
    pol = np.random.choice(["H", "V"])
    c = Circle((-2.5, 0), 0.07,
               facecolor=photon_colors[pol],
               edgecolor="white", linewidth=1)
    ax1.add_patch(c)

    photons.append({
        "patch": c,
        "t": i * 0.15,
        "speed": 0.01 + 0.005 * np.random.rand(),
        "path": None,
        "pol": pol
    })

# =========================
# اللوحة اليمنى: معلومات
# =========================
ax2.set_facecolor("#1c2833")
ax2.axis("off")

ax2.text(0.5, 0.92, "PHOTON QUBIT",
         ha="center", fontsize=16,
         fontweight="bold", color="#2ecc71",
         path_effects=[pe.withStroke(linewidth=2, foreground="white")])

info = [
    "Encoding: Polarization",
    "Paths: Superposition",
    "Beam Splitter: 50 / 50",
    "Detection: Probabilistic",
]

for i, txt in enumerate(info):
    ax2.text(0.1, 0.75 - i * 0.1,
             "• " + txt,
             fontsize=12, color="white")

# =========================
# دالة الحركة
# =========================
def update(frame):
    for p in photons:
        p["t"] += p["speed"]

        # قبل مقسم الحزمة
        if p["t"] < 1:
            x = -2.5 + 2.3 * p["t"]
            y = 0

        # عند المقسم: اختيار مسار
        elif p["path"] is None:
            p["path"] = np.random.choice(["up", "down"])
            x, y = -0.2, 0

        # المسار العلوي
        elif p["path"] == "up":
            s = min(p["t"] - 1, 1)
            x = -0.2 + 2.6 * s
            y = 0.9 * s

        # المسار السفلي
        else:
            s = min(p["t"] - 1, 1)
            x = -0.2 + 2.6 * s
            y = -0.9 * s

        p["patch"].center = (x, y)

        # عند الوصول للكاشف
        if p["t"] > 2.2:
            p["t"] = 0
            p["path"] = None

    return []

# =========================
# تشغيل الحركة
# =========================
ani = animation.FuncAnimation(
    fig, update,
    frames=400,
    interval=30,
    blit=False
)

plt.tight_layout()
plt.show()
