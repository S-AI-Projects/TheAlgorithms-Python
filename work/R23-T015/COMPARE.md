# Task R23-T015: Comparison of Geodetic Distance Implementations

## 1. Overview
This report compares two geographical distance implementations in `geodesy/`:
- `geodesy/haversine_distance.py`: Great-circle distance on a spherical Earth of constant mean radius $R = 6,371,000$ m.
- `geodesy/lamberts_ellipsoidal_distance.py`: Distance on an oblate ellipsoid using Lambert's formula with WGS-84 parameters ($a = 6,378,137.0$ m, $b = 6,356,752.314245$ m, flattening $f \approx 1/298.257$).

## 2. API Differences
| Feature | `haversine_distance` | `lamberts_ellipsoidal_distance` |
|---|---|---|
| **Parameters** | `lat1, lon1, lat2, lon2: float` | `lat1, lon1, lat2, lon2: float` |
| **Input Validation** | None (silently computes out-of-bounds angles) | Strict bounds check: $-90 \le \text{lat} \le 90$, $-180 \le \text{lon} \le 180$ (raises `ValueError`) |
| **Return Type** | `float` (distance in meters) | `float` (distance in meters) |
| **Earth Model** | Mean sphere ($R = 6,371$ km) | WGS-84 oblate ellipsoid |

## 3. Results on 10 Worldwide City Pairs

| Pair | Haversine (km) | Lambert (km) | Diff (km) | Diff (%) |
|---|---|---|---|---|
| **San Francisco $\rightarrow$ Yosemite** | 253.257 | 253.540 | 0.283 | 0.112% |
| **New York $\rightarrow$ Los Angeles** | 3935.746 | 3939.694 | 3.948 | 0.100% |
| **London $\rightarrow$ Paris** | 343.556 | 343.591 | 0.035 | 0.010% |
| **Tokyo $\rightarrow$ Sydney** | 7825.819 | 7811.966 | 13.853 | 0.177% |
| **Cairo $\rightarrow$ Cape Town** | 7239.247 | 7226.306 | 12.941 | 0.179% |
| **Moscow $\rightarrow$ Beijing** | 5793.800 | 5798.624 | 4.824 | 0.083% |
| **Reykjavik $\rightarrow$ Oslo** | 1747.046 | 1748.879 | 1.834 | 0.105% |
| **Singapore $\rightarrow$ Nairobi** | 7454.949 | 7463.262 | 8.313 | 0.111% |
| **Buenos Aires $\rightarrow$ Rio de Janeiro** | 1967.773 | 1967.760 | 0.013 | 0.001% |
| **Mumbai $\rightarrow$ Dubai** | 1935.090 | 1936.562 | 1.473 | 0.076% |

## 4. Explanation: Sphere vs WGS-84 Ellipsoid
Because the Earth rotates, centrifugal force causes it to bulge at the equator and flatten at the poles:
- Equatorial radius: $a = 6,378.137$ km
- Polar radius: $b = 6,356.752$ km (difference of $\approx 21.385$ km)

The Haversine formula adopts a single compromise radius ($R = 6,371$ km).
- On routes traversing significant changes in latitude (e.g. **Tokyo $\rightarrow$ Sydney** spanning $35.68^\circ\text{N}$ to $33.87^\circ\text{S}$, or **Cairo $\rightarrow$ Cape Town** spanning $30.04^\circ\text{N}$ to $33.92^\circ\text{S}$), the spherical assumption accumulates an error of up to $13.85$ km ($0.18\%$).
- For shorter distances (e.g. **London $\rightarrow$ Paris** at $343.56$ km), the difference is negligible ($35$ meters or $0.010\%$).

## 5. Performance Benchmark
Benchmark run across 10,000 evaluations (100,000 pairwise calculations):
- `haversine_distance`: $0.40\ \mu\text{s}$ per call
- `lamberts_ellipsoidal_distance`: $1.55\ \mu\text{s}$ per call
- **Speed Ratio**: Haversine is approximately **$3.9\times$ faster**.

## 6. Recommendation for Beginners
- For **beginners, educational applications, games, or general mapping search** (e.g., finding stores within a 10 km radius), **Haversine** is recommended. The formula is compact, intuitive, $4\times$ faster, and its $\le 0.5\%$ error is imperceptible for everyday local use.
- For **aviation navigation, geodesy, marine routing, and satellite tracking**, **Lambert's formula** (or Vincenty's formulae) is necessary to avoid multi-kilometer navigation drift over intercontinental trajectories.
