import random
import time

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
