# ⚛️ Testes-Qiskit

Laboratório completo de **computação quântica** com experimentos práticos usando [Qiskit 1.0+](https://qiskit.org/) e [Qiskit Aer](https://qiskit.github.io/qiskit-aer/). Cada módulo implementa um algoritmo, protocolo ou técnica de engenharia quântica diferente — de criptografia a química computacional.

---

## 📁 Estrutura do Projeto

```
Testes-Qiskit/
│
├── 🔍 algoritmos/
│   ├── grover_search.py        ← Busca de Grover
│   └── teleportation.py        ← Teletransporte Quântico
│
├── 🔐 criptografia/
│   └── bb84_protocol.py        ← Protocolo BB84 (QKD)
│
├── ⚛️  quimica/
│   └── vqe_chemistry.py        ← VQE — Molécula de H₂
│
├── 📶 simulacao/
│   └── bell_noise_sim.py       ← Simulação de Ruído Térmico
│
├── 🛡️  mitigacao/
│   ├── transpiler_engine.py    ← Motor de Transpilação de Circuitos
│   └── zne_folding.py          ← Mitigação de Erros por ZNE (Folding)
│
├── 🎛️  primitivos/
│   └── primitives_v2_local.py  ← API Primitives V2 do Qiskit
│
└── 🛠️  utils/
    └── quantum_fidelity.py     ← Módulo compartilhado (Fidelidade de Uhlmann)
```

---

## 📖 Descrição Detalhada dos Módulos

---

### 🔍 `algoritmos/` — Algoritmos Quânticos Fundamentais

#### `grover_search.py` — Algoritmo de Busca de Grover

**O que é:** Implementação do **Algoritmo de Grover**, o algoritmo quântico mais famoso para acelerar buscas em bancos de dados não estruturados.

**Como funciona:**
- Em um banco de dados clássico com `N` entradas, uma busca leva em média `N/2` tentativas
- Grover resolve o mesmo problema em **√N tentativas** — uma vantagem quadrática real
- O experimento busca o estado `|11⟩` em um espaço de 4 possibilidades (`|00⟩`, `|01⟩`, `|10⟩`, `|11⟩`)

**Componentes do circuito:**
| Componente | O que faz |
|---|---|
| **Superposição (H⊗H)** | Coloca todos os 4 estados em superposição com igual probabilidade |
| **Oráculo (CZ)** | "Marca" o estado alvo invertendo sua **fase** (de +1 para -1) |
| **Difusor (Inversão em torno da média)** | **Amplifica** a amplitude do estado marcado, suprimindo os demais |
| **Medição** | Colapsa o estado — com ~100% de chance, retorna `|11⟩` |

**Por que é importante:** É a prova mais direta da **vantagem quântica** para busca. Com 2 qubits, 1 iteração é suficiente.

---

#### `teleportation.py` — Teletransporte Quântico

**O que é:** Implementa o **Protocolo de Teletransporte Quântico** completo com 3 qubits usando os **circuitos dinâmicos** do Qiskit 1.0+ (`if_test`).

**Como funciona:**
- **Não teleporta matéria** — teleporta o **estado quântico** (a informação) de um qubit para outro
- Requer um par emaranhado (**canal quântico**) compartilhado entre Alice e Bob
- Alice envia apenas **2 bits clássicos** pelo telefone; Bob usa esses bits para reconstruir o estado

**Protocolo com 3 qubits:**
| Qubit | Papel |
|---|---|
| `q[0]` | Qubit de Alice (estado secreto θ = π/4 a ser teleportado) |
| `q[1]` | Metade do par emaranhado (fica com Alice) |
| `q[2]` | Metade do par emaranhado (fica com Bob) |

**Validação:** Compara as probabilidades medidas pelo Bob com os valores teóricos de `cos²(θ/2)` e `sen²(θ/2)`. Erro < 2% = SUCESSO.

---

### 🔐 `criptografia/` — Segurança Quântica

#### `bb84_protocol.py` — Protocolo BB84 (Quantum Key Distribution)

**O que é:** Simulação completa do **Protocolo BB84**, o primeiro e mais usado protocolo de **distribuição de chave quântica (QKD)** do mundo, inventado por Bennett e Brassard em 1984.

**Por que é revolucionário:** A segurança é garantida pelas **leis da física**, não por matemática computacionalmente cara. É impossível escutar sem deixar rastro.

**Como funciona:**
1. **Alice** prepara qubits em bases aleatórias (`+` = base computacional, `x` = base diagonal)
2. **Eve (espiã)** tenta interceptar — ao medir, ela **destrói a superposição original** (Princípio da Não-Clonagem)
3. **Bob** mede com bases aleatórias
4. **Sifting:** Alice e Bob comparam bases pelo telefone (só guardam bits onde usaram a mesma base)
5. **Auditoria (QBER):** Calculam a Taxa de Erro de Bit Quântico. Se Eve esteve presente, o QBER sobe para ~25%

**Parâmetro de controle:**
```python
EVE_PRESENTE = True  # Ative/desative o espião para ver o impacto no QBER
TAMANHO_MENSAGEM = 100  # Número de qubits a enviar
```

---

### ⚛️ `quimica/` — Química Computacional Quântica

#### `vqe_chemistry.py` — VQE para a Molécula de Hidrogênio (H₂)

**O que é:** Usa o **VQE (Variational Quantum Eigensolver)** para calcular a energia do estado fundamental da molécula de **H₂** — um problema real de química quântica.

**Por que importa:** Simular moléculas em computadores clássicos se torna exponencialmente caro conforme o tamanho aumenta. O VQE é o algoritmo candidato a resolver isso em hardware quântico NISQ (ruidoso).

**Arquitetura Híbrida CPU ✆ QPU:**
```
[CPU] Otimizador COBYLA ajusta os ângulos
        ↓
[QPU] Circuito EfficientSU2 (Ansatz) executa com esses ângulos
        ↓
[CPU] Calcula a energia esperada ⟨H⟩ e decide a próxima iteração
        ↓
    Loop até convergir para o mínimo
```

**Métrica de sucesso:** Energia VQE deve atingir `-1.857275 Hartree` (valor exato do H₂). Gera um **gráfico de convergência** ao final.

---

### 📶 `simulacao/` — Simulação de Hardware Real

#### `bell_noise_sim.py` — Simulador de Ruído Térmico no Estado de Bell

**O que é:** Simula o comportamento do **Estado de Bell Singlete** (`|ψ⁻⟩ = (|01⟩ - |10⟩)/√2`) em um hardware quântico real, com **modelo de ruído térmico** T1/T2.

**Parâmetros de hardware simulados:**
| Parâmetro | Valor | Significado |
|---|---|---|
| `T1` | 50 µs | **Tempo de relaxamento de energia** — o qubit "esquece" que está em `|1⟩` e vai para `|0⟩` |
| `T2` | 30 µs | **Tempo de desfasamento** — o qubit perde a coerência da superposição |
| `gate_time` | 0.1 µs | Duracão de cada porta física no chip |

**Fluxo do experimento:**
1. Executa o circuito ideal (sem ruído) e salva `ρ_ideal`
2. Executa o mesmo circuito com o modelo de ruído e salva `ρ_ruidosa`
3. Usa `quantum_fidelity.py` para calcular `F(ρ_ideal, ρ_ruidosa)` e medir a degradação

---

### 🛡️ `mitigacao/` — Engenharia de Mitigação de Erros *(NOVO)*

#### `transpiler_engine.py` — Motor de Transpilação de Circuitos

**O que é:** Demonstra o processo de **Transpilação** — a tradução do circuito quântico ideal (matemático) para o circuito real que roda no hardware físico.

**O problema central:** Todo chip quântico tem uma **topologia de conexões físicas** — não dá para conectar qualquer qubit com qualquer outro diretamente.

```
# Topologia simulada (linha reta):
[Qubit 0] <---> [Qubit 1] <---> [Qubit 2]

# O circuito ideal tenta: Qubit 0 -> Qubit 2 (conexão INEXISTENTE)
# O Transpilador injeta portas SWAP para rotear pelo Qubit 1
```

**O que o transpilador faz automaticamente:**
- **Roteamento:** Injeta portas `SWAP` para mover qubits até vizinhos compatíveis
- **Tradução de portas:** Converte qualquer porta para as portas nativas do hardware (`rz`, `sx`, `x`, `cx`)
- **Otimização Nível 3:** Usa IA para minimizar a profundidade e o número de CNOTs (cada CNOT extra = mais ruído)

**Por que importa:** Todo circuito passa por transpilação antes de rodar em hardware real. Entender isso é fundamental para escrever código quântico eficiente.

---

#### `zne_folding.py` — Zero Noise Extrapolation (ZNE) via Gate Folding

**O que é:** Implementa a técnica de **Zero Noise Extrapolation (ZNE)**, uma das estratégias de **mitigação de erros** mais usadas para hardware NISQ.

**A ideia contraintuitiva:** Para remover o ruído, primeiro você o **amplifica de forma controlada**, depois **extrapola matematicamente** para o valor em ruído zero.

**Método: Gate Folding**
```
Circuito base:     H ─ CX ─ (Ruído 1x)
Circuito 3x:       H ─ CX ─ CX ─ CX ─ (Ruído 3x, mesma lógica: CX³ = CX)
Circuito 5x:       H ─ CX ─ CX ─ CX ─ CX ─ CX ─ (Ruído 5x)
```
- Cada `CX + CX` extra se cancela matematicamente (CX² = I)
- Mas fisicamente, **cada porta adiciona ruído real do hardware**
- Com os resultados em 1x, 3x e 5x, extrapola-se para o ponto `ruído = 0`

**Por que importa:** ZNE é usado ativamente em pesquisas com computadores quânticos reais (IBM, Google) para obter resultados mais precisos sem precisar de hardware perfeito.

---

### 🎛️ `primitivos/` — API Moderna do Qiskit

#### `primitives_v2_local.py` — Demonstração da API Primitives V2

**O que é:** Tutorial da nova **API Primitives V2** do Qiskit 1.0+, que unifica a forma de enviar e receber resultados de experimentos quânticos.

**Conceito de PUB (Primitive Unified Bloc):** Uma "caixa" que empacota circuito + parâmetros + shots para envio em lote.

**O experimento:** Testa 3 ângulos de rotação (`θ = 0, π/2, π`) em um estado de Bell paramétrico e exibe a distribuição de probabilidade de cada um em um único envio.

| Ângulo | Resultado Esperado |
|---|---|
| `θ = 0` | Estado `\|00⟩` com 100% |
| `θ = π/2` | Distribuição uniforme entre os estados |
| `θ = π` | Estado `\|11⟩` com 100% |

---

### 🛠️ `utils/` — Módulos Compartilhados

#### `quantum_fidelity.py` — Calculadora de Fidelidade de Uhlmann

**O que é:** Módulo base reutilizável que implementa a **Fidelidade de Uhlmann** — a métrica padrão da física quântica para comparar dois estados quânticos.

**Fórmula:**
$$F(\rho, \sigma) = \left[\text{Tr}\left(\sqrt{\sqrt{\rho}\,\sigma\,\sqrt{\rho}}\right)\right]^2$$

**Interpretação:**
| Valor | Significado |
|---|---|
| `F = 1.0` | Estados **idênticos** (hardware perfeito) |
| `F ≈ 0.99` | Excelênte — ruído mínimo |
| `F ≈ 0.90` | Aceitável — utilizável para circuitos curtos |
| `F < 0.90` | Crítico — erros térmicos severos |

**Importado por:** `simulacao/bell_noise_sim.py`

---

## 🗺️ Mapa de Dependências

```
utils/quantum_fidelity.py  ←──  simulacao/bell_noise_sim.py
       (módulo base)

Todos os outros módulos são independentes entre si.
```

---

## 🚀 Como Executar

### Pré-requisitos

```bash
pip install qiskit qiskit-aer qiskit-algorithms matplotlib scipy numpy
```

### Executando cada experimento

```bash
# Busca de Grover
python algoritmos/grover_search.py

# Teletransporte Quântico
python algoritmos/teleportation.py

# Criptografia BB84
python criptografia/bb84_protocol.py

# Química Quântica (VQE)
python quimica/vqe_chemistry.py

# Simulação de Ruído
python simulacao/bell_noise_sim.py

# Transpilação de Circuito
python mitigacao/transpiler_engine.py

# Mitigação de Erros ZNE
python mitigacao/zne_folding.py

# API Primitives V2
python primitivos/primitives_v2_local.py

# Calculadora de Fidelidade
python utils/quantum_fidelity.py
```

---

## 🎯 Progressão de Complexidade

```
primitivos  →  algoritmos  →  criptografia  →  simulacao  →  mitigacao  →  quimica
(API básica)    (busca/QT)     (BB84/QKD)    (ruído/fid.)  (transpile/ZNE)  (VQE/H₂)
```

---

## 🛠️ Stack Tecnológico

| Biblioteca | Uso |
|---|---|
| [Qiskit 1.0+](https://qiskit.org/) | Framework principal de computação quântica |
| [Qiskit Aer](https://qiskit.github.io/qiskit-aer/) | Simulador quântico de alta performance com modelos de ruído |
| [Qiskit Algorithms](https://qiskit-community.github.io/qiskit-algorithms/) | Algoritmos quânticos prontos (VQE, COBYLA) |
| [NumPy](https://numpy.org/) | Computação numérica e matrizes |
| [SciPy](https://scipy.org/) | Raiz quadrada matricial (Fidelidade de Uhlmann) |
| [Matplotlib](https://matplotlib.org/) | Visualização e gráficos |
