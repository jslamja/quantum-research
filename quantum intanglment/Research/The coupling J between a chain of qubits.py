import matplotlib.pyplot as plt

# عدد الكيوبتات
N = 6

# مواقع الكيوبتات على محور x
x = list(range(N))
y = [0]*N

# رسم الكيوبتات (دوائر)
plt.scatter(x, y, s=1000, c='skyblue', edgecolors='black', zorder=3)

# تسمية الكيوبتات
for i in range(N):
    plt.text(x[i], y[i], f"Q{i+1}", ha='center', va='center', fontsize=12, zorder=4)

# رسم الترابط بين الجيران (J)
for i in range(N-1):
    plt.plot([x[i], x[i+1]], [y[i], y[i+1]], 'k-', lw=3)
    # كتابة J على الرابط
    mid_x = (x[i]+x[i+1])/2
    mid_y = (y[i]+y[i+1])/2 + 0.1
    plt.text(mid_x, mid_y, "J", ha='center', va='bottom', fontsize=12, color='red')

# رسم السهم الذي يمثل المجال الخارجي B
for i in range(N):
    plt.arrow(x[i], y[i]-0.2, 0, -0.5, head_width=0.1, head_length=0.1, fc='green', ec='green')
    plt.text(x[i], y[i]-0.8, "B", ha='center', va='bottom', fontsize=12, color='green')

# إعداد الشكل
plt.ylim(-1.5, 1)
plt.axis('off')
plt.title("1D Qubit Chain: Qubits (blue), Coupling J (red), External Field B (green)")
plt.show()
