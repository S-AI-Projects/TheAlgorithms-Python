# Execution Trace of Neville's Algorithm: `maths/numerical_analysis/nevilles_method.py` (R23-T004)

## 1. Overview and Problem Definition
Neville's algorithm is a recursive polynomial interpolation method that computes the value of an interpolating polynomial $P(x)$ at an evaluation point $x_0$ given $n$ data points $(x_0, y_0), \dots, (x_{n-1}, y_{n-1})$.

We trace the doctest execution:
```python
neville_interpolate(x_points=(1, 2, 3, 4, 6), y_points=(6, 7, 8, 9, 11), x0=5)
```

Input variables:
- $n = 5$
- `x_points` = `(1, 2, 3, 4, 6)`
- `y_points` = `(6, 7, 8, 9, 11)`
- `x0` = `5`

---

## 2. Complete Returned Neville Table $q[i][j]$

The function initializes an $n \times n$ matrix $q$ and returns:
```python
[[0, 6, 0, 0, 0],
 [0, 7, 0, 0, 0],
 [0, 8, 10.0, 0, 0],
 [0, 9, 10.0, 10.0, 0],
 [0, 11, 10.0, 10.0, 10.0]]
```

### Table Representation: $q[j][i]$ (Rows = $j$, Columns = $i$)

| $j$ | $x_j$ | $y_j$ | Col 0 (`q[j][0]`) | Col 1 (`q[j][1]`) | Col 2 (`q[j][2]`) | Col 3 (`q[j][3]`) | Col 4 (`q[j][4]`) |
|:---:|:-----:|:-----:|:-----------------:|:-----------------:|:-----------------:|:-----------------:|:-----------------:|
| 0 | 1 | 6 | 0 | 6 | 0 | 0 | 0 |
| 1 | 2 | 7 | 0 | 7 | 0 | 0 | 0 |
| 2 | 3 | 8 | 0 | 8 | 10.0 | 0 | 0 |
| 3 | 4 | 9 | 0 | 9 | 10.0 | 10.0 | 0 |
| 4 | 6 | 11 | 0 | 11 | 10.0 | 10.0 | 10.0 |

Final interpolated value at $x_0 = 5$:
$$q[n-1][n-1] = q[4][4] = 10.0$$

---

## 3. Step-by-Step Execution Trace

### Phase 1: Table Initialization
- `q` is initialized to a $5 \times 5$ grid of zeroes.
- For each $i \in [0, 4]$, `q[i][1] = y_points[i]`:
  - `q[0][1] = 6`
  - `q[1][1] = 7`
  - `q[2][1] = 8`
  - `q[3][1] = 9`
  - `q[4][1] = 11`
- *Note*: Column 0 (`q[i][0]`) is left entirely as `0`.

---

### Phase 2: Neville Recurrence
The recurrence relation implemented in the code is:
$$q[j][i] = \frac{(x_0 - x_{j-i+1}) \cdot q[j][i-1] - (x_0 - x_j) \cdot q[j-1][i-1]}{x_j - x_{j-i+1}}$$

#### Detailed Step-by-Step Table:

| Step | Col ($i$) | Row ($j$) | $x_j$ | $x_{j-i+1}$ | $q[j][i-1]$ | $q[j-1][i-1]$ | Numerator Calculation | Denominator ($x_j - x_{j-i+1}$) | Computed $q[j][i]$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|:---:|
| **1** | 2 | 2 | 3 | 2 | 8 | 7 | $(5 - 2) \cdot 8 - (5 - 3) \cdot 7 = 24 - 14 = 10$ | $3 - 2 = 1$ | **10.0** |
| **2** | 2 | 3 | 4 | 3 | 9 | 8 | $(5 - 3) \cdot 9 - (5 - 4) \cdot 8 = 18 - 8 = 10$ | $4 - 3 = 1$ | **10.0** |
| **3** | 2 | 4 | 6 | 4 | 11 | 9 | $(5 - 4) \cdot 11 - (5 - 6) \cdot 9 = 11 - (-9) = 20$ | $6 - 4 = 2$ | **10.0** |
| **4** | 3 | 3 | 4 | 2 | 10.0 | 10.0 | $(5 - 2) \cdot 10.0 - (5 - 4) \cdot 10.0 = 30 - 10 = 20.0$ | $4 - 2 = 2$ | **10.0** |
| **5** | 3 | 4 | 6 | 3 | 10.0 | 10.0 | $(5 - 3) \cdot 10.0 - (5 - 6) \cdot 10.0 = 20 - (-10) = 30.0$ | $6 - 3 = 3$ | **10.0** |
| **6** | 4 | 4 | 6 | 2 | 10.0 | 10.0 | $(5 - 2) \cdot 10.0 - (5 - 6) \cdot 10.0 = 30 - (-10) = 40.0$ | $6 - 2 = 4$ | **10.0** |

---

## 4. Key Observations and Surprises

### 1. The Discarded First Point (`x_points[0]`, `y_points[0]`)
The most significant finding during debugger tracing is that **the first data point $(x_0, y_0) = (1, 6)$ is never used in the calculation**:
- In the recurrence loops, $i$ ranges from $2$ to $n-1$, and $j$ ranges from $i$ to $n-1$.
- The lowest row index accessed is $j - 1$. Since $j \ge i \ge 2$, the minimum value of $j - 1$ is $1$.
- Thus, `q[0][1]` is never read!
- Similarly, the index $j - i + 1 \ge 1$, so `x_points[0]` is never read either.
- Changing `(x_points[0], y_points[0])` from `(1, 6)` to `(9999, 9999)` produces the exact same final result (`10.0`). This is a 1-based indexing transcription artifact from textbook pseudocode.

### 2. Collinear Points Yield Constant 10.0
The test dataset points $(2, 7), (3, 8), (4, 9), (6, 11)$ all satisfy the linear relation:
$$y = x + 5$$
Since a unique linear polynomial passes through all collinear points, any polynomial interpolation of degree $\ge 1$ across these points will reproduce $P(x) = x + 5$. At $x_0 = 5$, $P(5) = 5 + 5 = 10.0$, causing every intermediate calculation in columns 2, 3, and 4 to yield exactly $10.0$.

### 3. Edge Case: Duplicate X-Coordinates
If two $x$-coordinates are identical (e.g. `x_points = (1, 2, 2)`), Neville's formula divides by $(x_j - x_{j-i+1})$. When $x_j = x_{j-i+1}$, this evaluates to zero, immediately triggering a `ZeroDivisionError: division by zero`.

---

## 5. Doctests Added to Code

Based on the execution trace, the following doctests were added to `maths/numerical_analysis/nevilles_method.py`:
1. Intermediate table value at $q[1][1]$:
   ```python
   >>> neville_interpolate((1, 2, 3, 4, 6), (6, 7, 8, 9, 11), 5)[1][1][1]
   7
   ```
2. Intermediate table value at $q[2][2]$:
   ```python
   >>> neville_interpolate((1, 2, 3, 4, 6), (6, 7, 8, 9, 11), 5)[1][2][2]
   10.0
   ```
3. Error edge case for duplicate $x$ points:
   ```python
   >>> neville_interpolate((1, 2, 2), (3, 4, 5), 2)
   Traceback (most recent call last):
       ...
   ZeroDivisionError: division by zero
   ```
All 5 original doctests remain intact and continue to pass.
