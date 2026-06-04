import colorsys

def generate_latex(info):
    tex = []
    tex.append("\\documentclass[a4paper]{article}")
    tex.append("\\usepackage{xcolor}")
    tex.append("\\setlength{\\unitlength}{0.5cm}")
    tex.append("\\usepackage[left=1.5cm, right=1.5cm, top=2cm, bottom=2cm]{geometry}\n")
    tex.append("\n\\begin{document}\n")

    for (r, v, c_v, r_c, s) in info:
        qtd_colors = len(c_v)
        if s == "Greedy Rects":
            tex.append(f"\\section*{{{len(r)} retângulos -- Cobertura Completa:}}")
            tex.append("\\vspace{1.5cm}")
        elif s == "Greedy Rects (Subconjunto)":
            tex.append(f"\\section*{{{len(r)} retângulos -- Subconjunto de tamanho {len(r_c)}}}")
            tex.append("\\vspace{1.5cm}")
        elif s == "Guardas Coloridos":
            tex.append(f"\\section*{{{len(r)} retângulos -- Guardas Coloridos:}}")
            tex.append("\\vspace{1.5cm}")
            qtd_colors = max([color_idx for _, color_idx in c_v]) if c_v else 0

        tex += generate_colors(qtd_colors)
        tex += generate_rects(r, v, c_v, r_c, s)

    tex.append("\n\\end{document}")
    return "\n".join(tex)


def generate_colors(qtd_colors : int):
    tex_colors = []
    for i in range(qtd_colors):
        hue = i / qtd_colors
        r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.8)
        r_p, g_p, b_p = colorsys.hsv_to_rgb(hue, 0.15, 0.95)

        tex_colors.append(f"\\definecolor{{corPonto{i+1}}}{{rgb}}{{{r:.2f},{g:.2f},{b:.2f}}}")
        tex_colors.append(f"\\definecolor{{corFundo{i+1}}}{{rgb}}{{{r_p:.2f},{g_p:.2f},{b_p:.2f}}}")
        
    return tex_colors

# exemplo de argumentos:
# rectangles = [1, 2, 3, 4]
# vertices = {
#     ('v1', (1, 3)): {2}, ('v2', (3, 3)): {1, 2}, ('v3', (4, 3)): {1}, 
#     ('v4', (1, 2)): {2, 4}, ('v5', (2, 2)): {2, 3, 4}, ('v6', (3, 2)): {1, 2, 3}, 
#     ('v7', (1, 1)): {4}, ('v8', (2, 1)): {3, 4}, ('v9', (3, 1)): {1, 3}, 
#     ('v10', (4, 1)): {1}
# }
# covered_vertices = {('v2', (3, 3)), ('v5', (2, 2))}
def generate_rects(rectangles : list[int], vertices : dict[tuple[str, tuple[int, int]], set[int]], covered_vertices, rects_to_cover : list[int], name : str = "Greedy"):
    if len(covered_vertices) == 0: return []

    # 1. Limites do desenho
    list_x = [coord[0] for _, coord in vertices.keys()]
    list_y = [coord[1] for _, coord in vertices.keys()]
    width = max(list_x) - min(list_x)
    height = max(list_y) - min(list_y)

    # 2. Fronteiras de cada retângulo
    coord_vertices = {v_id: (x, y) for (v_id, (x, y)) in vertices.keys()}
    limits_rects = {r: [
                    min(c[0] for (_, c), r_arr in vertices.items() if r in r_arr), # min_x
                    max(c[0] for (_, c), r_arr in vertices.items() if r in r_arr), # max_x
                    min(c[1] for (_, c), r_arr in vertices.items() if r in r_arr), # min_y
                    max(c[1] for (_, c), r_arr in vertices.items() if r in r_arr)  # max_y
                    ] for r in rectangles}

    # 3. Mapeamento de colors e Vigilância
    rect_color = {}
    point_colors = {}
    colored_rects = set()
    covered_v_ids = set()

    if name == "Guardas Coloridos":
        for (v_id, _), color_index in covered_vertices:
            covered_v_ids.add(v_id)
            point_colors[v_id] = f"corPonto{color_index}"
    else:
        for i_color, (v_id, _) in enumerate(sorted(covered_vertices)):
            covered_v_ids.add(v_id)
            point_color_name = f"corPonto{i_color+1}"
            background_color_name = f"corFundo{i_color+1}"
            point_colors[v_id] = point_color_name
            
            for (v_key, _), seen_rects in vertices.items():
                if v_key == v_id:
                    for r in seen_rects:
                        if r in rects_to_cover:
                            if r not in colored_rects:
                                rect_color[r] = background_color_name
                                colored_rects.add(r)

    # 4. Linhas do grid
    horizontal_lines = set()
    vertical_lines = set()
    for r, (x1, x2, y1, y2) in limits_rects.items():
        horizontal_lines.add((x1, x2, y1))
        horizontal_lines.add((x1, x2, y2))
        vertical_lines.add((x1, y1, y2))
        vertical_lines.add((x2, y1, y2))

    # 5. Montar a string do TeX
    tex = []
    tex.append("\\begin{center}")
    tex.append(f"\\begin{{picture}}({width},{height})(0,0)")
    
    tex.append("    % --- FUNDOS COLORIDOS ---")
    tex.append("    \\setlength{\\fboxsep}{0pt}%")
    tex.append("    \\setlength{\\fboxrule}{0pt}%")
    
    for r, (x1, x2, y1, y2) in sorted(limits_rects.items()):
        w = x2 - x1
        h = y2 - y1
        background_color = rect_color.get(r, "white")
        if background_color != "white":
            tex.append(f"    \\put({x1},{y1}){{\\fcolorbox{{{background_color}}}{{{background_color}}}{{\\makebox({w},{h}){{~}}}}}}")

    # ETAPA B: Linhas do grid
    tex.append("\n    % --- BORDAS DO GRID ---")
    for x1, x2, y in sorted(horizontal_lines, key=lambda t: (t[2], t[0])):
        tex.append(f"    \\put({x1},{y}){{\\line(1,0){{{x2 - x1}}}}}")
    for x, y1, y2 in sorted(vertical_lines, key=lambda t: (t[0], t[1])):
        tex.append(f"    \\put({x},{y1}){{\\line(0,1){{{y2 - y1}}}}}")

    # ETAPA C: Rótulos
    tex.append("\n    % --- RÓTULOS ---")
    for r, (x1, x2, y1, y2) in sorted(limits_rects.items()):
        w = x2 - x1
        h = y2 - y1
        if r in rects_to_cover:
            tex.append(f"    \\put({x1},{y1}){{\\makebox({w},{h}){{\\textbf{{{r}}}}}}}")
        else:
            tex.append(f"    \\put({x1},{y1}){{\\makebox({w},{h}){{{{{r}}}}}}}")

    # ETAPA D: Vértices com Guardas
    tex.append("\n    % --- VÉRTICES COM GUARDAS ---")
    for v_id, (x, y) in sorted(coord_vertices.items()):
        if v_id in covered_v_ids: 
            cor_ponto = point_colors[v_id]
            tex.append(f"    \\put({x},{y}){{\\color{{{cor_ponto}}}\\circle*{{0.5}}}}")
            tex.append(f"    \\put({x},{y}){{\\thicklines\\color{{black}}\\circle{{0.5}}}}")

    tex.append("\\end{picture}\n")
    tex.append("\\vspace{0.1cm}")

    if name == "Guardas Coloridos":
        qtd = len({cor for _, cor in covered_vertices})
        tex.append(f"\\textbf{{Solução {name}:}} {qtd} cor(es)")
    else:
        tex.append(f"\\textbf{{Solução {name}:}} {len(covered_vertices)} guarda(s)")

    tex.append("\\end{center}")
    tex.append("\\vspace{1.5cm}\n")
    
    return tex
