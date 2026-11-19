"""
Find the relativistic kinetic energy of a particle, given its rest mass and velocity.

Description:
In special relativity, the kinetic energy of a particle is the extra energy
it possesses due to its motion beyond the energy associated with its rest mass.
It is defined as the difference between total relativistic energy and rest energy:

    KE = (gamma - 1) * m * c^2

where:
- KE: Relativistic kinetic energy in Joules (J).
- mass (m): Rest mass of the body in kilograms (kg), where m >= 0.
- velocity (v): Speed of the body relative to observer in meters per second (m/s).
- c: Speed of light in vacuum (299,792,458 m/s).
- gamma: The dimensionless Lorentz factor, defined as:
      gamma = 1 / sqrt(1 - v^2 / c^2)

At non-relativistic velocities (v << c), applying a first-order Taylor expansion
(1 - v^2 / c^2)^(-1/2) approx 1 + 1/2 * (v^2 / c^2) reveals that the relativistic
formula reduces to the classical Newtonian kinetic energy:

    KE approx (1/2) * m * v^2

Reference:
    https://en.wikipedia.org/wiki/Kinetic_energy#Relativistic_kinetic_energy_of_rigid_bodies
"""

from math import sqrt

from scipy.constants import c  # speed of light in vacuum (299792458 m/s)


def relativistic_kinetic_energy(mass: float, velocity: float) -> float:
    """
    Calculate relativistic kinetic energy.
    mass --- kg
    velocity ---- m/s
    K.E ---- j

    >>> relativistic_kinetic_energy(10,10)
    598.6912157608277
    >>> relativistic_kinetic_energy(40,200000)
    800000266962.5057
    >>> relativistic_kinetic_energy(50,100000)
    250000021062.11475
    >>> relativistic_kinetic_energy(0,0)
    0.0
    >>> relativistic_kinetic_energy(100,0)
    0.0
    >>> v = 1.0
    >>> m = 2.0
    >>> ke = relativistic_kinetic_energy(m, v)
    >>> classical_ke = 0.5 * m * v**2
    >>> abs(ke - classical_ke) / classical_ke < 1e-9
    True

    """

    if mass < 0:
        raise ValueError("The mass of a body cannot be negative")
    if abs(velocity) <= 1:
        return 0.5 * mass * velocity**2
    gamma = 1 / sqrt(1 - (velocity**2 / c**2))
    return (gamma - 1) * mass * c**2


if __name__ == "__main__":
    import doctest

    doctest.testmod()
