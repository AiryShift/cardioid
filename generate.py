import argparse
from Circle import Circle
import config as cfg
import numpy as np
from PIL import Image
import cmath
import time


def configure_argparser():
    parser = argparse.ArgumentParser('Generates a shape')
    parser.add_argument(
        '-s', '--size',
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
    start_time = time.time()

    # Create circle and join anchors
    circle = Circle(args.radius, args.anchors, args.epsilon)
    for anchor in range(args.anchors):
        circle.join_anchors(anchor, (anchor * args.multiplier) % args.anchors)

    image_array = np.zeros((args.size, args.size, 3), 'uint8')
    centre = complex(args.size / 2, args.size / 2)
    for i in range(args.size):
        if not i % 20:
            print('i={}, running time={}'.format(i, time.time() - start_time))
        normalised_point = complex(0, i) - centre
        for j in range(args.size):
            if circle.on_circumference(normalised_point):
                image_array[j, i, :] = 255
            elif circle.on_line(normalised_point):
                image_array[j, i, 0] = 255
            normalised_point += 1

    # Output rendered image
    image = Image.fromarray(image_array)
    image.save(cfg.OUT_FILE)

    print('Took {} seconds'.format(time.time() - start_time))

if __name__ == '__main__':
    main()
