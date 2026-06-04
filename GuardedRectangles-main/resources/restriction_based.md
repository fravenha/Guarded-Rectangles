## Ex 2(a) - Restriction based Programming

Defining the mathematical model for a constraint-based programming solution to this variant of the Guarded Rectangles problem.

## Data & Parameters
A block is the largest rectangle of the partition and covers the entire partition. Going forward, the term "rectangle" refers to an unpartitioned sub-rectangle.

*   **Rectangles:** The set of unpartitioned rectangles that form the block is defined as $R$, where $n$ is the total number of rectangles:
    $$R = \{r_1, r_2, r_3, \dots, r_n\}$$

*   **Vertices:** The set of all vertices in a block is defined as $V$, where $m$ is the total number of vertices:
    $$V = \{v_1, v_2, v_3, \dots, v_m\}$$

*   **Perimeters:** Each rectangle has a specific set of vertices along its perimeter. The subset of $V$ that defines the vertices along the perimeter of rectangle $r_j$ is defined as $V_{r_j}$:
    $$V_{r_j} \subseteq V$$

*   **Visibility:** The set of rectangles that a guard at vertex $v_i$ can see is given by $cover(v_i)$:
    $$cover(v_i) \subseteq R$$

*   **Minimum acceptable coverage:** 
    *   $P$: A real number percentage 
    $$P \in (0,1], P \in \mathbb{R_0^+}$$
    >Note: P = 0 is satisfiable with 0 guards.

    *   $G$: The total integer number of rectangles that must be guarded.
    $$G = ceiling(n \cdot P)$$
    $$G \in [1, n], G \in \mathbb{Z_0^+}$$
## Decision Variables

*   Let: $k_i$ be the decision variable representing the vertex chosen to guard rectangle $r_i$ or 0 for unguarded rectangles.
    $$k_i \in V_{r_i} \cup \{0\} \\ r_i \in R$$

## Constraints (Restrictions)
*   **Variable Domains:**
    $$k_i \in V_{r_i}$$

*   **Coverage:** At least $G$ rectangles must be guarded.
    $$|\{r_i | k_i \neq 0 \}|=G$$

## Goal
Minimize the total number of distinct vertices:
$$|\{k_i | k_i \neq 0\}|$$