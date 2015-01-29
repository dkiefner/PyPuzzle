from abc import ABCMeta, abstractmethod
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

    def df_search(self, node, g, bound, final_state, heuristic):
        f = g + heuristic.get_costs(node.puzzle_state, final_state)
        # print("f={0}, g={1}, bound={2}".format(f, g, bound))
        # print("check node:" + node.puzzle_state.get_formatted_state()())

        if f > bound:
            return f
        if node.puzzle_state == final_state:
            return node

        c_min = sys.maxsize

        children = node.get_children()
        for child in children:
            t = self.df_search(child, g + node.cost, bound, final_state, heuristic)
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

        return children

    def get_formatted_solution(self):
        node = self
        puzzle_state_list = []
        while node is not None:
            puzzle_state_list.append(node.puzzle_state)
            node = node.parent

        puzzle_state_list.reverse()
        formatted = ""
        for depth, puzzle_state in enumerate(puzzle_state_list):
            formatted += "\nDepth=" + str(depth)
            formatted += puzzle_state.get_formatted_state()

        return formatted

    def __hash__(self):
        return hash((self.cost, self.parent))