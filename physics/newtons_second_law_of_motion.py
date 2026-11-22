r"""
Description:
    Newton's second law of motion pertains to the behavior of objects for which
    all existing forces are not balanced.
    The second law states that the acceleration of an object is dependent upon
    two variables - the net force acting upon the object and the mass of the object.
    The acceleration of an object depends directly
    upon the net force acting upon the object,
    and inversely upon the mass of the object.
    As the force acting upon an object is increased,
    the acceleration of the object is increased.
    As the mass of an object is increased, the acceleration of the object is decreased.

Source: https://www.physicsclassroom.com/class/newtlaws/Lesson-3/Newton-s-Second-Law

Formulation: F_net = m • a

Diagrammatic Explanation::

              Forces are unbalanced
                        |
                        |
                        |
                        V
               There is acceleration
                        /\
                       /  \
                      /    \
                     /      \
                    /        \
                   /          \
                  /            \
    __________________      ____________________
   | The acceleration |    | The acceleration   |
   | depends directly |    | depends inversely  |
   | on the net force |    | upon the object's  |
   |                  |    | mass               |
   |__________________|    |____________________|

Units: 1 Newton = 1 kg • meters/seconds^2

How to use?

Inputs::

    ______________ _____________________ ___________
   | Name         | Units               | Type      |
   |--------------|---------------------|-----------|
   | mass         | in kgs              | float     |
   |--------------|---------------------|-----------|
   | acceleration | in meters/seconds^2 | float     |
   |______________|_____________________|___________|

Output::

    ______________ _______________________ ___________
   | Name         | Units                 | Type      |
   |--------------|-----------------------|-----------|
   | force        | in Newtons            | float     |
   |______________|_______________________|___________|

"""


def newtons_second_law_of_motion(mass: float, acceleration: float) -> float:
    """
    Calculates force from `mass` and `acceleration` using Newton's second law:
    F = m * a.

    Args:
        mass (float): Mass of the object in kilograms. Must be non-negative.
        acceleration (float): Acceleration of the object in meters/second^2.
            Can be positive, zero, or negative (indicating directional acceleration).

    Returns:
        float: Net force acting on the object in Newtons.

    Raises:
        TypeError: If mass or acceleration is not a numeric value (int or float),
            including boolean values.
        ValueError: If mass is negative.

    Examples:
        >>> newtons_second_law_of_motion(10, 10)
        100
        >>> newtons_second_law_of_motion(2.0, 1)
        2.0
        >>> newtons_second_law_of_motion(0, 10)
        0
        >>> newtons_second_law_of_motion(10, 0)
        0
        >>> newtons_second_law_of_motion(2.0, -9.8)
        -19.6
        >>> newtons_second_law_of_motion(-5, 10)
        Traceback (most recent call last):
        ...
        ValueError: Mass must be a non-negative value
        >>> newtons_second_law_of_motion("10", 10)
        Traceback (most recent call last):
        ...
        TypeError: Mass must be a numeric value (int or float), not str
        >>> newtons_second_law_of_motion(True, 10)
        Traceback (most recent call last):
        ...
        TypeError: Mass must be a numeric value (int or float), not bool
        >>> newtons_second_law_of_motion(10, "10")
        Traceback (most recent call last):
        ...
        TypeError: Acceleration must be a numeric value (int or float), not str
        >>> newtons_second_law_of_motion(10, False)
        Traceback (most recent call last):
        ...
        TypeError: Acceleration must be a numeric value (int or float), not bool
    """
    if isinstance(mass, bool) or not isinstance(mass, (int, float)):
        msg = f"Mass must be a numeric value (int or float), not {type(mass).__name__}"
        raise TypeError(msg)
    if isinstance(acceleration, bool) or not isinstance(acceleration, (int, float)):
        msg = (
            "Acceleration must be a numeric value (int or float), "
            f"not {type(acceleration).__name__}"
        )
        raise TypeError(msg)
    if mass < 0:
        raise ValueError("Mass must be a non-negative value")

    return mass * acceleration


if __name__ == "__main__":  # pragma: no cover
    import doctest

    # run doctest
    doctest.testmod()

    # demo
    mass = 12.5
    acceleration = 10
    force = newtons_second_law_of_motion(mass, acceleration)
    print("The force is ", force, "N")
