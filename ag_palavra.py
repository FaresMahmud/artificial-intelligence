"""
Algoritmo Genético Interativo - Procurar Palavra
Versão interativa onde o usuário escolhe a palavra alvo e os parâmetros
do AG (taxa de mutação, crossover, gerações)

Baseado no material do Prof. Alexandre Zamberlan - Técnicas de IA
UFN - Ciência da Computação
"""

import random
import string

# ─── FUNÇÕES AUXILIARES ────────────────────────────────────────
def obter_parametros():
    """Coleta os parâmetros do usuário via entrada."""
    print("\n" + "=" * 60)
    print("   ALGORITMO GENÉTICO INTERATIVO - PROCURADOR DE PALAVRAS")
    print("=" * 60)
    
    # Palavra alvo
    while True:
        palavra_alvo = input("\n🎯 Digite a palavra que o AG deve encontrar: ").strip()
        if len(palavra_alvo) > 0:
            palavra_alvo = palavra_alvo.upper()
            break
        print("❌ Palavra não pode estar vazia!")
    
    # Parâmetros
    print("\n📊 Configure os parâmetros do Algoritmo Genético:\n")
    
    while True:
        try:
            tam_populacao = int(input("   → Tamanho da população (ex: 20): "))
            if tam_populacao < 2:
                print("      ❌ Mínimo 2 indivíduos!")
                continue
            break
        except ValueError:
            print("      ❌ Digite um número inteiro!")
    
    while True:
        try:
            taxa_crossover = float(input("   → Taxa de Crossover (0-1, ex: 0.8): "))
            if not (0 <= taxa_crossover <= 1):
                print("      ❌ Digite um valor entre 0 e 1!")
                continue
            break
        except ValueError:
            print("      ❌ Digite um número!")
    
    while True:
        try:
            taxa_mutacao = float(input("   → Taxa de Mutação (0-1, ex: 0.1): "))
            if not (0 <= taxa_mutacao <= 1):
                print("      ❌ Digite um valor entre 0 e 1!")
                continue
            break
        except ValueError:
            print("      ❌ Digite um número!")
    
    while True:
        try:
            num_geracoes = int(input("   → Máximo de gerações (ex: 1000): "))
            if num_geracoes < 1:
                print("      ❌ Mínimo 1 geração!")
                continue
            break
        except ValueError:
            print("      ❌ Digite um número inteiro!")
    
    return {
        'palavra_alvo': palavra_alvo,
        'tam_cromossomo': len(palavra_alvo),
        'tam_populacao': tam_populacao,
        'taxa_crossover': taxa_crossover,
        'taxa_mutacao': taxa_mutacao,
        'num_geracoes': num_geracoes
    }


# ─── 1. REPRESENTAÇÃO ──────────────────────────────────────────
def criar_cromossomo(tamanho):
    """Cria um cromossomo aleatório: string com caracteres aleatórios."""
    alfabeto = string.ascii_uppercase + ' '
    return ''.join(random.choice(alfabeto) for _ in range(tamanho))

def criar_populacao(tamanho_pop, tamanho_crom):
    """Cria a população inicial aleatoriamente."""
    return [criar_cromossomo(tamanho_crom) for _ in range(tamanho_pop)]


# ─── 2. FUNÇÃO DE APTIDÃO / FITNESS ───────────────────────────
def calcular_fitness(cromossomo, alvo):
    """
    Fitness = número de caracteres corretos na posição correta.
    Quanto mais caracteres corretos, melhor.
    """
    return sum(1 for i, char in enumerate(cromossomo) if char == alvo[i])


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
def crossover(pai, mae, taxa_crossover):
    """
    Divide os cromossomos (strings) em um ponto aleatório e troca as partes.
    Exemplo (corte na posição 4):
      Pai: "HELO | MUNDO"
      Mãe: "PALA | VRAS"
      F1:  "HELO | VRAS"
      F2:  "PALA | MUNDO"
    """
    if random.random() > taxa_crossover:
        return pai, mae  # sem cruzamento

    corte = random.randint(1, len(pai) - 1)
    filho1 = pai[:corte] + mae[corte:]
    filho2 = mae[:corte] + pai[corte:]
    return filho1, filho2


# ─── 5. MUTAÇÃO ────────────────────────────────────────────────
def mutacao(cromossomo, taxa_mutacao):
    """
    Para cada gene (caractere), há taxa_mutacao de chance de trocar por outro.
    Garante diversidade e evita convergência prematura.
    """
    alfabeto = string.ascii_uppercase + ' '
    resultado = []
    
    for char in cromossomo:
        if random.random() < taxa_mutacao:
            resultado.append(random.choice(alfabeto))
        else:
            resultado.append(char)
    
    return ''.join(resultado)


# ─── 6. ELITISMO ───────────────────────────────────────────────
def pegar_elite(populacao, fitness_lista):
    """
    Copia o melhor indivíduo direto para a próxima geração.
    Garante que o melhor nunca piore.
    """
    idx_melhor = fitness_lista.index(max(fitness_lista))
    return populacao[idx_melhor]


# ─── 7. LOOP PRINCIPAL DO AG ───────────────────────────────────
def executar_ag(params):
    """Executa o algoritmo genético com os parâmetros fornecidos."""
    
    print("\n" + "=" * 60)
    print("   🧬 INICIANDO ALGORITMO GENÉTICO")
    print("=" * 60)
    print(f"🎯 Palavra alvo     : {params['palavra_alvo']}")
    print(f"👥 População        : {params['tam_populacao']} indivíduos")
    print(f"🔄 Crossover        : {params['taxa_crossover']*100:.0f}%")
    print(f"🧬 Mutação          : {params['taxa_mutacao']*100:.1f}%")
    print(f"⏳ Máx. gerações    : {params['num_geracoes']}")
    print("=" * 60 + "\n")
    
    # PASSO 1: Inicializar população
    populacao = criar_populacao(params['tam_populacao'], params['tam_cromossomo'])
    
    melhor_global = None
    melhor_fitness_global = 0
    
    for geracao in range(1, params['num_geracoes'] + 1):
        
        # PASSO 2: Calcular aptidão
        fitness_lista = [calcular_fitness(c, params['palavra_alvo']) for c in populacao]
        
        melhor_fitness = max(fitness_lista)
        media_fitness = sum(fitness_lista) / len(fitness_lista)
        idx_melhor = fitness_lista.index(melhor_fitness)
        melhor_cromossomo = populacao[idx_melhor]
        
        # Atualizar melhor global
        if melhor_fitness > melhor_fitness_global:
            melhor_fitness_global = melhor_fitness
            melhor_global = melhor_cromossomo
        
        # Exibir progresso a cada geração (ou a cada 10 se muitas gerações)
        if geracao == 1 or geracao % max(1, params['num_geracoes'] // 20) == 0 or melhor_fitness == params['tam_cromossomo']:
            print(f"Gen {geracao:4d} │ Melhor: {melhor_fitness:2d}/{params['tam_cromossomo']} │ "
                  f"Média: {media_fitness:.1f} │ {melhor_cromossomo}")
        
        # PASSO 3: Critério de parada — solução ótima encontrada?
        if melhor_fitness == params['tam_cromossomo']:
            print(f"\n🎉 SOLUÇÃO ENCONTRADA na geração {geracao}!")
            print(f"   Palavra: {melhor_cromossomo}")
            print(f"   Fitness: {melhor_fitness}/{params['tam_cromossomo']} (100%)")
            break
        
        # Elitismo: guarda o melhor
        elite = pegar_elite(populacao, fitness_lista)
        
        # PASSO 4 + 5 + 6: Seleção → Crossover → Mutação → Nova geração
        nova_populacao = [elite]
        
        while len(nova_populacao) < params['tam_populacao']:
            # Seleção por roleta
            pai = selecao_roleta(populacao, fitness_lista)
            mae = selecao_roleta(populacao, fitness_lista)
            
            # Crossover
            filho1, filho2 = crossover(pai, mae, params['taxa_crossover'])
            
            # Mutação
            filho1 = mutacao(filho1, params['taxa_mutacao'])
            filho2 = mutacao(filho2, params['taxa_mutacao'])
            
            nova_populacao.append(filho1)
            if len(nova_populacao) < params['tam_populacao']:
                nova_populacao.append(filho2)
        
        populacao = nova_populacao
    
    else:
        # Se saiu do loop sem encontrar solução
        print(f"\n⏱️  Máximo de gerações atingido!")
        print(f"   Melhor encontrado: {melhor_global}")
        print(f"   Fitness: {melhor_fitness_global}/{params['tam_cromossomo']} "
              f"({melhor_fitness_global/params['tam_cromossomo']*100:.1f}%)")
    
    print("\n" + "=" * 60)


# ─── FUNÇÃO PRINCIPAL ───────────────────────────────────────────
if __name__ == "__main__":
    random.seed()  # seed diferente a cada execução
    
    params = obter_parametros()
    executar_ag(params)
    
    print("\n✅ Programa finalizado!\n")
