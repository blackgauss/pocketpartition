import pytest
import math
from pocketpartition.core.numerical_semigroup import NumericalSemigroup
from pocketpartition.core.kunz import kunz_tuple, KunzVector, FourierKunzVector, KunzPolyhedron, kunz_distance


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


# ---------------------------------------------------------------------------
# KunzVector
# ---------------------------------------------------------------------------

class TestKunzVector:

    def test_is_tuple_subclass(self):
        kv = KunzVector(S(3, 4, 5))
        assert isinstance(kv, tuple)

    def test_coords_match_kunz_tuple(self):
        for gens in [(2, 3), (3, 4, 5), (3, 5), (4, 6, 7)]:
            ns = S(*gens)
            kv = KunzVector(ns)
            assert tuple(kv) == kunz_tuple(ns)

    def test_semigroup_property(self):
        ns = S(3, 4, 5)
        kv = KunzVector(ns)
        assert kv.semigroup is ns

    def test_multiplicity_property(self):
        ns = S(4, 5, 6, 7)
        kv = KunzVector(ns)
        assert kv.multiplicity == 4

    def test_genus_property(self):
        ns = S(3, 5)
        kv = KunzVector(ns)
        assert kv.genus == ns.genus

    def test_frobenius_property(self):
        ns = S(3, 5)
        kv = KunzVector(ns)
        assert kv.frobenius_number == ns.frobenius_number

    def test_coord_1indexed(self):
        # <3,4,5>: kunz tuple (1,1), so coord(1)=1, coord(2)=1
        ns = S(3, 4, 5)
        kv = KunzVector(ns)
        assert kv.coord(1) == kv[0]
        assert kv.coord(2) == kv[1]

    def test_coord_out_of_range(self):
        kv = KunzVector(S(3, 4, 5))
        with pytest.raises(IndexError):
            kv.coord(0)
        with pytest.raises(IndexError):
            kv.coord(3)   # m-1 = 2 is the max valid index

    def test_repr_contains_multiplicity(self):
        kv = KunzVector(S(3, 4, 5))
        assert "m=3" in repr(kv)

    def test_construct_from_semigroup_with_generators(self):
        kv = KunzVector(NumericalSemigroup(generators=[5, 6, 7, 8, 9]))
        assert len(kv) == 4   # m=5, length=4

    def test_immutable(self):
        kv = KunzVector(S(3, 4, 5))
        with pytest.raises((TypeError, AttributeError)):
            kv[0] = 99


# ---------------------------------------------------------------------------
# FourierKunzVector
# ---------------------------------------------------------------------------

class TestFourierKunzVector:

    def _fkv(self, *gens):
        return FourierKunzVector(S(*gens))

    # --- construction ---

    def test_construct_from_semigroup(self):
        fkv = FourierKunzVector(S(3, 4, 5))
        assert isinstance(fkv, FourierKunzVector)

    def test_construct_from_kunz_vector(self):
        kv = KunzVector(S(3, 4, 5))
        fkv = FourierKunzVector(kv)
        assert isinstance(fkv, FourierKunzVector)

    def test_construct_rejects_bad_type(self):
        with pytest.raises(TypeError):
            FourierKunzVector((1, 2, 3))

    # --- grid ---

    def test_grid_points_length(self):
        fkv = self._fkv(3, 4, 5)
        assert len(fkv.grid_points) == fkv.multiplicity

    def test_grid_points_values(self):
        fkv = self._fkv(4, 5, 6, 7)   # m=4
        expected = (0.0, 0.25, 0.5, 0.75)
        for a, b in zip(fkv.grid_points, expected):
            assert math.isclose(a, b)

    def test_grid_values_length(self):
        fkv = self._fkv(3, 4, 5)
        assert len(fkv.grid_values) == fkv.multiplicity

    def test_grid_values_first_is_zero(self):
        # f(0) = 0 by convention (residue-0 class)
        fkv = self._fkv(3, 5)
        assert fkv.grid_values[0] == 0.0

    def test_grid_values_max_is_one(self):
        # After normalisation, max value must be 1.0
        for gens in [(2, 3), (3, 4, 5), (3, 5), (4, 6, 7)]:
            fkv = FourierKunzVector(S(*gens))
            assert math.isclose(max(fkv.grid_values), 1.0), (
                f"max grid value != 1.0 for <{gens}>: {fkv.grid_values}"
            )

    def test_grid_values_all_in_unit_interval(self):
        fkv = self._fkv(5, 6, 7, 8, 9)
        assert all(0.0 <= v <= 1.0 for v in fkv.grid_values)

    # --- evaluation ---

    def test_call_at_zero(self):
        fkv = self._fkv(3, 4, 5)
        assert fkv(0.0) == 0.0

    def test_call_at_grid_point(self):
        fkv = self._fkv(3, 4, 5)   # m=3, grid_values=(0, v1, v2)
        # x = 1/3 falls in bin 1 -> grid_values[1]
        assert math.isclose(fkv(1 / 3), fkv.grid_values[1])

    def test_call_periodicity(self):
        fkv = self._fkv(3, 4, 5)
        assert math.isclose(fkv(0.0), fkv(1.0))
        assert math.isclose(fkv(0.5), fkv(1.5))

    def test_call_and_evaluate_equivalent(self):
        fkv = self._fkv(4, 5, 6, 7)
        for x in [0.0, 0.1, 0.25, 0.5, 0.7, 0.99]:
            assert fkv(x) == fkv.evaluate(x)

    def test_step_function_constant_within_bin(self):
        fkv = self._fkv(4, 5, 6, 7)   # m=4, bin width = 0.25
        # All x in [0.25, 0.5) should give grid_values[1]
        expected = fkv.grid_values[1]
        for x in [0.25, 0.30, 0.40, 0.4999]:
            assert math.isclose(fkv(x), expected), f"f({x}) != {expected}"

    # --- Fourier coefficients ---

    def test_fourier_coeff_0_is_mean(self):
        # c_0 = (1/m) * sum of grid values = mean of grid values
        fkv = self._fkv(3, 4, 5)
        c0 = fkv.fourier_coefficient(0)
        mean = sum(fkv.grid_values) / fkv.multiplicity
        assert math.isclose(c0.real, mean, rel_tol=1e-9)
        assert math.isclose(c0.imag, 0.0, abs_tol=1e-12)

    def test_fourier_coefficients_dict_keys(self):
        fkv = self._fkv(3, 4, 5)
        coeffs = fkv.fourier_coefficients(3)
        assert set(coeffs.keys()) == {-3, -2, -1, 0, 1, 2, 3}

    def test_fourier_coefficients_conjugate_symmetry(self):
        # f is real so c_{-n} = conj(c_n)
        fkv = self._fkv(4, 6, 7)
        for n in range(1, 5):
            cn = fkv.fourier_coefficient(n)
            c_neg = fkv.fourier_coefficient(-n)
            assert math.isclose(cn.real, c_neg.real, abs_tol=1e-12)
            assert math.isclose(cn.imag, -c_neg.imag, abs_tol=1e-12)

    def test_partial_sum_converges_to_mean_at_zero_modes(self):
        # With n_max=0, partial sum == c_0 everywhere
        fkv = self._fkv(3, 4, 5)
        c0 = fkv.fourier_coefficient(0).real
        for x in [0.0, 0.33, 0.66, 0.99]:
            assert math.isclose(fkv.partial_sum(x, 0), c0, rel_tol=1e-9)

    def test_partial_sum_real(self):
        # partial_sum should always return a real float
        fkv = self._fkv(5, 6, 7, 8, 9)
        for x in [0.1, 0.4, 0.7]:
            val = fkv.partial_sum(x, 5)
            assert isinstance(val, float)

    def test_repr(self):
        fkv = self._fkv(3, 4, 5)
        r = repr(fkv)
        assert "FourierKunzVector" in r
        assert "m=3" in r


# ---------------------------------------------------------------------------
# FourierKunzVector.distance  &  kunz_distance
# ---------------------------------------------------------------------------

class TestKunzDistance:

    def _fkv(self, *gens):
        return FourierKunzVector(S(*gens))

    # --- identity ---

    def test_distance_self_is_zero(self):
        fkv = self._fkv(3, 4, 5)
        assert math.isclose(fkv.distance(fkv), 0.0, abs_tol=1e-12)

    def test_distance_identical_semigroups_is_zero(self):
        # Two independently created FKVs for the same semigroup
        f1 = self._fkv(3, 4, 5)
        f2 = self._fkv(3, 4, 5)
        assert math.isclose(f1.distance(f2), 0.0, abs_tol=1e-12)

    # --- symmetry ---

    def test_distance_is_symmetric(self):
        f1 = self._fkv(3, 4, 5)
        f2 = self._fkv(3, 5)
        assert math.isclose(f1.distance(f2), f2.distance(f1), rel_tol=1e-9)

    # --- non-negativity ---

    def test_distance_is_nonnegative(self):
        pairs = [
            ((3, 4, 5), (3, 5)),
            ((4, 5, 6, 7), (4, 6, 7)),
            ((2, 3), (3, 4, 5)),
        ]
        for g1, g2 in pairs:
            d = self._fkv(*g1).distance(self._fkv(*g2))
            assert d >= 0.0, f"Negative distance for {g1} vs {g2}: {d}"

    # --- different multiplicities (uses lcm grid) ---

    def test_distance_different_multiplicities(self):
        # m=2 vs m=3: lcm=6, should compute without error
        f1 = self._fkv(2, 3)
        f2 = self._fkv(3, 4, 5)
        d = f1.distance(f2)
        assert d >= 0.0

    def test_distance_triangle_inequality(self):
        f1 = self._fkv(3, 4, 5)
        f2 = self._fkv(3, 5)
        f3 = self._fkv(4, 5, 6, 7)
        d12 = f1.distance(f2)
        d23 = f2.distance(f3)
        d13 = f1.distance(f3)
        assert d13 <= d12 + d23 + 1e-12, (
            f"Triangle inequality failed: {d13} > {d12} + {d23}"
        )

    # --- type error ---

    def test_distance_rejects_bad_type(self):
        fkv = self._fkv(3, 4, 5)
        with pytest.raises(TypeError):
            fkv.distance((1, 2, 3))

    # --- kunz_distance convenience function ---

    def test_kunz_distance_from_semigroups(self):
        s1 = S(3, 4, 5)
        s2 = S(3, 5)
        d = kunz_distance(s1, s2)
        assert d >= 0.0

    def test_kunz_distance_matches_method(self):
        s1 = S(3, 4, 5)
        s2 = S(3, 5)
        d_func = kunz_distance(s1, s2)
        d_method = self._fkv(3, 4, 5).distance(self._fkv(3, 5))
        assert math.isclose(d_func, d_method, rel_tol=1e-12)

    def test_kunz_distance_from_kunz_vectors(self):
        kv1 = KunzVector(S(3, 4, 5))
        kv2 = KunzVector(S(3, 5))
        d = kunz_distance(kv1, kv2)
        assert d >= 0.0

    def test_kunz_distance_from_fourier_vectors(self):
        f1 = self._fkv(3, 4, 5)
        f2 = self._fkv(3, 5)
        d = kunz_distance(f1, f2)
        assert math.isclose(d, f1.distance(f2), rel_tol=1e-12)

    def test_kunz_distance_same_semigroup_is_zero(self):
        s = S(4, 6, 7)
        assert math.isclose(kunz_distance(s, s), 0.0, abs_tol=1e-12)

    def test_kunz_distance_rejects_bad_type(self):
        with pytest.raises(TypeError):
            kunz_distance(S(3, 4, 5), [1, 2, 3])

    # --- norm parameter ---

    def test_distance_invalid_norm_raises(self):
        f1 = self._fkv(3, 4, 5)
        f2 = self._fkv(3, 5)
        with pytest.raises(ValueError):
            f1.distance(f2, norm="L3")

    def test_distance_all_norms_self_is_zero(self):
        fkv = self._fkv(3, 4, 5)
        for norm in ("L1", "L2", "Linf"):
            assert math.isclose(fkv.distance(fkv, norm=norm), 0.0, abs_tol=1e-12), \
                f"{norm} self-distance != 0"

    def test_distance_all_norms_symmetric(self):
        f1 = self._fkv(3, 4, 5)
        f2 = self._fkv(3, 5)
        for norm in ("L1", "L2", "Linf"):
            assert math.isclose(
                f1.distance(f2, norm=norm), f2.distance(f1, norm=norm), rel_tol=1e-9
            ), f"{norm} distance not symmetric"

    def test_distance_all_norms_nonnegative(self):
        f1 = self._fkv(4, 5, 6, 7)
        f2 = self._fkv(4, 6, 7)
        for norm in ("L1", "L2", "Linf"):
            assert f1.distance(f2, norm=norm) >= 0.0

    def test_distance_norm_ordering(self):
        # For any two functions on a finite set of N points:
        #   Linf >= L2 >= L1  (after accounting for normalisation)
        # Concretely: Linf >= L2 always; L1 <= L2 * sqrt(N) but we just check Linf >= L2
        f1 = self._fkv(3, 5)
        f2 = self._fkv(3, 4, 5)
        d_l1   = f1.distance(f2, norm="L1")
        d_l2   = f1.distance(f2, norm="L2")
        d_linf = f1.distance(f2, norm="Linf")
        assert d_linf >= d_l2 - 1e-12,  f"Linf={d_linf} < L2={d_l2}"
        assert d_l2   >= d_l1 - 1e-12,  f"L2={d_l2} < L1={d_l1}"

    def test_kunz_distance_l1_norm(self):
        s1 = S(3, 4, 5)
        s2 = S(3, 5)
        d = kunz_distance(s1, s2, norm="L1")
        assert d >= 0.0
        # should differ from L2
        d_l2 = kunz_distance(s1, s2, norm="L2")
        assert not math.isclose(d, d_l2, rel_tol=1e-6)

    def test_kunz_distance_linf_norm(self):
        s1 = S(3, 4, 5)
        s2 = S(3, 5)
        d = kunz_distance(s1, s2, norm="Linf")
        assert d >= 0.0

    def test_kunz_distance_norm_case_insensitive(self):
        # norm strings should be case-insensitive
        s1 = S(3, 4, 5)
        s2 = S(3, 5)
        assert math.isclose(
            kunz_distance(s1, s2, norm="l1"),
            kunz_distance(s1, s2, norm="L1"),
            rel_tol=1e-12,
        )
        assert math.isclose(
            kunz_distance(s1, s2, norm="linf"),
            kunz_distance(s1, s2, norm="Linf"),
            rel_tol=1e-12,
        )

    def test_kunz_distance_invalid_norm_raises(self):
        with pytest.raises(ValueError):
            kunz_distance(S(3, 4, 5), S(3, 5), norm="L3")
