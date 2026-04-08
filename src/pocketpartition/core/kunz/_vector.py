"""
KunzVector — the Kunz coordinate vector as an immutable tuple subclass.
"""

__all__ = ['KunzVector']

from ..numerical_semigroup import NumericalSemigroup
from ._coords import _compute_kunz_coords


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
        """The multiplicity of the underlying semigroup (equals ``m``, the vector length plus one)."""
        return self._semigroup.multiplicity()

    @property
    def genus(self) -> int:
        """The genus (number of gaps) of the underlying semigroup."""
        return self._semigroup.genus

    @property
    def frobenius_number(self) -> int:
        """The Frobenius number (largest gap) of the underlying semigroup."""
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
