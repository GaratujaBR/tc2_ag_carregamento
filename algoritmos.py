import random
import time

# Classe Individuo (se você estiver usando uma)
class Individuo:
    def __init__(self, genoma):
        self.genoma = genoma
        self.fitness = 0

# Funções do Algoritmo Genético
def inicializar_populacao(tamanho_populacao, tamanho_genoma):
    return [Individuo([random.choice([0, 1]) for _ in range(tamanho_genoma)]) for _ in range(tamanho_populacao)]

def calcular_fitness(individuo, dados_conteineres, max_peso, max_volume):
    peso_total = 0
    volume_total = 0
    valor_total = 0
    for i, bit in enumerate(individuo.genoma):
        if bit == 1:
            peso, volume, valor = dados_conteineres[i]
            peso_total += peso
            volume_total += volume
            valor_total += valor
    if peso_total > max_peso:
        valor_total -= (peso_total - max_peso) * 1000
    if volume_total > max_volume:
        valor_total -= (volume_total - max_volume) * 100
    return max(0, valor_total)

def selecao_torneio(populacao, tamanho_torneio=3):
    selecionados = random.sample(populacao, tamanho_torneio)
    return max(selecionados, key=lambda ind: ind.fitness)

def crossover_dois_pontos(pai1, pai2):
    ponto1, ponto2 = sorted(random.sample(range(len(pai1.genoma)), 2))
    filho1_genoma = pai1.genoma[:ponto1] + pai2.genoma[ponto1:ponto2] + pai1.genoma[ponto2:]
    filho2_genoma = pai2.genoma[:ponto1] + pai1.genoma[ponto1:ponto2] + pai2.genoma[ponto2:]
    return Individuo(filho1_genoma), Individuo(filho2_genoma)

def mutacao(individuo, taxa_mutacao):
    for i in range(len(individuo.genoma)):
        if random.random() < taxa_mutacao:
            individuo.genoma[i] = 1 - individuo.genoma[i]

def algoritmo_genetico(dados_conteineres, max_peso, max_volume, tamanho_populacao, num_geracoes, taxa_crossover, taxa_mutacao):
    tamanho_genoma = len(dados_conteineres)
    populacao = inicializar_populacao(tamanho_populacao, tamanho_genoma)
    melhor_global = None

    for _ in range(num_geracoes):
        for individuo in populacao:
            individuo.fitness = calcular_fitness(individuo, dados_conteineres, max_peso, max_volume)
        
        melhor_atual = max(populacao, key=lambda ind: ind.fitness)
        if melhor_global is None or melhor_atual.fitness > melhor_global.fitness:
            melhor_global = Individuo(melhor_atual.genoma)
            melhor_global.fitness = melhor_atual.fitness

        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            if random.random() < taxa_crossover:
                pai1, pai2 = selecao_torneio(populacao), selecao_torneio(populacao)
                filho1, filho2 = crossover_dois_pontos(pai1, pai2)
                nova_populacao.extend([filho1, filho2])
            else:
                nova_populacao.append(selecao_torneio(populacao))

        for individuo in nova_populacao:
            mutacao(individuo, taxa_mutacao)

        populacao = nova_populacao

    return melhor_global

def decodificar_solucao(melhor_individuo, dados_conteineres):
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

# Heurística Gulosa
def heuristica_gulosa(dados_conteineres, max_peso, max_volume):
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

# Algoritmo de Aproximação por Razão (AAR)
def algoritmo_aproximacao_razao(dados_conteineres, max_peso, max_volume):
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
    def gerar_solucao_inicial():
        return [random.choice([0, 1]) for _ in range(len(dados_conteineres))]

    def calcular_valor(solucao):
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

# Função para executar e comparar todos os algoritmos
def executar_comparacao(dados_conteineres, max_peso, max_volume, params_ag):
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