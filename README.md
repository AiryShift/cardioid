# Cardioid Generator

Among other images... It's pretty I swear!

## How It Works

1. Draw a circle.

1. Choose a positive, large integer `N`. 100 is a good value for `N`.

1. Mark `N` distinct points around the circumfrence, evenly spaced.

1. Choose a starting point. Index this point as `0`.

1. Continue indexing points, incrementing by one each time and going either clockwise or anticlockwise, until all points are indexed.
    For example, point clockwise of point `0` would be indexed `1`, and the one clockwise of that would be indexed `2`.

1. Choose a positive integer in the range `2..N - 1`. Call it `m`.

1. For each of the `N` points, join the point with index `k` to the point with index `(k * m) % N` with a line.

## Example Image

![](https://cdn.rawgit.com/AiryShift/cardioid/05b39bfc4de95dc0f8b6b02c7e06d0c92c234b41/output/s1200r550e0.01a200m2v2.svg)
