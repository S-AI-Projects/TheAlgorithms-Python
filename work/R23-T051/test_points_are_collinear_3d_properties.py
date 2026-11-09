from hypothesis import assume, given, settings, strategies as st

from maths.points_are_collinear_3d import are_collinear

coord = st.integers(-1000, 1000)
point = st.tuples(coord, coord, coord)
scalar = st.integers(-100, 100)
fcoord = st.floats(-100, 100, allow_nan=False, allow_infinity=False)
fpoint = st.tuples(fcoord, fcoord, fcoord)
fscalar = st.floats(-10, 10, allow_nan=False, allow_infinity=False)


def cross(u, w):
    return (
        u[1] * w[2] - u[2] * w[1],
        u[2] * w[0] - u[0] * w[2],
        u[0] * w[1] - u[1] * w[0],
    )


@settings(max_examples=2000)
@given(a=point, v=point, t=scalar, s=scalar)
def test_points_on_a_line_are_collinear_exact(a, v, t, s):
    b = tuple(a[i] + t * v[i] for i in range(3))
    c = tuple(a[i] + s * v[i] for i in range(3))
    assert are_collinear(a, b, c)


@settings(max_examples=2000)
@given(a=fpoint, v=fpoint, t=fscalar, s=fscalar)
def test_points_on_a_line_are_collinear_float(a, v, t, s):
    b = tuple(a[i] + t * v[i] for i in range(3))
    c = tuple(a[i] + s * v[i] for i in range(3))
    assert are_collinear(a, b, c, accuracy=6)


@settings(max_examples=2000)
@given(a=point, v=point, w=point, t=scalar, s=scalar)
def test_perturbed_points_are_not_collinear(a, v, w, t, s):
    assume(cross(v, w) != (0, 0, 0))
    assume(t != 0)
    b = tuple(a[i] + t * v[i] for i in range(3))
    c = tuple(a[i] + s * v[i] + w[i] for i in range(3))
    assert not are_collinear(a, b, c)
