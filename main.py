import random
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from algoritmo_genetico import algoritmo_genetico, decodificar_solucao
from heuristica_gulosa import heuristica_gulosa
from visualizacoes import plot_comparison, plot_boxplot, plot_execution_time, plot_improvements
from utils import gerar_dados_conteineres

# Configurações globais
random.seed(42)  # Para reprodutibilidade
plt.style.use('seaborn')
sns.set_palette("deep")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

def executar_comparacao(dados_conteineres, max_peso, max_volume, params_ag):
    # Executar heurística gulosa
    tempo_inicio_gulosa = time.time()
    resultado_gulosa = heuristica_gulosa(dados_conteineres, max_peso, max_volume)
    tempo_gulosa = time.time() - tempo_inicio_gulosa
    
    # Executar algoritmo genético
    tempo_inicio_ag = time.time()
    melhor_solucao_ag = algoritmo_genetico(dados_conteineres, max_peso, max_volume, **params_ag)
    tempo_ag = time.time() - tempo_inicio_ag
    resultado_ag = decodificar_solucao(melhor_solucao_ag, dados_conteineres)
    
    return {
        "Gulosa": {
            "conteineres": resultado_gulosa[0],
            "peso_total": resultado_gulosa[1],
            "volume_total": resultado_gulosa[2],
            "valor_total": resultado_gulosa[3],
            "tempo_execucao": tempo_gulosa
        },
        "AG": {
            "conteineres": resultado_ag[0],
            "peso_total": resultado_ag[1],
            "volume_total": resultado_ag[2],
            "valor_total": resultado_ag[3],
            "tempo_execucao": tempo_ag
        }
    }

def executar_ag_multiplas_vezes(dados_conteineres, max_peso, max_volume, params_ag, num_execucoes=10):
    resultados = []
    for _ in range(num_execucoes):
        melhor_solucao = algoritmo_genetico(dados_conteineres, max_peso, max_volume, **params_ag)
        resultado = decodificar_solucao(melhor_solucao, dados_conteineres)
        resultados.append(resultado[3])  # Armazena apenas o valor total
    return resultados

def experimento_completo(max_peso, max_volume, num_conteineres, params_ag, num_execucoes_consistencia=10):
    dados_conteineres = gerar_dados_conteineres(num_conteineres)
    
    print("Executando comparação única AG vs Heurística Gulosa...")
    resultados = executar_comparacao(dados_conteineres, max_peso, max_volume, params_ag)
    
    print("Executando múltiplas execuções do AG para análise de consistência...")
    resultados_ag_multiplos = executar_ag_multiplas_vezes(dados_conteineres, max_peso, max_volume, params_ag, num_execucoes_consistencia)
    
    print("\nResultados da comparação:")
    for algoritmo, resultado in resultados.items():
        print(f"\n{algoritmo}:")
        print(f"Valor total do frete: ${resultado['valor_total'] * 1000:.2f}")
        print(f"Peso total: {resultado['peso_total']} toneladas")
        print(f"Volume total: {resultado['volume_total']} metros cúbicos")
        print(f"Tempo de execução: {resultado['tempo_execucao']:.4f} segundos")
        print(f"Número de contêineres carregados: {len(resultado['conteineres'])}")
    
    print("\nAnálise de consistência do AG:")
    print(f"Média do valor total: ${np.mean(resultados_ag_multiplos) * 1000:.2f}")
    print(f"Desvio padrão: ${np.std(resultados_ag_multiplos) * 1000:.2f}")
    print(f"Valor mínimo: ${min(resultados_ag_multiplos) * 1000:.2f}")
    print(f"Valor máximo: ${max(resultados_ag_multiplos) * 1000:.2f}")
    
    # Gerar visualizações
    print("\nGerando visualizações...")
    plot_comparison(resultados['AG']['valor_total'], resultados['Gulosa']['valor_total'], 
                    'Comparação de Valor Total do Frete', 'Valor do Frete ($)', 'resultados/valor_frete_comparacao.png')
    
    plot_comparison(len(resultados['AG']['conteineres']), len(resultados['Gulosa']['conteineres']), 
                    'Comparação do Número de Contêineres', 'Número de Contêineres', 'resultados/num_conteineres_comparacao.png')
    
    plot_boxplot(resultados_ag_multiplos, 'Distribuição dos Resultados do AG', 'Valor do Frete ($)', 'resultados/ag_resultados_distribuicao.png')
    
    plot_execution_time(resultados['AG']['tempo_execucao'], resultados['Gulosa']['tempo_execucao'], 
                        'Comparação de Tempo de Execução', 'resultados/tempo_execucao_comparacao.png')
    
    melhoria_valor = ((np.mean(resultados_ag_multiplos) / resultados['Gulosa']['valor_total']) - 1) * 100
    melhoria_conteineres = ((len(resultados['AG']['conteineres']) / len(resultados['Gulosa']['conteineres'])) - 1) * 100
    plot_improvements([melhoria_valor, melhoria_conteineres], ['Valor do Frete', 'Número de Contêineres'], 
                      'Melhorias Percentuais do AG vs HG', 'resultados/melhorias_percentuais.png')
    
    print("Experimento concluído. Os resultados e visualizações foram salvos na pasta 'resultados/'.")

if __name__ == "__main__":
    MAX_PESO = 1000  # toneladas
    MAX_VOLUME = 5000  # metros cúbicos
    NUM_CONTEINERES = 50

    params_ag = {
        "tamanho_populacao": 100,
        "num_geracoes": 1000,
        "taxa_crossover": 0.8,
        "taxa_mutacao": 0.01
    }

    experimento_completo(MAX_PESO, MAX_VOLUME, NUM_CONTEINERES, params_ag)