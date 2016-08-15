import functools

import cmath
from cmath import pi


def is_close(a, b, *, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class Circle:
    def __init__(self, radius, num_anchors, EPS):
        self.radius = radius
        self.num_anchors = num_anchors
        self.EPS = EPS
        self.joined_anchors = []

    def join_anchors(self, start, end):
        pairing = [start, end]
        pairing.sort()
        if pairing not in self.joined_anchors:
            self.joined_anchors.append(tuple(pairing))

    @functools.lru_cache(maxsize=False)
    def _get_anchor(self, offset):
        return cmath.rect(self.radius, 2 * pi / self.num_anchors * offset)

    @functools.lru_cache(maxsize=False)
    def _anchor_distance(self, start, end):
        return abs(self._get_anchor(start) - self._get_anchor(end))

    def on_circumference(self, external_point):
        return is_close(abs(external_point), self.radius, rel_tol=self.EPS)

    def on_line(self, external_point):
        for start, end in self.joined_anchors:
            # Triangle inequality
            triangle_base = self._anchor_distance(start, end)
            arm_1 = abs(self._get_anchor(start) - external_point)
            arm_2 = abs(self._get_anchor(end) - external_point)
            if is_close(triangle_base, arm_1 + arm_2, rel_tol=self.EPS / 250):
                return True
        return False
