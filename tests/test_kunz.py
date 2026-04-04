import pytest
from pocketpartition.core.numerical_semigroup import NumericalSemigroup
from pocketpartition.core.kunz import kunz_tuple, KunzPolyhedron


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def S(*generators):
    """Convenience: build a NumericalSemigroup from generators."""
    return NumericalSemigroup(generators=list(generators))


# ---------------------------------------------------------------------------
# kunz_tuple
# ---------------------------------------------------------------------------

class TestKunzTuple:

    def test_known_value_multiplicity_3(self):
        # S = <3, 4, 5>  gaps = {1, 2}  multiplicity = 3
        # Apery set w.r.t. 3: {0, 4, 5}  -> residues 1->4, 2->5
        # kunz tuple = (4//3, 5//3) = (1, 1)
        ns = S(3, 4, 5)
        assert kunz_tuple(ns) == (1, 1)

    def test_known_value_multiplicity_4(self):
        # S = <4, 5, 6, 7>  gaps = {1,2,3}  multiplicity = 4
        # Apery set w.r.t. 4: {0, 5, 6, 7}
        # residue 1->5 (5//4=1), residue 2->6 (6//4=1), residue 3->7 (7//4=1)
        ns = S(4, 5, 6, 7)
        assert kunz_tuple(ns) == (1, 1, 1)

    def test_length_is_multiplicity_minus_one(self):
        for gens, mult in [((3, 5), 3), ((4, 5, 6, 7), 4), ((5, 6, 7, 8, 9), 5)]:
            ns = S(*gens)
            kt = kunz_tuple(ns)
            assert len(kt) == mult - 1, f"Expected length {mult - 1}, got {len(kt)}"

    def test_all_entries_positive(self):
        # Every Kunz coordinate must be a positive integer
        for gens in [(3, 5), (4, 6, 7), (5, 7, 8, 9), (6, 7, 8, 9, 11)]:
            ns = S(*gens)
            kt = kunz_tuple(ns)
            assert all(x > 0 for x in kt), f"Non-positive entry in {kt}"

    def test_returns_tuple(self):
        ns = S(3, 5)
        assert isinstance(kunz_tuple(ns), tuple)

    def test_multiplicity_2(self):
        # S = <2, 3>  gaps = {1}  multiplicity = 2
        # Apery set w.r.t. 2: {0, 3}  -> residue 1 -> 3  -> 3//2 = 1
        ns = S(2, 3)
        assert kunz_tuple(ns) == (1,)

    def test_symmetric_semigroup(self):
        # S = <3, 5>  gaps = {1, 2, 4, 7}  multiplicity = 3
        # Apery set w.r.t. 3: {0, 10, 5}
        # residue 1 -> 10  (10//3 = 3), residue 2 -> 5  (5//3 = 1)
        # kunz tuple = (3, 1)
        ns = S(3, 5)
        assert kunz_tuple(ns) == (3, 1)

    def test_large_multiplicity(self):
        # Just ensure it runs without error for a larger multiplicity
        ns = S(7, 8, 9, 10, 11, 12, 13)
        kt = kunz_tuple(ns)
        assert len(kt) == 6


# ---------------------------------------------------------------------------
# KunzPolyhedron
# ---------------------------------------------------------------------------

class TestKunzPolyhedron:

    # --- construction ---

    def test_init_stores_m(self):
        kp = KunzPolyhedron(3)
        assert kp.m == 3

    def test_init_rejects_zero(self):
        with pytest.raises(ValueError):
            KunzPolyhedron(0)

    def test_init_rejects_negative(self):
        with pytest.raises(ValueError):
            KunzPolyhedron(-5)

    def test_corner_length(self):
        for m in range(2, 8):
            kp = KunzPolyhedron(m)
            assert len(kp.corner) == m

    def test_corner_values(self):
        kp = KunzPolyhedron(4)
        assert kp.corner == (0.0, 0.25, 0.5, 0.75)

    # --- is_point: valid semigroup Kunz tuples ---

    def test_is_point_accepts_valid_kunz_tuple(self):
        # Every actual Kunz coordinate vector of a semigroup must be a valid point
        for gens in [(3, 5), (3, 4, 5), (4, 5, 6, 7), (5, 6, 7, 8, 9)]:
            ns = S(*gens)
            m = ns.multiplicity()
            kt = kunz_tuple(ns)
            kp = KunzPolyhedron(m)
            assert kp.is_point(kt), f"Valid kunz tuple {kt} rejected for m={m}"

    def test_is_point_multiplicity_3_simple(self):
        kp = KunzPolyhedron(3)
        # (1, 1) is the kunz tuple of <3,4,5>
        # Residues 1-indexed: i=1,j=1 -> s=2 < 3: c1+c1=2 >= c2=1 ✓
        #                      i=1,j=2 -> s=3 == m: always ok ✓
        #                      i=2,j=2 -> s=4 > 3: c2+c2+1=3 >= c1=1 ✓
        assert kp.is_point((1, 1)) is True

    def test_is_point_multiplicity_3_another(self):
        kp = KunzPolyhedron(3)
        # (1, 2): i=1,j=1 -> 1+1=2 >= c2=2 ✓; i=1,j=2 -> s=3==m ok ✓
        #         i=2,j=2 -> s=4>3: 2+2+1=5 >= c1=1 ✓
        assert kp.is_point((1, 2)) is True

    # --- is_point: invalid points ---

    def test_is_point_rejects_negative_entry(self):
        kp = KunzPolyhedron(3)
        assert kp.is_point((-1, 1)) is False

    def test_is_point_rejects_zero_entry(self):
        kp = KunzPolyhedron(3)
        # (0, 0): i=1,j=1 -> s=2 < 3: c1+c1=0 >= c2=0 ✓
        # but i=1,j=2 -> s=3==m ok; i=2,j=2 -> s=4>3: c2+c2+1=1 >= c1=0 ✓
        # Actually (0,0) satisfies the inequalities — it's the corner of the polyhedron.
        # The polyhedron itself allows 0 coords; only real semigroup kunz tuples are >= 1.
        # Test a point that truly violates: (0, 2) -> i=1,j=1: 0+0=0 < c2=2 -> False
        assert kp.is_point((0, 2)) is False

    def test_is_point_rejects_violated_inequality(self):
        # Construct a point that violates p[i] + p[j] >= p[i+j] for i+j < m
        # m=3, try (2, 1): i=0,j=0 -> p[0]+p[0]=4 >= p[0]=2 ✓
        #                   i=0,j=1 -> p[0]+p[1]=3 >= p[1]=1 ✓ (i+j=1 < 3)
        # Actually that passes — use a clearly bad case:
        # m=4, try p=(3,1,1): i=0,j=0 -> 6 >= p[0]=3 ✓
        #                      i=0,j=1 -> i+j=1 < 4: 3+1=4 >= p[1]=1 ✓
        # Need i+j < m case failure: p[i]+p[j] < p[i+j]
        # m=4, p=(1,1,5): i=0,j=0->p[0]+p[0]=2>=p[0]=1✓; i=0,j=1->2>=1✓
        #                  i=0,j=2->i+j=2<4: p[0]+p[2]=6>=p[2]=5✓
        #                  i=1,j=1->i+j=2<4: 1+1=2 >= p[2]=5? NO -> False
        kp = KunzPolyhedron(4)
        assert kp.is_point((1, 1, 5)) is False

    # --- round-trip: every semigroup's kunz tuple is a valid polyhedron point ---

    def test_round_trip_multiple_semigroups(self):
        # Every kunz tuple produced by a real semigroup must satisfy the polyhedron
        test_cases = [
            (2, 3),
            (3, 4, 5),
            (3, 5),
            (4, 5, 6, 7),
            (4, 6, 7),
            (5, 6, 7, 8, 9),
            (6, 7, 8, 9, 10, 11),
        ]
        for gens in test_cases:
            ns = S(*gens)
            m = ns.multiplicity()
            kt = kunz_tuple(ns)
            kp = KunzPolyhedron(m)
            assert kp.is_point(kt), (
                f"Round-trip failed: semigroup <{', '.join(map(str,gens))}> "
                f"gave kunz tuple {kt} which KunzPolyhedron({m}).is_point rejected"
            )
