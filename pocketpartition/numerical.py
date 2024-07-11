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

    def small_elements(self):
        """
        Compute the small elements of the numerical set.

        Returns:
        set of int: The small elements of the numerical set.
        """
        gaps = self.gaps
        frobenius_number = max(gaps)
        small_elements = []
        for s in range(frobenius_number):
            if s not in gaps:
                small_elements.append(s)
        return small_elements

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
    
    def multiplicity(self):
        """
        Compute the multiplicity of the numerical semigroup.

        Returns:
        int: The multiplicity of the numerical semigroup.
        """
        small_elements = self.small_elements()
        nonzero = [element for element in small_elements if element !=0]
        return min(nonzero) if nonzero else self.frobenius_number + 1

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
        multiplicity = self.multiplicity()
        
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

        aux.sort()
        gen = set(aux)
        
        def remove_sum_of_two_elements(A):
            to_remove = set()
            for x in A:
                for y in A:
                    if (x + y) in A:
                        to_remove.add(x+y)
                        break  # No need to check further once x is found to be removable
            A.difference_update(to_remove)
        
        remove_sum_of_two_elements(gen)
        min_gens = list(gen)
        min_gens.sort()
        return min_gens

    def _compute_generators_from_gaps(self):
        """
        Compute the generators of the numerical semigroup given its gaps.

        Returns:
        list of int: The generators of the numerical semigroup.
        """
        multiplicity = self.multiplicity()
        generators = [multiplicity]
        frobenius_number = max(self.gaps) if self.gaps else 0
        equiv_classes = [0]

        for i in range(multiplicity + 1, frobenius_number):
            if i not in self.gaps and i % multiplicity not in equiv_classes:
                generators.append(i)
                equiv_classes.append(i % multiplicity)
        
        for i in range(frobenius_number + 1, frobenius_number + 1 + multiplicity):
            if i % multiplicity not in equiv_classes:
                generators.append(i)
            if len(equiv_classes) == multiplicity:
                break

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
    
    def gap_poset(self):
        """
        Compute the poset of the gaps of the numerical semigroup.

        Returns:
        set of tuple: The poset of the gaps of the numerical semigroup.
        """
        gaps = self.gaps
        poset = [(y, x) for x in gaps for y in gaps if x <= y and (y - x) not in gaps]
        return poset
    
    def void_poset(self):
        """
        Compute the poset of the void of the numerical semigroup.
        
        Returns:
        set of tuple: The poset of the void of the numerical semigroup.
        """
        void = self.void()
        gaps = self.gaps
        poset = [(y, x) for x in void for y in void if x <= y and (y - x) not in gaps]
        return poset