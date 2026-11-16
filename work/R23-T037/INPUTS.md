# `greedy_min_vertex_cover` input cases

The public function accepts an adjacency-list mapping whose vertices are
integers and whose neighbor lists describe an undirected graph.

| Category | Input | Expected behavior |
| --- | --- | --- |
| Valid | Existing sample graph | Return a set covering every edge. |
| Boundary | Empty mapping `{}` | Return the empty set; the edge-coverage check is vacuously true. |
| Boundary | One edge plus an isolated vertex | Return one endpoint; also exercises skipping an already-zero-degree queue entry. |
| Valid | Star graph | Return the center; every edge has that endpoint. |
| Valid | Four-vertex cycle | Return opposite vertices; every edge touches one of them. |
| Invalid | `None` instead of an adjacency mapping | Currently raises `AttributeError` when `.items()` is accessed; the doctest records this behavior. |

Each graph doctest checks the cover property directly with
`all(vertex in cover or neighbor in cover for each adjacency entry)`. The
single-edge graph includes an isolated vertex specifically to exercise the
queue's zero-degree skip path.
