from collections import deque
from ..core.numerical_semigroup import NumericalSemigroup

def bfs_to_depth(root, depth):
    if depth < 0:
        return []

    queue = deque([(root, 0)])  # (node, current_depth)
    nodes_at_depth_g = []

    while queue:
        node, current_depth = queue.popleft()

        if current_depth == depth:
            nodes_at_depth_g.append(node)
        elif current_depth < depth:
            for child in node.get_children():
                queue.append((child, current_depth + 1))

    return nodes_at_depth_g

def bfs_up_to_depth(root, depth):
    if depth < 0:
        return []

    queue = deque([(root, 0)])  # (node, current_depth)
    nodes = []

    while queue:
        node, current_depth = queue.popleft()

        nodes.append(node)
        if current_depth < depth:
            for child in node.get_children():
                queue.append((child, current_depth + 1))

    return nodes

def WithGenus(g):
    return bfs_to_depth(NumericalSemigroup(generators={1}), g)

def WithMaxGenus(g):
    return bfs_up_to_depth(NumericalSemigroup(generators={1}), g)