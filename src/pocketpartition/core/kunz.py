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
        # Check if all elements in p are non-negative
        if any(x < 0 for x in p):
            return False 
        valid_point = True
        # Iterate over all pairs (i, j) where i <= j
        for i in range(len(p)):
            for j in range(i, len(p)):
                # Check conditions based on i + j
                if i + j < self.m:
                    if p[i] + p[j] >= p[i + j]:
                        valid_point = valid_point and True
                    else:
                        return False
                elif i + j >= self.m:
                    if p[i] + p[j] + 1 >= p[i + j - self.m]:
                        valid_point = valid_point and True
                    else:
                        return False        
        return valid_point
