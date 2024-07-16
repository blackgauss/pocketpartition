from collections import defaultdict, deque

def topological_sort(elements, relations):
    # Initialize in-degree dictionary
    in_degree = {element: 0 for element in elements}
    for parent, child in relations:
        if parent not in in_degree or child not in in_degree:
            raise ValueError(f"Element '{parent}' or '{child}' not found in elements list.")
        in_degree[child] += 1

    # Initialize queue with nodes having zero in-degree
    queue = deque([element for element in elements if in_degree[element] == 0])
    sorted_elements = []

    while queue:
        element = queue.popleft()
        sorted_elements.append(element)
        for parent, child in relations:
            if parent == element:
                in_degree[child] -= 1
                if in_degree[child] == 0:
                    queue.append(child)

    # If the sorted elements do not include all elements, add isolated elements
    if len(sorted_elements) != len(elements):
        for element in elements:
            if element not in sorted_elements:
                sorted_elements.append(element)

    return sorted_elements

def compute_layout(elements, relations):
    sorted_elements = topological_sort(elements, relations)

    rank = {element: None for element in elements}
    rank[sorted_elements[0]] = 0  # Start with the first element in topologically sorted order

    for element in sorted_elements:
        if rank[element] is None:
            rank[element] = 0  # Assign rank 0 to isolated or disconnected elements
        for parent, child in relations:
            if parent == element:
                if rank[child] is None:
                    rank[child] = rank[element] + 1
                else:
                    rank[child] = max(rank[child], rank[element] + 1)

    # Group elements by their rank
    levels = defaultdict(list)
    for element in elements:
        levels[rank[element]].append(element)

    # Calculate positions: x position based on the order within the rank, y position based on the rank
    positions = {}
    child_count = defaultdict(int)
    for parent, child in relations:
        child_count[parent] += 1

    for level, nodes in levels.items():
        for index, node in enumerate(nodes):
            if level > 0:
                # Align node directly below its parent if the parent has only one child
                parent_x = None
                for parent, child in relations:
                    if child == node and rank[parent] == level - 1 and child_count[parent] == 1:
                        if parent in positions:
                            parent_x = positions[parent][0]
                        break
                if parent_x is not None:
                    positions[node] = (parent_x, -level * 2)
                else:
                    # Use original positioning based on index
                    x = 0 if index == 0 else positions[nodes[index - 1]][0] + 2
                    positions[node] = (x, -level * 2)
            else:
                # Position root level nodes based on index
                x = 0 if index == 0 else positions[nodes[index - 1]][0] + 2
                positions[node] = (x, -level * 2)

    return positions

def generate_tikz(elements, relations):
    positions = compute_layout(elements, relations)

    # Find the largest element
    largest_element = max(elements)

    tikz_code = "\\documentclass{standalone}\n"
    tikz_code += "\\usepackage{tikz}\n"
    tikz_code += "\\begin{document}\n"
    tikz_code += "\\begin{tikzpicture}[scale=1, transform shape]\n"

    # Add nodes with positions
    for element, pos in positions.items():
        if element == largest_element:
            tikz_code += f"  \\node[draw, rectangle] ({element}) at ({pos[0]},{pos[1]}) {{{element}}};\n"
        else:
            tikz_code += f"  \\node ({element}) at ({pos[0]},{pos[1]}) {{{element}}};\n"

    # Draw the cover relations
    tikz_code += "  % Draw the cover relations\n"
    for i, j in relations:
        tikz_code += f"  \\draw ({i}) -- ({j});\n"

    tikz_code += "\\end{tikzpicture}\n"
    tikz_code += "\\end{document}\n"

    return tikz_code