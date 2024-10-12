import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from utils import gerar_dados_conteineres, gerar_dados_conteineres_estaticos, decodificar_solucao, executar_ag_multiplas_vezes, executar_comparacao
from algoritmo_genetico import selecao_torneio, selecao_roleta, selecao_ranking
from visualizacoes import plot_comparison, plot_improvements
import argparse

# Configurações globais
sns.set_theme()
sns.set_palette("deep")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

def experimento_completo(max_peso, max_volume, num_conteineres, dados_conteineres, params_ag, num_execucoes_consistencia=10):
    """
    Executa um experimento completo para o problema de carregamento de contêineres,
    comparando diferentes algoritmos e analisando a consistência do Algoritmo Genético (AG).

    Args:
        max_peso (int): Peso máximo que o navio pode carregar (em toneladas).
        max_volume (int): Volume máximo que o navio pode carregar (em metros cúbicos).
        num_conteineres (int): Número de contêineres disponíveis para carregamento.
        dados_conteineres (list): Lista de tuplas contendo os dados dos contêineres (peso, volume, valor).
        params_ag (dict): Dicionário contendo os parâmetros para o algoritmo genético.
        num_execucoes_consistencia (int, optional): Número de execuções do AG para análise de consistência.
                                                    Defaults to 10.
    """
    # Cria a pasta 'resultados' se ela não existir
    if not os.path.exists('resultados'):
        os.makedirs('resultados')

    print("Executando comparação entre todos os algoritmos...")
    # Executa a comparação entre os algoritmos e armazena os resultados
    resultados = executar_comparacao(dados_conteineres, max_peso, max_volume, params_ag)

    print("Executando múltiplas execuções do AG para análise de consistência...")
    # Executa o AG múltiplas vezes para análise de consistência
    resultados_ag_multiplos = executar_ag_multiplas_vezes(dados_conteineres, max_peso, max_volume, params_ag, num_execucoes_consistencia)

    # Imprime os resultados da comparação entre os algoritmos
    print("\nResultados da comparação:")
    for algoritmo, resultado in resultados.items():
        print(f"\n{algoritmo}:")
        print(f"Valor total do frete: ${resultado['valor_total']:.2f}")
        print(f"Peso total: {resultado['peso_total']} toneladas")
        print(f"Volume total: {resultado['volume_total']} metros cúbicos")
        print(f"Número de contêineres carregados: {len(resultado['conteineres'])}")

    # Imprime os resultados da análise de consistência do AG
    print("\nAnálise de consistência do AG:")
    print(f"Média do valor total: ${np.mean(resultados_ag_multiplos):.2f}")
    print(f"Desvio padrão: ${np.std(resultados_ag_multiplos):.2f}")
    print(f"Valor mínimo: ${min(resultados_ag_multiplos):.2f}")
    print(f"Valor máximo: ${max(resultados_ag_multiplos):.2f}")

    # Gera as visualizações dos resultados
    print("\nGerando visualizações...")

    # Cria a pasta de resultados não existir
    pasta_resultados = 'resultados'
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)

    # Comparação de Valor Total do Frete
    valores_frete = [resultado['valor_total'] for resultado in resultados.values()]
    labels = list(resultados.keys())
    plot_comparison(valores_frete, labels,
                'Comparação de Valor Total do Frete', 'Valor do Frete ($)',
                os.path.join(pasta_resultados, 'valor_frete_comparacao.png'))

    # Comparação do Número de Contêineres
    num_conteineres = [len(resultado['conteineres']) for resultado in resultados.values()]
    plot_comparison(num_conteineres, labels,
                    'Comparação do Número de Contêineres', 'Número de Contêineres',
                    os.path.join(pasta_resultados, 'num_conteineres_comparacao.png'))

    # Comparação de Peso Total
    pesos_totais = [resultado['peso_total'] for resultado in resultados.values()]
    plot_comparison(pesos_totais, labels,
                    'Comparação de Peso Total', 'Peso Total (toneladas)',
                    os.path.join(pasta_resultados, 'peso_total_comparacao.png'),
                    tipo_dado='peso')

    # Comparação de Volume Total
    volumes_totais = [resultado['volume_total'] for resultado in resultados.values()]
    plot_comparison(volumes_totais, labels,
                    'Comparação de Volume Total', 'Volume Total (metros cúbicos)',
                    os.path.join(pasta_resultados, 'volume_total_comparacao.png'),
                    tipo_dado='volume')

    # Melhorias Percentuais do AG em relação aos outros algoritmos
    melhorias = []
    valores = []
    conteineres = []
    for algoritmo in resultados:
        if algoritmo != 'AG':
            melhoria_valor = ((resultados['AG']['valor_total'] / resultados[algoritmo]['valor_total']) - 1) * 100
            valores.append(melhoria_valor)
            melhoria_conteineres = ((len(resultados['AG']['conteineres']) / len(resultados[algoritmo]['conteineres'])) - 1) * 100
            conteineres.append(melhoria_conteineres)
    melhorias.extend(valores)
    melhorias.extend(conteineres)

    labels = [f'{alg} (Valor)' for alg in resultados if alg != 'AG'] + [f'{alg} (Contêineres)' for alg in resultados if alg != 'AG']
    plot_improvements(melhorias, labels, 'Melhorias Percentuais do AG vs Outros Algoritmos',
        os.path.join(pasta_resultados, 'melhorias_percentuais.png'))

    print("Experimento concluído. Os resultados e visualizações foram salvos na pasta 'resultados/'.")

parser = argparse.ArgumentParser(description='Experimento de carregamento de contêineres.')
parser.add_argument('--dados', choices=['estaticos', 'aleatorios'], default='aleatorios',
                    help='Tipo de dados a serem usados (estaticos ou aleatorios)')
parser.add_argument('--selecao', choices=['torneio', 'roleta', 'ranking'], default='torneio',
                    help='Função de seleção a ser utilizada (torneio, roleta ou ranking)')

if __name__ == "__main__":
    try:
        MAX_PESO = 1000  # toneladas
        MAX_VOLUME = 3000  # metros cúbicos
        NUM_CONTEINERES = 50

        args = parser.parse_args()

        # Verifica como os dados serão gerados
        if args.dados == 'estaticos':
            dados_conteineres = gerar_dados_conteineres_estaticos()
        else:
            dados_conteineres = gerar_dados_conteineres(NUM_CONTEINERES)

        # Verifica qual função de seleção deve ser usada
        funcao_selecao = selecao_torneio
        if args.selecao == 'roleta':
            funcao_selecao = selecao_roleta
        elif args.selecao == 'ranking':
            funcao_selecao = selecao_ranking

        params_ag = {
            "tamanho_populacao": 100,
            "num_geracoes": 1000,
            "taxa_crossover": 0.8,           # 1 para sempre existir crossover
            "taxa_mutacao": 0.01,
            "funcao_selecao": funcao_selecao # Adiciona a função de seleção aqui
        }

        experimento_completo(MAX_PESO, MAX_VOLUME, NUM_CONTEINERES, dados_conteineres, params_ag)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        import traceback
        traceback.print_exc()
