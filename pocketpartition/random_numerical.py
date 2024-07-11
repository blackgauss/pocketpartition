from numerical import NumericalSemigroup
import random

def RandomNumericalSemigroupWithGenus(g):
    """
    Generates a random numerical semigroup with a given genus.
        https://github.com/gap-packages/numericalsgps/blob/master/gap/random.gi
    Parameters:
    g (int): The genus of the numerical semigroup.

    Returns:
    NumericalSemigroup: The generated numerical semigroup.
    """
    s = NumericalSemigroup(generators={1})
    gapset = []
    for i in range(g):
        mingens = s.minimal_generating_set()
        x = random.choice(mingens)
        gapset.append(x)
        s = NumericalSemigroup(gaps=gapset)
    return s