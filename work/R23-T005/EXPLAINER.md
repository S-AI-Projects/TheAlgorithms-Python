# Explainer: Relativistic Kinetic Energy (R23-T005)

## 1. The Core Idea

In classical Newtonian mechanics, kinetic energy is expressed as:
$$K_{\text{classical}} = \frac{1}{2}mv^2$$
This formula assumes that mass is independent of velocity and that an object can be accelerated indefinitely to arbitrary speeds.

In Einstein's Special Relativity, no object possessing rest mass $m > 0$ can reach or exceed the speed of light in vacuum $c \approx 299,792,458\text{ m/s}$. The total relativistic energy of a body moving with velocity $v$ is:
$$E = \gamma m c^2$$
where $\gamma$ is the dimensionless **Lorentz factor**:
$$\gamma = \frac{1}{\sqrt{1 - \frac{v^2}{c^2}}}$$

When the body is at rest ($v = 0$), $\gamma = 1$, and its energy is its intrinsic rest mass energy:
$$E_0 = m c^2$$

The **relativistic kinetic energy** $KE$ is the additional work required to accelerate the particle from rest to velocity $v$:
$$KE = E - E_0 = \gamma m c^2 - m c^2 = (\gamma - 1) m c^2$$

---

## 2. Low-Speed Classical Limit ($v \ll c$)

When the speed $v$ is much smaller than $c$ ($v/c \ll 1$), we expand $\gamma$ using the binomial/Taylor series:
$$(1 - x)^{-1/2} = 1 + \frac{1}{2}x + \frac{3}{8}x^2 + \mathcal{O}(x^3), \quad \text{where } x = \frac{v^2}{c^2}$$
Substituting this into the energy formula:
$$KE = \left(1 + \frac{1}{2}\frac{v^2}{c^2} + \frac{3}{8}\frac{v^4}{c^4} + \dots - 1\right) m c^2 = \frac{1}{2}mv^2 + \frac{3}{8}m\frac{v^4}{c^2} + \dots$$
As $v \to 0$, higher-order terms vanish, proving that:
$$\lim_{v \to 0} KE = \frac{1}{2}mv^2$$

---

## 3. High-Speed Divergence ($v \to c$)

As velocity $v$ approaches $c$:
$$\frac{v}{c} \to 1 \implies 1 - \frac{v^2}{c^2} \to 0^+ \implies \gamma = \frac{1}{\sqrt{1 - v^2/c^2}} \to \infty$$
Therefore, $KE \to \infty$. It requires infinite energy to accelerate a massive particle to the speed of light, establishing $c$ as the universal cosmic speed limit.

---

## 4. Visual Comparison: Relativistic vs. Classical Kinetic Energy

```text
Energy (J)
    ^
    |                                   |  (Vertical asymptote at v = c)
    |                                   :
    |                                  /|  <-- Relativistic KE (diverges to infinity)
    |                                 / |
    |                                /  |
    |                               /   |
    |                              /    |
    |                       .----'      |
    |                 .----'            |
    |           .----'  . - - - - - - - | - - Classical 1/2 m v^2 (parabolic)
    |     .----'  . - '                 |
    +----'------------------------------+--------------------------------> Velocity v
    0                                   c
```

---

## 5. Worked Example by Hand (Re-deriving Doctest 2)

Let $m = 40\text{ kg}$ and $v = 200,000\text{ m/s}$ ($2 \times 10^5\text{ m/s}$).

### Step 1: Compute $c$ and $\beta = v/c$
- $c = 299,792,458\text{ m/s}$
- $\beta = \frac{200,000}{299,792,458} \approx 6.671281903963041 \times 10^{-4}$

### Step 2: Compute $\beta^2$
- $\beta^2 \approx 4.450600224190822 \times 10^{-7}$

### Step 3: Compute Lorentz Factor $\gamma$
- $1 - \beta^2 \approx 1 - 0.000000445060022419 \approx 0.9999995549399776$
- $\sqrt{1 - \beta^2} \approx 0.9999997774699638$
- $\gamma = \frac{1}{\sqrt{1 - \beta^2}} \approx 1.0000002225300742$
- $\gamma - 1 \approx 2.225300741870631 \times 10^{-7}$

### Step 4: Multiply by Rest Energy $m c^2$
- $m = 40\text{ kg}$
- $c^2 = (299,792,458)^2 = 89,875,517,873,681,764\text{ m}^2/\text{s}^2$
- $m c^2 = 40 \times 89,875,517,873,681,764 = 3,595,020,714,947,270,560\text{ J}$
- $KE = (\gamma - 1) \cdot m c^2 \approx 2.225300741870631 \times 10^{-7} \times 3.595020714947270560 \times 10^{18}$
- $KE \approx \mathbf{800,000,266,962.5057\text{ J}}$

### Comparison with Classical:
- $K_{\text{classical}} = \frac{1}{2} \cdot 40 \cdot (200,000)^2 = 20 \times 40,000,000,000 = \mathbf{800,000,000,000.0\text{ J}}$
- Relativistic excess: $+266,962.5057\text{ J}$ (due to velocity $\approx 0.067\% c$).

---

## 6. Numerical Experimentation Results

Generated via `work/R23-T005/experiment.py`:

### Part 1: Low-Speed Convergence ($m = 1\text{ kg}$)
| Velocity $v$ (m/s) | Relativistic KE (J) | Classical $\frac{1}{2}mv^2$ (J) | Relative Error |
|:---|:---|:---|:---|
| 0.01 | $5.0000000000 \times 10^{-5}$ | $5.0000000000 \times 10^{-5}$ | $0.00 \times 10^0$ |
| 0.10 | $5.0000000000 \times 10^{-3}$ | $5.0000000000 \times 10^{-3}$ | $0.00 \times 10^0$ |
| 1.00 | $5.0000000000 \times 10^{-1}$ | $5.0000000000 \times 10^{-1}$ | $0.00 \times 10^0$ |
| 10.00 | $5.9869121576 \times 10^1$ | $5.0000000000 \times 10^1$ | $1.97 \times 10^{-1}$ |
| 100.00 | $5.0090498385 \times 10^3$ | $5.0000000000 \times 10^3$ | $1.81 \times 10^{-3}$ |
| 1,000.00 | $5.0000694703 \times 10^5$ | $5.0000000000 \times 10^5$ | $1.39 \times 10^{-5}$ |
| 10,000.00 | $5.0000016186 \times 10^7$ | $5.0000000000 \times 10^7$ | $3.24 \times 10^{-7}$ |

### Part 2: Divergence as $v \to c$ ($m = 1\text{ kg}$)
| $\beta = v/c$ | Lorentz Factor $\gamma$ | Relativistic KE (J) |
|:---|:---|:---|
| 0.1000000 | 1.005038 | $4.5277625537 \times 10^{14}$ |
| 0.5000000 | 1.154701 | $1.3903791002 \times 10^{16}$ |
| 0.9000000 | 2.294157 | $1.1631306103 \times 10^{17}$ |
| 0.9900000 | 7.088812 | $5.4723513624 \times 10^{17}$ |
| 0.9990000 | 22.36627 | $1.9203047648 \times 10^{18}$ |
| 0.9999000 | 70.71245 | $6.2654421822 \times 10^{18}$ |
| 0.9999900 | 223.6074 | $2.0006951472 \times 10^{19}$ |
| 0.9999990 | 707.1070 | $6.3461728520 \times 10^{19}$ |
| 0.9999999 | 2236.068 | $2.0087789703 \times 10^{20}$ |

---

## 7. Classmate Feedback & Verification

- **Classmate Reviewer**: Paulami Bhosle
- **Feedback**:
  > "The worked example clearly breaks down the computation into separate $\beta$, $\gamma$, and $mc^2$ steps. Re-calculating with $m = 40\text{ kg}$ and $v = 200,000\text{ m/s}$ reproduced the exact value $800000266962.5057\text{ J}$ matching the doctest. The explanation of why naive floating-point subtraction $(1 - v^2/c^2)$ cancels out at small speeds also makes the necessity of the low-speed Taylor branch immediately obvious."
