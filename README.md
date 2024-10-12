# Otimização de Carregamento de Navio usando Algoritmo Genético

Este projeto explora o problema clássico de otimização de carregamento de navios, utilizando um Algoritmo Genético (AG) para maximizar o lucro de uma viagem entre dois portos. O objetivo é determinar a combinação ideal de contêineres a serem carregados, considerando suas características de peso, volume e valor do frete, respeitando as restrições de capacidade do navio.

Para avaliar a eficácia do AG, comparamos seu desempenho com outros métodos de otimização, incluindo a Heurística Gulosa e a Busca Local. Analisamos os resultados em termos de valor total do frete, peso e volume utilizados, além do tempo de execução de cada algoritmo. Através de visualizações gráficas, buscamos fornecer uma análise comparativa clara e intuitiva do desempenho de cada método.

Este projeto visa contribuir para o entendimento de como algoritmos de otimização podem ser aplicados a problemas logísticos complexos, como o carregamento de navios, com o intuito de auxiliar na tomada de decisões mais eficientes e rentáveis.

## **Componentes do Grupo 10**

- Cristiano Carvalho
- Fabiano Pimenta
- Gabriel Neves
- Gustavo Pinheiro

## Estrutura do Projeto

- `main.py`: Script principal para executar o experimento.
- `algoritmo_genetico.py`: Implementação do algoritmos genético.
- `buscal_local.py`: Implementação do algoritmo de busca local.
- `heuristica_gulosa.py`: Implementação do algoritmo de heurística gulosa.
- `visualizacoes.py`: Funções para criar gráficos e visualizações.
- `utils.py`: Funções utilitárias.

## Como Executar

1. **Clone o repositório:**
   ```
   git clone https://github.com/seu-usuario/tc2_ag_carregamento.git
   ```
2. **Navegue até o diretório do projeto:**
   ```
   cd tc2_ag_carregamento
   ```
3. **Execução**

   ### **Parâmetros**

   O script aceita os seguintes parâmetros de linha de comando:

   ### `--dados`

   Define o tipo de dados a serem utilizados. As opções disponíveis são:

   - `estaticos`: Utiliza um conjunto de dados fixo.
   - `aleatorios`: Gera um conjunto de dados aleatórios.

   **Valor padrão**: `aleatorios`

   ### `--selecao`

   Especifica a função de seleção a ser utilizada. As opções disponíveis são:

   - `torneio`: Utiliza o método de seleção por torneio.
   - `roleta`: Utiliza o método de seleção por roleta.
   - `ranking`: Utiliza o método de seleção por ranking.

   **Valor padrão**: `torneio`

   ### Exemplos de Uso

   - **Usando dados aleatórios e seleção por torneio** (valores padrão):
   ```bash
   python main.py
   ```
   - **Usando dados estáticos**
   ```bash
   python main.py --dados estaticos
   ```
   - **Usando dados aleatórios**
   ```bash
   python main.py --dados aleatorios
   ```
   - **Usando dados estáticos e seleção por roleta**
   ```bash
   python main.py --dados estaticos --selecao roleta
   ```
   - **Usando dados aleatórios e seleção por ranking**
   ```bash
   python main.py --dados aleatorios --selecao ranking
   ```

## Requisitos

- Python 3.7+
- Bibliotecas: numpy, matplotlib, seaborn

## Resultados

Os resultados, incluindo gráficos comparativos, serão salvos na pasta `resultados/`.
