import functools

import cmath
from cmath import pi


class Circle:
    def __init__(self, radius, num_anchors):
        self.radius = radius
        self.num_anchors = num_anchors
        self.joined_anchors = []

    def join_anchors(self, start, end):
        pairing = sorted([start, end])
        if pairing not in self.joined_anchors:
            self.joined_anchors.append(tuple(pairing))

    @functools.lru_cache(maxsize=False)
    def coordinates(self, offset):
        return cmath.rect(self.radius, 2 * pi / self.num_anchors * offset)
