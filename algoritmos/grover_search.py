from qiskit import QuantumCircuit, transpile
# pyrefly: ignore [missing-import]
from qiskit_aer import AerSimulator

def create_oracle():
    """
    O Oráculo: Marca a resposta certa invertendo a fase dela.
    Nosso alvo é o estado |11>.
    A porta CZ (Controlled-Z) faz exatamente isso: só aplica Z se ambos os qubits forem 1.
    """
    oracle = QuantumCircuit(2, name="Oraculo")
    oracle.cz(0, 1) # Inverte o sinal apenas do estado |11>
    return oracle

def create_diffuser():
    """
    O Difusor: Amplifica o estado que foi marcado negativamente pelo Oráculo.
    Ele inverte todas as amplitudes em torno da média.
    """
    diffuser = QuantumCircuit(2, name="Difusor")
    
    # 1. Tira da superposição
    diffuser.h([0, 1])
    # 2. Aplica X para alinhar a fase
    diffuser.x([0, 1])
    # 3. Aplica a porta CZ (A mágica da inversão em torno da média)
    diffuser.cz(0, 1)
    # 4. Desfaz o X e o H
    diffuser.x([0, 1])
    diffuser.h([0, 1])
    
    return diffuser

def build_grover_circuit():
    """Constrói a arquitetura completa do Algoritmo de Grover."""
    qc = QuantumCircuit(2, 2)

    # PASSO 1: Superposição Inicial (Colocando todas as gavetas na mesa)
    qc.h([0, 1])
    qc.barrier()

    # PASSO 2: Aplicar o Oráculo
    qc.append(create_oracle(), [0, 1])
    qc.barrier()

    # PASSO 3: Aplicar o Difusor (Amplificação)
    qc.append(create_diffuser(), [0, 1])
    qc.barrier()

    # PASSO 4: Medição
    qc.measure([0, 1], [0, 1])
    
    return qc

if __name__ == "__main__":
    print("="*50)
    print("INICIANDO ALGORITMO DE BUSCA DE GROVER")
    print("="*50)

    circuito_grover = build_grover_circuit()
    
    # Execução no Simulador
    simulador = AerSimulator()
    print("Compilando o circuito...")
    circuito_compilado = transpile(circuito_grover, simulador)
    
    print("Vasculhando o banco de dados...")
    # Rodamos 1000 vezes para ter estatística
    resultado = simulador.run(circuito_compilado, shots=1000).result()
    contagens = resultado.get_counts()

    # Relatório Forense
    print("\n" + "="*40)
    print("RESULTADOS DA MEDIÇÃO (1000 Shots)")
    print("="*40)
    
    # Formatação do dicionário de contagens para melhor leitura
    for estado, tiros in contagens.items():
        porcentagem = (tiros / 1000) * 100
        marcador = " <--- [ALVO ENCONTRADO!]" if estado == '11' else ""
        print(f"Gaveta |{estado}> : {porcentagem:>6.2f}% ({tiros} vezes){marcador}")
        
    print("\nStatus: " + ("SUCESSO ABSOLUTO. Vantagem Quântica Demonstrada." if '11' in contagens and contagens['11'] == 1000 else "FALHA NA AMPLIFICAÇÃO."))
