import random
import time

# Classe Individuo
class Individuo:
    def __init__(self, genoma):
        self.genoma = genoma
        self.fitness = 0

def gerar_dados_conteineres(num_conteineres):
    """
    Gera dados aleatórios para um determinado número de contêineres.

    Args:
        num_conteineres: O número de contêineres a serem gerados.

    Returns:
        Uma lista de tuplas, onde cada tupla representa um contêiner e contém:
            (peso, volume, valor)
    """
    dados_conteineres = []
    for _ in range(num_conteineres):
        peso = random.randint(1, 50)  # Peso entre 1 e 50 toneladas
        volume = random.randint(1, 100)  # Volume entre 1 e 100 metros cúbicos
        valor = random.randint(100, 1000)  # Valor entre 100 e 1000 unidades monetárias
        dados_conteineres.append((peso, volume, valor))
    return dados_conteineres

# Funções do Algoritmo Genético
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

def decodificar_solucao(melhor_individuo, dados_conteineres):
    """
    Decodifica a solução representada pelo melhor indivíduo encontrado pelo algoritmo genético.

    A função percorre o genoma do indivíduo e, para cada bit 1, adiciona o contêiner
    correspondente à lista de contêineres carregados. Também calcula o peso total,
    volume total e valor total dos contêineres carregados.

    Args:
        melhor_individuo: Objeto Individuo representando a melhor solução encontrada.
        dados_conteineres: Lista de tuplas contendo os dados dos contêineres (peso, volume, valor).

    Returns:
        Uma tupla contendo:
            - Uma lista de tuplas, onde cada tupla representa um contêiner carregado e contém:
                (índice do contêiner, peso, volume, valor).
            - O peso total dos contêineres carregados.
            - O volume total dos contêineres carregados.
            - O valor total dos contêineres carregados.
    """
    conteineres_carregados = []
    peso_total = 0
    volume_total = 0
    valor_total = 0
    for i, bit in enumerate(melhor_individuo.genoma):
        if bit == 1:
            peso, volume, valor = dados_conteineres[i]
            conteineres_carregados.append((i, peso, volume, valor))
            peso_total += peso
            volume_total += volume
            valor_total += valor
    return conteineres_carregados, peso_total, volume_total, valor_total

def heuristica_gulosa(dados_conteineres, max_peso, max_volume):
    """
    Implementa a heurística gulosa para o problema de carregamento de contêineres.

    A heurística consiste em ordenar os contêineres pela razão valor/(peso + volume)
    em ordem decrescente e selecionar os contêineres nessa ordem até que a capacidade
    máxima de peso ou volume do navio seja atingida.

    Args:
        dados_conteineres: Lista de tuplas contendo os dados dos contêineres (peso, volume, valor).
        max_peso: Peso máximo que o navio pode carregar.
        max_volume: Volume máximo que o navio pode carregar.

    Returns:
        Uma tupla contendo:
            - Uma lista de inteiros representando os índices dos contêineres selecionados.
            - O peso total dos contêineres selecionados.
            - O volume total dos contêineres selecionados.
            - O valor total dos contêineres selecionados.
    """
    conteineres_com_razao = [
        (i, dados[2] / (dados[0] + dados[1]), dados)
        for i, dados in enumerate(dados_conteineres)
    ]
    conteineres_ordenados = sorted(conteineres_com_razao, key=lambda x: x[1], reverse=True)

    conteineres_selecionados = []
    peso_total = 0
    volume_total = 0
    valor_total = 0

    for i, razao, (peso, volume, valor) in conteineres_ordenados:
        if peso_total + peso <= max_peso and volume_total + volume <= max_volume:
            conteineres_selecionados.append(i)
            peso_total += peso
            volume_total += volume
            valor_total += valor

    return conteineres_selecionados, peso_total, volume_total, valor_total

def algoritmo_aproximacao_razao(dados_conteineres, max_peso, max_volume):
    """
    Implementa o algoritmo de aproximação por razão para o problema de carregamento de contêineres.

    Este algoritmo calcula a razão valor/(peso + volume) para cada contêiner e os ordena
    em ordem decrescente dessa razão. Em seguida, percorre a lista ordenada e seleciona
    os contêineres até que a capacidade máxima de peso ou volume do navio seja atingida.

    Args:
        dados_conteineres: Lista de tuplas contendo os dados dos contêineres (peso, volume, valor).
        max_peso: Peso máximo que o navio pode carregar.
        max_volume: Volume máximo que o navio pode carregar.

    Returns:
        Uma tupla contendo:
            - Uma lista de inteiros representando os índices dos contêineres selecionados.
            - O peso total dos contêineres selecionados.
            - O volume total dos contêineres selecionados.
            - O valor total dos contêineres selecionados.
    """
    conteineres_com_razao = [
        (i, dados[2] / (dados[0] + dados[1]), dados)
        for i, dados in enumerate(dados_conteineres)
    ]
    conteineres_ordenados = sorted(conteineres_com_razao, key=lambda x: x[1], reverse=True)

    conteineres_selecionados = []
    peso_total = 0
    volume_total = 0
    valor_total = 0

    for i, razao, (peso, volume, valor) in conteineres_ordenados:
        if peso_total + peso <= max_peso and volume_total + volume <= max_volume:
            conteineres_selecionados.append(i)
            peso_total += peso
            volume_total += volume
            valor_total += valor

    return conteineres_selecionados, peso_total, volume_total, valor_total

# Busca Local
def busca_local(dados_conteineres, max_peso, max_volume, max_iteracoes=1000):
    """
    Implementa o algoritmo de Busca Local para o problema de carregamento de contêineres.

    A Busca Local começa com uma solução inicial aleatória e tenta melhorá-la
    iterativamente, explorando soluções vizinhas. Em cada iteração, um vizinho
    é gerado aleatoriamente e, se ele for melhor que a solução atual, a solução
    atual é substituída pelo vizinho. O processo continua até que um número
    máximo de iterações seja atingido.

    Args:
        dados_conteineres: Lista de tuplas contendo os dados dos contêineres (peso, volume, valor).
        max_peso: Peso máximo que o navio pode carregar.
        max_volume: Volume máximo que o navio pode carregar.
        max_iteracoes: Número máximo de iterações da busca local.

    Returns:
        Uma tupla contendo:
            - Uma lista de inteiros representando os índices dos contêineres selecionados.
            - O peso total dos contêineres selecionados.
            - O volume total dos contêineres selecionados.
            - O valor total dos contêineres selecionados.
    """

    def gerar_solucao_inicial():
        """Gera uma solução inicial aleatória."""
        return [random.choice([0, 1]) for _ in range(len(dados_conteineres))]

    def calcular_valor(solucao):
        """Calcula o valor total de uma solução, considerando as restrições."""
        peso_total = 0
        volume_total = 0
        valor_total = 0
        for i, bit in enumerate(solucao):
            if bit == 1:
                peso, volume, valor = dados_conteineres[i]
                peso_total += peso
                volume_total += volume
                valor_total += valor
        if peso_total > max_peso or volume_total > max_volume:
            return 0  # Solução inválida
        return valor_total

    def gerar_vizinho(solucao):
        """Gera uma solução vizinha a partir da solução atual."""
        vizinho = solucao.copy()
        indice = random.randint(0, len(vizinho) - 1)
        vizinho[indice] = 1 - vizinho[indice]  # Inverte o bit
        return vizinho

    melhor_solucao = gerar_solucao_inicial()
    melhor_valor = calcular_valor(melhor_solucao)

    for _ in range(max_iteracoes):
        vizinho = gerar_vizinho(melhor_solucao)
        valor_vizinho = calcular_valor(vizinho)
        if valor_vizinho > melhor_valor:
            melhor_solucao = vizinho
            melhor_valor = valor_vizinho

    # Decodificar a melhor solução
    conteineres_selecionados = []
    peso_total = 0
    volume_total = 0
    valor_total = 0
    for i, bit in enumerate(melhor_solucao):
        if bit == 1:
            peso, volume, valor = dados_conteineres[i]
            conteineres_selecionados.append(i)
            peso_total += peso
            volume_total += volume
            valor_total += valor

    return conteineres_selecionados, peso_total, volume_total, valor_total

def executar_comparacao(dados_conteineres, max_peso, max_volume, params_ag):
    """
    Executa e compara diferentes algoritmos para o problema de carregamento de contêineres.

    Esta função executa os seguintes algoritmos:
        - Algoritmo de Aproximação por Razão (AAR)
        - Heurística Gulosa
        - Busca Local
        - Algoritmo Genético (AG)

    Para cada algoritmo, a função registra o tempo de execução, a lista de contêineres
    selecionados, o peso total, o volume total e o valor total da carga.

    Args:
        dados_conteineres: Lista de tuplas contendo os dados dos contêineres (peso, volume, valor).
        max_peso: Peso máximo que o navio pode carregar.
        max_volume: Volume máximo que o navio pode carregar.
        params_ag: Um dicionário contendo os parâmetros para o algoritmo genético.

    Returns:
        Um dicionário contendo os resultados de cada algoritmo, onde a chave é o nome
        do algoritmo e o valor é outro dicionário com as seguintes chaves:
            - 'conteineres': Lista de inteiros representando os índices dos contêineres selecionados.
            - 'peso_total': Peso total dos contêineres selecionados.
            - 'volume_total': Volume total dos contêineres selecionados.
            - 'valor_total': Valor total dos contêineres selecionados.
            - 'tempo_execucao': Tempo de execução do algoritmo em segundos.
    """
    resultados = {}

    # AAR
    tempo_inicio = time.time()
    resultado_aar = algoritmo_aproximacao_razao(dados_conteineres, max_peso, max_volume)
    tempo_aar = time.time() - tempo_inicio
    resultados["AAR"] = {
        "conteineres": resultado_aar[0],
        "peso_total": resultado_aar[1],
        "volume_total": resultado_aar[2],
        "valor_total": resultado_aar[3],
        "tempo_execucao": tempo_aar
    }

    # Heurística Gulosa
    tempo_inicio = time.time()
    resultado_gulosa = heuristica_gulosa(dados_conteineres, max_peso, max_volume)
    tempo_gulosa = time.time() - tempo_inicio
    resultados["Gulosa"] = {
        "conteineres": resultado_gulosa[0],
        "peso_total": resultado_gulosa[1],
        "volume_total": resultado_gulosa[2],
        "valor_total": resultado_gulosa[3],
        "tempo_execucao": tempo_gulosa
    }

    # Busca Local
    tempo_inicio = time.time()
    resultado_bl = busca_local(dados_conteineres, max_peso, max_volume)
    tempo_bl = time.time() - tempo_inicio
    resultados["Busca Local"] = {
        "conteineres": resultado_bl[0],
        "peso_total": resultado_bl[1],
        "volume_total": resultado_bl[2],
        "valor_total": resultado_bl[3],
        "tempo_execucao": tempo_bl
    }

    # Algoritmo Genético
    tempo_inicio = time.time()
    melhor_solucao_ag = algoritmo_genetico(dados_conteineres, max_peso, max_volume, **params_ag)
    tempo_ag = time.time() - tempo_inicio
    resultado_ag = decodificar_solucao(melhor_solucao_ag, dados_conteineres)
    resultados["AG"] = {
        "conteineres": resultado_ag[0],
        "peso_total": resultado_ag[1],
        "volume_total": resultado_ag[2],
        "valor_total": resultado_ag[3],
        "tempo_execucao": tempo_ag
    }

    return resultados
