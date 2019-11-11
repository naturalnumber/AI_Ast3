import math
from random import randint, random

piece_map = {0:"Q", 1:"R", 2:"B"}

def boardString(fun, xs, ys, types):
    board = [["" for _ in range(fun.size)] for _ in range(fun.size)]

    for i in range(fun.total_pieces):
        board[ys[i]-1][xs[i]-1] += piece_map[types[i]]

    result = ""

    for i in range(fun.size):
        for j in range(fun.size):
            if board[i][j] == "":
                result += " _ "
            else:
                result += " "+board[i][j]+" "
        result += "\n"

    return result

def random_successor(fun, xs, ys, types, param):
    new_sol_x = [0] * (fun.total_pieces)
    new_sol_y = [0] * (fun.total_pieces)

    for i in range(fun.total_pieces):
        new_sol_x[i] = randint(1, fun.size)
        new_sol_y[i] = randint(1, fun.size)

    return new_sol_x, new_sol_y

def mutated_successor(fun, xs:list, ys:list, types, param):
    new_sol_x = xs.copy()
    new_sol_y = ys.copy()

    for i in range(param):
        idx = randint(0, fun.total_pieces - 1)
        new_sol_x[idx] = randint(1, fun.size)
        new_sol_y[idx] = randint(1, fun.size)

    return new_sol_x, new_sol_y


def random_search(fun, max_evals):
    best_fit = fun.total_pieces + 1

    new_sol_x = [0] * (fun.total_pieces)
    new_sol_y = [0] * (fun.total_pieces)
    new_sol_type = [0] * (fun.queens) + [1] * (fun.rooks) + [2] * (fun.bishops)
    fun_evals = 0

    while fun_evals < max_evals:
        for i in range(fun.total_pieces):
            new_sol_x[i] = randint(1, fun.size)
            new_sol_y[i] = randint(1, fun.size)

        if fun.check_constraints(new_sol_x, new_sol_y, new_sol_type):
            fun_evals += 1
            new_fit = fun.evaluate(new_sol_x, new_sol_y, new_sol_type)
            if new_fit < best_fit:
                best_fit = new_fit
                best_x = new_sol_x.copy()
                best_y = new_sol_y.copy()
                best_type = new_sol_type.copy()

    return (best_x, best_y, best_type, best_fit)


def semi_random(fun, max_evals):
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
    fun_evals = 1

    new_sol_x = current_x.copy()
    new_sol_y = current_y.copy()
    new_sol_type = [0] * (fun.queens) + [1] * (fun.rooks) + [2] * (fun.bishops)

    mutations = fun.total_pieces
    while fun_evals < max_evals:
        for i in range(mutations):
            idx = randint(0, fun.total_pieces - 1)
            new_sol_x[idx] = randint(1, fun.size)
            new_sol_y[idx] = randint(1, fun.size)

        if fun.check_constraints(new_sol_x, new_sol_y, new_sol_type):
            fun_evals += 1
            new_fit = fun.evaluate(new_sol_x, new_sol_y, new_sol_type)
            if new_fit < current_fit:
                current_fit = new_fit
                current_x = new_sol_x.copy()
                current_y = new_sol_y.copy()
            else:
                new_sol_x = current_x.copy()
                new_sol_y = current_y.copy()

            mutations = int(fun.total_pieces * (float(max_evals - fun_evals) / max_evals)) + 1

    return (current_x, current_y, current_type, current_fit)


def simulated_annealing(fun, max_evals):
    T0 = 1000000

    def schedule(i):
        return T0 * (0.9995 ** i)

    def pass_function(dE, T):
        try:
            p = math.exp(dE / T)
            r = random()
            #print(f"comparision: {dE} > 0 or {p} > {r}")

            return p > r
        except:
            #print(f"comparision error")
            return False


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
        T = schedule(fun_evals)

        #print(f"t = {fun_evals} T = {T}")

        if T < 1e-10 or current_fit == 0:
            break

        #for i in range(fun.total_pieces):
        #    new_sol_x[i] = randint(1, fun.size)
        #    new_sol_y[i] = randint(1, fun.size)

        idx = randint(0, fun.total_pieces - 1)
        new_sol_x[idx] = randint(1, fun.size)
        new_sol_y[idx] = randint(1, fun.size)

        if fun.check_constraints(new_sol_x, new_sol_y, new_sol_type):
            fun_evals += 1
            new_fit = fun.evaluate(new_sol_x, new_sol_y, new_sol_type)

            dE = current_fit - new_fit

            #print(f"current: {current_fit}; {current_x}; {current_y};")
            #print(boardString(fun, current_x, current_y, current_type))
            #print(f"new: {new_fit}; {new_sol_x}; {new_sol_y};")
            #print(boardString(fun, new_sol_x, new_sol_y, current_type))

            if dE > 0 or pass_function(dE, T):
                #print(f"current <-: {new_fit}; {new_sol_x}; {new_sol_y};")
                current_fit = new_fit
                current_x = new_sol_x.copy()
                current_y = new_sol_y.copy()
            else:
                new_sol_x = current_x.copy()
                new_sol_y = current_y.copy()

    return (current_x, current_y, current_type, current_fit)
