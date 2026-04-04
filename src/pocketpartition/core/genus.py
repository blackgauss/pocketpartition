__all__ = ['WithGenus', 'WithMaxGenus']

from collections import deque
from ..core.numerical_semigroup import NumericalSemigroup

def bfs_to_depth(root, depth):
    if depth < 0:
        return

    queue = deque([(root, 0)])

    while queue:
        node, current_depth = queue.popleft()

        if current_depth == depth:
            yield node
        elif current_depth < depth:
            for child in node.get_children():
                queue.append((child, current_depth + 1))

def bfs_up_to_depth(root, depth):
    if depth < 0:
        return

    queue = deque([(root, 0)])

    while queue:
        node, current_depth = queue.popleft()

        yield node
        if current_depth < depth:
            for child in node.get_children():
                queue.append((child, current_depth + 1))

def WithGenus(g):
    """Yield all numerical semigroups of genus exactly g."""
    yield from bfs_to_depth(NumericalSemigroup(generators={1}), g)

def WithMaxGenus(g):
    """Yield all numerical semigroups of genus at most g."""
    yield from bfs_up_to_depth(NumericalSemigroup(generators={1}), g)