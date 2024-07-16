from .numerical_set import NumericalSet
from .numerical_semigroup import NumericalSemigroup
from .partition import Partition
from typing import Union

def atom_monoid(T:Union[NumericalSet, NumericalSemigroup, Partition]) -> NumericalSemigroup:
    gapset = T.atom_monoid_gaps()
    return NumericalSemigroup(gaps=gapset)

def partition(T:Union[NumericalSet, NumericalSemigroup]) -> Partition:
    return Partition(T.partition())