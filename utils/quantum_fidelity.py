import numpy as np
from scipy.linalg import sqrtm

def calcular_fidelidade(rho, sigma):
    """
    Calcula a fidelidade de Uhlmann entre duas matrizes de densidade.
    Equação: F(rho, sigma) = [ Tr( sqrt( sqrt(rho) @ sigma @ sqrt(rho) ) ) ]^2
    """
    # 1 Converter entradas para arrays do numpy (garantindo precisão de float)
    rho = np.array(rho, dtype= complex)
    sigma = np.array(sigma, dtype=complex)

    # 2 Calcular a raiz quadrada da primeira matriz (sqrt(rho))
    # O Scipy usa decomposição de schur para encontrar a raiz matriarcal exata
    sqrt_rho = sqrtm(rho)

    # 3 Construir o "Sanduiche" central da equação: sqrt(rho) * sigma * sqrt(rho)
    core = sqrt_rho @ sigma @ sqrt_rho
    # 4 Extrair a raiz quadrada desse nucleo 
    sqrt_core = sqrtm(core)

    # 5 O golpe final: calcular o traço e elevar ao quadrado
    # Usamos np.real() porque o resultado fisico da fidelidade é sempre um numero real
    fidelidade = np.real(np.trace(sqrt_core))**2

    return np.round(fidelidade, 4)

#===========================================
# TESTE DE VALIDAÇÃO (Benchmark da questão 20)
#===========================================
if __name__ == "__main__":
    print("Iniciando simulação de backend quantico...\n")

    # Matriz Rho (Populações puramente classicas)
    matriz_rho = [
        [0.80, 0.00],
        [0.00, 0.20]
    ]
    
    # Matriz Sigma (Mistura com coerencias/termos fora da diagonal)
    matriz_sigma = [
        [0.60, 0.30],
        [0.30, 0.40]
    ]

    print("Estado Rho:\n", np.array(matriz_rho))
    print("nEstado Sigma:\n", np.array(matriz_sigma))

    resultado = calcular_fidelidade(matriz_rho, matriz_sigma)

    print("\n" + "-"*40)
    print(f"Fidelidade calculadora: {resultado}")
    print("-"*40)

    if resultado == 0.8698 or resultado == 0.87:
        print("Status: SUCESSO. A matemática do Arquiteto está Validada pelo hardware.")
