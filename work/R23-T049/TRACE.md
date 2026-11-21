# Seeded TSP generation trace

I traced `init`, `fitness`, both selection helpers, `crossing`, and `mutate`
with `python -m pdb` using four cities on a unit square, population size 4,
and seed 23. The trace helper was temporary; the seeded doctest in
`genetic_algorithm/travelling_salesman_problem.py` now reproduces the roulette
selection generation steps.

| Step | Seed / operation | Values observed |
| --- | --- | --- |
| Initial setup | `random.seed(23)`; cities `{0: [0, 0], 1: [1, 0], 2: [1, 1], 3: [0, 1]}` | `cities_list = [1, 2, 3]`; population size = 4 |
| Initial population | `init(cities, 4)` | `[[0, 2, 1, 3, 0], [0, 3, 2, 1, 0], [0, 2, 3, 1, 0], [0, 3, 1, 2, 0]]` |
| Fitness | `fitness(cities, population, [], inf)` | Distances `[4.828427, 4.0, 4.828427, 4.828427]`; fitness `[0.207107, 0.25, 0.207107, 0.207107]`; best so far `([0, 3, 2, 1, 0], 4.0)` |
| Tournament selection | Reset `random.seed(23)`; `chose_ts(...)` | `[[0, 2, 3, 1, 0], [0, 2, 1, 3, 0], [0, 3, 1, 2, 0], [0, 3, 2, 1, 0]]` |
| Roulette selection | Reset `random.seed(23)`; `chose_rws(...)` | `[[0, 3, 1, 2, 0], [0, 3, 1, 2, 0], [0, 3, 1, 2, 0], [0, 2, 1, 3, 0]]` |
| Crossover, pair 0 and 2 | `crossover_probability=1.0` | Both parents were `[0, 3, 1, 2, 0]`; offspring remained `[0, 3, 1, 2, 0]` and `[0, 3, 1, 2, 0]`. |
| Crossover, pair 1 and 3 | `crossover_probability=1.0` | Parents `[0, 3, 1, 2, 0]` and `[0, 2, 1, 3, 0]`; offspring `[0, 2, 1, 3, 0]` and `[0, 3, 1, 2, 0]`. |
| Mutation | `mutation_probability=1.0` for each offspring | New population `[[0, 3, 2, 1, 0], [0, 2, 1, 3, 0], [0, 3, 1, 2, 0], [0, 3, 1, 2, 0]]` |

The two selection operators were compared separately from the roulette-based
generation used for crossover and mutation: each selection call started with
the same seed so its output is directly reproducible.

## What surprised me

Roulette selection selected the same lower-fitness tour three times and did not
select the current best tour in this draw. The best-so-far result remained
available separately as `best_path` / `best_distance`, but the population itself
does not guarantee that its best individual survives selection. The seeded
doctest records the exact selected population and its later crossover and
mutation results.

## Validation

- Baseline: `uv run pytest genetic_algorithm/travelling_salesman_problem.py` — passed; 8 pytest items.
- Baseline direct doctests: `uv run python -m doctest -v genetic_algorithm/travelling_salesman_problem.py` — 39 passed.
- After adding the seeded generation doctest: the same pytest command passed; direct doctests passed (53 examples).
