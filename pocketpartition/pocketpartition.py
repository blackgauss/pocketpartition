class NumericalSet:
    def __init__(self, gaps):
        """
        Initialize the numerical set with its gaps.

        Parameters:
        gaps (list of int): The gaps of the numerical set.
        """
        self.gaps = set(gaps)
        self.frobenius_number = max(self.gaps) if self.gaps else -1

    def atom_monoid(self):
        """
        Compute the gaps of the atom monoid.

        Returns:
        set of int: The gaps of the atom monoid.
        """
        gaps_atom_monoid = set()
        max_gap = max(self.gaps) if self.gaps else 0
        for x in range(max_gap + max_gap + 1):
            if any(x + t in self.gaps for t in range(max_gap + 1) if t not in self.gaps):
                gaps_atom_monoid.add(x)
        return gaps_atom_monoid

    def apery_set(self, n):
        """
        Compute the Apéry set of the numerical set with respect to n.

        Parameters:
        n (int): The modulus for the Apéry set computation.

        Returns:
        set of int: The Apéry set with respect to n.
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a nonnegative integer")
        
        if n in self.atom_monoid():
            raise ValueError("n must not be in the gaps of the atom monoid")

        apery_set = set()
        max_gap = max(self.gaps) if self.gaps else 0
        for k in range(n):
            x = k
            while x in self.gaps:
                x += n
            apery_set.add(x)

        return apery_set

class Partition:
    def __init__(self, partition):
        """
        Initialize the Partition object with a given partition.

        Parameters:
        partition (list of int): A list representing the partition.
        """
        self.partition = partition

    def conjugate(self):
        """
        Compute the conjugate partition of the partition.

        Returns:
        list of int: The conjugate partition of the partition.
        """
        return [sum(1 for p in self.partition if p > i) for i in range(max(self.partition))]
    
    def hook_lengths(self, i=None, j=None):
        """
        Compute the hook length of a cell in the partition.

        Parameters:
        i (int, optional): The row index of the cell. If None, compute hook lengths for all cells.
        j (int, optional): The column index of the cell. If None, compute hook lengths for all cells.

        Returns:
        int or list of int: The hook length of the cell if i and j are specified, 
                            or a list of all hook lengths if i and j are None.
        """
        if i is None and j is None:
            hook_lengths = []
            conjugate_partition = self.conjugate()
            for i in range(len(self.partition)):
                for j in range(len(conjugate_partition)):
                    hook_length = self.partition[i] + conjugate_partition[j] - i - j - 1
                    hook_lengths.append(hook_length)
            return hook_lengths
        elif i is not None and j is not None:
            return self.partition[i] + self.conjugate()[j] - i - j - 1
        else:
            raise ValueError("Both i and j must be specified or both must be None.")
    
    def profile(self):
        """
        Compute the profile of the partition as a series of moves (Right and Up).

        Returns:
        list of str: A list of moves representing the profile of the partition.
        """
        partition = self.partition
        moves = []
        n = len(partition)
        max_width = partition[0]
        
        # Start at the bottom-left corner
        current_row = n - 1
        current_col = 0
        
        while current_row >= 0 and current_col < max_width:
            # Move right until we reach the end of the row
            while current_col < partition[current_row]:
                moves.append("Right")
                current_col += 1
            
            # Move up until we reach a row that has boxes in the current column
            while current_row >= 0 and (current_col >= partition[current_row]):
                moves.append("Up")
                current_row -= 1
        
        return moves
    
    def hook_lengths(self, box=None):
        """
        Compute the hook lengths for the partition.

        Parameters:
        box (tuple of int, optional): The cell coordinates (i, j) to compute the hook length for. 
                                      If None, compute hook lengths for all cells.

        Returns:
        int or list of list of int: The hook length of the specified cell, or a matrix of hook lengths for all cells.
        """
        partition = self.partition
        n = len(partition)
        
        def get_hook_length(i, j):
            if i >= n or j >= partition[i]:
                raise ValueError(f"Box ({i}, {j}) is out of bounds for the given partition.")
            right = partition[i] - j - 1
            below = sum(1 for k in range(i + 1, n) if partition[k] > j)
            return right + below + 1
        
        if box:
            i, j = box
            return get_hook_length(i, j)
        
        hook_lengths = [[0] * partition[i] for i in range(n)]
        
        for i in range(n):
            for j in range(partition[i]):
                hook_lengths[i][j] = get_hook_length(i, j)
        
        return hook_lengths
    
    def gaps(self):
        """
        Compute the gaps in the profile of the partition.

        Returns:
        list of int: A list of gaps in the profile.
        """
        profile = self.profile()
        i = 0
        gap_set = []
        for step in profile:
            if step == "Up":
                gap_set.append(i)
            i += 1
        return gap_set
