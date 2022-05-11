def GAQueens(population_size, num_iterations):
    return 1

if __name__ == '__main__':
    pop_size = [100]
    num_iterations = [10]
    for size in pop_size:
        for iter in num_iterations:
            GAQueens(size, iter)