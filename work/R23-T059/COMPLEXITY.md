# R23-T059: expected vs measured cost of `blockchain/simple_proof_of_work.py`

## 1. Expected complexity (derivation)
`proof_of_work` tries nonce = 0, 1, 2, ... until `sha256(block + transactions + previous_hash + nonce)`
starts with `difficulty` zeros.
- A hex digit of a SHA-256 hash is "0" with probability 1/16, and the digits behave like independent random digits, so one attempt succeeds with probability **p = 16^-difficulty**.
- The number of attempts until the first success is **geometric**: expected value `1/p = 16^difficulty`, standard deviation about the same (`sqrt(1-p)/p`).
- Each attempt does a fixed amount of work (format a short string, one SHA-256), so the expected time is **O(16^difficulty) = O(2^(4*difficulty))**, space **O(1)**. Each extra leading zero multiplies the expected work by **16**.

## 2. Method (`work/R23-T059/bench.py`)
- Difficulty 0 to 5 (6 levels). `attempts = nonce + 1`; time measured per call with `timeit.timeit(..., number=1)`.
- The function is deterministic (same input -> same nonce), so each run uses a different block number (0, 1, 2, ...). Attempts are therefore **exactly reproducible on any machine**; times are not.
- Runs per level: 100 / 20000 / 5000 / 1000 / 400 / 60 (cheap levels get many runs because individual runs vary a lot).

## 3. Results
| difficulty | runs | expected 16^d | mean attempts | 95% CI | mean/expected | mean time (s) | us/attempt | attempts x vs previous | time x vs previous |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 1 | 1.0 | 1.0 - 1.0 | 1.0 | 0.000001 | 1.42 | - | - |
| 1 | 20000 | 16 | 16.1 | 15.8 - 16.3 | 1.003 | 0.000010 | 0.60 | 16.1 | 6.8 |
| 2 | 5000 | 256 | 258.7 | 251.5 - 265.8 | 1.01 | 0.000139 | 0.54 | 16.1 | 14.4 |
| 3 | 1000 | 4,096 | 4,254.4 | 3,990.8 - 4,517.9 | 1.039 | 0.002284 | 0.54 | 16.4 | 16.4 |
| 4 | 400 | 65,536 | 64,150.2 | 57,940.0 - 70,360.5 | 0.979 | 0.036135 | 0.56 | 15.1 | 15.8 |
| 5 | 60 | 1,048,576 | 1,077,340.1 | 824,178.3 - 1,330,501.8 | 1.027 | 0.626333 | 0.58 | 16.8 | 17.3 |

(Measured on a cloud Linux machine, Python 3.13. Raw data: `results.csv`; plot: `pow_benchmark.png`.)

## 4. Reading the results
- **Attempts:** the measured mean is within 4% of `16^d` at every level and every 95% interval contains `16^d`. The growth per level is x16.1, x16.1, x16.4, x15.1, x16.8, i.e. about x16.
- **Time:** time per attempt is constant (about 0.54-0.60 microseconds), so time follows attempts: x14.4, x16.4, x15.8, x17.3 per level from difficulty 2 up. The d0 -> d1 time ratio (x6.8) is lower only because one-hash runs are dominated by the fixed cost of the call and the timer, not by hashing.
- **Wide variance:** the standard deviation is about as large as the mean, so a single run can be far from `16^d`, and a small sample can mislead. Difficulty 5 used only 60 runs, so its interval is about +-23%; its x16.8 is consistent with 16 but is not a precise estimate.

## 5. A false alarm worth recording
An earlier pass with 100 runs at difficulty 4 gave a mean of 49,272 (0.75x expected, outside its 95% interval), and 1,000 runs at difficulty 1 gave 14.6 (0.91x). I re-checked before trusting either:
- difficulty 4 with 800 runs: mean 62,610 (0.955x; batches of 100 ranged from 49,272 to 70,790);
- difficulty 1 with 20,000 runs on three different input sets: 16.05, 15.84 and 16.12.

So those were low samples, not a bias in the algorithm. The final table uses larger samples.

## 6. Where it appears in the code
The derivation and the measured attempt counts were added to the docstring of `proof_of_work`; the 7 `>>>` lines of doctests and the `ValueError` for a negative difficulty are unchanged.

## 7. Re-run on my MacBook (same attempts, faster machine)

| difficulty | runs | expected 16^d | mean attempts | 95% CI | mean/expected | mean time (s) | us/attempt | attempts x vs previous | time x vs previous |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 1 | 1.0 | 1.0 - 1.0 | 1.0 | 0.000001 | 0.79 | nan | nan |
| 1 | 20000 | 16 | 16.1 | 15.8 - 16.3 | 1.003 | 0.000004 | 0.28 | 16.1 | 5.6 |
| 2 | 5000 | 256 | 258.7 | 251.5 - 265.8 | 1.01 | 0.000065 | 0.25 | 16.1 | 14.7 |
| 3 | 1000 | 4,096 | 4,254.4 | 3,990.8 - 4,517.9 | 1.039 | 0.001092 | 0.26 | 16.4 | 16.7 |
| 4 | 400 | 65,536 | 64,150.2 | 57,940.0 - 70,360.5 | 0.979 | 0.016539 | 0.26 | 15.1 | 15.1 |
| 5 | 60 | 1,048,576 | 1,077,340.1 | 824,178.3 - 1,330,501.8 | 1.027 | 0.278970 | 0.26 | 16.8 | 16.9 |
