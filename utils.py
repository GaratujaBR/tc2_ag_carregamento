import random
from algoritmo_genetico import algoritmo_genetico
from heuristica_gulosa import heuristica_gulosa
from busca_local import busca_local

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

def gerar_dados_conteineres_estaticos():
    """
    Retorna uma lista estática de 50 contêineres com valores preenchidos.

    Returns:
        Uma lista de tuplas, onde cada tupla representa um contêiner e contém:
            (peso, volume, valor)
    """
    return [
        (9, 97, 288), (29, 7, 315), (11, 77, 145), (50, 56, 460), (30, 74, 619),
        (18, 16, 276), (35, 36, 715), (50, 55, 956), (26, 87, 534), (8, 90, 956),
        (26, 39, 830), (35, 4, 741), (3, 45, 285), (46, 8, 234), (1, 90, 850),
        (15, 100, 490), (43, 84, 738), (34, 32, 447), (25, 58, 994), (29, 56, 949),
        (26, 94, 641), (16, 18, 305), (42, 90, 584), (5, 87, 472), (33, 32, 810),
        (38, 26, 529), (48, 4, 803), (6, 10, 595), (49, 98, 331), (16, 21, 749),
        (49, 62, 518), (5, 100, 706), (49, 45, 487), (16, 54, 942), (18, 47, 167),
        (2, 77, 812), (26, 69, 668), (27, 41, 231), (44, 67, 523), (32, 92, 715),
        (2, 61, 629), (35, 28, 777), (13, 81, 223), (4, 11, 371), (12, 78, 818),
        (1, 70, 930), (18, 17, 165), (46, 3, 572), (24, 74, 891), (13, 74, 890)
    ]

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

def executar_ag_multiplas_vezes(dados_conteineres, max_peso, max_volume, params_ag, num_execucoes=10):
    resultados = []
    for _ in range(num_execucoes):
        melhor_solucao = algoritmo_genetico(dados_conteineres, max_peso, max_volume, False, **params_ag)
        resultado = decodificar_solucao(melhor_solucao, dados_conteineres)
        resultados.append(resultado[3])  # Armazena apenas o valor total
    return resultados

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

    # Heurística Gulosa
    resultado_gulosa = heuristica_gulosa(dados_conteineres, max_peso, max_volume)
    resultados["Gulosa"] = {
        "conteineres": resultado_gulosa[0],
        "peso_total": resultado_gulosa[1],
        "volume_total": resultado_gulosa[2],
        "valor_total": resultado_gulosa[3]
    }

    # Busca Local
    resultado_bl = busca_local(dados_conteineres, max_peso, max_volume)
    resultados["Busca Local"] = {
        "conteineres": resultado_bl[0],
        "peso_total": resultado_bl[1],
        "volume_total": resultado_bl[2],
        "valor_total": resultado_bl[3]
    }

    # Algoritmo Genético
    melhor_solucao_ag = algoritmo_genetico(dados_conteineres, max_peso, max_volume, True, **params_ag)
    resultado_ag = decodificar_solucao(melhor_solucao_ag, dados_conteineres)
    resultados["AG"] = {
        "conteineres": resultado_ag[0],
        "peso_total": resultado_ag[1],
        "volume_total": resultado_ag[2],
        "valor_total": resultado_ag[3]
    }

    return resultados
