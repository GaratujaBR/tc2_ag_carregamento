import random
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from algoritmos import gerar_dados_conteineres, executar_comparacao, algoritmo_genetico, decodificar_solucao, selecao_torneio, selecao_roleta, selecao_ranking
from visualizacoes import plot_comparison, plot_boxplot, plot_execution_time, plot_improvements

# Configurações globais
random.seed(42)  # Para reprodutibilidade
sns.set_theme()
sns.set_palette("deep")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

def executar_ag_multiplas_vezes(dados_conteineres, max_peso, max_volume, params_ag, num_execucoes=10):
    resultados = []
    for _ in range(num_execucoes):
        melhor_solucao = algoritmo_genetico(dados_conteineres, max_peso, max_volume, **params_ag)
        resultado = decodificar_solucao(melhor_solucao, dados_conteineres)
        resultados.append(resultado[3])  # Armazena apenas o valor total
    return resultados

def experimento_completo(max_peso, max_volume, num_conteineres, params_ag, num_execucoes_consistencia=10):
    if not os.path.exists('resultados'):
        os.makedirs('resultados')

    dados_conteineres = gerar_dados_conteineres(num_conteineres)

    print("Executando comparação entre todos os algoritmos...")
    resultados = executar_comparacao(dados_conteineres, max_peso, max_volume, params_ag)

    print("Executando múltiplas execuções do AG para análise de consistência...")
    resultados_ag_multiplos = executar_ag_multiplas_vezes(dados_conteineres, max_peso, max_volume, params_ag, num_execucoes_consistencia)

    print("\nResultados da comparação:")
    for algoritmo, resultado in resultados.items():
        print(f"\n{algoritmo}:")
        print(f"Valor total do frete: ${resultado['valor_total']:.2f}")
        print(f"Peso total: {resultado['peso_total']} toneladas")
        print(f"Volume total: {resultado['volume_total']} metros cúbicos")
        print(f"Tempo de execução: {resultado['tempo_execucao']:.4f} segundos")
        print(f"Número de contêineres carregados: {len(resultado['conteineres'])}")

    print("\nAnálise de consistência do AG:")
    print(f"Média do valor total: ${np.mean(resultados_ag_multiplos):.2f}")
    print(f"Desvio padrão: ${np.std(resultados_ag_multiplos):.2f}")
    print(f"Valor mínimo: ${min(resultados_ag_multiplos):.2f}")
    print(f"Valor máximo: ${max(resultados_ag_multiplos):.2f}")

    # Gerar visualizações
    print("\nGerando visualizações...")

    # Comparação de Valor Total do Frete
    valores_frete = [resultado['valor_total'] for resultado in resultados.values()]
    labels = list(resultados.keys())
    plot_comparison(valores_frete, labels,
                'Comparação de Valor Total do Frete', 'Valor do Frete ($)',
                'resultados/valor_frete_comparacao.png')

    # Comparação do Número de Contêineres
    num_conteineres = [len(resultado['conteineres']) for resultado in resultados.values()]
    plot_comparison(num_conteineres, labels,
                    'Comparação do Número de Contêineres', 'Número de Contêineres',
                    'resultados/num_conteineres_comparacao.png')

    # Boxplot dos resultados do AG
    plot_boxplot(resultados_ag_multiplos, filename='resultados/ag_resultados_distribuicao.png')

    # Comparação de Tempo de Execução
    tempos_execucao = [resultado['tempo_execucao'] for resultado in resultados.values()]
    labels = list(resultados.keys())
    plot_execution_time(tempos_execucao, labels,
                    filename='resultados/tempo_execucao_comparacao.png')

    # Melhorias Percentuais
    melhorias = []
    for algoritmo in resultados:
        if algoritmo != 'AG':
            melhoria_valor = ((resultados['AG']['valor_total'] / resultados[algoritmo]['valor_total']) - 1) * 100
            melhoria_conteineres = ((len(resultados['AG']['conteineres']) / len(resultados[algoritmo]['conteineres'])) - 1) * 100
            melhorias.extend([melhoria_valor, melhoria_conteineres])

    labels = [f'{alg} (Valor)' for alg in resultados if alg != 'AG'] + [f'{alg} (Contêineres)' for alg in resultados if alg != 'AG']
    plot_improvements(melhorias, labels, 'Melhorias Percentuais do AG vs Outros Algoritmos', 'resultados/melhorias_percentuais.png')

    print("Experimento concluído. Os resultados e visualizações foram salvos na pasta 'resultados/'.")

if __name__ == "__main__":
    try:
        MAX_PESO = 1000  # toneladas
        MAX_VOLUME = 5000  # metros cúbicos
        NUM_CONTEINERES = 50

        params_ag = {
            "tamanho_populacao": 100,
            "num_geracoes": 1000,
            "taxa_crossover": 0.8,
            "taxa_mutacao": 0.01,
            "funcao_selecao": selecao_ranking # selecao_torneio  # Adiciona a função de seleção aqui
        }

        experimento_completo(MAX_PESO, MAX_VOLUME, NUM_CONTEINERES, params_ag)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        import traceback
        traceback.print_exc()
