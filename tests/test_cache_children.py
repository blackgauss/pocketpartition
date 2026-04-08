"""
Tests for cached get_children() on NumericalSemigroup.
"""

from pocketpartition.core.numerical_semigroup import NumericalSemigroup
from pocketpartition import WithGenus, WithMaxGenus


def S(*gens):
    return NumericalSemigroup(generators=set(gens))


class TestGetChildrenCache:

    def test_returns_tuple(self):
        s = S(3, 4, 5)
        assert isinstance(s.get_children(), tuple)

    def test_same_object_returned_on_repeated_calls(self):
        s = S(3, 4, 5)
        first = s.get_children()
        second = s.get_children()
        assert first is second  # lru_cache returns the exact same object

    def test_children_are_numerical_semigroups(self):
        s = S(3, 4, 5)
        for child in s.get_children():
            assert isinstance(child, NumericalSemigroup)

    def test_children_genus_is_one_more(self):
        s = S(3, 4, 5)  # genus 2
        for child in s.get_children():
            assert child.genus == s.genus + 1

    def test_root_children_count(self):
        # The root is N itself (represented by NumericalSemigroup({1}), with gaps={}).
        # Its only child is the semigroup with gaps={1}: NumericalSemigroup({2,3}).
        root = NumericalSemigroup(generators={1})
        assert len(root.get_children()) == 1

    def test_cache_shared_across_two_references(self):
        # Singleton: two variable references to the same semigroup share cache
        a = S(3, 5)
        b = S(3, 5)
        assert a is b
        a.get_children()  # warm the cache
        assert b.get_children() is a.get_children()

    def test_no_duplicate_children(self):
        s = S(3, 5)
        children = s.get_children()
        # Every child should be distinct
        assert len(children) == len(set(children))

    def test_bfs_still_correct_after_caching(self):
        # WithGenus relies on get_children(); verify counts match Sloane A007323
        expected = {0: 1, 1: 1, 2: 2, 3: 4, 4: 7, 5: 12, 6: 23}
        for g, count in expected.items():
            result = list(WithGenus(g))
            assert len(result) == count, f"genus {g}: expected {count}, got {len(result)}"

    def test_with_max_genus_correctness(self):
        g = 5
        result = list(WithMaxGenus(g))
        assert all(s.genus <= g for s in result)
        # Total count for genus 0..5 = 1+1+2+4+7+12 = 27
        assert len(result) == 27

    def test_cache_across_bfs_calls(self):
        # Clear cache so we get deterministic hit/miss counts
        NumericalSemigroup.get_children.cache_clear()

        before = NumericalSemigroup.get_children.cache_info()
        warm_result = list(WithGenus(6))
        after_warm = NumericalSemigroup.get_children.cache_info()

        cached_result = list(WithGenus(6))
        after_cached = NumericalSemigroup.get_children.cache_info()

        assert len(warm_result) == 23
        assert len(cached_result) == 23
        # First traversal should have produced only misses
        assert after_warm.misses > before.misses
        assert after_warm.hits == before.hits
        # Second traversal should reuse every cached result (all hits, no new misses)
        assert after_cached.hits > after_warm.hits
        assert after_cached.misses == after_warm.misses
