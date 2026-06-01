"""
Tests for cached apery_set() and the early-exit _compute_kunz_coords
implementation on NumericalSemigroup.
"""

import pytest
from pocketpartition.core.numerical_semigroup import NumericalSemigroup
from pocketpartition.core.kunz import kunz_tuple
from pocketpartition.core.kunz._coords import _compute_kunz_coords


def S(*gens):
    return NumericalSemigroup(generators=set(gens))


class TestAperySetCache:

    def test_apery_set_returns_same_object_on_repeat(self):
        s = S(3, 4, 5)
        first = s.apery_set(3)
        second = s.apery_set(3)
        assert first is second  # lru_cache returns the exact same object

    def test_apery_set_correct_values_multiplicity_3(self):
        # <3,4,5>: Apery(3) = {0, 4, 5}
        s = S(3, 4, 5)
        assert s.apery_set(3) == {0, 4, 5}

    def test_apery_set_correct_values_multiplicity_4(self):
        # <4,5,6,7>: Apery(4) = {0, 5, 6, 7}
        s = S(4, 5, 6, 7)
        assert s.apery_set(4) == {0, 5, 6, 7}

    def test_apery_set_size_equals_n(self):
        for gens, n in [((3, 5), 3), ((4, 5, 6, 7), 4), ((2, 3), 2)]:
            s = S(*gens)
            assert len(s.apery_set(n)) == n

    def test_apery_set_different_n_cached_independently(self):
        s = S(3, 5)
        a3 = s.apery_set(3)
        a5 = s.apery_set(5)
        assert a3 is not a5
        # Call again — each should come from cache
        assert s.apery_set(3) is a3
        assert s.apery_set(5) is a5


class TestComputeKunzCoordsEarlyExit:

    def test_matches_known_multiplicity_3(self):
        s = S(3, 4, 5)
        assert _compute_kunz_coords(s) == (1, 1)

    def test_matches_known_multiplicity_4(self):
        s = S(4, 5, 6, 7)
        assert _compute_kunz_coords(s) == (1, 1, 1)

    def test_matches_known_multiplicity_2(self):
        s = S(2, 3)
        assert _compute_kunz_coords(s) == (1,)

    def test_matches_kunz_tuple_for_various_semigroups(self):
        cases = [
            (3, 5),
            (4, 6, 7),
            (5, 7, 8, 9),
            (6, 7, 8, 9, 11),
            (3, 7, 11),
        ]
        for gens in cases:
            s = S(*gens)
            assert _compute_kunz_coords(s) == kunz_tuple(s)

    def test_all_coords_positive(self):
        for gens in [(3, 5), (4, 6, 7), (5, 6, 7, 8, 9)]:
            s = S(*gens)
            assert all(c > 0 for c in _compute_kunz_coords(s))

    def test_length_is_multiplicity_minus_one(self):
        for gens in [(2, 3), (3, 4, 5), (4, 5, 6, 7), (5, 6, 7, 8, 9)]:
            s = S(*gens)
            assert len(_compute_kunz_coords(s)) == s.multiplicity() - 1

    def test_large_frobenius_small_multiplicity(self):
        # <2, 101>: gaps = {1, 3, 5, ..., 99}, frobenius = 99, multiplicity = 2
        # Apery(2) = {0, 101} -> coord for residue 1 = 101 // 2 = 50 (wait: 101 % 2 = 1)
        s = S(2, 101)
        coords = _compute_kunz_coords(s)
        assert len(coords) == 1
        assert coords[0] == 101 // 2  # = 50 (integer division)
