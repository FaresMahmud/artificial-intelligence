# Artificial Intelligence

Estudos e implementações sobre Inteligência Artificial, com foco em Algoritmos Genéticos e suas aplicações.

---

## 📚 Conteúdo

### ag_palavra.py ⭐ **NOVO**
**Algoritmo Genético Interativo - Procurador de Palavras**

Versão interativa e gamificada do AG que encontra palavras escolhidas pelo usuário. O programa interage com o usuário perguntando:
- 🎯 Qual palavra o AG deve encontrar?
- 👥 Tamanho da população
- 🔄 Taxa de crossover (0-1)
- 🧬 Taxa de mutação (0-1)
- ⏳ Máximo de gerações

**Como executar:**
```bash
python ag_palavra.py
```

**Exemplo de uso:**
```
🎯 Digite a palavra que o AG deve encontrar: HELLO WORLD
→ Tamanho da população: 30
→ Taxa de Crossover: 0.8
→ Taxa de Mutação: 0.15
→ Máximo de gerações: 500
```

**Características:**
- ✅ Interface interativa com validação de entrada
- ✅ Representação por string (cromossomos são palavras)
- ✅ Fitness baseado em caracteres corretos na posição correta
- ✅ Suporta espaços e letras maiúsculas
- ✅ Mostra progresso a cada geração
- ✅ Para quando encontra a solução exata
- ✅ Exibe estatísticas (melhor, média, aptidão relativa)

---

### aula.py
**Algoritmo Genético - Implementação Didática** (Prof. Alexandre Zamberlan - Técnicas de IA)

Implementação completa de um Algoritmo Genético para maximizar a quantidade de 1s em cromossomos binários.

#### Conceitos Cobertos:
- ✔ **Representação Binária** - Cromossomos como listas de bits
- ✔ **Função de Aptidão (Fitness)** - Avaliação dos indivíduos (soma dos 1s)
- ✔ **Seleção por Roleta** - Seleção proporcional ao fitness
- ✔ **Crossover de 1 Ponto** - Recombinação de cromossomos pais
- ✔ **Mutação Binária** - Inversão aleatória de bits para diversidade
- ✔ **Elitismo** - Preservação do melhor indivíduo entre gerações

#### Parâmetros Padrão:
- Cromossomo: 16 bits
- População: 10 indivíduos
- Taxa de Crossover: 80%
- Taxa de Mutação: 5%
- Gerações: 20
- Objetivo: Encontrar cromossomo com 16 bits = 1 (solução ótima)

#### Como Executar:
```bash
python aula.py
```

#### Saída Esperada:
Mostra evolução geracional com melhor fitness, média de aptidão e cromossomo da geração.

---

## 🎯 Problema Resolvido

**Maximizar a quantidade de 1s num cromossomo binário**

Desafios de Algoritmos Genéticos:
1. Muita restrições nas soluções
2. Desconhecimento do estado final desejado
3. Caminho para atingir o objetivo não é óbvio
4. Função de avaliação não trivial
5. Métricas para avaliar progresso intermediário
6. Operadores genéticos apropriados para o problema

Repositório para projetos de IA e problemas clássicos.

## Projetos

- `missionarios-canibais/` — solução do problema Missionários e Canibais com busca em largura (BFS).
