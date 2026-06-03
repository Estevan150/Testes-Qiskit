from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap

# =========================================
# 1. A MENTE DO ARQUITETO (Circuito Ideal)
# =========================================
qc_ideal = QuantumCircuit(3)
qc_ideal.h(0)
qc_ideal.cx(0,1)
# O "Problema": Estamos mandando o Qubit 0 interagir direto com o Qubit 2
qc_ideal.cx(0,2)

print("="*50)
print("1. CIRCUITO IDEAL (Matemática Pura)")
print("="*50)
print(f"Profundidade do circuito: {qc_ideal.depth()}")
print(f"Portas usadas: {dict(qc_ideal.count_ops())}\n")

# ==========================================
# 2. O HARDWARE FÍSICO (O "Metal")
# ==========================================
# Vamos simular um chip onde os qubits estão em uma linha reta:
# [Qubit 0] <---> [Quibit 1] <---> [Qubit 2]
# Veja que não existe conexão direta entre 0 e 2!
conexoes = [[0, 1], [1, 0], [1, 2], [2, 1]]
mapa_fisico = CouplingMap(conexoes)

# Portas que o micro-ondas do hardware realmente entende
portas_base_do_hardware = ['rz', 'sx', 'x', 'cx']

# ==========================================
# 3. O MOTOR DE TRANSPILAÇÃO
# ==========================================
print("Iniciando Transpilação de Nível 3 (Otimização Máxima)...")

# Passamos nosso circuto pelo Transpiledor, dizendo a ele as regras do hardware
qc_real = transpile(
    qc_ideal,
    coupling_map= mapa_fisico,
    basis_gates=portas_base_do_hardware,
    optimization_level=3 # Nível 3 aciona a IA pesada de otimização de rotas
)

print("\n" + "="*50)
print("2. O CIRCUITO TRANSPILADO(O que realmente roda na máquina)")
print(f"Profundidade do circuito: {qc_real.depth()}")
print(f"Portas usadas: {dict(qc_real.count_ops())}")

# Para ilustrar a genialidada do Qiskit, vamos ver quantas portas SWAP e CNOTs extras ele injetou
cnot_ideal = qc_ideal.count_ops().get('cx', 0)
cnot_real = qc_real.count_ops().get('cx', 0)

print("\n--- ANÁLISE DE CUSTO DO HARDWARE ---")
print(f"CNOTs desejados : {cnot_ideal}")
print(f"CNOTs reais executados : {cnot_real} (Custo do roteamento)")
