from ortools.linear_solver import pywraplp

class Node:

    def __init__(self, i, name):
        self.index = i
        self.adj = []
        self.color = None
        self.name = name

    def addEdge(self, node : 'Node'):
        if node not in self.adj:
            self.adj.append(node)

    @property
    def adj_colors(self):
        return [n.color for n in self.adj if n.color is not None]

    @property
    def saturation(self):
        return len(set(self.adj_colors))

    @property
    def degree(self):
        return len(self.adj)



class ColoredGuards:

    def __init__(self, guarded_vertices, named_vertices, rects_to_points):
        self.nodes = []
        self.colors = []

        vertex_to_index = {}
        for i, v in enumerate(guarded_vertices):
            self.nodes.append(Node(i, v))
            vertex_to_index[v] = i

        for v in guarded_vertices:
            i = vertex_to_index[v]
            for seen_r in named_vertices[v]: # max 3 rects
                for neighbor in rects_to_points[seen_r]: # max 3 vertices
                    if neighbor in guarded_vertices and neighbor != v:
                        neighbor_index = vertex_to_index[neighbor]
                        self.nodes[i].addEdge(self.nodes[neighbor_index])
                        self.nodes[neighbor_index].addEdge(self.nodes[i])


    def d_satur(self):
        q = [node for node in self.nodes]
        while len(q) > 0:
            q.sort(key=lambda n: (n.saturation, n.degree), reverse=True)
            curr = q.pop(0)
            self.assign_color(curr)
        return len(self.colors)


    def assign_color(self, node : Node):
        next_color = None
        for c in self.colors:
            if c not in node.adj_colors:
                next_color = c
                break
        
        if next_color is None:
            next_color = len(self.colors) + 1
            self.colors.append(next_color)

        node.color = next_color


    def lp_colors(self):
        solver = pywraplp.Solver.CreateSolver("SAT")
        if not solver: return

        # variaveis:
        x = {} # x_i_c
        for node in self.nodes:
            for c in self.colors:
                i = node.index
                x[(i, c)] = solver.IntVar(0, 1, f"x_{i}_{c}") 
        
        y = {}  # y_j
        for c in self.colors:
            y[c] = solver.IntVar(0, 1, f"y_{c}")

        # restricoes:
        for node in self.nodes: 
            i = node.index
            # 1) todo nó deve receber uma cor
            solver.Add(solver.Sum([x[(i, c)] for c in self.colors]) == 1)

            for c in self.colors:
                # 2) se um nó 'i' usa a cor 'c',a cor 'c' deve ser 1
                solver.Add(x[(i, c)] <= y[c])

            for adj in node.adj:
                j = adj.index
                if i<j: 
                    for c in self.colors:
                        # 3) só um dos nós de uma aresta pode usar uma cor c
                        solver.Add(x[(i, c)] + x[(j, c)] <= 1)

        for c in range(len(self.colors) - 1):
            curr_c = self.colors[c]
            next_c = self.colors[c + 1]
            # 4) quebra de simetria
            solver.Add(y[curr_c] >= y[next_c])

        solver.Minimize(solver.Sum(list(y.values())))
        status = solver.Solve()
        solution = set()

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            print("* Qtd de cores por LP = ", int(solver.Objective().Value()))
            for ((i, c), var) in x.items():
                if var.solution_value() > 0.5:
                    solution.add((self.nodes[i].name, c))
        
        return solution


def color_guards(guarded_vertices, named_vertices, rectangles):
    rect_to_points = [set() for _ in range(len(rectangles)+1)]
    for vertice, set_rectangles in named_vertices.items():
        for r in set_rectangles:
            rect_to_points[r].add(vertice)

    graph = ColoredGuards(guarded_vertices, named_vertices, rect_to_points)

    dsatur = graph.d_satur()
    # print(f"Qtd de cores com DSatur = {dsatur}")
    return graph.lp_colors()



# outra versão
def coloring(vertices: dict[tuple[str, tuple[int, int]], set[int]], retangulos: list[int], qtd_guardas: int, max_colors : int):
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver: return

    y = {} # y[v]: 1 se o vértice v for selecionado
    for (nome, coords) in vertices.keys():
        y[(nome, coords)] = solver.BoolVar(f"y_{nome}")

    w = {} # w[c]: 1 se a cor c for usada
    for c in range(1, max_colors+1):
        w[c] = solver.BoolVar(f"color_used_{c}")

    x = {} # x[v, c]: 1 se o vértice v for selecionado E receber a cor c
    for (nome, coords) in vertices.keys():
        for c in range(1, max_colors+1):
            x[(nome, coords, c)] = solver.BoolVar(f"x_{nome}_{c}")

    rect_to_points = [set() for _ in range(len(retangulos)+1)]
    for vertice, conjunto_retangulos in vertices.items():
        for r in conjunto_retangulos:
            rect_to_points[r].add(vertice)

    # --- RESTRIÇÕES ---

    # 1) A quantidade exata de vértices escolhidos deve ser igual a `qtd_guardas`
    solver.Add(sum(y.values()) == qtd_guardas)

    # 2) Todos os retângulos precisam ser cobertos por pelo menos um vértice escolhido
    for vertices_do_rect_i in rect_to_points:
        if not vertices_do_rect_i: continue
        vars_vertices = [y[v] for v in list(vertices_do_rect_i)]
        solver.Add(sum(vars_vertices) >= 1)

    for v in vertices.keys():
        # 3) Se o vértice for escolhido (y[v]=1), ele deve ter exatamente 1 cor. Se não (y[v]=0), tem 0.
        solver.Add(sum(x[(v[0], v[1], c)] for c in range(1, max_colors+1)) == y[v])
        
        # 4) Um vértice só pode usar uma cor `c` se a cor `c` estiver marcada como usada (w[c]=1)
        for c in range(1, max_colors+1):
            solver.Add(x[(v[0], v[1], c)] <= w[c])

    # 5) Para cada retângulo e cada cor, no máximo 1 vértice pode ter essa cor.
    for r_verts in rect_to_points:
        if not r_verts: continue
        for c in range(1, max_colors+1):
            solver.Add(sum(x[(v[0], v[1], c)] for v in r_verts) <= 1)

    # 6) Quebra de Simetria
    for c in range(1, max_colors):
        solver.Add(w[c] >= w[c+1])

    solver.Minimize(sum(w.values()))
    status = solver.Solve()

    solution = set()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        qtd_cores = int(solver.Objective().Value())
        print(f"* Qtd de cores por LP2 = {qtd_cores}")
        
        for (nome, coords) in vertices.keys():
            if y[(nome, coords)].solution_value() > 0.5:
                for c in range(1, max_colors+1):
                    if x[(nome, coords, c)].solution_value() > 0.5:
                        solution.add(((nome, coords), c))
                        break
    
    return solution