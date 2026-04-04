__all__ = ['kunz_tuple', 'KunzVector', 'FourierKunzVector', 'KunzPolyhedron', 'kunz_distance']

import math
from .numerical_semigroup import NumericalSemigroup


# ---------------------------------------------------------------------------
# Internal helper (kept for backward compatibility and reuse)
# ---------------------------------------------------------------------------

def _compute_kunz_coords(S: NumericalSemigroup) -> tuple:
    m = S.multiplicity()
    A = S.apery_set(m)
    kunz_tup = []
    for res in range(1, m):
        for n in A:
            if n % m == res:
                kunz_tup.append(n // m)
    return tuple(kunz_tup)


def kunz_tuple(S: NumericalSemigroup) -> tuple:
    """Return the Kunz coordinate tuple of S as a plain tuple."""
    return _compute_kunz_coords(S)


# ---------------------------------------------------------------------------
# KunzVector
# ---------------------------------------------------------------------------

class KunzVector(tuple):
    """
    The Kunz coordinate vector of a NumericalSemigroup, stored as an
    immutable tuple of positive integers of length m-1.

    Entry k (0-indexed) is  w_{k+1} = min{ n in S : n ≡ k+1  (mod m) } / m,
    where m is the multiplicity of S.

    Because KunzVector subclasses tuple, it supports all standard tuple
    operations.  The originating semigroup is accessible via `.semigroup`.
    """

    def __new__(cls, S: NumericalSemigroup):
        coords = _compute_kunz_coords(S)
        instance = super().__new__(cls, coords)
        return instance

    def __init__(self, S: NumericalSemigroup):
        self._semigroup = S
        # tuple.__init__ takes no arguments
        super().__init__()

    # --- semigroup pass-throughs ---

    @property
    def semigroup(self) -> NumericalSemigroup:
        """The NumericalSemigroup this vector was built from."""
        return self._semigroup

    @property
    def multiplicity(self) -> int:
        return self._semigroup.multiplicity()

    @property
    def genus(self) -> int:
        return self._semigroup.genus

    @property
    def frobenius_number(self) -> int:
        return self._semigroup.frobenius_number

    # --- coordinate access (1-indexed, matching residue notation) ---

    def coord(self, i: int) -> int:
        """
        Return w_i (1-indexed).  i must satisfy 1 <= i <= m-1.
        """
        m = self.multiplicity
        if not (1 <= i <= m - 1):
            raise IndexError(f"Index {i} out of range for multiplicity {m}.")
        return self[i - 1]

    # --- display ---

    def __repr__(self) -> str:
        return (f"KunzVector(m={self.multiplicity}, "
                f"coords={tuple(self)}, genus={self.genus})")


# ---------------------------------------------------------------------------
# FourierKunzVector
# ---------------------------------------------------------------------------

class FourierKunzVector:
    """
    The normalized Kunz function viewed as a step function on the circle S^1.

    Starting from a KunzVector  v = (w_1, ..., w_{m-1})  we build:

        f : S^1 → [0, 1]
        f(i/m) = w_i / max_j(w_j)      for i = 1, ..., m-1
        f(0)   = 0                       (convention: 0 residue class maps to 0)

    The domain is discretised as  {0, 1/m, 2/m, ..., (m-1)/m} ⊂ [0,1)
    and f is extended to all of [0,1) as a right-continuous step function
    (piecewise-constant on each interval [i/m, (i+1)/m)).

    Parameters
    ----------
    source : KunzVector | NumericalSemigroup
        Either a KunzVector or a NumericalSemigroup (converted automatically).
    """

    def __init__(self, source):
        if isinstance(source, NumericalSemigroup):
            source = KunzVector(source)
        if not isinstance(source, KunzVector):
            raise TypeError("source must be a KunzVector or NumericalSemigroup.")
        self._kunz = source
        m = source.multiplicity
        raw_max = max(source)           # max over w_1 ... w_{m-1}
        # normalised values at each grid point i/m, i = 0, 1, ..., m-1
        # index 0  (residue 0) -> 0 by convention
        self._grid: tuple[float, ...] = (0.0,) + tuple(
            source[i] / raw_max for i in range(m - 1)
        )
        self._m = m
        self._max_raw = raw_max

    # --- properties ---

    @property
    def kunz_vector(self) -> KunzVector:
        return self._kunz

    @property
    def multiplicity(self) -> int:
        return self._m

    @property
    def grid_points(self) -> tuple[float, ...]:
        """The m normalised domain points {0, 1/m, ..., (m-1)/m}."""
        return tuple(i / self._m for i in range(self._m))

    @property
    def grid_values(self) -> tuple[float, ...]:
        """Normalised function values at each grid point."""
        return self._grid

    # --- evaluation ---

    def __call__(self, x: float) -> float:
        """
        Evaluate f at x ∈ [0, 1).

        f is the right-continuous step function that equals  w_i / max(w)
        on the half-open interval  [i/m, (i+1)/m)  for i = 0, 1, ..., m-1,
        with the convention that f on [0, 1/m) equals 0 (residue 0 class).

        Parameters
        ----------
        x : float
            A value in [0, 1).  x = 1.0 is also accepted and mapped to 0
            (periodicity).

        Returns
        -------
        float
            f(x) ∈ [0, 1].
        """
        x = float(x) % 1.0          # enforce periodicity
        m = self._m
        # which bin does x fall into?  bin i covers [i/m, (i+1)/m)
        i = int(x * m)
        if i >= m:                   # numerical edge case
            i = m - 1
        return self._grid[i]

    def evaluate(self, x: float) -> float:
        """Alias for __call__."""
        return self(x)

    # --- Fourier coefficients ---

    def fourier_coefficient(self, n: int) -> complex:
        """
        Compute the n-th Fourier coefficient of f:

            c_n = ∫_0^1 f(x) e^{-2πi n x} dx

        Because f is a step function constant on each [i/m, (i+1)/m),
        the integral reduces to a finite sum:

            c_n = (1/m) Σ_{i=0}^{m-1}  f(i/m) · e^{-2πi n (i/m)}
                = (1/m) Σ_{i=0}^{m-1}  v_i · ω^{-ni}

        where  ω = e^{2πi/m}  is the primitive m-th root of unity and
        v_i = self._grid[i].

        Parameters
        ----------
        n : int
            Fourier mode index.

        Returns
        -------
        complex
            The n-th Fourier coefficient c_n.
        """
        m = self._m
        omega = 2 * math.pi / m
        total = sum(
            self._grid[i] * complex(math.cos(omega * n * i),
                                    -math.sin(omega * n * i))
            for i in range(m)
        )
        return total / m

    def fourier_coefficients(self, n_max: int) -> dict[int, complex]:
        """
        Compute Fourier coefficients c_n for n = -n_max, ..., n_max.

        Returns
        -------
        dict mapping int -> complex
        """
        return {n: self.fourier_coefficient(n) for n in range(-n_max, n_max + 1)}

    def partial_sum(self, x: float, n_max: int) -> float:
        """
        Evaluate the Fourier partial sum  S_{n_max}(x) = Σ_{|n|<=n_max} c_n e^{2πinx}.

        Useful for visualising how well the Fourier series reconstructs f.

        Parameters
        ----------
        x : float
            Point in [0, 1).
        n_max : int
            Number of modes on each side.

        Returns
        -------
        float
            Real part of the partial sum (imaginary part is ~0 for real f).
        """
        coeffs = self.fourier_coefficients(n_max)
        total = sum(
            coeffs[n] * complex(math.cos(2 * math.pi * n * x),
                                 math.sin(2 * math.pi * n * x))
            for n in range(-n_max, n_max + 1)
        )
        return total.real

    # --- L2 distance ---

    def distance(self, other: "FourierKunzVector") -> float:
        """
        Compute the L² distance between this FourierKunzVector and another.

        Both functions are step functions on [0, 1).  The L² norm is computed
        on a common evaluation grid of size lcm(m_self, m_other), which is
        the finest grid on which both functions are simultaneously constant.

        .. math::

            d(f, g) = \\left( \\int_0^1 |f(x) - g(x)|^2 \\, dx \\right)^{1/2}
                    = \\left( \\frac{1}{N} \\sum_{k=0}^{N-1}
                      \\bigl(f(k/N) - g(k/N)\\bigr)^2 \\right)^{1/2}

        where  N = lcm(m_self, m_other).

        Parameters
        ----------
        other : FourierKunzVector

        Returns
        -------
        float
            The L² distance ≥ 0.
        """
        if not isinstance(other, FourierKunzVector):
            raise TypeError("other must be a FourierKunzVector.")
        N = math.lcm(self._m, other._m)
        total = sum(
            (self(k / N) - other(k / N)) ** 2
            for k in range(N)
        )
        return math.sqrt(total / N)

    # --- display ---

    def __repr__(self) -> str:
        pts = ", ".join(f"{x:.3f}" for x in self._grid)
        return (f"FourierKunzVector(m={self._m}, "
                f"grid_values=({pts}))")


# ---------------------------------------------------------------------------
# Module-level convenience function
# ---------------------------------------------------------------------------

def kunz_distance(
    S: "NumericalSemigroup | KunzVector | FourierKunzVector",
    T: "NumericalSemigroup | KunzVector | FourierKunzVector",
) -> float:
    """
    Compute the L² distance between two numerical semigroups (or already-built
    Kunz / FourierKunz vectors) using their normalised Kunz step functions.

    Parameters
    ----------
    S, T : NumericalSemigroup | KunzVector | FourierKunzVector
        The two objects to compare.  NumericalSemigroup and KunzVector inputs
        are automatically converted to FourierKunzVector.

    Returns
    -------
    float
        d(f_S, f_T) ≥ 0, where equality holds iff the two normalised Kunz
        step functions are identical.

    Examples
    --------
    >>> from pocketpartition import NumericalSemigroup
    >>> from pocketpartition.core.kunz import kunz_distance
    >>> S = NumericalSemigroup(generators=[3, 4, 5])
    >>> T = NumericalSemigroup(generators=[3, 5])
    >>> kunz_distance(S, T)       # doctest: +ELLIPSIS
    0.816...
    """
    def _to_fkv(obj):
        if isinstance(obj, FourierKunzVector):
            return obj
        if isinstance(obj, KunzVector):
            return FourierKunzVector(obj)
        if isinstance(obj, NumericalSemigroup):
            return FourierKunzVector(obj)
        raise TypeError(
            f"Expected NumericalSemigroup, KunzVector, or FourierKunzVector, "
            f"got {type(obj).__name__}."
        )

    return _to_fkv(S).distance(_to_fkv(T))


# ---------------------------------------------------------------------------
# KunzPolyhedron
# ---------------------------------------------------------------------------

class KunzPolyhedron:
    def __init__(self, m: int):
        if m <= 0:
            raise ValueError("m must be a positive integer.")
        self.m = m
        self.corner = tuple([i/m for i in range(m)])

    def is_point(self, p: tuple[int]) -> bool:
        # p has length m-1, representing c_1 ... c_{m-1} (1-indexed residues).
        # p[k] corresponds to c_{k+1}.
        # Kunz polyhedron inequalities for all 1 <= i <= j <= m-1:
        #   i+j < m  =>  c_i + c_j >= c_{i+j}
        #   i+j > m  =>  c_i + c_j + 1 >= c_{i+j-m}
        #   i+j == m =>  c_i + c_j + 1 >= 1  (always true for non-negative coords)
        if any(x < 0 for x in p):
            return False
        m = self.m
        # residues are 1-indexed; i and j run from 1 to m-1
        for i in range(1, m):
            for j in range(i, m):
                ci = p[i - 1]
                cj = p[j - 1]
                s = i + j
                if s < m:
                    if ci + cj < p[s - 1]:
                        return False
                elif s > m:
                    if ci + cj + 1 < p[s - m - 1]:
                        return False
                # s == m: ci + cj + 1 >= 1 is always satisfied for non-negative values
        return True
