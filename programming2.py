from random import randint, shuffle, random

MAX_FITNESS = 28

def nonattacking(rep):
    '''Determine number of pairs of non-attacking queens'''
    pairs = 0
    for i in range(8):
        for j in range(i+1, 8):
            if not (rep[i] == rep[j] 
                or int(rep[i]) == ( int(rep[j]) + (i - j) )
                or int(rep[i]) == ( int(rep[j]) - (i - j) )
            ):
                pairs += 1
    return pairs
            
class Board:
    """Board class to represent the 8 queens has strings and determine fitness"""
    def __init__(self, rep):
        self.rep = rep
        self.fitness = nonattacking(self.rep)

def mutate(rep):
    """Mutate child string"""
    idx = randint(0,7)
    value = randint(1,8)
    rep = rep[:idx] + str(value) + rep[(idx+1):]
    return rep


def crossover(p1, p2, mutation_pct):
    """Crossover of two parent board reps"""

    """Crossover"""
    crossover_point = randint(1,7)
    child1 = p1[:crossover_point] + p2[crossover_point:]
    child2 = p2[:crossover_point] + p1[crossover_point:]

    """Mutate"""
    child1mut = random()
    child2mut = random()

    if child1mut < mutation_pct:
        child1 = mutate(child1)

    if child2mut < mutation_pct:
        child2 = mutate(child2)

    return Board(child1), Board(child2)

def generate_board():
    """Generate a possible representation of the 8 queens problem"""
    return Board(
        "".join([str(randint(1, 8)) for _ in range(8)])
    )

def GAQueens(population_size, num_iterations, mutation_pct = 0.01):
    population = [generate_board() for _ in range(population_size)]
    """Run through each generation"""
    for i in range(num_iterations):
        shuffle(population)
        half_pop = int(population_size/2)
        set1 = population[:half_pop]
        set2 = population[half_pop:]
        new_population = []
        '''Breeding stage'''
        for parent1, parent2 in zip(set1, set2):
            if parent1.fitness == MAX_FITNESS:
                print ("Solution found in {} iterations".format(i))
                return parent1.rep
            if parent2.fitness == MAX_FITNESS:
                print ("Solution found in {} iterations".format(i))
                return parent2.rep
            child1, child2 = crossover(parent1.rep, parent2.rep, mutation_pct)
            new_population.append(child1)
            new_population.append(child2)
        population = new_population
    return "No solution found in {} iterations".format(num_iterations)

if __name__ == '__main__':
    pop_size = [100, 250, 500, 1000]
    num_iterations = [1000]
    for size in pop_size:
        for iter in num_iterations:
            print ("Initial population size {}:".format(size))
            print ( GAQueens(size, iter) )