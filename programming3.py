from random import random, randint, choice
import numpy as np
from itertools import permutations

NUM_ROWS_COLS = 10
POSSIBLE_ACTIONS = ['N', 'E', 'S', 'W', 'P']

def create_grid():
    return np.array([
            ['0' if random() < 0.5 else '1' for _ in range(10) ] 
            for _ in range(10)
        ])

def sense_state(current_row, current_col, grid):
    state = ""
    # Add current
    state += grid[current_row][current_col]
    
    # Add north
    if current_row - 1 >= 0:
        state += grid[current_row - 1][current_col]
    else:
        state += '2'
    # Add east
    if current_col + 1 < NUM_ROWS_COLS:
        state += grid[current_row][current_col + 1]
    else:
        state += '2'
    # Add south
    if current_row + 1 < NUM_ROWS_COLS:
        state += grid[current_row + 1][current_col]
    else:
        state += '2'
    # Add west
    if current_col - 1 >= 0:
        state += grid[current_row][current_col - 1]
    else:
        state += '2'
    
    return state

def initialize_q():
    '''
    STATES: CNESW (Current, North, East, South, West)
    STATE REP: {0: Empty, 1: Can, 2: Wall}
    ACTIONS: { N, E, S, W, P (Pick up)}

    Create a dictionary which maps states -> {actions: q-value}
    '''
    q = {}
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    for m in range(3):
                        for a in POSSIBLE_ACTIONS:
                            q[str(i) + str(j) + str(k) + str(l) + str(m) + a] = 0
    return q

def run_action(row,col,action, grid):
    reward = 0
    if action == 'N':
        if row - 1 >= 0:
            row = row - 1
        else:
            reward = -5
    elif action == 'S':
        if row + 1 < NUM_ROWS_COLS:
            row = row + 1
        else:
            reward = -5
    elif action == 'W':
        if col - 1 >= 0:
            col = col - 1
        else:
            reward = -5
    elif action == 'S':
        if col + 1 < NUM_ROWS_COLS:
            col = col + 1 
        else:
            reward = -5
    elif action == 'C':
        if grid[row][col] == 0:
            reward = -1
        elif grid[row][col] == 1:
            reward = 10
            grid[row][col] = 0

    return row,col,grid,reward

def max_key_value(keys, q):
    max_key = None
    max_value = -10000
    for key in keys:
        if q[key] > max_value:
            max_key = key
            max_value = q[key]
        action = max_key[-1] # pull action state-action key
    return action, q[max_key]

def q_learning(num_actions, q_matrix, epsilon, eta=0.2, gamma=0.9):
    grid = create_grid()
    row, col = randint(0, 9), randint(0, 9)
    total_reward = 0

    # Run initial state work outside loop for performance
    current_state = sense_state(row, col, grid)
    keys = [key for key in q_matrix.keys() if current_state in key]
    action, value = max_key_value(keys, q_matrix) 
    for _ in range(num_actions):
        # Determine are state-action keys for this state
        if random() < epsilon: # randomly choose action and ignore optimal
            action = choice(POSSIBLE_ACTIONS)
            
        prev_state_action = current_state + action
        row,col,grid,reward = run_action(row,col,action,grid)
        total_reward += reward

        # q-learning
        current_state = sense_state(row, col, grid)
        keys = [key for key in q_matrix.keys() if current_state in key]
        action, value = max_key_value(keys, q_matrix) 
        q_matrix[prev_state_action] += eta* (reward + gamma*value - q_matrix[prev_state_action] )
    return q_matrix, total_reward


            
if __name__ == '__main__':
    episodes = 5000
    actions = 200
    epsilon_start = 0.1
    epsilon = epsilon_start
    q_matrix = initialize_q()
    rewards = []
    for ep in range(episodes):
        if ep % 50 == 0:
            epsilon -= epsilon_start * (episodes / (ep + 1))
        q_matrix, total_reward = q_learning(actions, q_matrix, epsilon)
        rewards.append(total_reward)
    print (rewards)