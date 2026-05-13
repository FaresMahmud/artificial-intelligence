"""
Algoritmo Genético - Implementação Didática
Baseado no material do Prof. Alexandre Zamberlan - Técnicas de IA
UFN - Ciência da Computação

Problema: MAXIMIZAR a quantidade de 1s num cromossomo binário
(problema simples para ver o AG funcionando passo a passo)

Conceitos do slide cobertos:
  ✔ Representação Binária
  ✔ Função de Aptidão (Fitness)
  ✔ Seleção por Roleta
  ✔ Crossover de 1 ponto
  ✔ Mutação binária
  ✔ Elitismo
"""

import random

# ─── PARÂMETROS (slide "Parâmetros") ───────────────────────────
TAM_CROMOSSOMO   = 16    # número de genes (bits)
TAM_POPULACAO    = 10    # indivíduos por geração
TAXA_CROSSOVER   = 0.8   # 80% de chance de cruzar
TAXA_MUTACAO     = 0.05  # 5% de chance de mutar cada gene
NUM_GERACOES     = 20    # critério de parada


# ─── 1. REPRESENTAÇÃO BINÁRIA ──────────────────────────────────
def criar_cromossomo():
    """Cria um cromossomo aleatório: lista de 0s e 1s."""
    return [random.randint(0, 1) for _ in range(TAM_CROMOSSOMO)]

def criar_populacao():
    """Cria a população inicial aleatoriamente."""
    return [criar_cromossomo() for _ in range(TAM_POPULACAO)]


# ─── 2. FUNÇÃO DE APTIDÃO / FITNESS ───────────────────────────
def calcular_fitness(cromossomo):
    """
    Aptidão = soma dos bits 1.
    Quanto mais 1s, melhor o indivíduo.
    """
    return sum(cromossomo)


# ─── 3. SELEÇÃO POR ROLETA ─────────────────────────────────────
def selecao_roleta(populacao, fitness_lista):
    """
    Cada indivíduo ocupa uma fatia da roleta proporcional ao seu fitness.
    Indivíduos mais aptos têm maior chance de ser selecionados.
    """
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


# ─── 4. CROSSOVER DE 1 PONTO ───────────────────────────────────
def crossover(pai, mae):
    """
    Divide os cromossomos em um ponto aleatório e troca as partes.
    Exemplo (corte na posição 4):
      Pai: [1,0,0,1 | 0,0,0,1,1,0,1,1,0,0,0,1]
      Mãe: [0,1,0,1 | 1,0,1,0,0,1,1,0,1,1,0,0]
      F1:  [1,0,0,1 | 1,0,1,0,0,1,1,0,1,1,0,0]
      F2:  [0,1,0,1 | 0,0,0,1,1,0,1,1,0,0,0,1]
    """
    if random.random() > TAXA_CROSSOVER:
        return pai[:], mae[:]  # sem cruzamento, retorna cópias

    corte = random.randint(1, TAM_CROMOSSOMO - 1)
    filho1 = pai[:corte] + mae[corte:]
    filho2 = mae[:corte] + pai[corte:]
    return filho1, filho2


# ─── 5. MUTAÇÃO BINÁRIA ────────────────────────────────────────
def mutacao(cromossomo):
    """
    Para cada gene, há TAXA_MUTACAO de chance de inverter o bit.
    0 → 1  ou  1 → 0
    Garante diversidade e evita convergência prematura.
    """
    return [
        1 - gene if random.random() < TAXA_MUTACAO else gene
        for gene in cromossomo
    ]


# ─── 6. ELITISMO ───────────────────────────────────────────────
def pegar_elite(populacao, fitness_lista):
    """
    Copia o melhor indivíduo direto para a próxima geração.
    Garante que o melhor fitness nunca piore entre gerações.
    """
    idx_melhor = fitness_lista.index(max(fitness_lista))
    return populacao[idx_melhor][:]


# ─── 7. LOOP PRINCIPAL DO AG ───────────────────────────────────
def executar_ag():
    print("=" * 55)
    print("   ALGORITMO GENÉTICO - Prof. Zamberlan / Técnicas IA")
    print("=" * 55)
    print(f"Cromossomo: {TAM_CROMOSSOMO} bits | População: {TAM_POPULACAO}")
    print(f"Crossover: {TAXA_CROSSOVER*100:.0f}% | Mutação: {TAXA_MUTACAO*100:.0f}%")
    print(f"Gerações: {NUM_GERACOES} | Objetivo: maximizar 1s\n")

    # PASSO 1: Inicializar população
    populacao = criar_populacao()

    for geracao in range(1, NUM_GERACOES + 1):

        # PASSO 2: Calcular aptidão
        fitness_lista = [calcular_fitness(c) for c in populacao]

        melhor_fitness = max(fitness_lista)
        media_fitness  = sum(fitness_lista) / len(fitness_lista)
        melhor_crom    = populacao[fitness_lista.index(melhor_fitness)]

        print(f"Geração {geracao:02d} | "
              f"Melhor: {melhor_fitness:2d}/{TAM_CROMOSSOMO} | "
              f"Média: {media_fitness:.1f} | "
              f"Cromossomo: {''.join(map(str, melhor_crom))}")

        # PASSO 3: Critério de parada — solução ótima encontrada?
        if melhor_fitness == TAM_CROMOSSOMO:
            print(f"\n✔ Solução ótima encontrada na geração {geracao}!")
            break

        # Elitismo: guarda o melhor
        elite = pegar_elite(populacao, fitness_lista)

        # PASSO 4 + 5 + 6: Seleção → Crossover → Mutação → Nova geração
        nova_populacao = [elite]  # elitismo: melhor entra direto

        while len(nova_populacao) < TAM_POPULACAO:
            # Seleção por roleta
            pai = selecao_roleta(populacao, fitness_lista)
            mae = selecao_roleta(populacao, fitness_lista)

            # Crossover
            filho1, filho2 = crossover(pai, mae)

            # Mutação
            filho1 = mutacao(filho1)
            filho2 = mutacao(filho2)

            nova_populacao.append(filho1)
            if len(nova_populacao) < TAM_POPULACAO:
                nova_populacao.append(filho2)

        populacao = nova_populacao

    # Resultado final
    fitness_lista = [calcular_fitness(c) for c in populacao]
    melhor_fitness = max(fitness_lista)
    melhor_crom    = populacao[fitness_lista.index(melhor_fitness)]

    print("\n" + "=" * 55)
    print("RESULTADO FINAL")
    print(f"  Melhor cromossomo : {''.join(map(str, melhor_crom))}")
    print(f"  Fitness           : {melhor_fitness}/{TAM_CROMOSSOMO}")
    print(f"  Aptidão relativa  : {melhor_fitness/TAM_CROMOSSOMO*100:.1f}%")
    print("=" * 55)


if __name__ == "__main__":
    random.seed(42)  # seed fixa para resultado reproduzível
    executar_ag()
