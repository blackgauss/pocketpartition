def is_list_of_positive_integers(lst):
    if not isinstance(lst, list):
        raise ValueError("Input must be a list.")
    if not all(isinstance(x, int) and x > 0 for x in lst):
        raise ValueError("All elements of the list must be positive integers.")
    return True

def is_non_increasing(lst):
    if not all(lst[i] >= lst[i + 1] for i in range(len(lst) - 1)):
        raise ValueError("List must be in non-increasing order.")
    return True

def get_instance(cls, key):
    if key in cls._instances:
        return cls._instances[key]
    instance = super(cls, cls).__new__(cls)
    cls._instances[key] = instance
    return instance

def compute_conjugate(partition):
    return [sum(1 for p in partition if p > i) for i in range(max(partition))]

def compute_hook_lengths(partition, conjugate):
    return [[partition[i] - (i + 1) + conjugate[j] - (j + 1) + 1 for j in range(partition[i])] for i in range(len(partition))]

def compute_profile(partition):
    moves = []
    n = len(partition)
    max_width = partition[0]
    
    current_row = n - 1
    current_col = 0
    
    while current_row >= 0 and current_col < max_width:
        while current_col < partition[current_row]:
            moves.append((1, 0))
            current_col += 1
        
        while current_row >= 0 and (current_col >= partition[current_row]):
            moves.append((0, 1))
            current_row -= 1
    
    return moves

def remove_sum_of_two_elements(A):
    to_remove = set()
    Acopy = A.copy()
    for x in A:
        for y in A:
            if (x + y) in A:
                to_remove.add(x+y)
                # break  # No need to check further once x is found to be removable
    Acopy.difference_update(to_remove)
    return Acopy