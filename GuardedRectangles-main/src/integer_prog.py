from ortools.linear_solver import pywraplp

def mip(retangulos : list[int], vertices : dict[tuple[str, tuple[int, int]], set[int]], rects_to_cover : list[int] = None):
    if not rects_to_cover:
        rects_to_cover = retangulos
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver: return
    
    variables = {}
    for (nome, coords)  in vertices.keys():
        variables[(nome, coords)] = solver.IntVar(0.0, 1.0, nome)

    rect_to_points = [set() for _ in range(len(retangulos)+1)]
    for vertice, conjunto_retangulos in vertices.items():
        for r in conjunto_retangulos:
            if r in rects_to_cover:
                rect_to_points[r].add(vertice)

    for vertices_do_rect_i in rect_to_points:
        if not vertices_do_rect_i: continue
        vars_vertices = [variables[v] for v in list(vertices_do_rect_i)]
        solver.Add(sum(vars_vertices) >= 1)
    
    solver.Minimize(sum(variables.values()))
    status = solver.Solve()

    vertices_com_guardas = set()
    if status == pywraplp.Solver.OPTIMAL:
        for (vert, var) in variables.items():
            if var.solution_value() > 0.5:
                vertices_com_guardas.add(vert)
    else:
        print("The problem does not have an optimal solution.")
        
    return vertices_com_guardas



