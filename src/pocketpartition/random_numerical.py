from .numerical import NumericalSemigroup
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
    for i in range(g):
        mingens = s.minimal_generating_set()
        x = random.choice(mingens)
        s = s.remove_minimal_generator(x)
    return s

def RandomGraphWalk(start, g):
    """
    Generates a random numerical semigroup with a given genus.
        https://github.com/gap-packages/numericalsgps/blob/master/gap/random.gi
    Parameters:
    g (int): The genus of the numerical semigroup.

    Returns:
    NumericalSemigroup: The generated numerical semigroup.
    """
    s = start
    for i in range(g):
        mingens = s.minimal_generating_set()
        x = random.choice(mingens)
        s = s.remove_minimal_generator(x)
    return s

def RandomTreeWalk(start, g):
    """
    Generates a random numerical semigroup with a given genus.
        https://github.com/gap-packages/numericalsgps/blob/master/gap/random.gi
    Parameters:
    g (int): The genus of the numerical semigroup.

    Returns:
    NumericalSemigroup: The generated numerical semigroup.
    """
    s = start
    for i in range(g):
        mingens = s.minimal_generating_set()
        frob = s.frobenius_number
        effective_gens = [gen for gen in mingens if gen > frob]
        if effective_gens:
            x = random.choice(effective_gens)
            s = s.remove_minimal_generator(x)
        else:
            return
    return s