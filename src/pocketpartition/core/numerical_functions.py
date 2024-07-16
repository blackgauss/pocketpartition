from .numerical_set import NumericalSet
from .numerical_semigroup import NumericalSemigroup
from .partition import Partition
from .poset import Poset
from typing import Union

__all__ = ['get_atom_monoid', 'get_partition', 'get_gap_poset', 'get_void_poset']

from .numerical_set import NumericalSet
from .numerical_semigroup import NumericalSemigroup
from .partition import Partition
from .poset import Poset
from typing import Union

def get_atom_monoid(T:Union[NumericalSet, NumericalSemigroup, Partition]) -> NumericalSemigroup:
    gapset = T.atom_monoid_gaps()
    return NumericalSemigroup(gaps=gapset)

def get_partition(T:Union[NumericalSet, NumericalSemigroup]) -> Partition:
    return Partition(T.partition())

def get_gap_poset(S:Union[NumericalSemigroup]) -> Poset:
    elements, relations = S.gap_poset()
    return Poset(elements, relations)

def get_void_poset(S:Union[NumericalSemigroup]) -> Poset:
    elements, relations = S.void_poset()
    return Poset(elements, relations)