__all__ = ['NumericalSet']  # Specify the items to be exported

class NumericalSet:
    _instances: dict = {}

    def __new__(cls, gaps):
        gaps_frozenset = frozenset(gaps)
        if gaps_frozenset in cls._instances:
            return cls._instances[gaps_frozenset]
        instance = super(NumericalSet, cls).__new__(cls)
        cls._instances[gaps_frozenset] = instance
        return instance

    def __init__(self, gaps):
        """
        Initialize the numerical set with its gaps.

        Parameters:
        gaps (list of int): The gaps of the numerical set.
        """
        self._gaps = frozenset(gaps)
        self._frobenius_number = max(self._gaps) if self._gaps else -1

    @property
    def gaps(self):
        return self._gaps

    @property
    def frobenius_number(self):
        return self._frobenius_number
    
    def __str__(self):
        return f"NumericalSet(genus={len(self.gaps)})"

    def __repr__(self):
        return f"NumericalSet(genus={len(self.gaps)}, frobenius_number={self.frobenius_number})"
    
    def atom_monoid_gaps(self):
        """
        Compute the gaps of the atom monoid.

        Returns:
        set of int: The gaps of the atom monoid.
        """
        gaps_atom_monoid = set()
        gaps = self.gaps.copy()
        max_gap = max(gaps) if gaps else 0
        for x in range(max_gap + max_gap + 1):
            if any(x + t in gaps for t in range(max_gap + 1) if t not in gaps):
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
            gaps = self.gaps.copy()
            if not gaps:
                return []

            # Sort the set gaps
            gaps = sorted(gaps)

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

    def small_elements(self):
        """
        Compute the small elements of the numerical set.

        Returns:
        set of int: The small elements of the numerical set.
        """
        gaps = self.gaps.copy()
        if not gaps:
            return set()
        frobenius_number = max(gaps)
        small_elements = []
        for s in range(frobenius_number):
            if s not in gaps:
                small_elements.append(s)
        return small_elements
    
    def multiplicity(self):
        """
        Compute the multiplicity of the numerical semigroup.

        Returns:
        int: The multiplicity of the numerical semigroup.
        """
        small_elements = self.small_elements()
        if not small_elements:
            return 1
        nonzero = [element for element in small_elements if element !=0]
        return min(nonzero) if nonzero else self.frobenius_number + 1