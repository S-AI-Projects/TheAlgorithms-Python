"""
* Author: Manuel Di Lullo (https://github.com/manueldilullo)
* Description: Approximization algorithm for minimum vertex cover problem.
               Greedy Approach. Uses graphs represented with an adjacency list
URL: https://mathworld.wolfram.com/MinimumVertexCover.html
URL: https://cs.stackexchange.com/questions/129017/greedy-algorithm-for-vertex-cover
"""

import heapq


def greedy_min_vertex_cover(graph: dict) -> set[int]:
    """
    Greedy APX Algorithm for min Vertex Cover
    @input: graph (graph stored in an adjacency list where each vertex
            is represented with an integer)
    @example:

    An empty graph has an empty vertex cover:
    >>> empty_graph = {}
    >>> empty_cover = greedy_min_vertex_cover(empty_graph)
    >>> empty_cover
    set()
    >>> all(
    ...     vertex in empty_cover or neighbor in empty_cover
    ...     for vertex, neighbors in empty_graph.items()
    ...     for neighbor in neighbors
    ... )
    True

    A graph with one edge (and one isolated vertex) needs one endpoint:
    >>> single_edge_graph = {0: [1], 1: [0], 2: []}
    >>> single_edge_cover = greedy_min_vertex_cover(single_edge_graph)
    >>> single_edge_cover
    {0}
    >>> all(
    ...     vertex in single_edge_cover or neighbor in single_edge_cover
    ...     for vertex, neighbors in single_edge_graph.items()
    ...     for neighbor in neighbors
    ... )
    True

    The center covers every edge in a star:
    >>> star_graph = {0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}
    >>> star_cover = greedy_min_vertex_cover(star_graph)
    >>> star_cover
    {0}
    >>> all(
    ...     vertex in star_cover or neighbor in star_cover
    ...     for vertex, neighbors in star_graph.items()
    ...     for neighbor in neighbors
    ... )
    True

    Opposite vertices cover every edge in a four-vertex cycle:
    >>> cycle_graph = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [2, 0]}
    >>> cycle_cover = greedy_min_vertex_cover(cycle_graph)
    >>> cycle_cover
    {0, 2}
    >>> all(
    ...     vertex in cycle_cover or neighbor in cycle_cover
    ...     for vertex, neighbors in cycle_graph.items()
    ...     for neighbor in neighbors
    ... )
    True

    Non-mapping input raises an attribute error when adjacency entries are read:
    >>> greedy_min_vertex_cover(None)
    Traceback (most recent call last):
    ...
    AttributeError: 'NoneType' object has no attribute 'items'

    Running this module directly also exercises its demonstration block:
    >>> from contextlib import redirect_stdout
    >>> from io import StringIO
    >>> import runpy
    >>> with redirect_stdout(StringIO()):
    ...     runpy.run_path(__file__, run_name="__main__")

    >>> graph = {0: [1, 3], 1: [0, 3], 2: [0, 3, 4], 3: [0, 1, 2], 4: [2, 3]}
    >>> greedy_min_vertex_cover(graph)
    {0, 1, 2, 4}
    """
    # queue used to store nodes and their rank
    queue: list[list] = []

    # for each node and his adjacency list add them and the rank of the node to queue
    # using heapq module the queue will be filled like a Priority Queue
    # heapq works with a min priority queue, so I used -1*len(v) to build it
    for key, value in graph.items():
        # O(log(n))
        heapq.heappush(queue, [-1 * len(value), (key, value)])

    # chosen_vertices = set of chosen vertices
    chosen_vertices = set()

    # while queue isn't empty and there are still edges
    #   (queue[0][0] is the rank of the node with max rank)
    while queue and queue[0][0] != 0:
        # extract vertex with max rank from queue and add it to chosen_vertices
        argmax = heapq.heappop(queue)[1][0]
        chosen_vertices.add(argmax)

        # Remove all arcs adjacent to argmax
        for elem in queue:
            # if v haven't adjacent node, skip
            if elem[0] == 0:
                continue
            # if argmax is reachable from elem
            # remove argmax from elem's adjacent list and update his rank
            if argmax in elem[1][1]:
                index = elem[1][1].index(argmax)
                del elem[1][1][index]
                elem[0] += 1
        # re-order the queue
        heapq.heapify(queue)
    return chosen_vertices


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    graph = {0: [1, 3], 1: [0, 3], 2: [0, 3, 4], 3: [0, 1, 2], 4: [2, 3]}
    print(f"Minimum vertex cover:\n{greedy_min_vertex_cover(graph)}")
