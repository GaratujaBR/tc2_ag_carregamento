import matplotlib.pyplot as plt
import seaborn as sns

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

def plot_comparison(valores, labels, title, ylabel, filename=None, tipo_dado='valor'):
    """
    Plota um gráfico de barras comparando diferentes valores.

    Args:
        valores: Lista de valores a serem plotados.
        labels: Lista de rótulos para as barras.
        title: Título do gráfico.
        ylabel: Rótulo do eixo y.
        filename: Nome do arquivo para salvar o gráfico (opcional).
        tipo_dado: Tipo de dado a ser plotado ('valor', 'conteineres', 'peso', 'volume').
    """
    fig, ax = plt.subplots()
    bars = ax.bar(labels, valores, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'][:len(valores)])
    ax.set_title(title)
    ax.set_ylabel(ylabel)

    # Formatação do texto nas barras
    for bar in bars:
        height = bar.get_height()
        if tipo_dado == 'valor':
            text = f'{height:.2f}'
        else:
            text = f'{int(height)}'  # Formata como inteiro para 'conteineres', 'peso' e 'volume'
        ax.text(bar.get_x() + bar.get_width()/2., height, text,
                ha='center', va='bottom', fontsize=8)

    ax.grid(axis='y', linestyle='--', alpha=0.7)
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

def plot_improvements(melhorias, labels=['Valor do Frete', 'Número de Contêineres'],
                      title='Melhorias Percentuais do AG vs HG', filename=None):
    """
    Plota um gráfico de barras mostrando as melhorias percentuais do Algoritmo Genético (AG)
    em relação a outros algoritmos.

    Args:
        melhorias (list): Uma lista contendo as melhorias percentuais do AG para cada métrica.
        labels (list, optional): Uma lista contendo os rótulos para as barras,
                                 representando as métricas comparadas.
                                 Defaults to ['Valor do Frete', 'Número de Contêineres'].
        title (str, optional): O título do gráfico.
                               Defaults to 'Melhorias Percentuais do AG vs HG'.
        filename (str, optional): O nome do arquivo para salvar o gráfico. Defaults to None.
    """
    fig, ax = plt.subplots()
    bars = ax.bar(labels, melhorias, color=['#ff99bb', '#66b300'])
    ax.set_title(title)
    ax.set_ylabel('Melhoria Percentual (%)')

    # Adiciona o valor da melhoria percentual acima de cada barra
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}%',
                ha='center', va='bottom', fontsize=8)

    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Salva o gráfico em um arquivo, se o nome do arquivo for fornecido
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()