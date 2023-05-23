from fileinput import close
from numpy import sqrt

"""Dictionary that tracks which indices can be swapped in 8 puzzle """
blank_index_to_swap_indices = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7]
}

def swap(state, idx1, idx2):
    """Helper function used to swap blanks and adjacent squares
    
    Inputs:
        state (list<str>): state space of 8 puzzle
        idx1 (int): first index to swap 
        idx2 (int): second index to swap

    Outputs:
        list<str>: state space of 8 puzzle after swapping 
    """
    state_copy = list(state)
    state_copy[idx1] = state[idx2]
    state_copy[idx2] = state[idx1]
    return state_copy

def next_states(state):
    """Determine next possible configurations of the 8 puzzle
    
    Inputs:
      state (list<str>): state space of 8 puzzle 
    
    Outputs:
        list<list<str>>: all possible next configurations of 8 puzzle
    """
    blank_idx = state.index('b')
    swap_indices = blank_index_to_swap_indices[blank_idx]
    return [swap(state, blank_idx, swap_idx) for swap_idx in swap_indices]

def misplaced_tiles(state1, state2):
    """Determine the number of misplaced tiles betwen state spaces
    
    Inputs:
      state1 (list<str>): state space of 8 puzzle
      state2 (list<str): state space of 8 puzzle
    
    Outputs:
        int: count of misplaced tiles
    """
    return sum( 1 if v1 != v2 else 0 for v1, v2 in zip(state1, state2) )

def manhattan_distance(state1, state2):
    """Implementation of manhattan distance

    Inputs:
      state1 (list<str>): state space of 8 puzzle
      state2 (list<str): state space of 8 puzzle
    
    Outputs:
        int: mahattan distance 
    """
    matrix1 = [
        [state1[0], state1[1], state1[2]],
        [state1[3], state1[4], state1[5]],
        [state1[6], state1[7], state1[8]] 
    ]
    matrix2 = [
        [state2[0], state2[1], state2[2]],
        [state2[3], state2[4], state2[5]],
        [state2[6], state2[7], state2[8]] 
    ]
    distance = 0
    for i in range(0, 3):
        for j in range(0, 3):
            value = matrix1[i][j]
            for k in range(0, 3):
                for l in range(0,3):
                    if matrix2[k][l] == value:
                        distance += abs(i-k) + abs(j-l)
                        break
                if matrix2[k][l] == value:
                    break
    return distance

def euclidean_distance(state1, state2):
    """Implementation of euclidean distance. 
    
    Inputs:
      state1 (list<str>): state space of 8 puzzle
      state2 (list<str): state space of 8 puzzle
    
    Outputs:
        int: euclidean distance 
    """
    matrix1 = [
        [state1[0], state1[1], state1[2]],
        [state1[3], state1[4], state1[5]],
        [state1[6], state1[7], state1[8]] 
    ]
    matrix2 = [
        [state2[0], state2[1], state2[2]],
        [state2[3], state2[4], state2[5]],
        [state2[6], state2[7], state2[8]] 
    ]
    distance = 0
    for i in range(0, 3):
        for j in range(0, 3):
            value = matrix1[i][j]
            for k in range(0, 3):
                for l in range(0,3):
                    if matrix2[k][l] == value:
                        distance += sqrt( (i-k)**2 + abs(j-l)**2 )
                        break
                if matrix2[k][l] == value:
                    break
    return distance

class Node:
    """Node class"""
    def __init__(
        self, 
        state,
        parent=None,
        depth=0
    ) -> None:
        """Constructor

        Inputs:
            self: object itself
            state (list<str>): state space of current 8 puzzle
            parent (list<str>): parent state space of current 8 puzzle
            depth (int): number of expansions to complete
        """
        self.state = state
        self.parent = parent
        self.possible_children = next_states(self.state)
        self.depth = depth

def best_first(
    root, 
    goal: list[str], 
    heuristic_function, 
    search_type: str, 
    terminate_at=1000
):
    """Implementation of the best first algorithm
    
    Inputs:
        goal (list<str>): goal configuration of 8 puzzle
        heuristic_function ( f(str) ): heuristic function for evaluation of optimal state
        search_type (str): type of search algorithm to use
        terminate: maximum number of expansions 

    Return:
      list<list<str>>: state spaces needed to go from initial -> final
    """
    count = 0
    closed_set = set()
    open_queue = [root]
    node = None

    """Identify different heuristic functions based on algorithm"""
    if search_type == 'greedy':
        sorting_helper = lambda y: heuristic_function(goal, y.state)
    elif search_type == 'a*':
        sorting_helper = lambda y: heuristic_function(goal, y.state) + y.depth
    
    """Loop through nodes available for expansion"""
    while open_queue and count < terminate_at:
        node = open_queue.pop(0)
        closed_set.add("".join(node.state))
        if node.state == goal:
            break
        open_queue.extend([ 
        Node(child_state, node, node.depth + 1) 
        for child_state in node.possible_children
        if "".join(child_state) not in closed_set
        ]) 
        open_queue = sorted(open_queue, key=sorting_helper)
        count += 1
    
    if node.state != goal:
        print ("Solution not found in {} expansions".format(terminate_at))
        return -1

    """Determine solution path and return average number of steps"""
    solution_steps = 0
    path = []
    while (node):
        path.append(" ".join(node.state))
        node = node.parent
        solution_steps += 1
        
    path.reverse()
    print (" -> ".join(path))
    return solution_steps

if __name__ == '__main__':
    g = ['1','2','3','4','5','6','7','8','b']
    r1 = Node(['1','5', '2','4','b','3','7','8','6'])
    r2 = Node(['4', '1', '3', 'b', '8', '5', '2', '7', '6'])
    r3 = Node(['2', '3', '5', '1', '4', '6', '7', 'b', '8'])
    r4 = Node('4 8 2 1 6 5 b 7 3'.split(" "))
    r5 = Node("3 2 1 7 8 b 6 5 4".split(" "))
    r = [r1, r2, r3, r4, r5]
    heuristics = [manhattan_distance, euclidean_distance, misplaced_tiles]
    searches = ['greedy', 'a*']

    for i, ri in enumerate(r):
        for search in searches:
            for heuristic in heuristics:
                print (
                    "Steps in {} via {} search and {} heuristic: ".format(
                        " ".join(ri.state),
                        search,
                        heuristic.__name__
                    )
                )
                print (
                    best_first(
                        ri, g, heuristic, search, terminate_at=100000
                    )
                )