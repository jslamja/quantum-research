import numpy as np
import matplotlib.pyplot as plt

# ===========================
# معادلات الإنتروبيا:
# 1. Von Neumann Entropy (S1)
#    S1 = - Tr(ρ log ρ)
#    ρ : density matrix (مصفوفة الحالة)
#    Tr : أثر المصفوفة (trace)
#    log : اللوغاريتم الطبيعي
#
# 2. Second Rényi Entropy (S2)
#    S2 = - log( Tr(ρ^2) )
#    ρ : density matrix
#    Tr : أثر المصفوفة
# ===========================

def von_neumann_entropy(rho):
    """Calculate Von Neumann entropy S1 = -Tr(rho log rho)"""
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 1e-12]  # تجاهل القيم الصفرية
    return -np.sum(evals * np.log(evals))

def second_renyi_entropy(rho):
    """Calculate Second Rényi entropy S2 = -log(Tr(rho^2))"""
    return -np.log(np.trace(rho @ rho))

# مثال: حالة مختلطة تتحرك من pure -> mixed
p_values = np.linspace(0, 1, 100)
S1_list = []
S2_list = []

for p in p_values:
    rho = np.array([[p, 0],
                    [0, 1-p]])  # density matrix for a single qubit
    S1_list.append(von_neumann_entropy(rho))
    S2_list.append(second_renyi_entropy(rho))

# رسم النتائج مع المعادلات فوق الشكل
plt.figure(figsize=(9,6))

plt.plot(p_values, S1_list, label=r"Von Neumann Entropy $S_1 = -\mathrm{Tr}(\rho \log \rho)$")
plt.plot(p_values, S2_list, label=r"Second Rényi Entropy $S_2 = -\log \mathrm{Tr}(\rho^2)$", linestyle='--')

# إضافة شرح الرموز داخل الشكل
plt.text(0.02, max(S1_list)*0.9, 
         r"$\rho$: density matrix" "\n" 
         r"$\mathrm{Tr}$: trace of the matrix" "\n" 
         r"$\log$: natural logarithm", 
         fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

plt.xlabel("Probability p (population of |0>)")
plt.ylabel("Entropy")
plt.title("Comparison: Von Neumann vs Second Rényi Entropy for a single qubit")
plt.legend()
plt.grid(True)
plt.show()
