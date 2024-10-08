import random

def gerar_dados_conteineres(num_conteineres):
    return [
        [random.randint(10, 50), random.randint(50, 200), random.randint(30, 100)]
        for _ in range(num_conteineres)
    ]