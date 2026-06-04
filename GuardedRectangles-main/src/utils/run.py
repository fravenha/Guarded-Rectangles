import math
import random
import time

from cp_solver import cp_solver
from utils.logger import logger
from utils.helpers import *
from utils.problem_parser import ProblemParser
from greedy import *
from integer_prog import mip
from constraints_propagation import branch_bound_ac3
from dynamic_programming import dynamic_programming_solver
from colored_guards import color_guards, coloring
from extended_guard import extended_guard


def run(n_retangulos : list[int], n_instancias : int, calcular_subconjuntos : bool):
    info_tex = []

    input_file_path = get_input_file(n_retangulos, n_instancias)
    try:
        all_groups = ProblemParser.parse_all(input_file_path)
        if not all_groups: return

        for group in all_groups:
            vertices_com_nomes = nomear_vertices(group)
            retangulos = list(group.rectangles.keys())
            vertices_candidatos = filtrar_vertices(len(retangulos), vertices_com_nomes)

            if calcular_subconjuntos:
                subconjuntos(vertices_com_nomes, retangulos, vertices_candidatos, info_tex, group) 
            conjunto(vertices_com_nomes, retangulos, vertices_candidatos, info_tex, group)

    except FileNotFoundError:
        logger.error(f"Error: The file was not found at path:\n{input_file_path}")

    return info_tex


def subconjuntos(vertices_com_nomes, retangulos, vertices_candidatos, info_tex, group):
    print()
    print(len(retangulos), "RETÂNGULOS (subconjuntos) --------")
 
    retangulos_copia = retangulos.copy()
    gerador = random.Random(42)
    gerador.shuffle(retangulos_copia)

    subconjuntos = {}
    total_elementos = len(retangulos_copia)

    for p in [0.30, 0.50, 0.70]:
        tamanho_subconjunto = math.ceil(total_elementos * p)
        subconjuntos[f"{int(p*100)}%"] = retangulos_copia[:tamanho_subconjunto]

    for porcentagem, rects_a_cobrir in subconjuntos.items():
        rects_a_cobrir.sort()
        print(f"\nSUBCONJUNTO {porcentagem} (tamanho {len(rects_a_cobrir)}):")

        greedy_rects_solution = greedy_rects(retangulos, vertices_candidatos, set(rects_a_cobrir))
        print("Greedy Rects Solution = ", len(greedy_rects_solution))
        
        greedy_verts_solution = greedy_verts(retangulos, vertices_candidatos, set(rects_a_cobrir))
        print("Greedy Verts Solution = ", len(greedy_verts_solution))
        
        greedy_rects_verts_solution = greedy_rects_verts(retangulos, vertices_candidatos, set(rects_a_cobrir))
        print("Greedy Rects and Verts Solution = ", len(greedy_rects_verts_solution))
        
        neighbors_greedy_solution = neighbors_greedy(retangulos, vertices_candidatos, set(rects_a_cobrir))
        print("Greedy Neighbors Solution = ", len(neighbors_greedy_solution))

        ip_solution = mip(retangulos, vertices_candidatos, set(rects_a_cobrir))
        print("IP Solution = ", len(ip_solution))

        cp_solution = cp_solver(retangulos, vertices_candidatos, set(rects_a_cobrir))
        print("CCP Solution = ", len(cp_solution))

        dynamic_solution = dynamic_programming_solver(retangulos, vertices_candidatos, set(rects_a_cobrir))
        print("Dynamic Programming Solution = ", len(dynamic_solution))

        extetended_solution1 = extended_guard(retangulos, vertices_candidatos, group, set(rects_a_cobrir), reach=1)
        print("Extended 1 Solution = ", len(extetended_solution1))

        extetended_solution2 = extended_guard(retangulos, vertices_candidatos, group, set(rects_a_cobrir), reach=2)
        print("Extended 2 Solution = ", len(extetended_solution2))
        
        print()
        if len(retangulos) <= 60: 
            info_tex.append((retangulos, vertices_com_nomes, greedy_rects_solution, rects_a_cobrir, "Greedy Rects (Subconjunto)"))
            info_tex.append((retangulos, vertices_com_nomes, greedy_verts_solution, rects_a_cobrir, "Greedy Verts (Subconjunto)"))
            # info_tex.append((retangulos, vertices_com_nomes, greedy_rects_verts_solution, rects_a_cobrir, "Greedy Rects and Verts (Subconjunto)"))
            # info_tex.append((retangulos, vertices_com_nomes, neighbors_greedy_solution, rects_a_cobrir, "Greedy Neighbors (Subconjunto)"))
            info_tex.append((retangulos, vertices_com_nomes, ip_solution, rects_a_cobrir, "Integer Programming (Subconjunto)"))
            info_tex.append((retangulos, vertices_com_nomes, cp_solution, rects_a_cobrir, "Constraint Programming (Subconjunto)"))
            info_tex.append((retangulos, vertices_com_nomes, dynamic_solution, rects_a_cobrir, "Dynamic Programming (Subconjunto)"))
            info_tex.append((retangulos, vertices_com_nomes, extetended_solution1, rects_a_cobrir, "Guardas com raio de alcance 1 (Subconjunto)"))
            info_tex.append((retangulos, vertices_com_nomes, extetended_solution2, rects_a_cobrir, "Guardas com raio de alcance 2 (Subconjunto)"))
    


def conjunto(vertices_com_nomes, retangulos, vertices_candidatos, info_tex, group):
    print()
    print(len(retangulos), "RETÂNGULOS --------")

    # ------- GREEDY SOLUTION -------
    start_time = time.time()
    greedy_rects_solution = greedy_rects(retangulos, vertices_candidatos)
    end_time = time.time()
    greedy2_time = end_time - start_time
    print("Greedy Rects Solution = ", len(greedy_rects_solution))

    start_time = time.time()
    greedy_verts_solution = greedy_verts(retangulos, vertices_candidatos)
    end_time = time.time()
    naive_greedy_time = end_time - start_time
    print("Greedy Verts Solution = ", len(greedy_verts_solution))
    
    start_time = time.time()
    greedy_rects_verts_solution = greedy_rects_verts(retangulos, vertices_candidatos)
    end_time = time.time()
    greedy3_time = end_time - start_time
    print("Greedy Rects and Verts Solution = ", len(greedy_rects_verts_solution))
    
    start_time = time.time()
    neighbors_greedy_solution = neighbors_greedy(retangulos, vertices_candidatos)
    end_time = time.time()
    neighbors_greedy_time = end_time - start_time
    print("Greedy Neighbors Solution = ", len(neighbors_greedy_solution))
    # ------- END GREEDY SOLUTION -------

    # ------- IP SOLUTION ----------
    start_time = time.time()
    ip_solution = mip(retangulos, vertices_candidatos)
    end_time = time.time()
    ip_time = end_time - start_time
    print("IP Solution = ", len(ip_solution))
    # ------- END IP SOLUTION -------
    
    # ------- CONSTRAINTS PROPAGATION SOLUTION -------
    start_time = time.time()
    constraints_prop_solution = branch_bound_ac3(group)
    end_time = time.time()
    constraints_prop_time = end_time - start_time
    print("Constraints Propagation Solution = ", len(constraints_prop_solution))
    # ------- END CONSTRAINTS PROPAGATION SOLUTION -------

    # ------- CP SOLUTION -------
    start_time = time.time()
    cp_solution = cp_solver(retangulos, vertices_candidatos)
    end_time = time.time()
    cp_time = end_time - start_time
    print("CCP Solution = ", len(cp_solution))
    # ------- END CP SOLUTION -------

    # ------- DYNAMIC PROG SOLUTION -------
    start_time = time.time()
    dynamic_prog_solution = dynamic_programming_solver(retangulos, vertices_candidatos)
    end_time = time.time()
    dynamic_prog_time = end_time - start_time
    print("Dynamic Programming Solution = ", len(dynamic_prog_solution))
    # ------- END DYNAMIC PROG SOLUTION -------

    colored_guards_solution = color_guards(ip_solution, vertices_candidatos, retangulos)
    qtd_cores = len({cor for _, cor in colored_guards_solution})
    colored_guards_solution2 = coloring(vertices_com_nomes, retangulos, len(ip_solution), qtd_cores)
    
    # guardas com visao de D retangulos
    # extetended_solution1 = extended_guard(retangulos, vertices_candidatos, group, reach=1)
    # print("Extended Solution (D=1) = ", len(extetended_solution1))
    extetended_solution2 = extended_guard(retangulos, vertices_candidatos, group, reach=2)
    print("Extended Solution (D=2) = ", len(extetended_solution2))
        
    print()
    salvar_em_csv(
        filename="resultados_algoritmos.csv",
        row=[len(retangulos),
        len(greedy_verts_solution),
        len(greedy_rects_solution),
        len(greedy_rects_verts_solution),
        len(neighbors_greedy_solution),
        len(constraints_prop_solution),
        len(cp_solution),
        len(ip_solution),
        len(dynamic_prog_solution),
        # len(extetended_solution1),
        len(extetended_solution2),
        ]
    )
    
    salvar_em_csv(
        filename="tempos_algoritmos.csv",
        row=[len(retangulos),
        naive_greedy_time,
        greedy2_time,
        greedy3_time,
        neighbors_greedy_time,
        constraints_prop_time,
        cp_time,
        ip_time,
        dynamic_prog_time
        ]
    )

    if len(retangulos) <= 60: 
        info_tex.append((retangulos, vertices_com_nomes, greedy_rects_solution, retangulos, "Greedy Rects"))
        info_tex.append((retangulos, vertices_com_nomes, greedy_verts_solution, retangulos, "Greedy Verts"))
        info_tex.append((retangulos, vertices_com_nomes, greedy_rects_verts_solution, retangulos, "Greedy Rects and Verts"))
        info_tex.append((retangulos, vertices_com_nomes, neighbors_greedy_solution, retangulos, "Greedy Neighbors"))
        info_tex.append((retangulos, vertices_com_nomes, ip_solution, retangulos, "Integer Programming"))
        info_tex.append((retangulos, vertices_com_nomes, constraints_prop_solution, retangulos, "Constraints Propagation"))
        info_tex.append((retangulos, vertices_com_nomes, cp_solution, retangulos, "Constraint Programming"))
        info_tex.append((retangulos, vertices_com_nomes, dynamic_prog_solution, retangulos, "Dynamic Programming"))
        info_tex.append((retangulos, vertices_com_nomes, colored_guards_solution, retangulos, "Guardas Coloridos"))
        info_tex.append((retangulos, vertices_com_nomes, colored_guards_solution2, retangulos, "Guardas Coloridos"))
        # info_tex.append((retangulos, vertices_com_nomes, extetended_solution1, retangulos, f"Guardas com raio de alcance de 1"))
        info_tex.append((retangulos, vertices_com_nomes, extetended_solution2, retangulos, f"Guardas com raio de alcance de 2"))
