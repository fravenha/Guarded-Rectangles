import math
import queue
import sys
from copy import deepcopy
from pprint import pprint

from rectangle_group import RectangleGroup
from utils.problem_parser import ProblemParser
from utils.logger import logger

Point = tuple[int, int]

class WorkingState:
    def __init__(self):
        self.assign: dict[int, Point | None] = {}
        """k_i → chosen guard vertex (None = not yet assigned). Keys are exactly R'."""
        self.dom: dict[int, set[Point]] = {}
        """Current domain for each variable in R' (perimeter vertices still available)."""
        self.best: set[Point] = set()
        """Minimum set of distinct guard vertices found so far."""

def select_unassigned_var(state: WorkingState) -> int | None:
    """MRV heuristic: pick the unassigned rectangle with the smallest domain."""
    best_id, best_size = None, math.inf
    for ri, v in state.assign.items():
        if v is None:
            sz = len(state.dom[ri])
            if sz < best_size:
                best_size, best_id = sz, ri
    return best_id


def order_vertex_values(rect_id: int, state: WorkingState, block: RectangleGroup) -> list[Point]:
    """LCV heuristic: prefer vertices shared with the most other unassigned R' neighbours."""
    unassigned_neighbours = {
        rj for rj in block.rectangles[rect_id].adj
        if rj in state.assign and state.assign[rj] is None
    }

    def score(v: Point) -> int:
        return sum(1 for rj in unassigned_neighbours if v in block.rectangles[rj].points)

    return sorted(state.dom[rect_id], key=score, reverse=True)

def lower_bound(state: WorkingState) -> int:
    """Worst case solution from current state
    """
    chosen: set[Point] = {v for v in state.assign.values() if v is not None}

    extra = sum(
        1 for ri, v in state.assign.items()
        if v is None and not (state.dom[ri] & chosen)
    )
    return len(chosen) + extra

def propagate_shared_vertex(rect_id: int, v: Point, state: WorkingState, block: RectangleGroup) -> bool:

    for rj in block.point_to_rect[v]:
        if rj == rect_id:
            continue
        if rj not in state.assign:
            continue                        # rj is not a decision variable (not in R')
        if state.assign[rj] is not None:
            continue                        # already assigned
        if v in state.dom[rj]:
            state.dom[rj] = {v}             # force rj to reuse the same guard
        else:
            return False                    # v was pruned from rj's domain → inconsistent
    return True


def ac_3_revise(ri: int, rj: int, state: WorkingState, block: RectangleGroup) -> bool:
    """Remove all v E dom_ri where v is shared by ri and v in dom_ri but not in dom_rj
    """
    shared = block.rectangles[ri].points & block.rectangles[rj].points
    to_remove = {v for v in state.dom[ri] if v in shared and v not in state.dom[rj]}
    if to_remove:
        state.dom[ri] -= to_remove
        return True
    return False


def ac_3(state: WorkingState, block: RectangleGroup, starting_rect: int | None = None) -> bool:

    unassigned_vars: set[int] = {ri for ri, v in state.assign.items() if v is None}

    q: queue.Queue[tuple[int, int]] = queue.Queue()

    if starting_rect is not None:
        # Only re-check neighbours of the rectangle that just changed.
        for rj in block.rectangles[starting_rect].adj:
            if rj in unassigned_vars:
                q.put((rj, starting_rect))
    else:
        for ri in unassigned_vars:
            for rj in block.rectangles[ri].adj:
                if rj in unassigned_vars:
                    q.put((ri, rj))

    in_queue: set[tuple[int, int]] = set(q.queue)

    while not q.empty():
        ri, rj = q.get()
        in_queue.discard((ri, rj))

        if ac_3_revise(ri, rj, state, block):
            # domain is empty, inconsistent
            if not state.dom[ri]:
                return False                
            for rk in block.rectangles[ri].adj:
                if rk != rj and rk in unassigned_vars:
                    arc = (rk, ri)
                    if arc not in in_queue:
                        q.put(arc)
                        in_queue.add(arc)

    return True


def _branch_bound(state: WorkingState, block: RectangleGroup) -> None:
    """Recursive branch-and-bound over R' variables.
    """

    # can we improve?
    lb = lower_bound(state)
    if lb >= len(state.best):
        return                              

    ri = select_unassigned_var(state)

    if ri is None:
        # All R' variables are assigned which is a solution.
        guards = {v for v in state.assign.values() if v is not None}
        if len(guards) < len(state.best):
            state.best = guards
        return

    for v in order_vertex_values(ri, state, block):
        dom_saved = deepcopy(state.dom)

        state.assign[ri] = v
        state.dom[ri] = {v}

        consistent = propagate_shared_vertex(ri, v, state, block)
        if consistent:
            consistent = ac_3(state, block, starting_rect=ri)

        if consistent:
            _branch_bound(state, block)

        # Backtrack
        state.assign[ri] = None
        state.dom = dom_saved

def branch_bound_ac3(block: RectangleGroup, rects_to_cover: set[int] | None = None) -> set[Point]:
    """Branch-and-bound solver with AC-3 constraint propagation.
    """
    if not rects_to_cover:
        rects_to_cover = set(block.rectangles.keys())

    required: set[int] = set(rects_to_cover)

    state = WorkingState()

    # Only create variables for rectangles in R'.
    for rect_id in required:
        rect = block.rectangles[rect_id]
        state.dom[rect_id] = set(rect.points)
        state.assign[rect_id] = None

    # Pessimistic upper bound: one distinct guard per required rectangle.
    state.best = set().union(*(block.rectangles[r].points for r in required))

    _branch_bound(state, block)

    return state.best


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    args = sys.argv
    file_path = args[1]
    with open(file_path, "r") as file:
        block = ProblemParser().parse_block(file)

    print("============== Rectangles ==============")
    for rect_id, rect in block.rectangles.items():
        print(f"  {rect}  points={rect.points}")

    print("\n============== All vertices ==============")
    pprint(block.points)

    print("\n============== Solving (full coverage) ==============")
    result = branch_bound_ac3(block)
    print(f"  Guards needed : {len(result)}")
    print(f"  Guard vertices: {result}")