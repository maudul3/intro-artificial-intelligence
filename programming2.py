from random import randint, shuffle, random
import matplotlib.pyplot as plt
from numpy import mean
from pathlib import Path

MAX_FITNESS = 28


def nonattacking(rep):
    """Determine number of pairs of non-attacking queens

    Inputs:
        rep (str): string representation of queens' positions

    Outputs:
        int: count of non-attacking queens
    """
    pairs = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if not (
                rep[i] == rep[j]
                or int(rep[i]) == (int(rep[j]) + (i - j))
                or int(rep[i]) == (int(rep[j]) - (i - j))
            ):
                pairs += 1
    return pairs


class Board:
    """Board class to represent the 8 queens has strings and determine fitness"""

    def __init__(self, rep):
        """Constructor

        Inputs:
            self: Board object itself
            rep (str): string representation of the queens' positions
        """
        self.rep = rep
        self.fitness = nonattacking(self.rep)


def mutate(rep):
    """Mutate child string by modifying a single position

    Inputs:
        rep (str): string representation of the queens' positions

    Outputs:
        (str): mutated representation of queens' positions
    """
    idx = randint(0, 7)
    value = randint(1, 8)
    rep = rep[:idx] + str(value) + rep[(idx + 1) :]
    return rep


def crossover(p1, p2, mutation_pct):
    """Crossover of two parent board reps

    Inputs:
        p1 (str): parent 1 representation of queens' positions
        p2 (str): parent 2 representation of queens' positions
        mutation_pct (float): likelihood of mutation of children

    Outputs:
        Board: child 1 of p1-p2 crossover
        Board: child 2 p1-p2 crossover
    """

    """Crossover"""
    crossover_point = randint(1, 7)
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
    """Generate a possible representation of the 8 queens problem

    Outputs:
        Board: Board representation of 8 queens problem
    """
    return Board("".join([str(randint(1, 8)) for _ in range(8)]))


def GAQueens(population_size, num_iterations, mutation_pct):
    """Runs an simulation of the GA queens problem via a genetic algorithm

    Inputs:
        population_size (int): size of initial population of boards
        num_iterations (int): number of generations in the simulation
        mutation_pct (float): mutation percentage likelihood in subsequent generation

    Outputs:
        tuple(str, int, list<float>):
            (
                representation of solution,
                number of generations to solution,
                average fitness for each generation
            )
    """
    population = [generate_board() for _ in range(population_size)]
    iterations = []
    average_fitness = []
    # Run through each generation
    for i in range(num_iterations):
        # Store data for plotting
        iterations.append(i)
        average_fitness.append(mean([x.fitness for x in population]))

        # Split the population for breeding
        shuffle(population)
        half_pop = int(population_size / 2)
        set1 = population[:half_pop]
        set2 = population[half_pop:]
        new_population = []
        if i % 15 == 0:
            print(set1[0].rep, set2[0].rep)
        # Breeding stage
        for parent1, parent2 in zip(set1, set2):
            if parent1.fitness == MAX_FITNESS:
                print("Solution found in {} iterations".format(i))
                return parent1.rep, iterations, average_fitness
            if parent2.fitness == MAX_FITNESS:
                print("Solution found in {} iterations".format(i))
                return parent2.rep, iterations, average_fitness
            child1, child2 = crossover(parent1.rep, parent2.rep, mutation_pct)
            new_population.append(child1)
            new_population.append(child2)
        population = new_population
    return (
        "No solution found in {} iterations".format(num_iterations),
        iterations,
        average_fitness,
    )


if __name__ == "__main__":
    pop_size = [100, 250, 500, 1000]
    mutation_pcts = [0.01, 0.001]
    max_num_generations = [2000]
    for size in pop_size:
        for pct in mutation_pcts:
            for gen in max_num_generations:
                print("Initial population size {} and mutation {}:".format(size, pct))
                final_solution, iterations, average_fitness = GAQueens(size, gen, pct)
                print(final_solution)
                plt.plot(iterations, average_fitness)
                plt.title("Population = {} and Mutation % = {}".format(size, pct))
                plt.xlabel("Generation #")
                plt.ylabel("Average fitness")
                plt.savefig(
                    Path().absolute()
                    / Path("prog2pop{}mutation{}.jpeg".format(size, pct))
                )
                plt.clf()
