# Main Module
import time
import threading
import sys

from model import heuristic, solver

from model.puzzle_state import PuzzleState
from model import solver
from model import heuristic




# ------------------------------------------------------------
# Given states
# ------------------------------------------------------------

solvable_start_array = [[6, 1, 10, 2], [7, 11, 4, 14], [5, None, 9, 15], [8, 12, 13, 3]]
solvable_start_array_simple = [[1, 2, 3, 4], [5, 6, 11, 7], [9, 10, 15, None], [13, 14, 12, 8]]
solvable_start_array_max_depth = [[None, 12, 9, 13], [15, 11, 10, 14], [3, 7, 2, 5], [4, 8, 6, 1]]
unsolvable_start_array = [[13, 10, 11, 6], [5, 7, 4, 8], [1, 11, 14, 9], [3, 15, 2, None]]
final_array = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, None]]

solvable_start_array_lc_vertical = [[7, 9, 1, 8], [5, None, 2, 10], [3, 4, 11, 6], [15, 13, 14, 12]]
solvable_start_array_lc_horizontal = [[11, 10, None, 9], [12, 15, 3, 5], [13, 8, 2, 4], [1, 6, 7, 14]]


# ------------------------------------------------------------
# Solving thread
# ------------------------------------------------------------
def solve_puzzle():
    start_state = PuzzleState(solvable_start_array_simple)
    final_state = PuzzleState(final_array)
    lc_heuristic = heuristic.LinearConflict()
    ida_star_solver = solver.IDAStar()

    # print info
    print("start state:" + start_state.get_formatted_state())
    print("final state:" + final_state.get_formatted_state())
    print("inversions: " + str(start_state.get_inversion_count()))
    print("is_solvable: " + str(solver.Solver.is_solvable(start_state, final_state)))

    # start solving
    result = ida_star_solver.solve(start_state, final_state, lc_heuristic)
    if isinstance(result, solver.Node):
        print("Found solution:")
        print("cost=" + str(result.cost))
        print(result.get_formatted_solution())

    else:
        print("Didn't found solution until depth.")


# ------------------------------------------------------------
# Timer thread
# ------------------------------------------------------------
def start_timer(cancel_event):
    print()
    start_time = time.time()
    e_sec = 0
    e_min = 0
    e_hour = 0
    while not cancel_event.isSet():
        elapsed_time = int(time.time() - start_time)
        e_sec = int(elapsed_time % 60)
        e_min = int((elapsed_time / 60) % 60)
        e_hour = int((elapsed_time / (60 * 60)) % 60)
        print("Elapsed time: {0:0=2d}:{1:0=2d}:{2:0=2d}".format(e_hour, e_min, e_sec), end="\r")
        time.sleep(1)

    print("Elapsed time: {0:0=2d}:{1:0=2d}:{2:0=2d}".format(e_hour, e_min, e_sec))
    return


cancel_timer_event = threading.Event()
timer_thread = threading.Thread(name="timer_thread", target=start_timer, args=(cancel_timer_event,))


# ------------------------------------------------------------
# Start program
# ------------------------------------------------------------

try:
    timer_thread.start()
    solve_puzzle()
except (KeyboardInterrupt, SystemExit):
    # stop timer thread if system exits before done solving
    cancel_timer_event.set()
    print("Solving canceled")
    sys.exit()


# cancel timer after solve is finished
print("\nFinished")
cancel_timer_event.set()