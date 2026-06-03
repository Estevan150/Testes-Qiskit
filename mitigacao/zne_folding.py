from qiskit import QuantumCircuit

def fold_circuit(circuito_original, fator_de_escala):
    """
    Função arquitetural para aplicar 'Folding' (Dobragem) em portas de 2 qubits. 
    Aumenta a profundidade do circuito para amplificar o ruído propositalmente,
    sem alterar a lógica matematica do algoritmo.
    """
    qc_dobrado = QuantumCircuit(*circuito_original.qregs, *circuito_original.cregs)

    for instrucao in circuito_original.data:
        porta = instrucao.operation
        qubits = instrucao.qubits
        clbits = instrucao.clbits

        # Adicionamos a porta original
        qc_dobrado.append(porta, qubits, clbits)

        # Se for uma porta CNOT (cx) e quisermos esticar o ruído
        if porta.name == 'cx' and fator_de_escala > 1:
            # fator_de_escala 3 significa adicionar mais DUAS portas para cancelar
            # CX + CX + CX = CX (Matematicamente equivalente, fisicamente ruidoso)
            pares_extras = (fator_de_escala - 1) // 2
            for _ in range(pares_extras):
                qc_dobrado.append(porta, qubits, clbits) # Vai
                qc_dobrado.append(porta, qubits, clbits) # Volta (Cancela)

    return qc_dobrado

if __name__ == "__main__":
    print("="*50)
    print("ENGENHARIA DE MITIGAÇÃO: PREPARAÇÃO PARA ZNE")
    print("="*50)

    # Criamos um circuito alvo simples
    qc_base = QuantumCircuit(2)
    qc_base.h(0)
    qc_base.cx(0,1)
    
    print("\n1. CIRCUITO BASE (Ruído 1x)")
    print(f"Profundidade: {qc_base.depth()} | Portas: {dict(qc_base.count_ops())}")

    # Criamos a versão esticada para 3x o ruído
    qc_3x = fold_circuit(qc_base, fator_de_escala=3)
    print("\n2. CIRCUITO ESTICADO (Ruído 3x - Primeira dobra)")
    print(f"Profundidade: {qc_3x.depth()} | Portas: {dict(qc_3x.count_ops())}")

    # Criamos a versão esticada para 5x o ruído
    qc_5x = fold_circuit(qc_base, fator_de_escala=5)
    print("\n3. CIRCUITO SUPER ESTICADO (Ruído 5x - Segunda dobra)")
    print(f"Profundidade: {qc_5x.depth()} | Portas: {dict(qc_5x.count_ops())}")

    print("\nStatus: Módulos de extrapolação gerados com sucesso. Prontos para envio via Primitives V2.")
