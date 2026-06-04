# escolhe um vertice do retangulo que possui menos vertices
def greedy_rects(rectangles : list[int], vertices : dict[tuple[str, tuple[int, int]], set[int]], rects_to_cover : set[int] = None):
    if not rects_to_cover:
        rects_to_cover = set(rectangles)
    guarded_vertices = set()

    # lista de conjuntos de vertices que veem cada retangulo i
    rect_to_points = [set() for _ in range(len(rectangles)+1)]
    for vertex, rectangle_set in vertices.items():
        for r in rectangle_set:
            if r in rects_to_cover:
                rect_to_points[r].add(vertex)

    while len(rects_to_cover) != 0:
        best_rect = min(rects_to_cover, key=lambda r: len(rect_to_points[r]))

        # retangulo que possui menos vertices que o veem
        candidate_vertices = rect_to_points[best_rect]
        if not candidate_vertices: break

        best_vertex = list(candidate_vertices)[0]
        
        # guardar vertice escolhido
        guarded_vertices.add(best_vertex)
        rects_to_cover -= vertices[best_vertex]
        for r in rectangles:
            rect_to_points[r].discard(best_vertex)
        for covered_rect in vertices[best_vertex]:
            rect_to_points[covered_rect] = set()

    return guarded_vertices


# escolhe o vertice que ve mais retangulos ainda nao cobertos
def greedy_verts(rectangles: list[int], vertices : dict[tuple[str, tuple[int, int]], set[int]], rects_to_cover : set[int] = None):
    if not rects_to_cover:
        rects_to_cover = set(rectangles)
    guarded_vertices = set()

    while len(rects_to_cover) != 0:
        # vertice que ve mais retangulos ainda nao cobertos
        best_vertex = max(vertices.keys(), key=lambda v: (len(vertices[v].intersection(rects_to_cover)), -int(v[0][1:])))
        
        # nem o melhor vertice cobre mais nada
        if len(vertices[best_vertex].intersection(rects_to_cover)) == 0:
            break

        guarded_vertices.add(best_vertex)
        rects_to_cover -= vertices[best_vertex]

    return guarded_vertices


# escolhe o vertice que ve mais retangulos do retangulo que possui menos vertices
def greedy_rects_verts(rectangles : list[int], vertices : dict[tuple[str, tuple[int, int]], set[int]],  rects_to_cover : set[int] = None):
    if not rects_to_cover:
        rects_to_cover = set(rectangles)
    guarded_vertices = set()

    # lista de conjuntos de vertices que veem cada retangulo i
    rect_to_points = [set() for _ in range(len(rectangles)+1)]
    for vertex, rectangle_set in vertices.items():
        for r in rectangle_set:
            if r in rects_to_cover:
                rect_to_points[r].add(vertex)

    while len(rects_to_cover) != 0:
        best_rect = min(rects_to_cover, key=lambda r: len(rect_to_points[r]))

        # retangulo que possui menos vertices que o veem
        candidate_vertices = rect_to_points[best_rect]
        if not candidate_vertices: break

        best_vertex = max(candidate_vertices, key=lambda v: len(vertices[v].intersection(rects_to_cover)))
        
        # guardar vertice escolhido
        guarded_vertices.add(best_vertex)
        rects_to_cover -= vertices[best_vertex]
        for r in rectangles:
            rect_to_points[r].discard(best_vertex)
        for covered_rect in vertices[best_vertex]:
            rect_to_points[covered_rect] = set()

    return guarded_vertices


# escolhe o melhor vertice do retangulo com menos vertices candidatos
# sendo o melhor vertice aquele que tem menos substitutos melhores nos outros retangulos que vê
def neighbors_greedy(rectangles : list[int], vertices : dict[tuple[str, tuple[int, int]], set[int]],  rects_to_cover : set[int] = None):
    def vertex_strength(v):
            return len(vertices[v].intersection(rects_to_cover))

    def evaluate_candidate_vertex(vi):
        # quantos retângulos ainda não cobertos o Vi consegue cobrir?
        rects_of_vi = vertices[vi].intersection(rects_to_cover)
        
        priority_score = 0
        for rk in rects_of_vi:
            # quem é o melhor vértice do mundo que consegue ver o retângulo rk?
            best_in_world_for_rk = max(rect_to_points[rk], key=vertex_strength)
            
            # Se o vi é o melhor ou empata com o melhor para o retângulo rk, 
            # a responsabilidade do vi aumenta (ganha pontos de prioridade)
            if vertex_strength(vi) >= vertex_strength(best_in_world_for_rk):
                priority_score += 1

        return priority_score

    ###
    if not rects_to_cover:
        rects_to_cover = set(rectangles)

    guarded_vertices = set()
    rect_to_points = [set() for _ in range(len(rectangles) + 1)]
    for vertex, rectangle_set in vertices.items():
        for r in rectangle_set:
            if r in rects_to_cover:
                rect_to_points[r].add(vertex)

    while rects_to_cover:
        # Seleciona o retângulo ainda não coberto com menos vértices que o veem
        best_rect = min(rects_to_cover, key=lambda r: len(rect_to_points[r]))
        candidate_vertices = rect_to_points[best_rect]
        
        if not candidate_vertices:
            break  
        
        # Escolhemos o vértice candidato que tem a MAIOR pontuação de prioridade
        # (Aquele que os outros retângulos mais dependem dele e não têm substitutos melhores)
        best_vertex = max(candidate_vertices, key=evaluate_candidate_vertex)

        # Aplica a escolha e atualiza os conjuntos
        guarded_vertices.add(best_vertex)
        rectangles_covered_now = vertices[best_vertex].intersection(rects_to_cover)
        rects_to_cover -= rectangles_covered_now
        
        # Limpeza dos vértices e retângulos processados
        for r in rectangles:
            rect_to_points[r].discard(best_vertex)
            
        for covered_rect in rectangles_covered_now:
            rect_to_points[covered_rect] = set()

    return guarded_vertices