from abc import ABCMeta, abstractmethod
from math import fabs


# ------------------------------------------------------------
# Abstract heuristic class
# ------------------------------------------------------------
class Heuristic(metaclass=ABCMeta):
    @abstractmethod
    def get_costs(self, current_state, final_state):
        raise NotImplementedError()


# ------------------------------------------------------------
# Concrete Manhattan Distance heuristic
# ------------------------------------------------------------
class ManhattanDistance(Heuristic):
    def get_costs(self, current_state, final_state):
        start_pos_map = current_state.position_map
        final_pos_map = final_state.position_map
        distance = 0

        for tile, pos in start_pos_map.items():
            if tile is not None:
                distance += fabs(pos[0] - final_pos_map[tile][0]) + fabs(pos[1] - final_pos_map[tile][1])

        return int(distance)


# ------------------------------------------------------------
# Concrete Manhattan Distance heuristic
# ------------------------------------------------------------
class LinearConflict(ManhattanDistance):
    def get_costs(self, current_state, final_state):
        distance = super().get_costs(current_state, final_state)

        distance += self.get_cost_for_linear_vertical_conflicts(current_state)
        distance += self.get_cost_for_linear_horizontal_conflicts(current_state)

        return int(distance)

    def get_cost_for_linear_vertical_conflicts(self, puzzle_state):
        length = puzzle_state.get_len()
        conflicts = 0

        for i, row in enumerate(puzzle_state.state_array):
            max_value = -1
            for j, col in enumerate(puzzle_state.state_array):
                cell_value = puzzle_state.get_tile((j, i))
                # check if tile is in final row
                if cell_value is not None and int((cell_value - 1) / length) == i:
                    if cell_value > max_value:
                        max_value = cell_value
                    else:
                        # linear conflict
                        conflicts += 2

        return conflicts

    def get_cost_for_linear_horizontal_conflicts(self, puzzle_state):
        length = puzzle_state.get_len()
        conflicts = 0

        for i, col in enumerate(puzzle_state.state_array):
            max_value = -1
            for j, row in enumerate(puzzle_state.state_array):
                cell_value = puzzle_state.get_tile((i, j))
                # check if tile is in final row
                if cell_value is not None and cell_value % length == i + 1:
                    if cell_value > max_value:
                        max_value = cell_value
                    else:
                        # linear conflict
                        conflicts += 2

        return conflicts