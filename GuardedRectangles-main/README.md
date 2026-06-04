# Guarded Rectangles

Trabalho para a disciplina de Métodos de Apoio a Decisão: Estudo de Caso do Problema de Vigilância de Partições Retangulares.

## Sobre

Este projeto analisa o problema de determinar a menor quantidade de guardas (posicionados nos vértices) necessários para vigiar uma partição de retângulos adjacentes. Um guarda tem alcance sobre todos os retângulos incidentes ao seu respectivo vértice. 

O trabalho resolve duas variantes do problema: a cobertura total da partição e a cobertura restrita a um subconjunto de retângulos. Para isso, foram implementadas diferentes abordagens, incluindo algoritmos *greedy*, programação inteira (IP), programação por restrições (CP), programação dinâmica (DP) e extensões de coloração e raio de distância variável.

## Pré-requisitos

O projeto requer Python, a biblioteca OR-Tools e pacotes do LaTeX para compilar a visualização dos resultados.

```bash
# Dependência do solver em Python
python -m pip install ortools

# Dependências do sistema (Debian/Ubuntu) para renderização do PDF
sudo apt install texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
```

## Execução

Para rodar o programa e testar novas instâncias, execute o arquivo principal:

```bash
python src/main.py
```

### Entradas Interativas

Ao rodar o script, o terminal solicitará os parâmetros de criação dos testes:

* **Nº de retângulos (separados por espaço):** Define as dimensões dos problemas que serão gerados. Exemplo: `5 10 15 20`
* **Nº de instâncias:** Define a quantidade de malhas diferentes geradas para cada conjunto de retângulos. Exemplo: `5`
* **Calcular subconjuntos?:** Insira `0` (Negativo) ou `1` (Positivo).

### Saídas e Resultados

O programa exibirá no console um comparativo das soluções encontradas por cada método. Exemplo de saída:

```text
20 RETÂNGULOS --------
Greedy Verts Solution =  9
Greedy Rects Solution =  9
Greedy Rects and Verts Solution =  9
Greedy Neighbors Solution =  9
IP Solution =  8
Dynamic Programming Solution =  8
* Qtd de cores por LP =  3
```

Ao final da execução, três arquivos são exportados para o diretório local:

* `output.pdf`: Representações visuais das soluções geométricas encontradas por cada algoritmo (gerado para instâncias de até 60 retângulos).
* `resultados_algoritmos.csv`: Planilha contendo a quantidade de guardas calculada por cada método em cada instância.
* `tempos_algoritmos.csv`: Planilha contendo o tempo de execução computacional de cada método avaliado.