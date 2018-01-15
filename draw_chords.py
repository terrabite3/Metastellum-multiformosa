import math
import cairo
import subprocess
import os.path
import threading
from numpy import arange
from multiprocessing.dummy import Pool
from functools import partial
import itertools
import colorsys

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

count_lock = threading.Lock()
count = 0

def blah(product, modulo=1000, width=1080, height=1080, thinness=5000, decimal_digits=1, verbose=False, overwrite=False):

    global count
    global count_lock
    global total_frames
    with count_lock:
        count += 1
        value = count
    if (value * 100) % total_frames == 0:
        message = str(value * 100 // total_frames) + '%'
        print(message, end='')

    filename = make_name(product, prefix='frames/chord', decimal_digits=decimal_digits)

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



    ctx.set_source_rgb (1, 1, 1) # Solid color
    ctx.stroke ()


    ctx.arc(0, 0, 0.5, 0, 2 * math.pi)
    ctx.set_line_width(0.002)
    ctx.stroke()

    surface.write_to_png (filename) # Output to PNG

    if verbose:
        print(filename + ' done')



def make_name(number, prefix='chord', suffix='.png', decimal_digits=0, total_digits=5):
    shifted = number * 10 ** decimal_digits
    name = str(int(shifted))

    while len(name) < total_digits:
        name = '0' + name

    return prefix + name + suffix

    # if decimal_digits == 0:
    #     name = str(number)
    # else:
    #     f = '%.' + str(decimal_digits) + 'f'
    #     name = f % number
    #     name = name.replace('.', '')
    # return prefix + name + suffix



# Do the thing
modulo = 1000
start_product = 22
end_product = 23
step_product = 0.001 #0
digits = 3

products = arange(start_product, end_product, step_product)
total_frames = len(products)

work_function = partial(blah, decimal_digits=digits)


test = False
if test:
    blah(3, modulo=1000, thinness=5000, verbose=True, overwrite=True)

    exit()

multithread = True
if multithread:
    pool = Pool(6)
    pool.map(work_function, products)
else:
    for p in products:
        work_function(p)


make_video = False
if make_video:
    print('Making video')
    # os.system(r'C:\cygwin64\bin\bash.exe --login -c "make_video.sh')
    command = r'C:\ffmpeg\bin\ffmpeg.exe -y -framerate 60 -i "frames/chord%0' + str(digits + 2) + 'd.png" -c:v libx264rgb -preset slow -crf 18 -c:a copy output.mkv'

    p = subprocess.Popen(command, stderr=subprocess.PIPE)

    while p.poll() is None:
        print(p.stderr.readline())
    print(p.stderr.read())

print('All done')