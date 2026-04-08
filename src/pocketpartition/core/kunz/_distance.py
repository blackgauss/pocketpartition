"""
kunz_distance — module-level convenience function for comparing semigroups.
"""

__all__ = ['kunz_distance']

from ..numerical_semigroup import NumericalSemigroup
from ._vector import KunzVector
from ._fourier import FourierKunzVector


def kunz_distance(
    S: "NumericalSemigroup | KunzVector | FourierKunzVector",
    T: "NumericalSemigroup | KunzVector | FourierKunzVector",
    norm: str = "L2",
) -> float:
    """
    Compute the distance between two numerical semigroups (or already-built
    Kunz / FourierKunz vectors) using their normalised Kunz step functions.

    Parameters
    ----------
    S, T : NumericalSemigroup | KunzVector | FourierKunzVector
        The two objects to compare.  NumericalSemigroup and KunzVector inputs
        are automatically converted to FourierKunzVector.
    norm : {"L1", "L2", "Linf"}
        Which norm to use (default ``"L2"``):

        - ``"L1"``   — sum of absolute differences (normalised by grid size)
        - ``"L2"``   — root-mean-square differences  *(default)*
        - ``"Linf"`` — maximum absolute difference

    Returns
    -------
    float
        d(f_S, f_T) ≥ 0, where equality holds iff the two normalised Kunz
        step functions are identical.

    Examples
    --------
    >>> from pocketpartition import NumericalSemigroup, kunz_distance
    >>> S = NumericalSemigroup(generators=[3, 4, 5])
    >>> T = NumericalSemigroup(generators=[3, 5])
    >>> kunz_distance(S, T)                  # L2 (default)  # doctest: +ELLIPSIS
    0.816...
    >>> kunz_distance(S, T, norm="L1")       # doctest: +ELLIPSIS
    0.666...
    >>> kunz_distance(S, T, norm="Linf")     # doctest: +ELLIPSIS
    1.0...
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

    return _to_fkv(S).distance(_to_fkv(T), norm=norm)
