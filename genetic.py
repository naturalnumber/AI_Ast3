import math
from random import randint, random


class Solution:
    def __init__(self, fit, xs, ys, types):
        self.fit = fit
        self.xs = xs
        self.ys = ys
        self.types = types

    def __lt__(self, other) -> bool:
        return self.fit < other.fit

    def __le__(self, other) -> bool:
        return self.fit <= other.fit

    def __eq__(self, other) -> bool:
        return self.fit == other.fit

    def __ne__(self, other) -> bool:
        return self.fit != other.fit

    def __gt__(self, other) -> bool:
        return self.fit > other.fit

    def __ge__(self, other) -> bool:
        return self.fit >= other.fit

def make_random(fun, current_type):
    current_x = [0] * (fun.total_pieces)
    current_y = [0] * (fun.total_pieces)

    for i in range(fun.total_pieces):
        current_x[i] = randint(1, fun.size)
        current_y[i] = randint(1, fun.size)

    # creating the first solution again and again until we get a feasible one
    while not fun.check_constraints(current_x, current_y, current_type):
        for i in range(fun.total_pieces):
            current_x[i] = randint(1, fun.size)
            current_y[i] = randint(1, fun.size)

    return current_x, current_y


def genetic_search(fun, max_evals):
    def cross(mother, father):
        compare = 0.5
        if mother[0] < father[0]:
            compare -= (father[0] - mother[0])/fun.total_pieces/5
        else:
            compare += (mother[0] - father[0])/fun.total_pieces/5

        child_x = [0] * (fun.total_pieces)
        child_y = [0] * (fun.total_pieces)
        for i in range(fun.total_pieces):
            child_x = mother[1][i] if random() > compare else father[1][i]
            child_y = mother[2][i] if random() > compare else father[2][i]

        while not fun.check_constraints(current_x, current_y, mother[3]):
            for i in range(fun.total_pieces):
                child_x = mother[1][i] if random() > compare else father[1][i]
                child_y = mother[2][i] if random() > compare else father[2][i]

        child_fit = fun.evaluate(child_x, child_y, mother[3])

        return (child_fit, child_x, child_y, mother[3])

    def mutate(soln, param):
        mutant_x:list = soln[1].copy()
        mutant_y:list = soln[2].copy()

        for i in range(param):
            idx = randint(0, fun.total_pieces - 1)
            mutant_x[idx] = randint(1, fun.size)
            mutant_y[idx] = randint(1, fun.size)

        while not fun.check_constraints(current_x, current_y, soln[3]):
            for i in range(param):
                idx = randint(0, fun.total_pieces - 1)
                mutant_x[idx] = randint(1, fun.size)
                mutant_y[idx] = randint(1, fun.size)

        mutant_fit = fun.evaluate(mutant_x, mutant_y, soln[3])

        return (mutant_fit, mutant_x, mutant_y, soln[3])

    current_type = [0] * (fun.queens) + [1] * (fun.rooks) + [2] * (fun.bishops)

    population = []

    pop_size = 100

    for sol in range(pop_size):
        current_x, current_y = make_random(fun, current_type)
        current_fit = fun.evaluate(current_x, current_y, current_type)
        population.append((current_fit, current_x, current_y, current_type))

    new_population = []
    fun_evals = 0

    parents = []

    while fun_evals < max_evals:
        population.sort()
        parents.clear()
        new_population.clear()

        if population[0][0] <= 0:
            break

        for i in range(5):
            new_population.append(population[i])
            parents.append(population[i])

        for i in range(len(population)):
            candidate = population[i]
            prob = ((candidate[0] + 1)/(fun.total_pieces + 2))

            if prob**2 < random():
                parents.append(candidate)
                if prob < random():
                    population.append(candidate)

        while len(population) < pop_size:
            mother = parents[randint(0, len(population) - 1)]
            father = parents[randint(0, len(population) - 1)]

            child = cross(mother, father)

            if random() < 0.05:
                child = mutate(child, randint(1, 2))

            population.append(child)
        fun_evals += 1
    population.sort()

    return (population[0][1], population[0][2], population[0][3], population[0][0])
