#!/usr/bin/env python
"""A simple utility that quantizes JPEG images.

For simplicity, the output is represented in greyscale.
"""

__author__ = 'Aryan Naraghi (aryan.naraghi@gmail.com)'

import argparse
import Image
import ImageOps
import sys


def power_of_two(value):
    float_res = float(value)
    value = int(value)
    if float_res != value or value & (value - 1) != 0:
        raise argparse.ArgumentTypeError(
            'Value must be a perfect square: {0}'.format(value))
    return value


def quantize(value, factor):
    return int(float(value) / factor) * factor


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quantizes an image.')
    parser.add_argument(
        'image', type=str, help='The path to the image to quantize.')
    parser.add_argument(
        'levels', type=power_of_two,
        help='The desired number of intensity levels.')
    parser.add_argument(
        '--outfile', '-o',
        help=('The file to place the output in. If not specified, the output '
              'is written to stdout.'))

    args = parser.parse_args()
    img = Image.open(args.image)
    if img.format != 'JPEG':
        raise ValueError('Given image must be JPEG. Received: {0}'.format(
                img.format))

    img = ImageOps.grayscale(img)

    factor = 256 / args.levels
    img.putdata([quantize(pixel, factor) for pixel in img.getdata()])

    outfile = args.outfile or sys.stdout
    img.save(outfile, format='JPEG', quality=100)
