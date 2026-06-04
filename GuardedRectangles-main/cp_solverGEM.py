from ortools.sat.python import cp_model

def otimizar_cobertura_vigias(retangulos, vertices, retangulos_a_cobrir, rects_to_points):

    model = cp_model.CpModel()

    # Mapeamento de Vértices para IDs Inteiros ---
    lista_vertices = list(vertices.keys())
    map_v_to_id = {vertice: idx for idx, vertice in enumerate(lista_vertices)}

    # Variáveis de Decisão
    X = {}
    Y = {}

    # Y[id_vertice] = 1 se o vértice está ativo, 0 caso contrário
    for idx, vertice in enumerate(lista_vertices):
        nome_limpo = vertice[0] # Usar só o nome para o rótulo interno da variável
        Y[idx] = model.NewBoolVar(f'Y_ativo_{nome_limpo}')

    # X[r] = ID do vértice atribuído para cobrir o retângulo r
    for r in retangulos_a_cobrir:
        # Vértices candidatos que veem o retângulo 'r' (converter chaves para IDs)
        candidatos_keys = rects_to_points.get(r, [])
        candidatos_ids = [map_v_to_id[v] for v in candidatos_keys]
        
        if not candidatos_ids:
            print(f"Erro: O retângulo {r} precisa ser coberto mas não é visível por nenhum vértice!")
            return
            
        dominio_visivel = cp_model.Domain.FromValues(candidatos_ids)
        X[r] = model.NewIntVarFromDomain(dominio_visivel, f'X_rect_{r}')

        # Restrições de Canalização (Channeling)
        # Se o vértice (c_id) não estiver ativo, ele não pode ser o valor de X[r]
        for c_id in candidatos_ids:
            model.Add(X[r] != c_id).OnlyEnforceIf(Y[c_id].Not())

    # Função Objetivo
    # Minimizar o número total de vértices ativados
    model.Minimize(sum(Y[idx] for idx in range(len(lista_vertices))))

    # Resolução
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Processamento dos Resultados
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("\n--- SOLUÇÃO ENCONTRADA ---")
        print(f"Número mínimo de postos a ativar: {int(solver.ObjectiveValue())}")
        
        print("\nAtribuições:")
        postos_ativados = set()
        
        for r in retangulos_a_cobrir:
            # Descobrir qual o ID inteiro escolhido e reverter para a chave original
            id_escolhido = solver.Value(X[r])
            vertice_escolhido = lista_vertices[id_escolhido]
            postos_ativados.add(vertice_escolhido)
            
            nome_v, coords_v = vertice_escolhido
            print(f" -> O Retângulo {r} será vigiado pelo vértice '{nome_v}' em {coords_v}")
            
        print("\nResumo dos Vértices Ativos:")
        for v in postos_ativados:
            print(f" * Ativado: {v[0]} nas coordenadas {v[1]}")
    else:
        print("\nNão foi encontrada nenhuma solução. É impossível cobrir todos os retângulos exigidos.")


# ==========================================
# Exemplo de Utilização com os teus Dados
# ==========================================
if __name__ == "__main__":
    
    # Os teus inputs
    retangulos = [1, 2, 3, 4]
    
    vertices = {
        ('v1', (1, 3)): {2}, 
        ('v2', (3, 3)): {1, 2}, 
        ('v5', (2, 2)): {2, 3, 4}
    }
    
    # Exemplo: Só queremos cobrir os retângulos 2, 3 e 4
    retangulos_a_cobrir = [2, 3, 4]
    
    # Criar a relação Rects_to_points invertendo o dicionário de vértices
    # (Para não teres de escrever isto à mão, o código gera-o automaticamente a partir dos vértices)
    rects_to_points = {r: [] for r in retangulos}
    for vertice, rects_visiveis in vertices.items():
        for r in rects_visiveis:
            rects_to_points[r].append(vertice)
            
    # Executar o modelo
    otimizar_cobertura_vigias(retangulos, vertices, retangulos_a_cobrir, rects_to_points)