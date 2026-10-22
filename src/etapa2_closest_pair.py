import math
from typing import List, Tuple, Optional

Point = Tuple[float, float]


def euclidean_distance(p1: Point, p2: Point) -> float:
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.hypot(dx, dy)


def closest_pair_brute_force(points: List[Point]) -> Tuple[float, Optional[Tuple[Point, Point]]]:
    n = len(points)
    if n < 2:
        return float('inf'), None

    min_dist = float('inf')
    best_pair = None

    for i in range(n):
        p_i = points[i]
        for j in range(i + 1, n):
            p_j = points[j]
            d = euclidean_distance(p_i, p_j)
            if d < min_dist:
                min_dist = d
                best_pair = (p_i, p_j)

    return min_dist, best_pair


def _closest_pair_rec(
    px: List[Tuple[float, float, int]],
    py: List[Tuple[float, float, int]],
    threshold: int = 3
) -> Tuple[float, Optional[Tuple[Point, Point]]]:
    n = len(px)

    if n <= threshold:
        pts = [(p[0], p[1]) for p in px]
        return closest_pair_brute_force(pts)

    mid = n // 2
    mid_point = px[mid]
    mid_x = mid_point[0]

    qx = px[:mid]
    rx = px[mid:]

    left_ids = {p[2] for p in qx}

    qy = [p for p in py if p[2] in left_ids]
    ry = [p for p in py if p[2] not in left_ids]

    d1, pair1 = _closest_pair_rec(qx, qy, threshold=threshold)
    d2, pair2 = _closest_pair_rec(rx, ry, threshold=threshold)

    if d1 <= d2:
        delta = d1
        best_pair = pair1
    else:
        delta = d2
        best_pair = pair2

    strip = [p for p in py if abs(p[0] - mid_x) < delta]
    strip_len = len(strip)

    for i in range(strip_len):
        p_i = (strip[i][0], strip[i][1])
        limit = min(i + 8, strip_len)
        for j in range(i + 1, limit):
            if (strip[j][1] - strip[i][1]) >= delta:
                break
            p_j = (strip[j][0], strip[j][1])
            d = euclidean_distance(p_i, p_j)
            if d < delta:
                delta = d
                best_pair = (p_i, p_j)

    return delta, best_pair


def closest_pair_divide_conquer(
    points: List[Point],
    threshold: int = 3
) -> Tuple[float, Optional[Tuple[Point, Point]]]:
    n = len(points)
    if n < 2:
        return float('inf'), None

    pts_with_id = [(float(pt[0]), float(pt[1]), idx) for idx, pt in enumerate(points)]

    px = sorted(pts_with_id, key=lambda p: (p[0], p[1]))
    py = sorted(pts_with_id, key=lambda p: (p[1], p[0]))

    return _closest_pair_rec(px, py, threshold=threshold)
