#!/usr/bin/env python3


import math
import cairo
import subprocess
import os.path
from numpy import arange, linspace
import colorsys
import argparse
import time
import glob

import multiprocessing

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


def draw_frame(filename, product, modulo, size, thinness=5000, verbose=False):
    filename = str(filename)
    product = float(product)
    modulo = int(modulo)
    size = int(size)
    thinness = int(thinness)
    verbose = bool(verbose)

    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context (surface)

    ctx.scale (size, size) # Normalizing the canvas

    pat = cairo.SolidPattern(0, 0, 0, 1)

    ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
    ctx.set_source (pat)
    ctx.fill ()

    ctx.translate(0.5, 0.5)
    # Provide a small border around the circle
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

        # Set the color based on the end position -- this looks prettier
        setColorHsv(ctx, theta1, 1, 1)
        drawLine(ctx, start, end)
        ctx.stroke()



    # The white circle should cover the lines for a clean edge
    ctx.set_operator(cairo.OPERATOR_OVER)

    # Draw the circle
    ctx.set_source_rgb (1, 1, 1) # Solid white
    ctx.stroke ()


    ctx.arc(0, 0, 0.5, 0, 2 * math.pi)
    ctx.set_line_width(0.002)
    ctx.stroke()


    if verbose:
        print('writing ' + filename, end='')

    surface.write_to_png (filename) # Output to PNG
    
    if verbose:
        print(' done')


def make_name(number, prefix='chord', suffix='.png', decimal_digits=0, total_digits=5):
    shifted = number * 10 ** decimal_digits
    name = str(int(shifted))

    while len(name) < total_digits:
        name = '0' + name

    return prefix + name + suffix


def get_epoch(filename):
    try:
        with open(filename, 'r') as epoch_file:
            epoch = float(epoch_file.readline())
    except:
        with open(filename, 'w') as epoch_file:
            epoch = time.time()
            epoch_file.write(str(epoch) + '\n')
    return epoch



def render_frame(time):
    # delta_time = (float(args.time) + i * float(args.time_step)) * unit_time

    frame_num = time + 1
    # if verbose:
    #     print(frame_num)

    filename = make_name(frame_num, prefix='frames/chord', suffix='.png', decimal_digits=5, total_digits=8)

    if os.path.exists(filename):
        return

    draw_frame(filename, frame_num, num_lines, size, thinness=5000)
    # if verbose:
    #     print(filename)

# The number of lines to draw
num_lines = 2000 

# The number of seconds to take to advance by "1"
unit_time = 60 * 60 * 24   # 1 day

size = 2160

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Draw a frame of Metastellum multiformosa')

    # parser.add_argument('-s', '--size', dest='size', action='store', default=0, help='width and height of image')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-t', '--time', dest='time', action='store')
    # parser.add_argument('--time-step', dest='time_step', action='store')
    parser.add_argument('-e', '--end-time', dest='end_time', action='store')
    parser.add_argument('-n', dest='num_frames', action='store', default=1)
    args = parser.parse_args()

    verbose = args.verbose

    # size = args.size
    # if size == 0:
    #     with open('/sys/class/graphics/fb0/virtual_size', 'r') as fb_size:
    #         sizes = fb_size.readline().split(',')
    #         size = min(int(sizes[0]), int(sizes[1]))
    #         if verbose: 
    #             print('Detected size ' + str(size))
    #         # Double the size for anti-aliasing
    #         size *= 2


            
    # epoch = get_epoch('epoch.txt')



    # The number of lines to draw
    num_lines = 2000 

    # The number of seconds to take to advance by "1"
    unit_time = 60 * 60 * 24   # 1 day
    # unit_time = 60


    # Ctrl+C stops the image viewer, but not the script.
    # After writing each frame, check that the image view is running.
    # If it isn't running for three consecutive frames, end the script.
    # strikes_left = 3



    # for i in range(int(args.num_frames)):



    start_time = float(args.time)
    end_time = float(args.end_time)
    num_frames = int(args.num_frames)

    pool = multiprocessing.Pool(16)
    pool.map(render_frame, linspace(start_time, end_time, num_frames, endpoint=False))


# 60 fps
# 30 seconds per "1"
# 1800 frames per "1"
# Song is 30 minutes long
# 54000 frames total

# No, I think 30 seconds per "1" is too fast. 60 is better