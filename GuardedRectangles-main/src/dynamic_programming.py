def dynamic_programming_solver(retangulos, vertices, rects_a_cobrir=None):

    #se não for especificado subconjunto, cobre todos
    if rects_a_cobrir is None:
        rects_a_cobrir = retangulos

    rects_a_cobrir = list(rects_a_cobrir)

    m = len(rects_a_cobrir)

    #limitação prática da DP por bitmask
    if m > 23:
        return set()

    #mapear apenas os retângulos que devem ser cobertos
    rect_index = {
        rect: i for i, rect in enumerate(rects_a_cobrir)
    }

    #converter cobertura de cada vértice para bitmask
    vertex_masks = {}

    for vertex, rects_seen in vertices.items():
        mask = 0

        for r in rects_seen:
            if r in rect_index:
                mask |= (1 << rect_index[r])

        vertex_masks[vertex] = mask

    FULL_MASK = (1 << m) - 1

    INF = float('inf')

    # dp[mask] = menor nº de guardas para obter esta cobertura
    dp = [INF] * (1 << m)

    #para reconstruir a solução
    parent = [None] * (1 << m)

    dp[0] = 0

    for mask in range(1 << m):

        if dp[mask] == INF:
            continue

        for vertex, cover_mask in vertex_masks.items():

            new_mask = mask | cover_mask

            if dp[mask] + 1 < dp[new_mask]:
                dp[new_mask] = dp[mask] + 1
                parent[new_mask] = (mask, vertex)

    #não existe solução
    if dp[FULL_MASK] == INF:
        return set()

    #reconstruir solução ótima
    solution = set()

    current = FULL_MASK

    while current != 0:
        previous, vertex = parent[current]
        solution.add(vertex)
        current = previous

    return solution
