import numpy as np
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2
# --- PATCH V2: Usando o novo Estimator de alta performance do Qiskit 1.0+ ---
from qiskit.primitives import StatevectorEstimator 
# pyrefly: ignore [missing-import]
from qiskit_algorithms.optimizers import COBYLA
# pyrefly: ignore [missing-import]
from qiskit_algorithms import VQE

# ==========================================
# 1. O AMBIENTE FÍSICO (O Problema)
# ==========================================
print("Configurando a Molécula de Hidrogênio (H2)...")
h2_op = SparsePauliOp.from_list([
    ("II", -1.0523732),
    ("IZ", 0.3979374),
    ("ZI", -0.3979374),
    ("ZZ", -0.0112801),
    ("XX", 0.1809311)
])

energia_exata = -1.857275
print(f"Alvo a ser atingido (Energia Mínima Exata): {energia_exata} Hartree\n")

# ==========================================
# 2. O CIRCUITO PARAMETRIZADO (O "Cérebro" Quântico)
# ==========================================
ansatz = EfficientSU2(num_qubits=2, reps=1, entanglement='linear', insert_barriers=True)
num_parametros = ansatz.num_parameters
print(f"O circuito quântico foi criado com {num_parametros} parâmetros ajustáveis.\n")

# ==========================================
# 3. A INTELIGÊNCIA ARTIFICIAL (O Otimizador Clássico)
# ==========================================
otimizador = COBYLA(maxiter=100) 

# ==========================================
# 4. TELEMETRIA (Monitoramento em Tempo Real)
# ==========================================
historico_energia = []
historico_iteracoes = []

def callback_telemetria(avaliacoes, parametros, energia, desvio_padrao):
    historico_energia.append(energia)
    historico_iteracoes.append(avaliacoes)
    if avaliacoes % 10 == 0 or avaliacoes == 1:
        print(f"Iteração [{avaliacoes:03d}] -> Energia Atual: {energia:.5f}")

# ==========================================
# 5. A EXECUÇÃO DO LOOP HÍBRIDO (VQE)
# ==========================================
print("="*50)
print("INICIANDO O LOOP HÍBRIDO (VQE CPU + QPU)")
print("="*50)

# --- PATCH V2: Instanciando o novo motor ---
estimador = StatevectorEstimator()
chute_inicial = np.random.random(num_parametros)

vqe = VQE(
    estimator=estimador,
    ansatz=ansatz,
    optimizer=otimizador,
    initial_point=chute_inicial, # Passando o chute inicial direto para o algoritmo
    callback=callback_telemetria
)

# Rodamos o algoritmo
resultado = vqe.compute_minimum_eigenvalue(operator=h2_op)

# ==========================================
# 6. RELATÓRIO FORENSE
# ==========================================
energia_final = resultado.eigenvalue.real
erro = abs(energia_exata - energia_final)

print("\n" + "="*50)
print("RELATÓRIO DE SÍNTESE QUÍMICA")
print("="*50)
print(f"Energia Teórica (Alvo) : {energia_exata:.5f} Hartree")
print(f"Energia VQE (Encontrada) : {energia_final:.5f} Hartree")
print(f"Margem de Erro         : {erro:.5f} Hartree")

if erro < 0.01:
    print("\nStatus: SUCESSO! Precisão Química Alcançada.")
else:
    print("\nStatus: INCOMPLETO. O otimizador caiu em um mínimo local. Tente rodar novamente.")

# ==========================================
# 7. DASHBOARD VISUAL (Gráfico)
# ==========================================
plt.figure(figsize=(10, 6))
plt.plot(historico_iteracoes, historico_energia, label='Energia VQE', color='blue', marker='o')
plt.axhline(y=energia_exata, color='red', linestyle='--', label='Energia Exata (Alvo)')
plt.title('Descida do Gradiente Híbrido: Encontrando o Estado Fundamental do H2')
plt.xlabel('Iterações do Loop (CPU <-> QPU)')
plt.ylabel('Energia do Sistema (Hartree)')
plt.legend()
plt.grid(True)
plt.show()
