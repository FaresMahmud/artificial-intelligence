"""
Algoritmo Genético Interativo - Procurar Palavra
Versão interativa onde o usuário escolhe a palavra alvo e configura
os parâmetros do AG (população, taxa de mutação, crossover, gerações)

Baseado em material do Prof. Alexandre Zamberlan - Técnicas de IA
"""

import random
import string
from datetime import datetime
import os

def obter_parametros():
    """Coleta a palavra alvo e parâmetros do usuário."""
    print("\n" + "=" * 50)
    print("Algoritmo Genético - Procurador de Palavras")
    print("=" * 50)
    
    # Pedir palavra alvo
    while True:
        palavra_alvo = input("\nDigite a palavra alvo: ").strip()
        if len(palavra_alvo) > 0:
            palavra_alvo = palavra_alvo.upper()
            break
        print("Erro: palavra não pode estar vazia")
    
    # Parâmetros do AG
    print("\nConfigure os parâmetros:\n")
    
    while True:
        try:
            tam_populacao = int(input("Tamanho da população (ex: 20): "))
            if tam_populacao < 2:
                print("Mínimo 2 indivíduos")
                continue
            break
        except ValueError:
            print("Digite um número inteiro")
    
    # Taxa de crossover aleatória
    taxa_crossover = random.uniform(0.7, 0.95)
    
    while True:
        try:
            taxa_mutacao = float(input("Taxa de mutação em % (ex: 5): "))
            if not (0 <= taxa_mutacao <= 100):
                print("Digite um valor entre 0 e 100")
                continue
            taxa_mutacao = taxa_mutacao / 100  # Converter pra decimal
            break
        except ValueError:
            print("Digite um número válido")
    
    while True:
        try:
            num_geracoes = int(input("Máximo de gerações (ex: 50000): "))
            if num_geracoes < 1:
                print("Mínimo 1 geração")
                continue
            break
        except ValueError:
            print("Digite um número inteiro")
    
    return {
        'palavra_alvo': palavra_alvo,
        'tam_cromossomo': len(palavra_alvo),
        'tam_populacao': tam_populacao,
        'taxa_crossover': taxa_crossover,
        'taxa_mutacao': taxa_mutacao,
        'num_geracoes': num_geracoes
    }


def criar_cromossomo(tamanho):
    """Cria cromossomo aleatório: string com caracteres aleatorios."""
    alfabeto = string.ascii_uppercase + ' '
    return ''.join(random.choice(alfabeto) for _ in range(tamanho))


def criar_populacao(tamanho_pop, tamanho_crom):
    """Cria população inicial."""
    return [criar_cromossomo(tamanho_crom) for _ in range(tamanho_pop)]


def calcular_fitness(cromossomo, alvo):
    """Calcula fitness: quantidade de caracteres corretos na posição certa."""
    return sum(1 for i, char in enumerate(cromossomo) if char == alvo[i])


def selecao_roleta(populacao, fitness_lista):
    """Seleciona indivíduo por roleta (proporcional ao fitness)."""
    fitness_total = sum(fitness_lista)
    if fitness_total == 0:
        return random.choice(populacao)

    ponto = random.uniform(0, fitness_total)
    acumulado = 0
    for individuo, fitness in zip(populacao, fitness_lista):
        acumulado += fitness
        if acumulado >= ponto:
            return individuo
    return populacao[-1]


def crossover(pai, mae, taxa_crossover):
    """Crossover de 1 ponto."""
    if random.random() > taxa_crossover:
        return pai, mae

    corte = random.randint(1, len(pai) - 1)
    filho1 = pai[:corte] + mae[corte:]
    filho2 = mae[:corte] + pai[corte:]
    return filho1, filho2


def mutacao(cromossomo, taxa_mutacao):
    """Mutação: troca aleatória de caracteres."""
    alfabeto = string.ascii_uppercase + ' '
    resultado = []
    
    for char in cromossomo:
        if random.random() < taxa_mutacao:
            resultado.append(random.choice(alfabeto))
        else:
            resultado.append(char)
    
    return ''.join(resultado)


def pegar_elite(populacao, fitness_lista):
    """Retorna o melhor indivíduo da população."""
    idx_melhor = fitness_lista.index(max(fitness_lista))
    return populacao[idx_melhor]


def executar_ag(params):
    """Executa o algoritmo genético."""
    
    # Criar arquivo temporário com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"AG_RELATORIO_{params['palavra_alvo']}_{timestamp}.txt"
    caminho_arquivo = os.path.join(os.path.expanduser("~"), "Desktop", nome_arquivo)
    
    # Se Desktop não existe, salvar na pasta do script
    if not os.path.exists(os.path.dirname(caminho_arquivo)):
        caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)
    
    # Escrever cabeçalho no arquivo
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("RELATORIO DE EXECUÇÃO - ALGORITMO GENÉTICO\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Palavra alvo: {params['palavra_alvo']}\n")
        f.write(f"População: {params['tam_populacao']}\n")
        f.write(f"Crossover: {params['taxa_crossover']*100:.1f}%\n")
        f.write(f"Mutação: {params['taxa_mutacao']*100:.1f}%\n")
        f.write(f"Max gerações: {params['num_geracoes']}\n")
        f.write("\n" + "=" * 60 + "\n\n")
    
    print("\n" + "=" * 50)
    print("Executando AG...")
    print("=" * 50)
    print(f"Palavra alvo: {params['palavra_alvo']}")
    print(f"População: {params['tam_populacao']}")
    print(f"Crossover: {params['taxa_crossover']*100:.0f}%")
    print(f"Mutação: {params['taxa_mutacao']*100:.1f}%")
    print(f"Max gerações: {params['num_geracoes']}")
    print("=" * 50 + "\n")
    
    populacao = criar_populacao(params['tam_populacao'], params['tam_cromossomo'])
    
    melhor_global = None
    melhor_fitness_global = 0
    
    for geracao in range(1, params['num_geracoes'] + 1):
        fitness_lista = [calcular_fitness(c, params['palavra_alvo']) for c in populacao]
        
        melhor_fitness = max(fitness_lista)
        media_fitness = sum(fitness_lista) / len(fitness_lista)
        idx_melhor = fitness_lista.index(melhor_fitness)
        melhor_cromossomo = populacao[idx_melhor]
        
        if melhor_fitness > melhor_fitness_global:
            melhor_fitness_global = melhor_fitness
            melhor_global = melhor_cromossomo
        
        # Escrever geração no arquivo
        with open(caminho_arquivo, 'a', encoding='utf-8') as f:
            f.write(f"Gen {geracao:5d} | Melhor: {melhor_fitness:2d}/{params['tam_cromossomo']} | "
                    f"Media: {media_fitness:5.2f} | {melhor_cromossomo}\n")
        
        # Mostrar progresso no console (a cada 10% das gerações ou quando achar solução)
        if geracao == 1 or geracao % max(1, params['num_geracoes'] // 20) == 0 or melhor_fitness == params['tam_cromossomo']:
            print(f"Gen {geracao:4d} | Melhor: {melhor_fitness:2d}/{params['tam_cromossomo']} | "
                  f"Media: {media_fitness:.1f} | {melhor_cromossomo}")
        
        # Se achou a solução
        if melhor_fitness == params['tam_cromossomo']:
            print(f"\nSolucao encontrada na geracao {geracao}!")
            print(f"Palavra: {melhor_cromossomo}")
            print(f"Fitness: {melhor_fitness}/{params['tam_cromossomo']} (100%)")
            
            # Escrever resultado final no arquivo
            with open(caminho_arquivo, 'a', encoding='utf-8') as f:
                f.write("\n" + "=" * 60 + "\n")
                f.write(f"SOLUÇÃO ENCONTRADA NA GERAÇÃO {geracao}\n")
                f.write("=" * 60 + "\n")
                f.write(f"Palavra: {melhor_cromossomo}\n")
                f.write(f"Fitness: {melhor_fitness}/{params['tam_cromossomo']} (100%)\n")
            break
        
        elite = pegar_elite(populacao, fitness_lista)
        nova_populacao = [elite]
        
        while len(nova_populacao) < params['tam_populacao']:
            pai = selecao_roleta(populacao, fitness_lista)
            mae = selecao_roleta(populacao, fitness_lista)
            
            filho1, filho2 = crossover(pai, mae, params['taxa_crossover'])
            
            filho1 = mutacao(filho1, params['taxa_mutacao'])
            filho2 = mutacao(filho2, params['taxa_mutacao'])
            
            nova_populacao.append(filho1)
            if len(nova_populacao) < params['tam_populacao']:
                nova_populacao.append(filho2)
        
        populacao = nova_populacao
    
    else:
        print(f"\nMax de geracoes atingido!")
        print(f"Melhor encontrado: {melhor_global}")
        print(f"Fitness: {melhor_fitness_global}/{params['tam_cromossomo']} "
              f"({melhor_fitness_global/params['tam_cromossomo']*100:.1f}%)")
        
        # Escrever resultado final no arquivo
        with open(caminho_arquivo, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 60 + "\n")
            f.write("MÁXIMO DE GERAÇÕES ATINGIDO\n")
            f.write("=" * 60 + "\n")
            f.write(f"Melhor encontrado: {melhor_global}\n")
            f.write(f"Fitness: {melhor_fitness_global}/{params['tam_cromossomo']} "
                    f"({melhor_fitness_global/params['tam_cromossomo']*100:.1f}%)\n")
    
    print("\n" + "=" * 50)
    print(f"Relatório salvo em: {caminho_arquivo}")
    print("=" * 50)


if __name__ == "__main__":
    random.seed()
    
    params = obter_parametros()
    executar_ag(params)
    
    print("Fim.\n")
