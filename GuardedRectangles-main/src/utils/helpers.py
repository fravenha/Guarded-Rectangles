import csv
import os
import subprocess


def nomear_vertices(group):
    pontos_ordenados = sorted(group.point_to_rect.items(), key=lambda item: (-item[0][1], item[0][0]))

    vertices_com_nomes = {} 
    for j, (coord, retangulos) in enumerate(pontos_ordenados, start=1):
        vertices_com_nomes[(f"v{j}", coord)] = retangulos
    return vertices_com_nomes

def filtrar_vertices(n_retangulos, vertices_com_nomes):
    # filtra apenas vertices internos, retirando os vertices da borda exterior do conjunto
    min_x = min(k[1][0] for k in vertices_com_nomes)
    max_x = max(k[1][0] for k in vertices_com_nomes)
    min_y = min(k[1][1] for k in vertices_com_nomes)
    max_y = max(k[1][1] for k in vertices_com_nomes)

    vertices_internos = {
        (nome, (x, y)): rects 
        for (nome, (x, y)), rects in vertices_com_nomes.items()
        if min_x < x < max_x and min_y < y < max_y
    }
    
    rect_to_points = [set() for _ in range(n_retangulos+1)]
    for vertice, conjunto_retangulos in vertices_internos.items():
        for r in conjunto_retangulos:
            rect_to_points[r].add(vertice)
    
    for i in range(1, len(rect_to_points)):
        if len(rect_to_points[i]) == 0:
            return vertices_com_nomes

    return vertices_internos

def salvar_em_csv(row, filename="resultados_algoritmos.csv"):
    # Verifica se o arquivo já existe para saber se precisa colocar cabeçalho
    arquivo_existe = os.path.exists(filename)
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if not arquivo_existe:
            writer.writerow([
                "Qtd_Retangulos", 
                "Greedy_Verts", 
                "Greedy_Rects", 
                "Greedy_Rects_and_Verts", 
                "Greedy_Neighbors", 
                "Constraints Propagation",
                "Constraint Programming",
                "Integer Programming",
                "Dynamic Programming",
                "Extended Solution (D=1)",
                "Extended Solution (D=2)"
            ])
            
        writer.writerow(row)


def get_input_file(n_retangulos, n_instancias):
    input_file_path = "./resources/inputs/new_input"
    qtd_groups = len(n_retangulos) * n_instancias

    with open(input_file_path, 'w') as file_input:
        file_input.write(str(qtd_groups) + "\n")

        for n in n_retangulos:
            # gerar rects
            subprocess.run(
                ["./../rects_generator.out", "res", "resFigs.tex"],
                input=f"{n} {n_instancias}\n",
                cwd="./resources/rects_tex",
                stdout=subprocess.DEVNULL,
                text=True
            )
            file_path = "./resources/rects_tex/res"

            # passar todos os casos para um só arquivo input
            with open(file_path, 'r') as arquivo_gerado:
                next(arquivo_gerado, None) 
                for linha in arquivo_gerado:
                    file_input.write(linha)
                    file_input.flush()
    return input_file_path