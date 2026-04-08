"""
pocketpartition.core.kunz
=========================

Kunz coordinate machinery for numerical semigroups.

Sub-modules
-----------
_coords      : _compute_kunz_coords, kunz_tuple
_vector      : KunzVector
_fourier     : FourierKunzVector
_distance    : kunz_distance
_polyhedron  : KunzPolyhedron

All public names are re-exported from this package so that existing imports
of the form ``from pocketpartition.core.kunz import ...`` continue to work
without modification.
"""

__all__ = [
    'kunz_tuple',
    'KunzVector',
    'FourierKunzVector',
    'kunz_distance',
    'KunzPolyhedron',
]

from ._coords import kunz_tuple, _compute_kunz_coords
from ._vector import KunzVector
from ._fourier import FourierKunzVector
from ._distance import kunz_distance
from ._polyhedron import KunzPolyhedron
