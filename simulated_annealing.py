'''
function SIMULATED-ANNEALING( problem, schedule) return a solution state
input: problem, a problem
schedule, a mapping from time to temperature controls the probability of downward steps
local variables: current, a solution.
next, a solution.
T, current temperature (we can assume T≥0)
current  MAKE-NODE(problem.INITIAL-STATE)
for t  1 to ∞ do
T  schedule[t]
if T = 0 then return current
next  a randomly selected successor of current
∆E  next.VALUE – current.VALUE
if ∆E > 0 then current  next
else current  next only with probability e∆E /T
'''
import math
from random import randint, random


def simulated_annealing(fun, max_evals, schedule):
    current_x = [0] * (fun.total_pieces)
    current_y = [0] * (fun.total_pieces)
    current_type = [0] * (fun.queens) + [1] * (fun.rooks) + [2] * (fun.bishops)
    for i in range(fun.total_pieces):
        current_x[i] = randint(1, fun.size)
        current_y[i] = randint(1, fun.size)

    # creating the first solution again and again until we get a feasible one
    while not fun.check_constraints(current_x, current_y, current_type):
        for i in range(fun.total_pieces):
            current_x[i] = randint(1, fun.size)
            current_y[i] = randint(1, fun.size)

    current_fit = fun.evaluate(current_x, current_y, current_type)

    new_sol_x = current_x.copy()
    new_sol_y = current_y.copy()
    new_sol_type = [0] * (fun.queens) + [1] * (fun.rooks) + [2] * (fun.bishops)

    fun_evals = 1

    while fun_evals < max_evals:
        T = schedule.getT(fun_evals)

        if T == 0:
            break

        for i in range(fun.total_pieces):
            new_sol_x[i] = randint(1, fun.size)
            new_sol_y[i] = randint(1, fun.size)

        if fun.check_constraints(new_sol_x, new_sol_y, new_sol_type):
            fun_evals += 1
            new_fit = fun.evaluate(new_sol_x, new_sol_y, new_sol_type)

            dE = new_fit - current_fit

            if dE > 0 or math.exp(dE / T) > random():
                current_fit = new_fit
                current_x = new_sol_x.copy()
                current_y = new_sol_y.copy()
            else:
                new_sol_x = current_x.copy()
                new_sol_y = current_y.copy()

    return (current_x, current_y, current_type, current_fit)
