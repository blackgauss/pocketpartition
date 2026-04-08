"""
Kunz coordinate computation.

This module provides the low-level helper that builds the Kunz coordinate
tuple from a NumericalSemigroup, and the public ``kunz_tuple`` wrapper.
"""

__all__ = ['kunz_tuple']

from ..numerical_semigroup import NumericalSemigroup


def _compute_kunz_coords(S: NumericalSemigroup) -> tuple:
    """
    Return the raw Kunz coordinate tuple for semigroup S.

    For each residue class ``r = 1, ..., m-1`` (where ``m`` is the
    multiplicity of S) this finds the smallest element of S in that
    residue class, then divides by ``m``.

    The implementation iterates forward from ``r`` in steps of ``m``,
    using the O(1) ``frozenset`` membership test on ``S.gaps``,
    and stops as soon as all ``m-1`` residue classes have been assigned.
    This avoids building the full Apéry set when the multiplicity is
    small relative to the Frobenius number.

    Parameters
    ----------
    S : NumericalSemigroup

    Returns
    -------
    tuple of int
        Length ``m - 1``, entries ``w_1, ..., w_{m-1}`` in residue order.
    """
    m = S.multiplicity()
    gaps = S.gaps  # frozenset — O(1) membership tests
    coords = [None] * m  # index 0 unused; coords[r] = w_r
    remaining = m - 1    # how many residues still need filling

    n = 1
    while remaining:
        r = n % m
        if r != 0 and coords[r] is None and n not in gaps:
            coords[r] = n // m
            remaining -= 1
        n += 1

    return tuple(coords[1:])


def kunz_tuple(S: NumericalSemigroup) -> tuple:
    """
    Return the Kunz coordinate tuple of a numerical semigroup.

    For a semigroup S with multiplicity m, the Kunz tuple is the vector
    ``(w_1, ..., w_{m-1})`` where ``w_i = min{ n in S : n ≡ i (mod m) } / m``.

    Parameters
    ----------
    S : NumericalSemigroup

    Returns
    -------
    tuple of int
        Length ``m - 1``, all entries positive.

    Examples
    --------
    >>> from pocketpartition import NumericalSemigroup
    >>> from pocketpartition.core.kunz import kunz_tuple
    >>> S = NumericalSemigroup(generators=[3, 4, 5])
    >>> kunz_tuple(S)
    (1, 1)
    """
    return _compute_kunz_coords(S)

