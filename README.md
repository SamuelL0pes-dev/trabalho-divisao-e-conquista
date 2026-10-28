# Trabalho Prático: Paradigma de Divisão e Conquista

**Alunos / Dupla:** Samuel Lopes e Rodrigo Temporal  
**Disciplina:** Análise e Projeto de Algoritmos (APA)  
**Data de Entrega:** 28/10/2026

Este trabalho aborda o paradigma de **Divisão e Conquista** aplicado a dois problemas fundamentais (não relacionados à ordenação), incluindo a implementação de soluções ingênuas de força bruta, a formulação em divisão e conquista, a solução linear $O(n)$ da questão desafio (Algoritmo de Kadane), uma bateria completa de testes automatizados com cobertura de casos de borda e uma avaliação experimental rigorosa com análise assintótica e geração de relatório técnico em PDF.

---

## 📋 Entregáveis Atendidos

- [x] **Repositório Git com o código-fonte e instruções de execução**, com histórico de commits refletindo o ciclo evolutivo do desenvolvimento.
- [x] **Arquivo de casos de teste com as entradas e saídas esperadas** (formatos legível `.txt` e estruturado `.json`), cobrindo rigorosamente todos os casos normais e de borda obrigatórios (vetores negativos, unitários, empates, pontos coincidentes, etc.).
- [x] **Relatório em PDF com até 8 páginas** (`report/relatorio_divisao_conquista.pdf` e cópia em `D:\Downloads\Relatorio_Divisao_e_Conquista.pdf`), contendo resolução analítica das recorrências via Teorema Mestre, demonstração formal da geometria dos 7 vizinhos, tabelas de medições com médias e desvios padrão, gráficos comparativos de tempo, estudo do limiar ótimo e análise do ponto de crossover.
- [x] **Arquivos CSV com as medições brutas e sumarizadas**, além da especificação completa do hardware utilizado.
- [x] **Questão Desafio**: Implementação e análise comparativa do Algoritmo Linear de Kadane $O(n)$ na Etapa 1.

---

## 📁 Estrutura do Repositório

```text
trabalho_divisao_conquista/
├── src/
│   ├── __init__.py
│   ├── etapa1_max_subarray.py       # Força Bruta O(n²), D&C O(n log n) e Kadane O(n)
│   └── etapa2_closest_pair.py       # Força Bruta O(n²) e D&C O(n log n) com poda de 7 vizinhos
├── tests/
│   ├── __init__.py
│   ├── test_etapa1.py               # 8 testes cobrindo todos os casos de borda da Etapa 1
│   ├── test_etapa2.py               # 9 testes cobrindo todos os casos de borda da Etapa 2
│   └── test_cases_io.py             # Validação automatizada contra arquivos de casos de teste
├── test_cases/
│   ├── etapa1_casos_teste.txt       # Arquivo de casos de teste formatado (Etapa 1)
│   ├── etapa1_casos_teste.json      # Versão estruturada em JSON (Etapa 1)
│   ├── etapa2_casos_teste.txt       # Arquivo de casos de teste formatado (Etapa 2)
│   └── etapa2_casos_teste.json      # Versão estruturada em JSON (Etapa 2)
├── benchmarks/
│   ├── run_benchmarks.py            # Script automatizado de medição (5 repetições por tamanho)
│   ├── plot_graphs.py               # Script de geração dos gráficos de alta resolução
│   ├── benchmark_etapa1_bruto.csv   # Medições brutas da Etapa 1
│   ├── benchmark_etapa1_resumo.csv  # Médias e desvios padrão da Etapa 1
│   ├── benchmark_etapa2_bruto.csv   # Medições brutas da Etapa 2
│   ├── benchmark_etapa2_resumo.csv  # Médias, desvios e speedup da Etapa 2
│   ├── benchmark_etapa2_limiares.csv# Estudo de sensibilidade ao limiar (threshold de 2 a 128)
│   ├── benchmark_etapa2_crossover.csv# Estudo de crossover em instâncias pequenas (n <= 128)
│   ├── configuracao_maquina.json    # Metadados de hardware e ambiente
│   └── figures/                     # Figuras salvas em PNG de alta resolução
│       ├── etapa1_comparacao_tempos.png
│       ├── etapa2_comparacao_tempos.png
│       ├── etapa2_ajuste_teorico.png
│       ├── etapa2_estudo_limiar.png
│       ├── etapa2_crossover.png
│       └── faixa_7_vizinhos_geometria.png
├── report/
│   ├── generate_pdf_report.py       # Script de compilação do relatório acadêmico em PDF
│   └── relatorio_divisao_conquista.pdf # Relatório técnico final diagramado (8 páginas)
├── main.py                          # Interface unificada de linha de comando (CLI)
├── requirements.txt                 # Dependências do projeto
└── README.md                        # Documentação completa
```

---

## ⚙️ Ambiente e Configuração da Máquina Utilizada

As medições foram coletadas e validadas no seguinte hardware:

- **Processador:** AMD Ryzen 5 3400G with Radeon Vega Graphics (4 Cores / 8 Threads, ~3.7 GHz)
- **Memória RAM:** 16 GB DDR4
- **Sistema Operacional:** Microsoft Windows 11 Pro 64-bit
- **Interpretador:** Python 3.12.10 (CPython 64-bit)

---

## 🚀 Instalação e Execução

### 1. Clonar o Repositório e Instalar Dependências

```bash
# Clone ou acesse a pasta do projeto
cd D:\Downloads\trabalho_divisao_conquista

# Instale os pacotes necessários
pip install -r requirements.txt
```

### 2. Executando os Testes Automatizados (Critério: 40% da nota)

Para rodar todos os testes unitários e validar os arquivos de casos de teste:

```bash
# Via CLI principal:
python main.py --test

# Ou diretamente pelo módulo unittest:
python -m unittest discover -s tests -v
```

### 3. Executando os Algoritmos via CLI (`main.py`)

#### Etapa 1: Subarranjo de Soma Máxima
```bash
# Comparar todos os 3 algoritmos (Força Bruta, Divisão e Conquista e Kadane) para um vetor:
python main.py --etapa 1 --input "13 -3 -25 20 -3 -16 -23 18 20 -7 12 -5 -22 15 -4 7"

# Executar apenas Força Bruta O(n²):
python main.py --etapa 1 --alg bf --input "5 -2 8 -1 10 -20 4 2"

# Executar apenas Divisão e Conquista O(n log n):
python main.py --etapa 1 --alg dc --input "5 -2 8 -1 10 -20 4 2"

# Executar a questão desafio: Kadane O(n):
python main.py --etapa 1 --alg kd --input "5 -2 8 -1 10 -20 4 2"
```

#### Etapa 2: Par de Pontos Mais Próximos
```bash
# Comparar Força Bruta e Divisão e Conquista usando um arquivo de pontos:
python main.py --etapa 2 --file test_cases/etapa2_exemplo.txt

# Executar Divisão e Conquista com limiar customizado (ex: 16):
python main.py --etapa 2 --alg dc --threshold 16
```

### 4. Reproduzindo os Benchmarks e Gráficos

```bash
# Executa todas as medições de laboratório (salva os CSVs):
python main.py --benchmark

# Gera todos os gráficos e o diagrama geométrico em alta resolução:
python main.py --plot

# Compila o relatório em PDF com 8 páginas:
python main.py --report
```

---

## 🔬 Resumo Teórico e Recorrências

### Etapa 1: Subarranjo de Soma Máxima
- **Força Bruta:** Testa $\frac{n(n+1)}{2}$ subarranjos $\implies \Theta(n^2)$.
- **Divisão e Conquista:** Divide no meio e calcula cruzamento em tempo linear $\implies T(n) = 2T(n/2) + \Theta(n)$.
  - Pelo Teorema Mestre ($a=2, b=2, f(n)=\Theta(n) \implies n^{\log_2 2} = n$): **Caso 2 $\implies \Theta(n \log n)$**.
- **Kadane (Questão Desafio):** Programação dinâmica em uma única passagem $\implies \Theta(n)$ e espaço auxiliar $O(1)$.

### Etapa 2: Par de Pontos Mais Próximos
- **Força Bruta:** Compara todos os pares $\frac{n(n-1)}{2} \implies \Theta(n^2)$.
- **Divisão e Conquista:** Pré-ordenação por $x$ e $y$ em $O(n \log n)$ e chamadas recursivas com partição linear e faixa com no máximo 7 vizinhos:
  - $T(n) = 2T(n/2) + O(n)$.
  - Pelo Teorema Mestre: **Caso 2 $\implies O(n \log n)$**.
- **Justificativa dos 7 Vizinhos:** A faixa retangular de dimensão $2\delta \times \delta$ ao redor da linha vertical mediana é subdividida em 8 retângulos menores de $(\delta/2) \times (\delta/2)$. A diagonal máxima de cada retângulo é $\delta/\sqrt{2} \approx 0.707\delta < \delta$. Pelo Princípio da Casa dos Pombos, nenhum sub-retângulo pode conter mais de 1 ponto. Logo, excluindo o ponto de referência, restam no máximo $8 - 1 = 7$ vizinhos a verificar ordenados por $y$.
- **Justificativa do Limiar (Threshold):** Para $n \le 3$, a força bruta é estritamente necessária como caso base da geometria. No estudo empírico, identificou-se que um limiar de $T = 16$ atinge o tempo mínimo global (redução de 20,2% sobre $T=3$), equilibrando a sobrecarga de chamadas recursivas com o custo quadrático das folhas.
- **Ponto de Crossover:** A força bruta vence para instâncias microscópicas ($n \le 32$) devido à simplicidade de laços contíguos e localidade de cache L1. O cruzamento ocorre em $n \approx 32-40$, após o qual D&C torna-se exponencialmente superior.
