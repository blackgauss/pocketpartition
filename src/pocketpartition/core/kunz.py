__all__ = ['kunz_tuple']

from .numerical_semigroup import NumericalSemigroup

def kunz_tuple(S:NumericalSemigroup):
  m = S.multiplicity()
  A = S.apery_set(m)
  kunz_tup = list()
  for res in range(1, m):
    for n in A:
      if n % m == res:
        kunz_tup.append(n // m)
  return tuple(kunz_tup)


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
