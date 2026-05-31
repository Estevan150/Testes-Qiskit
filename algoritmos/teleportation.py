import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
# pyrefly: ignore [missing-import]
from qiskit_aer import AerSimulator

def build_teleportation_circuit():
    qr = QuantumRegister(3, name="q")
    crz = ClassicalRegister(1, name="crz")
    crx = ClassicalRegister(1, name="crx")
    cr_bob = ClassicalRegister(1, name="bob_medida") 
    
    qc = QuantumCircuit(qr, crz, crx, cr_bob)

    # PASSO 0: Preparação
    angulo_secreto = np.pi / 4
    qc.ry(angulo_secreto, 0)
    qc.barrier()

    # PASSO 1: Emaranhamento
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()

    # PASSO 2: Medição de Bell (Alice)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, crz) 
    qc.measure(1, crx) 
    qc.barrier()

    # PASSO 3: Correção do Bob (Padrão Moderno Qiskit 1.0+)
    with qc.if_test((crx, 1)):
        qc.x(2)
        
    with qc.if_test((crz, 1)):
        qc.z(2)
        
    qc.barrier()
    
    # AUDITORIA
    qc.measure(2, cr_bob)

    return qc, angulo_secreto

if __name__ == "__main__":
    print("="*50)
    print("INICIANDO PROTOCOLO DE TELETRANSPORTE (QISKIT 1.0+)")
    print("="*50)

    circuito, angulo = build_teleportation_circuit()
    
    simulador = AerSimulator()
    
    # A CHAVE DO SUCESSO: Compilar (transpilar) o circuito para o simulador entender os IFs
    print("Compilando o circuito dinâmico...")
    circuito_compilado = transpile(circuito, simulador)
    
    # Execução
    resultado = simulador.run(circuito_compilado, shots=10000).result()
    contagens = resultado.get_counts()
    
    total_shots = sum(contagens.values())
    
    vitorias_0 = 0
    vitorias_1 = 0
    
    for chave, valor in contagens.items():
        bit_do_bob = chave.split()[0]
        if bit_do_bob == '0':
            vitorias_0 += valor
        else:
            vitorias_1 += valor
            
    prob_0 = vitorias_0 / total_shots
    prob_1 = vitorias_1 / total_shots
    
    prob_teorica_0 = np.cos(angulo/2)**2
    prob_teorica_1 = np.sin(angulo/2)**2
    
    print(f"\nEstado Original Preparado pela Alice (Teórico):")
    print(f"Probabilidade de Medir 0: {prob_teorica_0*100:.2f}%")
    print(f"Probabilidade de Medir 1: {prob_teorica_1*100:.2f}%")
    
    print(f"\nEstado Teletransportado para o Bob (Empírico em {total_shots} shots):")
    print(f"Medições do Bob resultando em 0: {prob_0*100:.2f}%")
    print(f"Medições do Bob resultando em 1: {prob_1*100:.2f}%")
    
    erro = abs(prob_teorica_0 - prob_0)
    if erro < 0.02:
        print("\nStatus: SUCESSO. Teletransporte executado perfeitamente!")
    else:
        print("\nStatus: FALHA. O estado não bate.")
