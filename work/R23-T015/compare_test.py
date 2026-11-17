"""Comparison test between haversine_distance and lamberts_ellipsoidal_distance (Task R23-T015)."""

import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from geodesy.haversine_distance import haversine_distance
from geodesy.lamberts_ellipsoidal_distance import lamberts_ellipsoidal_distance

CITY_PAIRS = [
    ("San Francisco", (37.7749, -122.4194), "Yosemite", (37.8651, -119.5383)),
    ("New York", (40.7128, -74.0060), "Los Angeles", (34.0522, -118.2437)),
    ("London", (51.5074, -0.1278), "Paris", (48.8566, 2.3522)),
    ("Tokyo", (35.6762, 139.6503), "Sydney", (-33.8688, 151.2093)),
    ("Cairo", (30.0444, 31.2357), "Cape Town", (-33.9249, 18.4241)),
    ("Moscow", (55.7558, 37.6173), "Beijing", (39.9042, 116.4074)),
    ("Reykjavik", (64.1466, -21.9426), "Oslo", (59.9139, 10.7522)),
    ("Singapore", (1.3521, 103.8198), "Nairobi", (-1.2921, 36.8219)),
    ("Buenos Aires", (-34.6037, -58.3816), "Rio de Janeiro", (-22.9068, -43.1729)),
    ("Mumbai", (19.0760, 72.8777), "Dubai", (25.2048, 55.2708)),
]


@pytest.mark.parametrize("c1, coords1, c2, coords2", CITY_PAIRS)
def test_city_pair_comparison(c1, coords1, c2, coords2):
    lat1, lon1 = coords1
    lat2, lon2 = coords2

    h_m = haversine_distance(lat1, lon1, lat2, lon2)
    l_m = lamberts_ellipsoidal_distance(lat1, lon1, lat2, lon2)

    diff_m = abs(h_m - l_m)
    diff_pct = (diff_m / l_m) * 100

    # Spherical Earth model typically agrees within 0.3% - 0.5% of WGS-84 ellipsoid
    assert diff_pct < 0.5, f"{c1} -> {c2} difference {diff_pct:.3f}% exceeds 0.5%"


def generate_comparison_table():
    print(
        f"| {'Pair':<33} | {'Haversine (km)':<15} | {'Lambert (km)':<15} | {'Diff (km)':<10} | {'Diff (%)':<10} |"
    )
    print(
        "|"
        + "-" * 35
        + "|"
        + "-" * 17
        + "|"
        + "-" * 17
        + "|"
        + "-" * 12
        + "|"
        + "-" * 12
        + "|"
    )
    for c1, (lat1, lon1), c2, (lat2, lon2) in CITY_PAIRS:
        h = haversine_distance(lat1, lon1, lat2, lon2) / 1000.0
        l = lamberts_ellipsoidal_distance(lat1, lon1, lat2, lon2) / 1000.0
        diff = abs(h - l)
        pct = (diff / l) * 100
        print(
            f"| {f'{c1} -> {c2}':<33} | {h:<15.3f} | {l:<15.3f} | {diff:<10.3f} | {pct:<9.3f}% |"
        )


if __name__ == "__main__":
    generate_comparison_table()
