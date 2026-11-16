"""Plot ear-clipping triangulations for three polygon shapes."""

# The evidence directory is intentionally not an importable Python package.
# ruff: noqa: INP001

import math
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt

from maths.ear_clipping_polygon_triangulation import triangulate_polygon


def main() -> None:
    """Triangulate the examples, save a figure, and report triangle counts."""
    star_polygon = [
        (
            (3 if index % 2 == 0 else 1.4)
            * math.cos(math.radians(90 + 36 * index)),
            (3 if index % 2 == 0 else 1.4)
            * math.sin(math.radians(90 + 36 * index)),
        )
        for index in range(10)
    ]
    examples = [
        ("Convex", [(0, 0), (4, 0), (4, 3), (0, 3)]),
        ("Concave", [(0, 0), (2, 0), (1, 1), (2, 2), (0, 2)]),
        ("Star-shaped", star_polygon),
    ]
    figure, axes = plt.subplots(1, len(examples), figsize=(13, 4))

    for axis, (name, polygon) in zip(axes, examples, strict=True):
        triangles = triangulate_polygon(polygon)
        assert len(triangles) == len(polygon) - 2

        for triangle_index, triangle in enumerate(triangles):
            triangle_x = [point[0] for point in triangle] + [triangle[0][0]]
            triangle_y = [point[1] for point in triangle] + [triangle[0][1]]
            axis.fill(
                triangle_x,
                triangle_y,
                color=f"C{triangle_index % 10}",
                alpha=0.28,
            )
            axis.plot(triangle_x, triangle_y, color="tab:blue", linewidth=1)

        boundary = [*polygon, polygon[0]]
        axis.plot(
            [point[0] for point in boundary],
            [point[1] for point in boundary],
            color="black",
            marker="o",
            linewidth=2,
        )
        axis.set_title(f"{name}: {len(polygon)} vertices, {len(triangles)} triangles")
        axis.set_aspect("equal", adjustable="datalim")
        axis.grid(alpha=0.2)
        axis.set_xlabel("x")
        axis.set_ylabel("y")
        print(f"{name}: {len(polygon)} vertices -> {len(triangles)} triangles")

    figure.tight_layout()
    output_path = Path(__file__).with_name("triangulations.png")
    figure.savefig(output_path, dpi=180)
    plt.close(figure)
    print(f"Saved figure: {output_path}")


if __name__ == "__main__":
    main()
