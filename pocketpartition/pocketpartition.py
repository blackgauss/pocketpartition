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
    
    def partition(self):
            """
            Creates a partition based on a specific walk profile using the gaps attribute.

            The walk is defined as follows:
            - Start at 0.
            - If the current number is in gaps, move up (create a new row with the same length as the current row).
            - If the current number is not in gaps, move right (add one box to the current row).
            - Continue this process until reaching the maximum number in gaps.
            - Collect the lengths of each row at the end of the walk.
            
            The resulting partition is returned as a list of integers in non-increasing order.

            Returns:
            list: A partition [a1, a2, ..., an] in non-increasing order, representing the profile of the walk.
            """
            if not self.gaps:
                return []

            # Sort the set gaps
            gaps = sorted(self.gaps)

            # Initialize the current row and the partition list
            current_row_length = 0
            partition = []

            for i in range(gaps[-1] + 1):
                if i in gaps:
                    if current_row_length > 0:
                        partition.append(current_row_length)
                else:
                    current_row_length += 1  # Move right means incrementing the row length

            # Ensure the partition is in descending order
            partition.sort(reverse=True)

            return partition

class NumericalSemigroup(NumericalSet):
    def __init__(self, gaps=None, generators=None):
        """
        Initialize the numerical semigroup with its gaps or generators.

        Parameters:
        gaps (list of int): The gaps of the numerical semigroup.
        generators (list of int): The generators of the numerical semigroup.
        
        Raises:
        ValueError: If the atom monoid of the numerical set is not equal to the set itself.
        """
        if generators is not None:
            # If generators are provided, compute the gaps from the generators
            self.gaps = self._compute_gaps_from_generators(generators)
        else:
            super().__init__(gaps)
            if self.atom_monoid() != self.gaps:
                raise ValueError("The provided gaps do not form a numerical semigroup because the atom monoid is not equal to the set itself.")
        self.frobenius_number = max(self.gaps) if self.gaps else -1

    def _compute_gaps_from_generators(self, generators):
        """
        Compute the gaps of the numerical semigroup given its generators.

        Parameters:
        generators (list of int): The generators of the numerical semigroup.

        Returns:
        set of int: The gaps of the numerical semigroup.
        """
        # Compute the elements of the semigroup up to twice the maximum generator
        semigroup = set()
        # max_gen = max(generators)
        product_of_gens = 1
        for gen in generators:
            product_of_gens *= gen
        bound = product_of_gens
        for i in range(bound):
            for g in generators:
                if i - g in semigroup or i - g == 0:
                    semigroup.add(i)
                    break

        # Identify the gaps, excluding 0
        gaps = set(range(1, bound)) - semigroup
        return gaps

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

    def minimal_generating_set(self):
        """
        Compute the minimal generating set of the numerical semigroup.

        Returns:
        list of int: The minimal generating set of the numerical semigroup.
        
        The algorithm used here is based on the method described by Rosales and Vasco in their works on numerical semigroups.
        """
        generators = self._compute_generators_from_gaps()
        multiplicity = min(generators)
        
        if multiplicity == 1:
            return [1]
        elif multiplicity == 2:
            odd_gen = next(g for g in generators if g % 2 == 1)
            return [2, odd_gen]

        # Initial reduction based on congruence modulo multiplicity
        aux = [multiplicity]
        for i in range(1, multiplicity):
            g = next((g for g in generators if g % multiplicity == i), None)
            if g is not None:
                aux.append(g)

        gen = set(aux)
        
        # Remove non-irreducible elements
        def sumNS(A, B, max_value):
            R = set()
            for a in A:
                for b in B:
                    if a + b > max_value:
                        break
                    else:
                        R.add(a + b)
            return R

        ss = sumNS(gen, gen, max(gen))
        while ss:
            gen -= ss
            ss = sumNS(ss, gen, max(gen))
        
        return list(gen)

    def _compute_generators_from_gaps(self):
        """
        Compute the generators of the numerical semigroup given its gaps.

        Returns:
        list of int: The generators of the numerical semigroup.
        """
        generators = []
        max_gap = max(self.gaps) if self.gaps else 0

        for i in range(1, max_gap + 1):
            if i not in self.gaps:
                generators.append(i)
        
        return generators
    
    def void(self):
        """
        Compute the void of the numerical semigroup.

        Returns:
        set: The void of the numerical semigroup.
        """
        gaps = self.gaps
        F = max(gaps)
        void = [g for g in gaps if g in gaps and F-g in gaps]
        return void
    
    def void_poset(self):
        """
        Compute the poset of the void of the numerical semigroup.
        
        Returns:
        set of tuple: The poset of the void of the numerical semigroup.
        """
        void = self.void()
        gaps = self.gaps
        poset = [(y, x) for x in void for y in void if x < y and (y - x) not in gaps]
        return poset



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
                moves.append((1,0))
                current_col += 1
            
            # Move up until we reach a row that has boxes in the current column
            while current_row >= 0 and (current_col >= partition[current_row]):
                moves.append((0,1))
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
            if step == (0,1):
                gap_set.append(i)
            i += 1
        return gap_set
    
    def small_nongaps(self):
        gaps = self.gaps()
        frobenius_number = max(gaps)
        nongaps = []
        for s in range(frobenius_number):
            if s not in gaps:
                nongaps.append(s)
        return nongaps

    
    def flip_nongap(self, s):
        """
        Flip a non-gap element in the partition.

        Parameters:
        s (int): The element to flip.

        Returns:
        list of int: The new partition after flipping the element.

        Raises:
        ValueError: If s is a gap in the partition or if s is a negative integer.
        """
        gaps = self.gaps()
        if s in gaps:
            raise ValueError(f"Cannot flip a gap. {s} is a gap in the partition.")
        if s < 0:
            raise ValueError("Input must be a nonnegative integer.")
        new_gaps = gaps.copy()
        new_gaps.append(s)
        new_partition = NumericalSet(new_gaps).partition()
        return new_partition
    
    def flip_end(self, i):
        """
        Flips the ith partition by making a right step and an up step.

        Parameters:
        i (int): The index of the partition to flip.

        Returns:
        list of int: The flipped partition.

        Raises:
        ValueError: If partition[i - 1] == partition[i] or partition[i - 1] == 1.
        """
        partition = self.partition
        idx = i - 1
        if i > len(partition):
            raise ValueError(f"Partition only has {len(partition)} parts. Cannot flip part number {i}.")
        if i < 1:
            raise ValueError("Input must be a positive integer.")
        if partition[idx] == partition[idx+1]:
            raise ValueError("Invalid flip operation. There is not a part to flip.")
        if partition[idx] == 1:
            raise ValueError("Invalid flip operation. Cannot flip a part of size 1.")
        flipped_partition = []
        if i == 1:
            flipped_partition.append(partition[0] - 1)
            flipped_partition.extend(partition[1:])
            return flipped_partition
        else:
            for j in range((idx - 1) + 1):
                flipped_partition.append(partition[j] - 1)
            flipped_partition.append(partition[idx] - 1)
            flipped_partition.append(partition[idx] - 1)
            for j in range(idx+1, len(partition)):
                flipped_partition.append(partition[j])
            flipped_partition.sort(reverse=True)
            return flipped_partition