class Partition:
    def __init__(self, partition):
        """
        Initialize the Partition object with a given partition.

        Parameters:
        partition (list of int): A list representing the partition.

        Raises:
        ValueError: If the partition is not a list of positive integers in non-increasing order.
        """
        if not isinstance(partition, list):
            raise ValueError("Partition must be a list.")
        
        if not all(isinstance(x, int) and x > 0 for x in partition):
            raise ValueError("All elements of the partition must be positive integers.")
        
        if not all(partition[i] >= partition[i+1] for i in range(len(partition) - 1)):
            raise ValueError("Partition must be in non-increasing order.")
        
        self.partition = partition

    def conjugate(self):
        """
        Compute the conjugate partition of the partition.

        Returns:
        list of int: The conjugate partition of the partition.
        """
        return [sum(1 for p in self.partition if p > i) for i in range(max(self.partition))]
    
    def hook_lengths(self):
        """
        Compute the hook length of a cell in the partition.
        Returns:
        list of int: A list of hook lengths for each cell in the partition.
        """
        p = self.partition
        conj = self.conjugate()
        return [[p[i]-(i+1)+conj[j]-(j+1)+1 for j in range(p[i])] for i in range(len(p))]
    
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
                moves.append((1,0))
                current_col += 1
            
            # Move up until we reach a row that has boxes in the current column
            while current_row >= 0 and (current_col >= partition[current_row]):
                moves.append((0,1))
                current_row -= 1
        
        return moves
    
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
            if step == (0,1):
                gap_set.append(i)
            i += 1
        return gap_set
    
    def nongaps(self):
        gaps = self.gaps()
        frobenius_number = max(gaps)
        nongaps = []
        for s in range(frobenius_number):
            if s not in gaps:
                nongaps.append(s)
        return nongaps
    
    def atom_partition(self):
        """
        Returns the atom partition of the given partition.

        Returns:
            list: The atom partition.
        """
        hook_partition = self.hook_lengths()
        hookset = [hook for row in hook_partition for hook in row]
        if len(hookset) == 0:
            return []
        hookset.sort()
        current_step = 0
        partition = []
        current_row = 0

        while current_step <= max(hookset):
            for i in range(current_step, max(hookset) + 1):
                if i in hookset:
                    partition.append(current_row)
                    current_step = i + 1
                    break
                current_row += 1
        partition.sort(reverse=True)
        return partition

    def is_semigroup(self):
        return self.atom_partition() == self.partition