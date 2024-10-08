import random

class Individuo:
    def __init__(self, genoma):
        self.genoma = genoma
        self.fitness = 0

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