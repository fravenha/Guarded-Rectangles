import subprocess

from utils.helpers import *
from utils.latex_generator import generate_latex
from utils.run import run

def main():
    n_retangulos = list(map(int, input("Nº de retângulos (separados por espaço): ").split()))
    n_instancias = int(input("Nº de instâncias: "))
    calcular_subconjuntos = bool(int(input("Calcular subconjuntos? [0/1] ")))
    
    info_tex = run(n_retangulos, n_instancias, calcular_subconjuntos)

    if info_tex:
        with open("resources/outputs/output.tex", "w", encoding="utf-8") as ficheiro:
                ficheiro.write(generate_latex(info_tex))
                ficheiro.flush()
                subprocess.run(["pdflatex", "./resources/outputs/output.tex"], stdout=subprocess.DEVNULL)
                print("\nFicheiro PDF gerado!")


if __name__ == "__main__":
    main()
