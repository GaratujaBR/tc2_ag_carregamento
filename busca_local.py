import random
import time

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
