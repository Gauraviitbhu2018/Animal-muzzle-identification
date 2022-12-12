__author__ = 'gkj'
# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageDraw
import utils
import argparse
import math
import frequency
import os
from utils import flatten, transpose
import pickle
import copy

#******************************* gabor********************
def gabor_kernel(W, angle, freq):
    cos = math.cos(angle)
    sin = math.sin(angle)

    yangle = lambda x, y: x * cos + y * sin
    xangle = lambda x, y: -x * sin + y * cos

    xsigma = ysigma = 4

    return utils.kernel_from_function(W, lambda x, y:
        math.exp(-(
            (xangle(x, y) ** 2) / (xsigma ** 2) +
            (yangle(x, y) ** 2) / (ysigma ** 2)) / 2) *
        math.cos(2 * math.pi * freq * xangle(x, y)))

def gabor(im, W, angles):
    (x, y) = im.size
    im_load = im.load()

    freqs = frequency.freq(im, W, angles)
    print "computing local ridge frequency done"

    gauss = utils.gauss_kernel(23)
    utils.apply_kernel(freqs, gauss)

    for i in range(1, x / W - 1):
        for j in range(1, y / W - 1):
            kernel = gabor_kernel(W, angles[i][j], freqs[i][j])
            for k in range(0, W):
                for l in range(0, W):
                    im_load[i * W + k, j * W + l] = utils.apply_kernel_at(
                        lambda x, y: im_load[x, y],
                        kernel,
                        i * W + k,
                        j * W + l)

    return im

#****************************************thinning**********************
usage = False

def apply_structure(pixels, structure, result):
    global usage
    usage = False

    def choose(old, new):
        global usage
        if new == result:
            usage = True
            return 0.0
        return old

    utils.apply_kernel_with_f(pixels, structure, choose)

    return usage

def apply_all_structures(pixels, structures):
    usage = False
    for structure in structures:
        usage |= apply_structure(pixels, structure, utils.flatten(structure).count(1))

    return usage

def make_thin(im):
    loaded = utils.load_image(im)
    utils.apply_to_each_pixel(loaded, lambda x: 0.0 if x > 10 else 1.0)
    print "loading phase done"

    t1 = [[1, 1, 1], [0, 1, 0], [0.1, 0.1, 0.1]]
    t2 = utils.transpose(t1)
    t3 = reverse(t1)
    t4 = utils.transpose(t3)
    t5 = [[0, 1, 0], [0.1, 1, 1], [0.1, 0.1, 0]]
    t7 = utils.transpose(t5)
    t6 = reverse(t7)
    t8 = reverse(t5)

    thinners = [t1, t2, t3, t4, t5, t6, t7]

    usage = True
    while(usage):
        usage = apply_all_structures(loaded, thinners)
        print "single thining phase done"

    print "thining done"

    utils.apply_to_each_pixel(loaded, lambda x: 255.0 * (1 - x))
    utils.load_pixels(im, loaded)
#    im.show()

def reverse(ls):
    cpy = ls[:]
    cpy.reverse()
    return cpy

#******************************** crossing number********************
cells = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

r = [[[0.0 for j1 in range(3)] for i in range(250)] for j in range(250)]

def minutiae_at(pixels, i, j):
    angles = []
    values = [pixels[i + k][j + l] for k, l in cells]
    #print values

    crossings = 0
    for k in range(0, 8):
        crossings += abs(values[k] - values[k + 1])
        if values[k] - values[k + 1]:
            angles.append(k)
    crossings /= 2
    if pixels[i][j] == 1:
        if crossings == 1:
            return "ending"
        if crossings == 3:
            print i
            m=i
            #a=[]
            if values[0]!=1:

                a = [angles[2*i+1]*(3.14/8) for i in [0,1,2]]
            else :
                a = [angles[2*i]*(3.14/8) for i in [0,1,2]]
            #a1 = [float("{0:.2f}".format(b)) for b in a]
            r[m][j] = [float("{0:.2f}".format(b)) for b in a]
            #r[m][j][0] = a1[0]
            #r[m][j][1] = a1[1]
            #r[m][j][2] = a1[2]
            print r[m][j]
            return "bifurcation"
    return "none"

def calculate_minutiaes(im):
    pixels = utils.load_image(im)
    utils.apply_to_each_pixel(pixels, lambda x: 0.0 if x > 10 else 1.0)
    (x, y) = im.size
    result = im.convert("RGB")
    draw = ImageDraw.Draw(result)

    colors = {"ending" : (150, 0, 0), "bifurcation" : (0, 150, 0)}

    ellipse_size = 1
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            minutiae = minutiae_at(pixels, i, j)
            if minutiae != "none":
                #print i,j,minutiae
                draw.ellipse([(i - ellipse_size, j - ellipse_size), (i + ellipse_size, j + ellipse_size)], outline = colors[minutiae])

    del draw

    return result

#********************************** __main__********************

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gabor filter applied")
    parser.add_argument("image", nargs=1, help = "Path to image")
    parser.add_argument("block_size", nargs=1, help = "Block size")
    parser.add_argument("--save", action='store_true', help = "Save result image as src_image_enhanced.gif")
    args = parser.parse_args()


    im = Image.open(args.image[0])
    im = im.convert("L")        #im.show()

        # gabor
    W = int(args.block_size[0])

    f = lambda x, y: 2 * x * y
    g = lambda x, y: x ** 2 - y ** 2

    angles = utils.calculate_angles(im, W, f, g)
    print "calculating orientation done"

    angles = utils.smooth_angles(angles)
    print "smoothing angles done"

    result = gabor(im, W, angles)
    #result.show()

    if args.save:
        base_image_name = os.path.splitext(os.path.basename(args.image[0]))[0]
        im.save(base_image_name + "_enhanced.gif", "GIF")

    # thinning
    make_thin(im)

    if args.save:
        base_image_name = os.path.splitext(os.path.basename(args.image[0]))[0]
        im.save(base_image_name + "_enhanced_thinned.gif", "GIF")

    # crossing number
    result = calculate_minutiaes(im)
    #    result.show()

    def save_obj(obj, base_image_name):
        with open('objm/'+base_image_name+'.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    base_image_name = os.path.splitext(os.path.basename(args.image[0]))[0]
    save_obj(r, base_image_name)
    print r
    r = [[[0.0 for j1 in range(3)] for i in range(250)] for j in range(250)]
    print r
    if args.save:
        base_image_name = os.path.splitext(os.path.basename(args.image[0]))[0]
        result.save(base_image_name + "_enhanced_thinned_minutiae.gif", "GIF")
       # print r

