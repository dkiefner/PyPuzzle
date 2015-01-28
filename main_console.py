# Main Module
from puzzle_state import PuzzleState
import solver
import heuristic
import time

# ------------------------------------------------------------
# Given states
# ------------------------------------------------------------

solvable_start_array = [[6, 1, 10, 2], [7, 11, 4, 14], [5, None, 9, 15], [8, 12, 13, 3]]
solvable_start_array_simple = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, None, 15]]
solvable_start_array_max_depth = [[None, 12, 9, 13], [15, 11, 10, 14], [3, 7, 2, 5], [4, 8, 6, 1]]
unsolvable_start_array = [[13, 10, 11, 6], [5, 7, 4, 8], [1, 11, 14, 9], [3, 15, 2, None]]
final_array = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, None]]

solvable_start_array_lc_vertical = [[7, 9, 1, 8], [5, None, 2, 10], [3, 4, 11, 6], [15, 13, 14, 12]]
solvable_start_array_lc_horizontal = [[11, 10, None, 9], [12, 15, 3, 5], [13, 8, 2, 4], [1, 6, 7, 14]]

# ------------------------------------------------------------
# Start
# ------------------------------------------------------------

start_time = time.time()

start_state = PuzzleState(solvable_start_array)
final_state = PuzzleState(final_array)

# ------------------------------------------------------------
# Formatting
# ------------------------------------------------------------
print("start state:")
start_state.pretty_print()
print("final state:")
final_state.pretty_print()

# ------------------------------------------------------------
# Solvability
# ------------------------------------------------------------
ida_star_solver = solver.IDAStar()
print("inversions: " + str(start_state.get_inversion_count()))
print("is_solvable: " + str(solver.Solver.is_solvable(start_state, final_state)))


# ------------------------------------------------------------
# Heuristic costs
# ------------------------------------------------------------

lc_heuristic = heuristic.LinearConflict()
print("sum costs=" + str(lc_heuristic.get_costs(start_state, final_state)))


# ------------------------------------------------------------
# Node
# ------------------------------------------------------------
node = solver.Node(start_state, None, 0);
node.get_children()


# ------------------------------------------------------------
# Solve
# ------------------------------------------------------------
result = ida_star_solver.solve(start_state, final_state, lc_heuristic)
if isinstance(result, solver.Node):
    print("Found solution:")
    result.puzzle_state.pretty_print()
else:
    print("Didn't found solution until depth.")

print("\nFinished in " + str(time.time() - start_time) + " seconds")