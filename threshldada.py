__author__ = 'gkj'
# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image
import numpy as np
import utils
import argparse
import math
import frequency
import os


def adaptive_thresh(input_img):

    h, w = input_img.shape

    S = w/8
    s2 = S/2
    T = 5.0

    #integral img
    int_img = np.zeros_like(input_img, dtype=np.uint32)
    for col in range(w):
        for row in range(h):
            int_img[row,col] = input_img[0:row,0:col].sum()

    #output img
    out_img = np.zeros_like(input_img)

    for col in range(w):
        for row in range(h):
            #SxS region
            y0 = max(row-s2, 0)
            y1 = min(row+s2, h-1)
            x0 = max(col-s2, 0)
            x1 = min(col+s2, w-1)

            count = (y1-y0)*(x1-x0)

            sum_ = int_img[y1, x1]-int_img[y0, x1]-int_img[y1, x0]+int_img[y0, x0]

            if input_img[row, col]*count < sum_*(100.-T)/100.:
                out_img[row,col] = 0
            else:
                out_img[row,col] = 255

    return out_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gabor filter applied")
    parser.add_argument("image", nargs=1, help = "Path to image")
    #parser.add_argument("block_size", nargs=1, help = "Block size")
    parser.add_argument("--save", action='store_true', help = "Save result image as src_image_enhanced.gif")
    args = parser.parse_args()

for m in range(1,13):
    for n in range(1,11):
        if (n<=9):
            image2_name = "C" + str(m) + "00" + str(n) + ".JPG"
            name = "C" + str(m) + "00" + str(n)
        else:
            image2_name = "images/C" + str(m) + "0" + str(n) + ".JPG"
            name = "C" + str(m) + "0" + str(n)
        im = Image.open(image2_name)
        im = im.convert("L")  # covert to grayscale
        #im.show()


        #im = Image.open(args.image[0])
        #im.show()
        #W = int(args.block_size[0])
        result = adaptive_thresh(np.array(im))
        im = Image.fromarray(result)
        #result.show()

        #if args.save:
        base_image_name = os.path.splitext(os.path.basename(args.image[0]))[0]
        im.save(name + "_adaptive.gif", "GIF")











