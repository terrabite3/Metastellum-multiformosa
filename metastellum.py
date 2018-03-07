#!/usr/bin/env python3


import math
import cairo
import subprocess
import os.path
from numpy import arange
import colorsys
import argparse
import time


def circle_point(theta):
    x = math.sin(2 * math.pi * theta) / 2
    y = math.cos(2 * math.pi * theta) / 2
    return x, y

def drawLine(ctx, start, end):
    ctx.move_to(start[0], start[1])
    ctx.line_to(end[0], end[1])

def setColorHsv(ctx, h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    ctx.set_source_rgb(r, g, b)


def blah(product, modulo=1000, width=1080, height=1080, thinness=5000, decimal_digits=1, verbose=False, overwrite=False):
    product = float(product)
    modulo = int(modulo)
    width = int(width)
    height = int(height)
    thinness = int(thinness)
    decimal_digits = int(decimal_digits)
    verbose = bool(verbose)
    overwrite = bool(overwrite)

    filename = make_name(product, prefix='frames/chord', decimal_digits=decimal_digits, total_digits=decimal_digits + 3)

    if os.path.isfile(filename) and not overwrite:
        if verbose:
            print(filename + ' skipped')
        return

    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context (surface)

    ctx.scale (width, height) # Normalizing the canvas

    pat = cairo.SolidPattern(0, 0, 0, 1)

    ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
    ctx.set_source (pat)
    ctx.fill ()

    ctx.translate(0.5, 0.5)
    ctx.scale(0.95, 0.95)

    ctx.set_line_width (1 / thinness)

    # Blend colors
    ctx.set_operator(cairo.OPERATOR_ADD)

    # Set antialians to BEST (the enum is missing from pycairo)
    # I can't tell if this has an effect
    ctx.set_antialias(6)


    ################################################
    # Loop here
    for i in arange(modulo):
        theta0 = i / modulo
        start = circle_point(theta0)
        theta1 = i * product / modulo
        end = circle_point(theta1)

        setColorHsv(ctx, theta1, 1, 1)
        drawLine(ctx, start, end)
        ctx.stroke()



    # The white circle should cover the lines for a clean edge
    ctx.set_operator(cairo.OPERATOR_OVER)

    # Draw the circle
    ctx.set_source_rgb (1, 1, 1) # Solid color
    ctx.stroke ()


    ctx.arc(0, 0, 0.5, 0, 2 * math.pi)
    ctx.set_line_width(0.002)
    ctx.stroke()


    if verbose:
        print('writing ' + filename, end='')

    surface.write_to_png (filename) # Output to PNG
    
    if verbose:
        print(' done')

    return filename


def make_name(number, prefix='chord', suffix='.png', decimal_digits=0, total_digits=5):
    shifted = number * 10 ** decimal_digits
    name = str(int(shifted))

    while len(name) < total_digits:
        name = '0' + name

    return prefix + name + suffix


parser = argparse.ArgumentParser(description='Draw a frame of Metastellum multiformosa')

parser.add_argument('-s', '--size', dest='size', action='store', default=0, help='width and height of image')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

verbose = args.verbose

size = args.size
if size == 0:
    with open('/sys/class/graphics/fb0/virtual_size', 'r') as fb_size:
        sizes = fb_size.readline().split(',')
        size = min(int(sizes[0]), int(sizes[1]))
        if verbose: 
            print('Detected size ' + str(size))
        # Double the size for anti-aliasing
        size *= 2




# Do the thing
num_lines = 2000 

if __name__ == '__main__':
    epoch = time.time()

    try:
        with open('epoch.txt', 'r') as epoch_file:
            epoch = float(epoch_file.readline())
    except:
        with open('epoch.txt', 'w') as epoch_file:
            epoch = time.time()
            epoch_file.write(str(epoch) + '\n')



    # The number of seconds to take to advance by "1"
    unit_time = 60 * 60 * 24
#    unit_time = 60

    while True:


        current_time = time.time()
        delta_time = current_time - epoch

        

        frame_num = delta_time / unit_time + 1
        if verbose:
            print(frame_num)

        filename = blah(frame_num, modulo=num_lines, width=size, height=size, thinness=5000, decimal_digits=5, verbose=verbose, overwrite=True)
        if verbose:
            print(filename)

        subprocess.run(['ln', '-s', '-f', filename, 'link1.png'])
        subprocess.run(['ln', '-s', '-f', filename, 'link2.png'])
        subprocess.run(['ln', '-s', '-f', filename, 'link3.png'])

        # Check if the image viewer is running
        ps = subprocess.Popen('ps -e | grep fbi', shell=True, stdout=subprocess.PIPE)
        output = ps.stdout.read()
        ps.stdout.close()
        ps.wait()
        if len(output) == 0:
            print('fbi is not running; exiting')
            break
