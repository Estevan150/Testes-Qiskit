# ⚛️ Testes-Qiskit

Laboratório de **computação quântica** com experimentos práticos usando [Qiskit](https://qiskit.org/) e [Qiskit Aer](https://qiskit.github.io/qiskit-aer/). Cada módulo implementa um algoritmo ou protocolo quântico diferente, indo de criptografia a química computacional.

---

## 📁 Estrutura do Projeto

```
Testes-Qiskit/
│
├── 🔍 algoritmos/
│   ├── grover_search.py       ← Busca de Grover
│   └── teleportation.py       ← Teletransporte Quântico
│
├── 🔐 criptografia/
│   └── bb84_protocol.py       ← Protocolo BB84 (QKD)
│
├── ⚛️  quimica/
│   └── vqe_chemistry.py       ← VQE — Molécula de H₂
│
├── 📶 simulacao/
│   └── bell_noise_sim.py      ← Simulação de Ruído Térmico
│
├── 🎛️  primitivos/
│   └── primitives_v2_local.py ← API Primitives V2 do Qiskit
│
└── 🛠️  utils/
    └── quantum_fidelity.py    ← Módulo compartilhado (Fidelidade de Uhlmann)
```

---

## 📖 Descrição dos Módulos

### 🔍 `algoritmos/`

| Arquivo | Descrição |
|---|---|
| `grover_search.py` | Implementa o **Algoritmo de Grover** para busca quadrática em banco de dados quântico. Busca o estado `\|11⟩` usando Oráculo (CZ) + Difusor em 1 iteração com ~100% de probabilidade. |
| `teleportation.py` | Protocolo de **Teletransporte Quântico** com 3 qubits usando circuitos dinâmicos do Qiskit 1.0+ (`if_test`). Transfere o estado de Alice para Bob usando emaranhamento + 2 bits clássicos. |

### 🔐 `criptografia/`

| Arquivo | Descrição |
|---|---|
| `bb84_protocol.py` | Simulação completa do protocolo **BB84** de distribuição de chave quântica (QKD). Inclui Alice, Bob e o espião Eve. Calcula o **QBER** (Quantum Bit Error Rate) para detectar interceptação. |

### ⚛️ `quimica/`

| Arquivo | Descrição |
|---|---|
| `vqe_chemistry.py` | Usa o **VQE (Variational Quantum Eigensolver)** para calcular a energia do estado fundamental da molécula de **H₂**. Arquitetura híbrida CPU+QPU com otimizador COBYLA e gráfico de convergência. |

### 📶 `simulacao/`

| Arquivo | Descrição |
|---|---|
| `bell_noise_sim.py` | Simula o **Estado de Bell Singlete** com modelo de **ruído térmico realista** (T1/T2). Usa `quantum_fidelity.py` para medir a degradação causada pelo ruído de hardware. |

### 🎛️ `primitivos/`

| Arquivo | Descrição |
|---|---|
| `primitives_v2_local.py` | Demonstração da nova **API Primitives V2** do Qiskit 1.0+ com `StatevectorSampler`. Testa 3 ângulos de rotação em um único PUB (Primitive Unified Bloc). |

### 🛠️ `utils/`

| Arquivo | Descrição |
|---|---|
| `quantum_fidelity.py` | Módulo compartilhado que implementa a **Fidelidade de Uhlmann** entre duas matrizes de densidade: `F(ρ,σ) = [Tr(√(√ρ·σ·√ρ))]²`. Importado por `bell_noise_sim.py`. |

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

# Primitives V2
python primitivos/primitives_v2_local.py

# Calculadora de Fidelidade
python utils/quantum_fidelity.py
```

---

## 🎯 Progressão de Complexidade

```
primitivos  →  algoritmos  →  criptografia  →  simulacao  →  quimica
(API básica)    (busca/QT)      (BB84/QKD)    (ruído+fid.)  (VQE/H₂)
```

---

## 🛠️ Stack Tecnológico

- **[Qiskit 1.0+](https://qiskit.org/)** — Framework de computação quântica
- **[Qiskit Aer](https://qiskit.github.io/qiskit-aer/)** — Simulador quântico de alta performance
- **[Qiskit Algorithms](https://qiskit-community.github.io/qiskit-algorithms/)** — Algoritmos quânticos (VQE, COBYLA)
- **[NumPy](https://numpy.org/)** / **[SciPy](https://scipy.org/)** — Computação científica
- **[Matplotlib](https://matplotlib.org/)** — Visualização de dados
