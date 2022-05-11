

from random import randint


def nonattacking(rep):
    '''Determine number of pairs of non-attacking queens'''
    pairs = 0
    for i in range(8):
        for j in range(i+1, 8):
            if not (rep[i] == rep[j] 
            or int(rep[i]) == int(rep[j]) + (i - j)
            or int(rep[j]) == int(rep[j]) - (i - j)):
                pairs += 1
    return pairs
            
class Board:
    def __init__(self, rep):
        self.rep = rep
        self.fitness = nonattacking(self.rep)

def generate_board():
    """Generate a possible representation of the 8 queens problem"""
    return Board(
        "".join([str(randint(1, 8)) for _ in range(8)])
    )

def GAQueens(population_size, num_iterations):
    initial_population = [generate_board() for _ in range(population_size)]

if __name__ == '__main__':
    pop_size = [100]
    num_iterations = [10]
    for size in pop_size:
        for iter in num_iterations:
            GAQueens(size, iter)