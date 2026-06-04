from queue import Queue
from ortools.linear_solver import pywraplp
from integer_prog import mip
from rectangle_group import RectangleGroup
from copy import deepcopy

Point = tuple[int, int]

def dfs(block: RectangleGroup, rect: int, visited_rects: set[int], curr_depth:int, max_depth:int, root_v:tuple[str, Point], vertices: dict[tuple[str, Point], set[int]]):
    if rect in visited_rects:
        return
    if curr_depth >= max_depth:
        return
    
    visited_rects.add(rect)
    vertices[root_v].add(rect)
    
    for ri in block.rectangles[rect].adj:
        dfs(block, ri, visited_rects, curr_depth+1, max_depth, root_v, vertices)
    return

def _compute_point_coverage(block: RectangleGroup, vertices: dict[tuple[str, Point], set[int]], reach:int):
    for v in vertices:
        curr_adj = vertices[v].copy()
        for r in curr_adj:
            dfs(block, r, set(), 0, reach, v, vertices)

def extended_guard(retangulos: list[int], vertices: dict[tuple[str, Point], set[int]], block:RectangleGroup, rects_to_cover: list[int] = None, reach: int = 1):
    aux_vertices = deepcopy(vertices)
    _compute_point_coverage(block, aux_vertices, reach)
    return mip(retangulos, aux_vertices, rects_to_cover)
