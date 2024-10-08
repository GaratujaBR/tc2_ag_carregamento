import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuração de estilo
#plt.style.use('seaborn')
sns.set_theme(style="whitegrid")  # Isso vai definir um estilo similar ao 'seaborn'
sns.set_palette("deep")

# Configuração global para tamanho menor dos gráficos
plt.rcParams['figure.figsize'] = (8, 4)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8

def plot_boxplot(resultados_ag, filename=None):
    fig, ax = plt.subplots()
    sns.boxplot(y=resultados_ag, color='#99ff99', ax=ax)
    ax.set_title('Distribuição dos Resultados do AG')
    ax.set_ylabel('Valor do Frete ($)')
    sns.stripplot(y=resultados_ag, color='#ff9999', jitter=0.3, size=4, ax=ax)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

def plot_comparison(valores, labels, title, ylabel, filename=None):
    fig, ax = plt.subplots()
    bars = ax.bar(labels, valores, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'][:len(valores)])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}',
                ha='center', va='bottom', fontsize=8)

    ax.grid(axis='y', linestyle='--', alpha=0.7)
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

def plot_execution_time(tempos, labels, filename=None):
    fig, ax = plt.subplots(figsize=(6, 4), dpi=50)
    bars = ax.bar(labels, tempos, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'][:len(tempos)])
    
    ax.set_title('Comparação de Tempo de Execução')
    ax.set_ylabel('Tempo (segundos)')

    ax.set_ylim([min(tempos) * 0.9, max(tempos) * 1.1])
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height, f'{height:.2f}s',
                ha='center', va='bottom', fontsize=8)

    plt.tight_layout()

    if filename:
        plt.savefig(filename, dpi=50, bbox_inches='tight')
    
    plt.close()


def plot_improvements(melhorias, labels=['Valor do Frete', 'Número de Contêineres'], title='Melhorias Percentuais do AG vs HG', filename=None):
    fig, ax = plt.subplots()
    bars = ax.bar(labels, melhorias, color=['#ff99bb', '#66b300'])
    ax.set_title(title)
    ax.set_ylabel('Melhoria Percentual (%)')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}%', 
                ha='center', va='bottom', fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

def gerar_todas_visualizacoes(resultados, resultados_ag, num_conteineres_ag, num_conteineres_hg):
    # Gráfico comparando valor total do frete
    plot_comparison(np.mean(resultados_ag), resultados['Gulosa']['valor_total'], 
                    'Comparação de Valor Total do Frete', 'Valor do Frete ($)', 'valor_frete_comparacao.png')

    # Gráfico comparando número de contêineres carregados
    plot_comparison(num_conteineres_ag, num_conteineres_hg, 
                    'Comparação do Número de Contêineres', 'Número de Contêineres', 'num_conteineres_comparacao.png')

    # Boxplot dos resultados do AG
    plot_boxplot(resultados_ag, 'ag_resultados_distribuicao.png')

    # Gráfico de barras comparando tempo de execução
    plot_execution_time(resultados['AG']['tempo_execucao'], resultados['Gulosa']['tempo_execucao'], 'tempo_execucao_comparacao.png')

    # Cálculo e gráfico das melhorias percentuais
    melhoria_valor = ((np.mean(resultados_ag) / resultados['Gulosa']['valor_total']) - 1) * 100
    melhoria_conteineres = ((num_conteineres_ag / num_conteineres_hg) - 1) * 100
    plot_improvements([melhoria_valor, melhoria_conteineres], 'melhorias_percentuais.png')

    # Análise dos resultados (imprime no console)
    print("\nAnálise dos Resultados:")
    print(f"Valor médio do AG: ${np.mean(resultados_ag) * 1000:.2f}")
    print(f"Valor da Heurística Gulosa: ${resultados['Gulosa']['valor_total'] * 1000:.2f}")
    print(f"Melhoria percentual do AG no valor do frete: {melhoria_valor:.2f}%")
    print(f"\nNúmero médio de contêineres (AG): {num_conteineres_ag:.2f}")
    print(f"Número de contêineres (HG): {num_conteineres_hg}")
    print(f"Melhoria percentual do AG no número de contêineres: {melhoria_conteineres:.2f}%")
    print(f"\nTempo de execução AG: {resultados['AG']['tempo_execucao']:.4f} segundos")
    print(f"Tempo de execução HG: {resultados['Gulosa']['tempo_execucao']:.4f} segundos")

__all__ = ['plot_comparison', 'plot_boxplot', 'plot_execution_time', 'plot_improvements', 'gerar_todas_visualizacoes']

