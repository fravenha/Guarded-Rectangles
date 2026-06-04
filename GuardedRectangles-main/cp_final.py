from ortools.sat.python import cp_model

def cp_solver(retangulos: list[int], vertices: dict[tuple[str, tuple[int, int]], set[int]], rects_to_cover: list[int] = None):
    if not rects_to_cover:
        rects_to_cover = retangulos
        
    model = cp_model.CpModel()
    
    # 1. Mapeamento de Vértices para IDs Inteiros (Necessário para o domínio do CP)
    lista_vertices = list(vertices.keys())
    map_v_to_id = {vertice: idx for idx, vertice in enumerate(lista_vertices)}
    
    # 2. Variáveis de Decisão (Mantendo a estrutura de chaves do seu MIP)
    # Y[vertice] = 1 se ativo, 0 caso contrário (Variável booleana de ativação)
    Y = {}
    for vertice in lista_vertices:
        nome, _ = vertice
        Y[vertice] = model.NewBoolVar(f'Y_{nome}')
        
    # X[r] = ID do vértice atribuído para cobrir o retângulo r (Variável de Atribuição Inteira)
    X = {}
    
    # 3. Construção da relação de cobertura (adaptada do seu padrão MIP)
    rect_to_points = {r: [] for r in rects_to_cover}
    for vertice, conjunto_retangulos in vertices.items():
        for r in conjunto_retangulos:
            if r in rects_to_cover:
                rect_to_points[r].append(vertice)
                
    # 4. Restrições e Formulação de CP (Diferente da Linear do MIP)
    for r in rects_to_cover:
        candidatos_keys = rect_to_points[r]
        candidatos_ids = [map_v_to_id[v] for v in candidatos_keys]
        
        if not candidatos_ids:
            print(f"Erro: O retângulo {r} não é visível por nenhum vértice!")
            return set()
            
        # O domínio de X[r] é estritamente o ID dos vértices que conseguem vê-lo
        dominio_visivel = cp_model.Domain.FromValues(candidatos_ids)
        X[r] = model.NewIntVarFromDomain(dominio_visivel, f'X_rect_{r}')
        

        # Se o vértice c_id NÃO está ativo, então X[r] NÃO pode receber esse ID
        for v_key, c_id in zip(candidatos_keys, candidatos_ids):
            model.Add(X[r] != c_id).OnlyEnforceIf(Y[v_key].Not())
            
    # 5. Função Objetivo (Minimizar a soma dos vértices ativos)
    model.Minimize(sum(Y[v] for v in lista_vertices))
    
    # 6. Resolução
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    vertices_com_guardas = set()
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for vertice in lista_vertices:
            if solver.Value(Y[vertice]) == 1:
                vertices_com_guardas.add(vertice)
    else:
        print("The problem does not have a feasible solution.")
        
    return vertices_com_guardas

