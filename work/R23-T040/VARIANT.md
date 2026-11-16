# Persistent range minimum variant

## What differs

`data_structures/binary_tree/persistent_segment_tree.py` stores a sum at each
node and combines children with addition. This implementation stores a minimum
and combines children with `min`, while keeping the same versioned-root idea:
`update(version, index, value)` appends a root and `query(version, left, right)`
reads any retained version. Nodes are immutable, and an update creates only the
nodes along its root-to-leaf path while sharing the untouched subtrees.

This is not a duplicate of `segment_tree_other.py`: that segment tree accepts a
generic combine function but updates its nodes in place, so it cannot answer a
query against an earlier version. `data_structures/arrays/sparse_table.py` is
also an RMQ structure, but it is static: it preprocesses O(n log n) values for
O(1) queries and does not provide updates or version history. The persistent
minimum tree instead uses O(n) initial nodes, O(log n) new nodes per update,
and O(log n) time for both an update and a query.

## Small timing comparison

Measured with Python 3.15.2 on this macOS worktree for an array of 4,096
integers. Each table entry is the median per-operation time over five repeats:
100 builds, 1,000 updates, or 20,000 range queries per repeat. The update
benchmark repeatedly branches from version 0; the query benchmark asks for
version 0 over `[321, 3500]`.

| Operation | Persistent sum | Persistent minimum |
| --- | ---: | ---: |
| Build (microseconds) | 1,134.37 | 1,616.65 |
| Update (microseconds) | 2.03 | 3.00 |
| Range query (microseconds) | 1.99 | 1.88 |

These are small, environment-specific timings rather than a performance claim.
The asymptotic costs and number of nodes created are the same as the sum tree;
the extra cost in this run is the constant-factor work of the minimum variant.
