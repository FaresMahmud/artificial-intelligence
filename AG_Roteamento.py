"""
Algoritmo Genético - Problema de Roteamento
Cidades: 1 a 9 | Rota perfeita: [1,2,3,4,5,6,7,8,9]

REGRAS DE APTIDÃO (penalidade — quanto MENOR, melhor):
  - Par adjacente (i, i+1) onde cidade[i] > cidade[i+1]: +10
  - Cada par de ocorrência da mesma cidade: +20
  Aptidão 0 = rota perfeita
"""

import random

#Configurações do AG 
CIDADES        = list(range(1, 10))   # [1..9]
ROTA_PERFEITA  = CIDADES[:]
TAM_POP        = 100
MAX_GERACOES   = 500
TX_MUTACAO     = 0.15
TX_CROSSOVER   = 0.85
TORNEIO_K      = 3


#Função de aptidão
def aptidao(rota: list[int]) -> int:
    """Calcula penalidade total. Aptidão 0 = perfeito."""
    penalidade = 0

    # Regra 1: par adjacente fora de ordem → +10
    for i in range(len(rota) - 1):
        if rota[i] > rota[i + 1]:
            penalidade += 10

    # Regra 2: cidade duplicada → +20 por par extra
    from collections import Counter
    contagem = Counter(rota)
    for cidade, qtd in contagem.items():
        if qtd > 1:
            penalidade += (qtd - 1) * 20   # 2 ocorr→+20, 3 ocorr→+40...

    return penalidade


def aptidao_detalhado(rota: list[int]) -> str:
    """Mostra o cálculo passo a passo."""
    from collections import Counter
    linhas   = [f"Rota: {rota}"]
    parcelas = []

    for i in range(len(rota) - 1):
        if rota[i] > rota[i + 1]:
            parcelas.append(f"  [{rota[i]}>{rota[i+1]}] → +10")

    contagem = Counter(rota)
    for cidade, qtd in contagem.items():
        if qtd > 1:
            pares = qtd - 1
            parcelas.append(f"  cidade {cidade} aparece {qtd}x → +{pares*20}")

    if parcelas:
        linhas.extend(parcelas)
        linhas.append(f"  TOTAL = {aptidao(rota)}")
    else:
        linhas.append("  PERFEITA! Aptidão = 0 ✓")

    return "\n".join(linhas)


# Inicialização
def individuo_aleatorio() -> list[int]:
    ind = CIDADES[:]
    random.shuffle(ind) # aqui embaralha 
    return ind

def populacao_inicial() -> list[list[int]]:
    return [individuo_aleatorio() for _ in range(TAM_POP)]


# Seleção por torneio 
def torneio(pop: list[list[int]]) -> list[int]:
    candidatos = random.sample(pop, TORNEIO_K)
    return min(candidatos, key=aptidao)


# Crossover (OX1) 
def crossover_ox(pai: list[int], mae: list[int]) -> tuple[list[int], list[int]]:
    n  = len(pai)
    a, b = sorted(random.sample(range(n), 2))

    def filho(p1, p2):
        segmento = p1[a:b+1]
        restante = [x for x in p2 if x not in segmento]
        return restante[:a] + segmento + restante[a:]

    return filho(pai, mae), filho(mae, pai)


# Mutação (swap) 
def mutacao(ind: list[int]) -> list[int]:
    ind = ind[:]
    i, j = random.sample(range(len(ind)), 2)
    ind[i], ind[j] = ind[j], ind[i]
    return ind


# Loop principal do AG 
def executar_ag(verbose: bool = True) -> tuple[list[int], int, list[int]]:
    pop      = populacao_inicial()
    historia = []                    # aptidão do melhor por geração

    for geracao in range(MAX_GERACOES):
        pop.sort(key=aptidao)
        melhor = pop[0]
        historia.append(aptidao(melhor))

        if aptidao(melhor) == 0:
            if verbose:
                print(f"\n✅ Solução perfeita encontrada na geração {geracao}!")
            break

        nova_pop = [melhor]          # elitismo: mantém o melhor

        while len(nova_pop) < TAM_POP:
            pai = torneio(pop)
            mae = torneio(pop)

            if random.random() < TX_CROSSOVER:
                f1, f2 = crossover_ox(pai, mae)
            else:
                f1, f2 = pai[:], mae[:]

            if random.random() < TX_MUTACAO:
                f1 = mutacao(f1)
            if random.random() < TX_MUTACAO:
                f2 = mutacao(f2)

            nova_pop.extend([f1, f2])

        pop = nova_pop[:TAM_POP]

        if verbose and geracao % 50 == 0:
            print(f"Geração {geracao:4d} | Melhor aptidão: {aptidao(melhor)} | Rota: {melhor}")

    melhor_final = min(pop, key=aptidao)
    return melhor_final, aptidao(melhor_final), historia


#  Main
if __name__ == "__main__":
    print("=" * 60)
    print("  ALGORITMO GENÉTICO — PROBLEMA DE ROTEAMENTO")
    print("  Cidades: 1–9 | Rota perfeita: 1 2 3 4 5 6 7 8 9")
    print("=" * 60)

   
    print("\n── VERIFICAÇÃO DOS EXEMPLOS ──────────────────────────────")
    exemplos = [
        [2, 8, 4, 0, 1, 5, 3, 6, 7],   # professor diz 30
        [6, 5, 3, 2, 0, 1, 3, 7, 5],   # filho1
    ]
    for ex in exemplos:
        print(aptidao_detalhado(ex))
        print()

    # ── Execução do AG ──
    print("── EXECUTANDO AG ─────────────────────────────────────────")
    random.seed(42)
    melhor, nota, historia = executar_ag(verbose=True)

    print("\n── RESULTADO FINAL ───────────────────────────────────────")
    print(aptidao_detalhado(melhor))
    print(f"\nTotal de gerações executadas: {len(historia)}")
    print(f"Aptidão inicial (geração 0):  {historia[0]}")
    print(f"Aptidão final:                {nota}")