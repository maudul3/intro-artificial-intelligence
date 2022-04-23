from random import randint, choice, uniform

def initialize_grid(dirty_squares=1):
    '''Create a 3x3 grid with a certain amount of dirty spaces'''
    '''0 == dirty and 1 == clean, for easy performance evaluation'''
    grid = [[1 for _ in range(3)] for _ in range(3)]
    while dirty_squares:
        i, j = randint(0,2), randint(0,2)
        if grid[i][j] == 1:
            grid[i][j] = 0
            dirty_squares -= 1
    return grid

def simple_reflex(grid):
    i, j = randint(0,2), randint(0,2)
    steps = 0
    '''Simple reflex movements'''
    for _ in range(1000):
        steps += 1
        # Suck case
        if grid[i][j] == 0:
            grid[i][j] = 1
        # Move case
        else:
            if i == 1 and j == 1:
                j = 0
            elif i == 0 and j < 2:
                j += 1
            elif i < 2 and j == 2:
                i += 1
            elif i == 2 and j > 0:
                j -= 1
            else:
                i -= 1
        performance_measure = sum((sum(row) for row in grid))
        if performance_measure == 9:
            return steps
    return steps

def simple_reflex_murphy(grid):
    i, j = randint(0,2), randint(0,2)
    steps = 0
    '''Simple reflex movements'''
    for _ in range(1000):
        steps += 1
        correct_reading = uniform(0, 1)
        proper_action = uniform(0,1)
        # Suck case
        if (
            (grid[i][j] == 0 and correct_reading > 0.1) 
            or (grid[i][j] == 1 and correct_reading <= 0.1)
          ):
            if proper_action > 0.25:
                grid[i][j] = 1
            else:
                grid[i][j] = 0
        # Move case
        elif (
            (grid[i][j] == 1 and correct_reading > 0.1) 
            or (grid[i][j] == 0 and correct_reading <= 0.1)
          ):
            if i == 1 and j == 1:
                j = 0
            elif i == 0 and j < 2:
                j += 1
            elif i < 2 and j == 2:
                i += 1
            elif i == 2 and j > 0:
                j -= 1
            else:
                i -= 1
        performance_measure = sum((sum(row) for row in grid))
        if performance_measure == 9:
            return steps
    return steps

def next_position(i, j, movement):
    if movement == 'up':
        i -= 1
    elif movement == 'down':
        i += 1
    elif movement == 'left':
        j -= 1
    elif movement == 'right':
        j += 1
    return i,j

def random_reflex(grid):
    i, j = randint(0,2), randint(0,2)
    steps = 0
    '''Simple reflex movements'''
    for _ in range(1000):
        steps += 1
        # Suck case
        next_choice = choice(['suck','move'])
        if next_choice == 'suck':
            grid[i][j] = 1
        # Move case
        else:
            if i == 0 and j == 0:
                movement = choice(['right', 'down'])
            elif i == 0 and j == 1:
                movement = choice(['right', 'down', 'left'])
            elif i == 0 and j == 2:
                movement = choice(['left', 'down'])
            elif i == 1 and j == 0:
                movement = choice(['right', 'down', 'up']) 
            elif i == 1 and j == 1:
                movement = choice(['right', 'left', 'down', 'up']) 
            elif i == 1 and j == 2:
                movement = choice(['left', 'down', 'up'])
            elif i == 2 and j == 0:
                movement = choice(['up', 'right'])
            elif i == 2 and j == 1:
                movement = choice(['up','left','right'])
            elif i == 2 and j == 2:
                movement = choice(['left','up'])
            i, j = next_position(i, j, movement)

        performance_measure = sum((sum(row) for row in grid))
        if performance_measure == 9:
            return steps
    return steps

def random_reflex_murphy(grid):
    i, j = randint(0,2), randint(0,2)
    steps = 0
    proper_action = uniform(0,1)
    '''Simple reflex movements'''
    for _ in range(1000):
        steps += 1
        # Suck case
        next_choice = choice(['suck','move'])
        if (
          (next_choice == 'suck')
        ):
            if (proper_action > 0.25):
                grid[i][j] = 1
            else:
                grid[i][j] = 0
        # Move case
        else:
            if i == 0 and j == 0:
                movement = choice(['right', 'down'])
            elif i == 0 and j == 1:
                movement = choice(['right', 'down', 'left'])
            elif i == 0 and j == 2:
                movement = choice(['left', 'down'])
            elif i == 1 and j == 0:
                movement = choice(['right', 'down', 'up']) 
            elif i == 1 and j == 1:
                movement = choice(['right', 'left', 'down', 'up']) 
            elif i == 1 and j == 2:
                movement = choice(['left', 'down', 'up'])
            elif i == 2 and j == 0:
                movement = choice(['up', 'right'])
            elif i == 2 and j == 1:
                movement = choice(['up','left','right'])
            elif i == 2 and j == 2:
                movement = choice(['left','up'])
            i, j = next_position(i, j, movement)

        performance_measure = sum((sum(row) for row in grid))
        if performance_measure == 9:
            return steps
    return steps
        
    
if __name__ == '__main__':
    experiments = 200
    simple_1 = simple_3 = simple_5 = 0
    random_1= random_3= random_5 = 0
    simple_murphy_1= simple_murphy_3= simple_murphy_5 = 0
    random_murphy_1= random_murphy_3= random_murphy_5 = 0
    for _ in range(experiments):
        '''Simple'''
        grid1 = initialize_grid(1)
        grid3 = initialize_grid(3)
        grid5 = initialize_grid(5) 
        simple_1 += simple_reflex(grid1)
        simple_3 += simple_reflex(grid3)
        simple_5 += simple_reflex(grid5)
        '''Random'''
        grid1 = initialize_grid(1)
        grid3 = initialize_grid(3)
        grid5 = initialize_grid(5) 
        random_1 += random_reflex(grid1)
        random_3 += random_reflex(grid3)
        random_5 += random_reflex(grid5)
        '''Simple Murphy's Law'''
        grid1 = initialize_grid(1)
        grid3 = initialize_grid(3)
        grid5 = initialize_grid(5) 
        simple_murphy_1 += simple_reflex_murphy(grid1)
        simple_murphy_3 += simple_reflex_murphy(grid3)
        simple_murphy_5 += simple_reflex_murphy(grid5)
        '''Random Murphy's Law'''
        grid1 = initialize_grid(1)
        grid3 = initialize_grid(3)
        grid5 = initialize_grid(5) 
        random_murphy_1 += random_reflex_murphy(grid1)
        random_murphy_3 += random_reflex_murphy(grid3)
        random_murphy_5 += random_reflex_murphy(grid5)
    
    print (simple_1/experiments, simple_3/experiments, simple_5/experiments)
    print (random_1/experiments, random_3/experiments, random_5/experiments)
    print (simple_murphy_1/experiments, simple_murphy_3/experiments, simple_murphy_5/experiments)
    print (random_murphy_1/experiments, random_murphy_3/experiments, random_murphy_5/experiments)

