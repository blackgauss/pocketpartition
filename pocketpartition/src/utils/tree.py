def bfs_at_depth(root, g):
    """
    Perform a BFS on a tree and return the nodes at depth g.
    
    :param root: The starting node of the tree.
    :param g: The depth at which to collect nodes.
    :return: A list of nodes at depth g.
    """
    if g < 0:
        return []

    # Initialize the queue with the root node and its depth (0)
    queue = [(root, 0)]
    result = []

    while queue:
        current_node, depth = queue.pop(0)
        
        # If we reach the desired depth, add the node to the result list
        if depth == g:
            result.append(current_node)
        
        # If the current depth is less than g, add the children to the queue
        if depth < g:
            children = current_node.get_children()
            for child in children:
                queue.append((child, depth + 1))

    return result
