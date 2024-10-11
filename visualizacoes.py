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
    plt.show()

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

__all__ = ['plot_comparison', 'plot_execution_time', 'plot_improvements']
