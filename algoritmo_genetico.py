import random
import time

# Classe Individuo
class Individuo:
    def __init__(self, genoma):
        self.genoma = genoma
        self.fitness = 0

def inicializar_populacao(tamanho_populacao, tamanho_genoma):
    """
    Inicializa a população do algoritmo genético com indivíduos aleatórios.

    Args:
        tamanho_populacao: O número de indivíduos na população.
        tamanho_genoma: O tamanho do genoma de cada indivíduo.

    Returns:
        Uma lista de objetos Individuo, representando a população inicial.
    """
    return [Individuo([random.choice([0, 1]) for _ in range(tamanho_genoma)]) for _ in range(tamanho_populacao)]

def calcular_fitness(individuo, dados_conteineres, max_peso, max_volume):
    """
    Calcula o fitness de um indivíduo, que representa uma solução para o problema de carregamento de contêineres.

    O fitness é definido como o valor total dos contêineres carregados no navio, desde que
    as restrições de peso e volume sejam respeitadas. Se as restrições forem violadas, o fitness
    é definido como 0, indicando uma solução inválida.

    Args:
        individuo: Objeto Individuo representando a solução a ser avaliada.
        dados_conteineres: Lista de tuplas contendo os dados dos contêineres (peso, volume, valor).
        max_peso: Peso máximo que o navio pode carregar.
        max_volume: Volume máximo que o navio pode carregar.

    Returns:
        O valor do fitness do indivíduo (valor total dos contêineres) se a solução for válida,
        ou 0 caso contrário.
    """
    peso_total = 0
    volume_total = 0
    valor_total = 0
    for i, bit in enumerate(individuo.genoma):
        if bit == 1:
            peso, volume, valor = dados_conteineres[i]
            peso_total += peso
            volume_total += volume
            valor_total += valor

    # Verifica se as restrições de peso e volume são respeitadas
    if peso_total > max_peso or volume_total > max_volume:
        return 0  # Solução inválida
    return valor_total  # Solução válida, retorna o valor total

def selecao_torneio(populacao, tamanho_torneio=3):
    """
    Seleciona um indivíduo da população usando o método de torneio.

    Args:
        populacao: A lista de indivíduos (objetos Individuo) da população atual.
        tamanho_torneio: O número de indivíduos que serão selecionados aleatoriamente
            para participar do torneio. O indivíduo com maior fitness entre os
            selecionados será o vencedor.

    Returns:
        O indivíduo (objeto Individuo) com o maior fitness entre os participantes
        do torneio.
    """
    selecionados = random.sample(populacao, tamanho_torneio)
    return max(selecionados, key=lambda ind: ind.fitness)

def selecao_roleta(populacao):
    """
    Seleciona um indivíduo da população usando o método da roleta.

    Args:
        populacao: Lista de indivíduos.

    Returns:
        Individuo selecionado.
    """
    # Calcula a soma total dos fitness da população
    soma_fitness = sum(individuo.fitness for individuo in populacao)

    # Gera um número aleatório entre 0 e a soma total dos fitness
    ponto_roleta = random.uniform(0, soma_fitness)

    # Percorre a população acumulando os fitness
    fitness_acumulado = 0
    for individuo in populacao:
        fitness_acumulado += individuo.fitness
        # Se o ponto da roleta cair dentro do intervalo do indivíduo, ele é selecionado
        if ponto_roleta <= fitness_acumulado:
            return individuo

def selecao_ranking(populacao):
    """
    Seleciona um indivíduo da população usando o método de ranking.

    Args:
        populacao: Lista de indivíduos.

    Returns:
        Individuo selecionado.
    """
    # Ordena a população em ordem crescente de fitness
    populacao_ordenada = sorted(populacao, key=lambda individuo: individuo.fitness)

    # Cria uma lista de ranks, onde o pior indivíduo tem rank 1 e o melhor tem rank N
    ranks = list(range(1, len(populacao) + 1))

    # Calcula a soma total dos ranks
    soma_ranks = sum(ranks)

    # Gera um número aleatório entre 0 e a soma total dos ranks
    ponto_roleta = random.uniform(0, soma_ranks)

    # Percorre a lista de ranks acumulando seus valores
    rank_acumulado = 0
    for i, rank in enumerate(ranks):
        rank_acumulado += rank
        # Se o ponto da roleta cair dentro do intervalo do rank, o indivíduo correspondente é selecionado
        if ponto_roleta <= rank_acumulado:
            return populacao_ordenada[i]

def crossover_dois_pontos(pai1, pai2):
    """
    Realiza o crossover de dois pontos entre dois indivíduos (pais).

    Este método de crossover seleciona aleatoriamente dois pontos de corte no genoma dos pais.
    Os genes entre esses pontos de corte são trocados entre os pais para gerar dois filhos.

    Args:
        pai1: O primeiro indivíduo (objeto Individuo) para o crossover.
        pai2: O segundo indivíduo (objeto Individuo) para o crossover.

    Returns:
        Uma tupla contendo dois novos indivíduos (objetos Individuo) que são
        os filhos resultantes do crossover.
    """
    ponto1, ponto2 = sorted(random.sample(range(len(pai1.genoma)), 2))
    filho1_genoma = pai1.genoma[:ponto1] + pai2.genoma[ponto1:ponto2] + pai1.genoma[ponto2:]
    filho2_genoma = pai2.genoma[:ponto1] + pai1.genoma[ponto1:ponto2] + pai2.genoma[ponto2:]
    return Individuo(filho1_genoma), Individuo(filho2_genoma)

def mutacao(individuo, taxa_mutacao):
    """
    Realiza a mutação em um indivíduo com uma determinada taxa.

    A mutação percorre cada gene (bit) do genoma do indivíduo.
    Para cada gene, um número aleatório entre 0 e 1 é gerado.
    Se esse número for menor que a taxa de mutação, o gene é invertido (0 vira 1 e vice-versa).

    Args:
        individuo: O indivíduo (objeto Individuo) a ser mutado.
        taxa_mutacao: A probabilidade de cada gene ser mutado.
    """
    for i in range(len(individuo.genoma)):
        if random.random() < taxa_mutacao:
            individuo.genoma[i] = 1 - individuo.genoma[i]

def algoritmo_genetico(dados_conteineres, max_peso, max_volume, tamanho_populacao, num_geracoes, taxa_crossover, taxa_mutacao, funcao_selecao):
    """
    Executa o algoritmo genético para encontrar a melhor solução para o problema de carregamento de contêineres.

    Args:
        dados_conteineres: Lista de tuplas contendo os dados dos contêineres (peso, volume, valor).
        max_peso: Peso máximo que o navio pode carregar.
        max_volume: Volume máximo que o navio pode carregar.
        tamanho_populacao: Número de indivíduos na população.
        num_geracoes: Número de gerações a serem evoluídas.
        taxa_crossover: Probabilidade de crossover entre dois pais.
        taxa_mutacao: Probabilidade de mutação de um gene.
        funcao_selecao: Função de seleção a ser utilizada (ex: selecao_torneio, selecao_roleta).

    Returns:
        Objeto Individuo representando o melhor indivíduo encontrado após a execução do algoritmo.
    """
    tamanho_genoma = len(dados_conteineres)
    populacao = inicializar_populacao(tamanho_populacao, tamanho_genoma)
    melhor_global = None

    for geracao in range(num_geracoes):
        # Avalia a população atual
        for individuo in populacao:
            individuo.fitness = calcular_fitness(individuo, dados_conteineres, max_peso, max_volume)

        # Seleciona o melhor indivíduo da geração atual
        melhor_atual = max(populacao, key=lambda ind: ind.fitness)

        # Atualiza o melhor global, se necessário
        if melhor_global is None or melhor_atual.fitness > melhor_global.fitness:
            melhor_global = Individuo(melhor_atual.genoma)
            melhor_global.fitness = melhor_atual.fitness

        # Cria a próxima geração
        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            # Aplica crossover com a probabilidade definida
            if random.random() < taxa_crossover:
                pai1, pai2 = funcao_selecao(populacao), funcao_selecao(populacao)
                filho1, filho2 = crossover_dois_pontos(pai1, pai2)
                nova_populacao.extend([filho1, filho2])
            else:
                # Se não houver crossover, seleciona um indivíduo para a próxima geração
                nova_populacao.append(funcao_selecao(populacao))

        # Aplica mutação na nova população
        for individuo in nova_populacao:
            mutacao(individuo, taxa_mutacao)

        # Atualiza a população para a próxima geração
        populacao = nova_populacao

    # Retorna o melhor indivíduo encontrado em todas as gerações
    return melhor_global
