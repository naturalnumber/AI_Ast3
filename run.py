from  objective_function import ObjectiveFunction
import algorithms

def get_stats(fun, algorithm, max_evals, num_runs):
    best_fit = fun.total_pieces
    worse_fit = 0
    average_fit = 0.0
    num_feasible = 0

    for i in range(num_runs):
        result = algorithm(fun, max_evals)
        if fun.check_constraints(result[0],result[1],result[2])==True:
            num_feasible+=1
        
        fitness = fun.evaluate(result[0],result[1],result[2])
        if fitness < best_fit:
            best_fit = fitness
        if fitness > worse_fit:
            worse_fit = fitness
        
        average_fit += fitness
    
    average_fit = average_fit/num_runs
        
    print("The %s algorithm returned %2d feasible solutions from %2d trials." %(algorithm.__name__, num_feasible, num_runs))
    print("The best found solution has a fitness of %2d." %(best_fit))
    print("The worse found solution has a fitness of %2d." %(worse_fit))
    print("The average fitness was %3.2f" %(average_fit))



if __name__ == '__main__':
     #import random_search
    #from algorithms import semi_random

    #define the problem (size, num of queens, num of rooks, num of bishops)
    fun = ObjectiveFunction(8,2,3,4)

    # set maximum number of evaluations
    max_evals = 100000

    #set algorithm
    #algorithm = algorithms.semi_random
    algorithm = algorithms.simulated_annealing

    # for a single run
    #result = algorithm(fun, max_evals)
    #print(fun.check_constraints(result[0],result[1],result[2]))
    #print(result)

    # to get some stats
    num_runs = 30
    get_stats(fun, algorithm, max_evals, num_runs)





