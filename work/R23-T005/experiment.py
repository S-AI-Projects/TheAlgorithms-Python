"""
Experiment for R23-T005: Relativistic Kinetic Energy Behavior.
Demonstrates:
1. Convergence to classical KE (1/2 * m * v^2) as v -> 0.
2. Divergence (unbounded growth) of relativistic KE as v -> c.
"""

from math import sqrt
from scipy.constants import c

def relativistic_ke(m: float, v: float) -> float:
    if abs(v) <= 1.0:
        return 0.5 * m * v**2
    gamma = 1 / sqrt(1 - (v**2 / c**2))
    return (gamma - 1) * m * c**2

def classical_ke(m: float, v: float) -> float:
    return 0.5 * m * v**2

def run_experiment() -> None:
    mass = 1.0  # 1 kg particle
    print("=" * 70)
    print("PART 1: Low-Speed Convergence (v -> 0)")
    print(f"Rest mass m = {mass} kg, Speed of light c = {c} m/s")
    print("-" * 70)
    print(f"{'Velocity v (m/s)':<18}{'Relativistic KE (J)':<24}{'Classical 1/2mv^2 (J)':<24}{'Relative Error':<16}")
    print("-" * 70)
    for v in [0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]:
        r_ke = relativistic_ke(mass, v)
        c_ke = classical_ke(mass, v)
        rel_err = abs(r_ke - c_ke) / c_ke if c_ke > 0 else 0.0
        print(f"{v:<18.2f}{r_ke:<24.10e}{c_ke:<24.10e}{rel_err:<16.8e}")

    print("\n" + "=" * 70)
    print("PART 2: Ultra-Relativistic Divergence (v -> c)")
    print("-" * 70)
    print(f"{'Fraction beta = v/c':<22}{'Lorentz Factor gamma':<24}{'Relativistic KE (J)':<24}")
    print("-" * 70)
    betas = [0.1, 0.5, 0.9, 0.99, 0.999, 0.9999, 0.99999, 0.999999, 0.9999999]
    for beta in betas:
        v = beta * c
        gamma = 1 / sqrt(1 - beta**2)
        r_ke = (gamma - 1) * mass * c**2
        print(f"{beta:<22.7f}{gamma:<24.6e}{r_ke:<24.10e}")

if __name__ == "__main__":
    run_experiment()
