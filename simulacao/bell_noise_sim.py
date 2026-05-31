import sys
import os
# Aponta para a pasta utils/ na raiz do projeto para importar o módulo compartilhado
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))

import numpy as np
from qiskit import QuantumCircuit
# pyrefly: ignore [missing-import]
from qiskit_aer import AerSimulator
# pyrefly: ignore [missing-import]
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error
from quantum_fidelity import calcular_fidelidade

def create_singlet_circuit():
    """Cria um circuito para o estado Singlete (Bell) |psi->"""
    qc = QuantumCircuit(2)
    # 1. Colocar o qubit 0 em sobreposição
    qc.h(0)
    # 2. Emaranhar o qubit 1 com o qubit 0
    qc.cx(0, 1)
    # 3. Aplicar a fase negativa e o flip para criar o estado específico |01> - |10>
    qc.x(1)
    qc.z(0)
    # Para o AerSimulator nos devolver a matriz de densidade, salvamos o estado
    qc.save_density_matrix()
    return qc

def simulate_with_noise(qc, t1_time, t2_time, gate_time):
    """Roda o circuito com um modelo de ruído de relaxamento térmico"""
    # Cria o simulador
    simulator = AerSimulator()
    
    # Cria o erro de relaxamento térmico para portas de 1 qubit (H, X, Z) e 2 qubits (CX)
    error_1q = thermal_relaxation_error(t1_time, t2_time, gate_time)
    error_2q = error_1q.tensor(error_1q) # Ruído de 2 qubits é o produto tensorial do ruído de 1 qubit

    # Adiciona os erros ao modelo de ruído
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x', 'z'])
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

    # Executa a simulação
    result = simulator.run(qc, noise_model=noise_model).result()
    # Extrai a matriz de densidade do resultado
    density_matrix = result.data()['density_matrix']
    return np.array(density_matrix)

if __name__ == "__main__":
    print("="*50)
    print("SIMULADOR DE RUÍDO TÉRMICO - ESTADO DE BELL")
    print("="*50)

    # 1. O Circuito Ideal
    circuito = create_singlet_circuit()
    
    # 2. Simulação Ideal (Sem ruído)
    print("\nExecutando Simulação IDEAL (Física Perfeita)...")
    sim_ideal = AerSimulator()
    result_ideal = sim_ideal.run(circuito).result()
    rho_ideal = np.array(result_ideal.data()['density_matrix'])
    
    print("\nMatriz de Densidade Ideal (Aproximada):")
    # Imprime apenas as partes reais para facilitar a leitura, arredondando perto de 0
    print(np.round(np.real(rho_ideal), 3))

    # 3. Simulação Realista (Com Ruído)
    # Parâmetros típicos de hardware (em microssegundos)
    # T1 = Relaxamento (perda de energia), T2 = Desfasamento (perda de coerência)
    # gate_time = tempo que a porta demora para executar
    t1_time = 50.0  
    t2_time = 30.0  
    gate_time = 0.1 # Se aumentarmos isso, o ruído piora drasticamente

    print(f"\nExecutando Simulação RUIDOSA (T1={t1_time}us, T2={t2_time}us)...")
    rho_ruidosa = simulate_with_noise(circuito, t1_time, t2_time, gate_time)

    print("\nMatriz de Densidade Ruidosa (Aproximada):")
    print(np.round(np.real(rho_ruidosa), 3))

    # 4. Auditoria de Qualidade
    fidelidade = calcular_fidelidade(rho_ideal, rho_ruidosa)
    
    print("\n" + "-"*40)
    print(f"FIDELIDADE DO HARDWARE: {fidelidade * 100:.2f}%")
    print("-" * 40)
    
    if fidelidade > 0.99:
        print("Status: EXCELENTE. Calibração perfeita.")
    elif fidelidade > 0.90:
        print("Status: BOM. Hardware utilizável para algoritmos curtos.")
    else:
        print("Status: ALERTA CRÍTICO. Erros térmicos severos detectados.")
