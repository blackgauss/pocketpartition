"""
Tests for __hash__ and __eq__ on NumericalSet and NumericalSemigroup.
"""

import pytest
from functools import lru_cache
from pocketpartition.core.numerical_set import NumericalSet
from pocketpartition.core.numerical_semigroup import NumericalSemigroup


def S(*gens):
    return NumericalSemigroup(generators=set(gens))


class TestNumericalSetHash:

    def test_equal_gap_sets_are_equal(self):
        a = NumericalSet([1, 2, 3])
        b = NumericalSet([3, 1, 2])
        assert a == b

    def test_different_gap_sets_are_not_equal(self):
        a = NumericalSet([1, 2])
        b = NumericalSet([1, 3])
        assert a != b

    def test_hash_equal_objects_have_same_hash(self):
        a = NumericalSet([1, 2, 3])
        b = NumericalSet([1, 2, 3])
        assert hash(a) == hash(b)

    def test_usable_as_dict_key(self):
        ns = NumericalSet([1, 2])
        d = {ns: "hello"}
        assert d[ns] == "hello"

    def test_usable_in_set(self):
        a = NumericalSet([1, 2])
        b = NumericalSet([1, 2])
        assert len({a, b}) == 1

    def test_not_equal_to_non_numerical_set(self):
        ns = NumericalSet([1, 2])
        assert ns.__eq__("not a set") is NotImplemented


class TestNumericalSemigroupHash:

    def test_equal_semigroups_are_equal(self):
        assert S(3, 4, 5) == S(3, 4, 5)

    def test_different_semigroups_are_not_equal(self):
        assert S(3, 4, 5) != S(3, 5)

    def test_hash_equal_semigroups_same_hash(self):
        assert hash(S(3, 4, 5)) == hash(S(3, 4, 5))

    def test_singleton_is_same_object(self):
        # The singleton pattern means same gaps → same object
        assert S(3, 4, 5) is S(3, 4, 5)

    def test_usable_as_dict_key(self):
        s = S(3, 4, 5)
        d = {s: 42}
        assert d[s] == 42

    def test_usable_in_set(self):
        s1 = S(3, 4, 5)
        s2 = S(3, 4, 5)
        assert len({s1, s2}) == 1

    def test_different_semigroups_in_set(self):
        assert len({S(3, 4, 5), S(3, 5), S(2, 3)}) == 3

    def test_lru_cache_works_on_semigroup_argument(self):
        call_count = 0

        @lru_cache(maxsize=None)
        def expensive(s: NumericalSemigroup) -> int:
            nonlocal call_count
            call_count += 1
            return s.genus

        s = S(3, 4, 5)
        result1 = expensive(s)
        result2 = expensive(s)
        assert result1 == result2
        assert call_count == 1  # called only once

    def test_lru_cache_distinguishes_different_semigroups(self):
        @lru_cache(maxsize=None)
        def genus_cached(s: NumericalSemigroup) -> int:
            return s.genus

        assert genus_cached(S(3, 4, 5)) == 2
        assert genus_cached(S(3, 5)) == 4

    def test_gaps_is_frozenset_when_constructed_from_generators(self):
        s = S(3, 4, 5)
        assert isinstance(s._gaps, frozenset)

    def test_gaps_is_frozenset_when_constructed_from_gaps(self):
        s = NumericalSemigroup(gaps=[1, 2])
        assert isinstance(s._gaps, frozenset)
