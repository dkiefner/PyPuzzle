from abc import ABCMeta, abstractmethod
from puzzle_state import PuzzleState
import copy
import sys


# ------------------------------------------------------------
# Abstract solver class
# ------------------------------------------------------------
class Solver(metaclass=ABCMeta):
    @abstractmethod
    def solve(self, start_state, final_state, heuristic):
        raise NotImplementedError()

    @staticmethod
    def is_solvable(start_state, final_state):
        if start_state is None or final_state is None:
            return False

        return start_state == final_state \
               or start_state.get_inversion_count() % 2 == 0


# ------------------------------------------------------------
# Concrete solver class for IDA* algorithm
# ------------------------------------------------------------
class IDAStar(Solver):
    # procedure ida_star(root)
    # bound := h(root)
    # loop
    # t := search(root, 0, bound)
    # if t = FOUND then return FOUND
    # if t = ∞ then return NOT_FOUND
    # bound := t
    # end loop
    # end procedure
    def solve(self, start_state, final_state, heuristic):
        start_state = start_state
        final_state = final_state
        heuristic = heuristic
        t = None

        if Solver.is_solvable(start_state, final_state):
            bound = heuristic.get_costs(start_state, final_state)
            start_node = Node(start_state, None, 0)

            while True:
                t = self.df_search(start_node, 0, bound, final_state, heuristic)
                if isinstance(t, Node):
                    break
                if t == sys.maxsize:
                    return None
                if isinstance(t, int):
                    bound = t

        return t

    # function search(node, g, bound)
    #   f := g + h(node)
    #   if f > bound then return f
    #   if is_goal(node) then return FOUND
    #   min := ∞
    #   for succ in successors(node) do
    #     t := search(succ, g + cost(node, succ), bound)
    #     if t = FOUND then return FOUND
    #     if t < min then min := t
    #   end for
    #   return min
    # end function
    def df_search(self, node, g, bound, final_state, heuristic):
        f = g + heuristic.get_costs(node.puzzle_state, final_state)

        if bound > 4:  # TODO remove
            return None

        # print("check node:")
        # print(node.puzzle_state.pretty_print())

        if f > bound:
            return f
        if node.puzzle_state == final_state:
            return node

        c_min = sys.maxsize

        children = node.get_children()
        for child in children:
            print("search children: f=" + str(f) + " g=" + str(g) + " bound=" + str(bound))
            t = self.df_search(child, g + node.cost + 1, bound, final_state, heuristic)
            if isinstance(t, Node):
                return t
            if t < c_min:
                c_min = t

        return c_min


# ------------------------------------------------------------
# Concrete solver class for A* algorithm
# ------------------------------------------------------------
class AStar(Solver):
    def solve(self, start_state, final_state, heuristic):
        print("solve a*")


# ------------------------------------------------------------
# Node
# ------------------------------------------------------------
class Node:
    def __init__(self, puzzle_state, parent, cost):
        self.puzzle_state = puzzle_state
        self.parent = parent
        self.cost = cost

    def get_children(self):
        children = []
        movements = self.puzzle_state.get_possible_movements(None)  # TODO ignore movement to parents state if available

        for move in movements:
            new_state = copy.deepcopy(self.puzzle_state)
            new_state.move(None, move)
            child = Node(new_state, self, self.cost + 1)
            children.append(child)
            # print("new state: move=" + str(move.current_move) + " cost=" + str(self.cost + 1))
            # new_state.pretty_print()

        return children

    def __hash__(self):
        return hash((self.cost, self.parent))