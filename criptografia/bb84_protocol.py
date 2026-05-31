import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
# pyrefly: ignore [missing-import]
from qiskit_aer import AerSimulator

# ==========================================
# PAINEL DE CONTROLE DO ARQUITETO
# ==========================================
TAMANHO_MENSAGEM = 100 # <--- Aqui você define o tamanho da mensagem e bits!
EVE_PRESENTE = True # <--- Mude isso para True depois do primeiro teste!

def gerar_bb84():
    print("="*60)
    print(f"SESSÃO BB84: {'[COMPROMETIDA POR EVE]' if EVE_PRESENTE else '[LINHA SEGURA]'}")
    print("="*60)

    # 1. Alice escolhe bits aleatórios e bases aleatórias (0 = Base +, 1 = Base X)
    alice_bits = np.random.randint(2, size=TAMANHO_MENSAGEM)
    alice_bases = np.random.randint(2, size=TAMANHO_MENSAGEM)
    
    # 2. Bob escolhe suas bases de medição aleatoriamente
    bob_bases = np.random.randint(2, size=TAMANHO_MENSAGEM)
    
    # Se a Eve estiver presente, ela também escolhe bases aleatórias para "espiar"
    eve_bases = np.random.randint(2, size=TAMANHO_MENSAGEM)

    bob_bits_medidos = []

    # Vamos processar qubit por qubit
    for i in range(TAMANHO_MENSAGEM):
        qc = QuantumCircuit(1, 1)

        # -- ALICE PREPARA O QUBIT --
        if alice_bits[i] == 1:
            qc.x(0) # Vira para |1>
        
        if alice_bases[i] == 1:
            qc.h(0) # Muda para a base X (Diagonal |+> ou |->)
            
        qc.barrier()

        # -- EVE INTERCEPTA (SE ATIVA) --
        if EVE_PRESENTE:
            # Eve tenta adivinhar a base
            if eve_bases[i] == 1:
                qc.h(0)
            qc.measure(0, 0) # Eve mede e destrói a superposição original!
            # Eve tenta re-preparar o qubit para enganar o Bob
            if eve_bases[i] == 1:
                qc.h(0)
            qc.barrier()

        # -- BOB MEDE O QUBIT --
        # Bob aplica a porta H se ele decidiu medir na base X
        if bob_bases[i] == 1:
            qc.h(0)
            
        qc.measure(0, 0)

        # -- EXECUÇÃO --
        simulador = AerSimulator()
        qc_compilado = transpile(qc, simulador)
        resultado = simulador.run(qc_compilado, shots=1).result()
        medicao = int(list(resultado.get_counts().keys())[0])
        bob_bits_medidos.append(medicao)

    # 3. A FASE DE PENEIRAMENTO (Sifting) - Alice e Bob comparam as bases pelo telefone
    chave_alice = []
    chave_bob = []
    
    for i in range(TAMANHO_MENSAGEM):
        if alice_bases[i] == bob_bases[i]: # Só guardam quando acertam a mesma base
            chave_alice.append(alice_bits[i])
            chave_bob.append(bob_bits_medidos[i])

    # 4. AUDITORIA DE SEGURANÇA (Calculando a Taxa de Erro - QBER)
    erros = 0
    tamanho_chave = len(chave_alice)
    
    for i in range(tamanho_chave):
        if chave_alice[i] != chave_bob[i]:
            erros += 1
            
    taxa_erro = (erros / tamanho_chave) * 100 if tamanho_chave > 0 else 0

    # -- RELATÓRIO FORENSE --
    print(f"\nBits originais de Alice : {alice_bits}")
    print(f"Bases da Alice (+/x)   : {['+' if b==0 else 'x' for b in alice_bases]}")
    if EVE_PRESENTE:
        print(f"Bases da Eve   (+/x)   : {['+' if b==0 else 'x' for b in eve_bases]}")
    print(f"Bases do Bob   (+/x)   : {['+' if b==0 else 'x' for b in bob_bases]}")
    print(f"Bits medidos pelo Bob : {bob_bits_medidos}")
    
    print("\n--- DEPOIS DA PENEIRA (Bases que deram match) ---")
    print(f"Chave da Alice : {chave_alice}")
    print(f"Chave do Bob   : {chave_bob}")
    
    print(f"\nTamanho da Chave Útil: {tamanho_chave} bits (aprox. 50% de descarte é normal)")
    print(f"Taxa de Erros (QBER) : {taxa_erro:.2f}%")
    
    print("\n" + "="*40)
    if taxa_erro == 0:
        print("STATUS FINAL: CHAVE 100% SEGURA. PODE USAR.")
    else:
        print("STATUS FINAL: ALERTA VERMELHO! HACKER NA LINHA! ABORTE A OPERAÇÃO.")
    print("="*40)

if __name__ == "__main__":
    gerar_bb84()
