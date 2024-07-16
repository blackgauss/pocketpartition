__all__ = ['NumericalSemigroup']

from .numerical_set import NumericalSet
from collections import Counter
from ..utils.helpers import remove_sum_of_two_elements
from functools import lru_cache

class NumericalSemigroup(NumericalSet):
    _instances = {}

    def __new__(cls, gaps=None, generators=None):
        if generators is not None:
            gaps_frozenset = frozenset(cls._compute_gaps_from_generators(generators))
        else:
            gaps_frozenset = frozenset(gaps)
        
        if gaps_frozenset in cls._instances:
            return cls._instances[gaps_frozenset]
        
        instance = super(NumericalSemigroup, cls).__new__(cls, gaps=gaps_frozenset)
        cls._instances[gaps_frozenset] = instance
        return instance
    
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
            self._gaps = self._compute_gaps_from_generators(generators)
        else:
            super().__init__(gaps)
            gaps = self._gaps
            if self.atom_monoid_gaps() != gaps:
                raise ValueError("The provided gaps do not form a numerical semigroup because the atom monoid is not equal to the set itself.")
        
        self._frobenius_number = max(gaps) if gaps else -1

    def __str__(self):
        return f"NumericalSemigroup(genus={len(self.gaps)})"

    def __repr__(self):
        return f"NumericalSemigroup(genus={len(self.gaps)}, frobenius_number={self.frobenius_number})"

    @staticmethod
    def _compute_gaps_from_generators(generators):
        """
        Compute the gaps of the numerical semigroup given its generators.

        Parameters:
        generators (list of int): The generators of the numerical semigroup.

        Returns:
        set of int: The gaps of the numerical semigroup.
        """
        # Compute the elements of the semigroup up to twice the maximum generator
        semigroup = set()
        reduced_gens = remove_sum_of_two_elements(set(generators))
        product_of_gens = 1
        for gen in reduced_gens:
            product_of_gens *= gen
        bound = product_of_gens
        for i in range(bound):
            for g in reduced_gens:
                if i - g in semigroup or i - g == 0:
                    semigroup.add(i)
                    break

        # Identify the gaps, excluding 0
        gaps = set(range(1, bound)) - semigroup
        return gaps
    

    @lru_cache(maxsize=None)
    def apery_set(self, n):
        """
        Compute the Apéry set of the numerical set with respect to n.

        Parameters:
        n (int): The modulus for the Apéry set computation.

        Returns:
        set of int: The Apéry set with respect to n.
        """
        gaps = self.gaps.copy()
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a nonnegative integer")
        
        if n in self.atom_monoid_gaps():
            raise ValueError("n must not be in the gaps of the atom monoid")

        apery_set = set()
        for k in range(n):
            x = k
            while x in gaps:
                x += n
            apery_set.add(x)

        return apery_set

    @lru_cache(maxsize=None)
    def minimal_generating_set(self):
        """
        Compute the minimal generating set of the numerical semigroup.

        Returns:
        list of int: The minimal generating set of the numerical semigroup.
        
        The algorithm used here is based on the method described by Rosales and Vasco in their works on numerical semigroups.
        """
        generators = self._compute_generators_from_gaps()
        generators.sort()
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
        
        min_gens = list(remove_sum_of_two_elements(gen))
        min_gens.sort()
        return min_gens

    def _compute_generators_from_gaps(self):
        """
        Compute the generators of the numerical semigroup given its gaps.

        Returns:
        list of int: The generators of the numerical semigroup.
        """
        gaps = self.gaps.copy()
        multiplicity = self.multiplicity()
        generators = [multiplicity]
        frobenius_number = max(gaps) if gaps else 0
        equiv_classes = [0]

        for i in range(multiplicity + 1, frobenius_number):
            if i not in gaps and i % multiplicity not in equiv_classes:
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
        gaps = self.gaps.copy()
        F = max(gaps)
        void = [g for g in gaps if (g in gaps) and (F-g in gaps)]
        return void
    
    def gap_poset(self):
        """
        Compute the poset of the gaps of the numerical semigroup.

        Returns:
        set of tuple: The poset of the gaps of the numerical semigroup.
        """
        gaps = self.gaps.copy()
        gap_relations = [(y, x) for x in gaps for y in gaps if x <= y and (y - x) not in gaps]
        return (gaps, gap_relations)
    
    def void_poset(self):
        """
        Compute the poset of the void of the numerical semigroup.
        
        Returns:
        set of tuple: The poset of the void of the numerical semigroup.
        """
        void = self.void().copy()
        gaps = self.gaps.copy()
        void_relations = [(y, x) for x in void for y in void if x <= y and (y - x) not in gaps]
        return (void, void_relations)

    @lru_cache(maxsize=None)
    def effective_weight(self):
            """
            Calculates the effective weight of the numerical partition.

            The effective weight is the sum of the number of boxes above each minimal generating set element.

            Returns:
                int: The effective weight of the numerical partition.
            """
            gaps = self.gaps.copy()
            def boxes_above(s):
                above = []
                for gap in gaps:
                    if gap > s:
                        above.append(gap - s)
                return len(above)
            min_gens = self.minimal_generating_set()
            ewt = 0
            for gen in min_gens:
                ewt += boxes_above(gen)
            return ewt
    
    def pseudofrobenius_numbers(self):
            """
            Calculates the pseudofrobenius numbers
            Returns:
                A list of unique pseudofrobenius numbers.
            """
            hookset = []
            small_elements = self.small_elements()
            gaps = self.gaps.copy()
            for s in small_elements:
                for gap in gaps:
                    if gap > s:
                        hookset.append(gap - s)
            element_counts = Counter(hookset)
            unique_elements = [element for element, count in element_counts.items() if count == 1]
            return unique_elements
    
    def type(self):
        return len(self.pseudofrobenius_numbers())

    def remove_minimal_generator(self, n):
        """
        Remove a minimal generator from a numerical semigroup.

        Parameters:
        n (int): The minimal generator to remove.

        Returns:
        NumericalSemigroup: The resulting numerical semigroup after removal.
        """
        if not isinstance(n, int):
            raise ValueError("The first argument must be an integer.")

        msg = self.minimal_generating_set()

        if n not in msg:
            raise ValueError(f"{n} must be a minimal generator of the numerical semigroup.")
        
        gaps = list(self.gaps.copy())
        gaps.append(n)
        return NumericalSemigroup(gaps=gaps)

    def effective_generators(self):
        mingens = self.minimal_generating_set()
        frob = self.frobenius_number
        effective_gens = [egen for egen in mingens if egen > frob]
        return effective_gens
    
    def get_children(self):
        gaps = self.gaps.copy()
        effective_gens = self.effective_generators()
        children = [NumericalSemigroup(gaps=list(gaps) + [egen]) for egen in effective_gens]
        return children
    
    def get_parent(self):
        gaps = self.gaps.copy()
        gaps = set(gaps)
        gaps.remove(max(gaps))
        return NumericalSemigroup(gaps)

    def special_gaps(self):
        """
        compute the gaps that can be added to S and still have a numerical semigroup.
        Returns:
            A list of special gaps.
        """
        gaps = self.gaps.copy()
        f = self.frobenius_number
        pf = self.pseudofrobenius_numbers()
        sgaps = []
        for p in pf:
            mult = [p * i for i in range(2, (f // p) + 1)]
            if not any(m in gaps for m in mult):
                sgaps.append(p)
        return sgaps
    
    def add_specialgap(self, p):
        """
        Add a special gap to the numerical semigroup.
        """
        if p not in self.special_gaps():
            raise ValueError(f"{p} is not a special gap for the numerical semigroup.")
        gaps = self.gaps.copy()
        gaps = set(gaps)
        gaps.remove(p)
        return NumericalSemigroup(gaps=gaps)
    
    def get_frobchildren(self):
        good_specialgaps = [p for p in self.special_gaps() if p != self.frobenius_number]
        children = [self.add_specialgap(p) for p in good_specialgaps]
        return children