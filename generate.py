import argparse
from Circle import Circle
import config as cfg
import numpy as np


def configure_argparser():
    parser = argparse.ArgumentParser('Generates a shape')
    parser.add_argument(
        '-s', '--image-size',
        type=int,
        default=cfg.IMAGE_SIZE,
        help='Pixel width and height of output image'
    )
    parser.add_argument(
        '-r', '--radius',
        type=float,
        default=cfg.RADIUS,
        help='Radius of the circle used'
    )
    parser.add_argument(
        '-e', '--epsilon',
        type=float,
        default=cfg.EPS,
        help='Default float precision'
    )
    parser.add_argument(
        '-a', '--anchors',
        type=int,
        default=cfg.ANCHORS,
        help='Number of anchors draw lines to'
    )
    parser.add_argument(
        '-m', '--multiplier',
        type=int,
        default=cfg.MULTIPLIER,
        help='Determines anchor to join to'
    )

    return parser.parse_args()


def main():
    args = configure_argparser()
    circle = Circle(args.radius, args.anchors, args.epsilon)
    for anchor in range(args.anchors):
        circle.join_anchors(anchor, (anchor * args.multiplier) % args.anchors)

if __name__ == '__main__':
    main()
