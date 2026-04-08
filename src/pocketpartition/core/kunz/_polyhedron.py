"""
KunzPolyhedron — membership testing for the Kunz polyhedral cone P(m).
"""

__all__ = ['KunzPolyhedron']


class KunzPolyhedron:
    """
    The Kunz polyhedron for a given multiplicity m.

    The Kunz polyhedron ``P(m)`` is the rational polyhedral cone in
    ``R^{m-1}`` defined by the inequalities:

    - ``c_i + c_j >= c_{i+j}``        for all ``1 <= i <= j <= m-1`` with ``i+j < m``
    - ``c_i + c_j + 1 >= c_{i+j-m}``  for all ``1 <= i <= j <= m-1`` with ``i+j > m``

    Every numerical semigroup of multiplicity m corresponds to an integer
    lattice point inside ``P(m)``, and conversely every such lattice point
    with all positive coordinates determines a numerical semigroup.

    Parameters
    ----------
    m : int
        The multiplicity.  Must be a positive integer.

    Attributes
    ----------
    m : int
        The multiplicity this polyhedron was built for.
    corner : tuple of float
        The ``m`` equally-spaced points ``(0, 1/m, 2/m, ..., (m-1)/m)``,
        representing the origin corner of the polyhedron in the normalised
        coordinate chart.

    Examples
    --------
    >>> from pocketpartition.core.kunz import KunzPolyhedron, kunz_tuple
    >>> from pocketpartition import NumericalSemigroup
    >>> kp = KunzPolyhedron(3)
    >>> S = NumericalSemigroup(generators=[3, 4, 5])
    >>> kp.is_point(kunz_tuple(S))
    True
    """

    def __init__(self, m: int):
        """
        Initialise the Kunz polyhedron for multiplicity m.

        Parameters
        ----------
        m : int
            Must be a positive integer.

        Raises
        ------
        TypeError
            If ``m`` is not an integer.
        ValueError
            If ``m`` is not a positive integer.
        """
        if not isinstance(m, int):
            raise TypeError(f"m must be an integer, got {type(m).__name__}.")
        if m <= 0:
            raise ValueError("m must be a positive integer.")
        self.m = m
        self.corner = tuple([i / m for i in range(m)])

    def is_point(self, p: tuple) -> bool:
        """
        Check whether a coordinate vector lies inside the Kunz polyhedron.

        Parameters
        ----------
        p : tuple of int or float
            A vector of length ``m - 1``.  Entry ``p[k]`` represents the
            coordinate ``c_{k+1}`` (1-indexed residue ``k+1`` mod ``m``).

        Returns
        -------
        bool
            ``True`` if ``p`` satisfies all Kunz polyhedron inequalities,
            ``False`` otherwise.

        Notes
        -----
        The inequalities checked are, for all ``1 <= i <= j <= m-1``:

        - ``i + j < m``  →  ``c_i + c_j >= c_{i+j}``
        - ``i + j > m``  →  ``c_i + c_j + 1 >= c_{i+j-m}``
        - ``i + j == m`` →  always satisfied for non-negative coordinates

        Raises
        ------
        ValueError
            If ``p`` does not have length ``m - 1``.

        Examples
        --------
        >>> kp = KunzPolyhedron(3)
        >>> kp.is_point((1, 1))   # Kunz tuple of <3, 4, 5>
        True
        >>> kp.is_point((-1, 1))  # negative coordinate
        False
        """
        # p has length m-1, representing c_1 ... c_{m-1} (1-indexed residues).
        # p[k] corresponds to c_{k+1}.
        m = self.m
        if len(p) != m - 1:
            raise ValueError(
                f"p must have length m-1 = {m - 1}, got {len(p)}."
            )
        if any(x < 0 for x in p):
            return False
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
