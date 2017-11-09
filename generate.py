#!/usr/bin/env python

import argparse
import os

import svgwrite

import config as cfg
from Circle import Circle


def configure_argparser():
    parser = argparse.ArgumentParser(
        'Generates a shape by joining lines between anchors on a circle'
    )
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

    return parser


def pixel_to_cm(num):
    # http://www.endmemo.com/sconvert/centimeterpixel.php
    return 0.026458 * num


def main():
    parser = configure_argparser()
    args = parser.parse_args()

    # Create circle and join anchors
    circle = Circle(args.radius, args.anchors)
    for anchor in range(args.anchors):
        circle.join_anchors(anchor, (anchor * args.multiplier) % args.anchors)

    filename = 's{}r{}a{}m{}.svg'.format(args.size,
                                            args.radius,
                                            args.anchors,
                                            args.multiplier)
    image_size_cm = '{}cm'.format(pixel_to_cm(args.size))
    dwg = svgwrite.drawing.Drawing(
        filename=filename,
        size=(image_size_cm, image_size_cm),
        debug=True)
    # viewbox to enable scrolling
    dwg.viewbox(0, 0, args.size, args.size)

    # Normalisation recenters the coordinate axes to the top left
    normalisation = complex(args.size / 2, args.size / 2)
    # Outlining circle
    dwg.add(svgwrite.shapes.Circle(
        center=(normalisation.real, normalisation.imag),
        r=args.radius,
        stroke='black',
        stroke_width=2))
    # Interconnecting lines
    lines_group = dwg.add(dwg.g(stroke_width=1, stroke='red'))
    for start, end in circle.joined_anchors:
        start = circle.coordinates(start) + normalisation
        end = circle.coordinates(end) + normalisation
        lines_group.add(dwg.line(start=(start.real, start.imag), end=(end.real, end.imag)))

    # Output rendered image
    prev_wd = os.getcwd()
    path_to_file = os.path.join(os.getcwd(), 'output')
    try:
        os.chdir(path_to_file)
        with open(filename, 'w', encoding='utf-8') as f:
            dwg.write(f)
    except OSError:
        print('Failed to save image file')
    finally:
        os.chdir(prev_wd)


if __name__ == '__main__':
    main()
