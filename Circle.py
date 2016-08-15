import cmath
import functools


def is_close(a, b, *, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class Circle:
    def __init__(self, radius, num_anchors, EPS):
        self.radius = radius
        self.num_anchors = num_anchors
        self.EPS = EPS
        self.joined_anchors = set()

    def join_anchors(self, start, end):
        pairing = [start, end]
        pairing.sort()
        self.joined_anchors.add(tuple(pairing))

    @functools.lru_cache(maxsize=False)
    def _get_anchor(self, offset):
        return cmath.rect(self.radius, 2 * cmath.pi / self.num_anchors * offset)

    @functools.lru_cache(maxsize=False)
    def _anchor_distance(self, start, end):
        return abs(self._get_anchor(start) - self._get_anchor(end))

    def on_circumference(self, external_point):
        return is_close(abs(external_point), self.radius, rel_tol=self.EPS)

    def on_line(self, external_point):
        for start, end in self.joined_anchors:
            if is_close(self._anchor_distance(start, end), external_point, rel_tol=self.EPS):
                return True
        return False
