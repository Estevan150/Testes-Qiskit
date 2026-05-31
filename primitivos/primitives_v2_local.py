from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorSampler

# ==========================================
# 1. A ESTRUTURA LÓGICA (O Circuito)
# ==========================================
# Em vez de fixar um ângulo, criamos um parâmentro 'theta'
theta = Parameter('0')

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1) # aqui é criado um estado de emaranhamento base
# E aqui aplicamos a rotação, mas não dizemos quanto. Deixamos a variavel 'theta'
qc.ry(theta, 0)
qc.measure_all()

print("Arquitetura do Circuito desenhada.")
print(f"Variáveis livres detectadas: {qc.parameters} ({qc.parameters})\n")

# ============================================
# 2. OS DADOS (A Carga útil)
# ============================================
# Em radianos: 0, pi/2, e pi
angulos_para_testar = [[0.0], [1.5708], [3.1415]]

# ============================================
# 3. O EMPACOTAMENTO (Criando o PUB)
# ============================================
# O formato de um PUB para o Sampler é uma tupla: (circuito, valores_dos_parametros)
meu_pub =(qc, angulos_para_testar)


# =============================================
# 4. A EXECUÇÃO LOCAL (Disparando o Motor)
# =============================================
print("Iniciando o motor local (StatevectorSampler)...")
# O StatevectorSampler resolve a matriz matematicamente de forma exata na sua RAM.
sampler_local = StatevectorSampler()

# Enviamos o container (PUB) para rodar. Note que passamos uma lista [meu_pub] pois poderiamos enviar varios PUBs deuma vez.
job = sampler_local.run([meu_pub], shots=1024)

# ==========================================
# 5. DESEMPACOTANDO O RESULTADO (PATCHED)
# ==========================================
resultado_completo = job.result()
dados_do_pub = resultado_completo[0] 

print("\n" + "="*50)
print("RELATÓRIO DE MEDIÇÕES DO SAMPLER V2")
print("="*50)

# Na V2, podemos acessar os arrays de bits brutos
bit_array = dados_do_pub.data.meas

# Vamos iterar exatamente pelo número de ângulos que enviamos
for i in range(len(angulos_para_testar)):
    # get_counts(i) garante que pegaremos o dicionário exato daquele ângulo
    contagens = bit_array.get_counts(i)
    
    print(f"-> Teste {i+1} (Ângulo θ = {angulos_para_testar[i][0]:.4f} rad):")
    print(f"   Distribuição de probabilidade: {contagens}\n")
