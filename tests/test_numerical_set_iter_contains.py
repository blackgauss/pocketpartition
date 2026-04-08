"""
Tests for __contains__ and __iter__ on NumericalSet and NumericalSemigroup.
"""

from pocketpartition.core.numerical_set import NumericalSet
from pocketpartition.core.numerical_semigroup import NumericalSemigroup


def S(*gens):
    return NumericalSemigroup(generators=set(gens))


class TestNumericalSetContains:

    def test_gap_is_not_contained(self):
        ns = NumericalSet([1, 2, 4])
        for g in [1, 2, 4]:
            assert g not in ns

    def test_non_gap_leq_frobenius_is_contained(self):
        ns = NumericalSet([1, 2, 4])  # frobenius = 4
        for e in [0, 3]:
            assert e in ns

    def test_beyond_frobenius_always_contained(self):
        ns = NumericalSet([1, 2, 4])  # frobenius = 4
        for e in [5, 6, 100]:
            assert e in ns

    def test_negative_is_not_contained(self):
        ns = NumericalSet([1, 2, 4])
        for n in [-1, -5]:
            assert n not in ns

    def test_zero_always_contained(self):
        ns = NumericalSet([1, 2, 4])
        assert 0 in ns

    def test_empty_gaps_everything_non_negative_contained(self):
        ns = NumericalSet([])  # frobenius = -1
        assert 0 in ns
        assert 1 in ns
        assert 100 in ns
        assert -1 not in ns


class TestNumericalSemigroupContains:

    def test_generators_are_elements(self):
        s = S(3, 4, 5)
        for g in [3, 4, 5]:
            assert g in s

    def test_gaps_not_in_semigroup(self):
        s = S(3, 4, 5)  # gaps = {1, 2}
        assert 1 not in s
        assert 2 not in s

    def test_zero_always_in_semigroup(self):
        s = S(3, 4, 5)
        assert 0 in s

    def test_large_element_in_semigroup(self):
        s = S(3, 5)  # frobenius = 7
        assert 100 in s


class TestNumericalSetIter:

    def test_iter_yields_non_gaps_in_order(self):
        ns = NumericalSet([1, 2, 4])  # gaps={1,2,4}, frobenius=4
        elements = list(ns)
        assert elements == sorted(elements), "iter should be ascending"
        for g in [1, 2, 4]:
            assert g not in elements
        for e in [0, 3, 5]:
            assert e in elements

    def test_iter_includes_frobenius_plus_one(self):
        ns = NumericalSet([1, 2, 4])  # frobenius = 4; 5 must be yielded
        assert 5 in list(ns)

    def test_iter_empty_gaps(self):
        ns = NumericalSet([])  # frobenius = -1 -> range(1) = [0]
        assert list(ns) == [0]

    def test_iter_sorted_ascending(self):
        ns = NumericalSet([1, 3, 5, 7])
        elements = list(ns)
        assert elements == sorted(elements)

    def test_iter_no_duplicates(self):
        ns = NumericalSet([1, 2, 5])
        elements = list(ns)
        assert len(elements) == len(set(elements))


class TestNumericalSemigroupIter:

    def test_semigroup_iter_starts_with_zero(self):
        s = S(3, 4, 5)
        elements = list(s)
        assert elements[0] == 0

    def test_semigroup_iter_contains_multiplicity(self):
        s = S(3, 4, 5)  # multiplicity = 3
        assert 3 in list(s)

    def test_semigroup_iter_no_gaps(self):
        s = S(3, 5)  # gaps: 1,2,4,7 -> frobenius=7
        elements = set(s)
        assert not (elements & set(s.gaps))

    def test_semigroup_iter_ascending(self):
        s = S(3, 5)
        elements = list(s)
        assert elements == sorted(elements)

    def test_semigroup_iter_usable_in_for_loop(self):
        s = S(2, 3)  # gaps = {1}, frobenius = 1
        collected = [e for e in s]
        assert 1 not in collected
        assert 0 in collected
        assert 2 in collected
