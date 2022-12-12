# Metody biometryczne
# Przemyslaw Pastuszka

import sobel
import argparse
import os
from PIL import Image

parser = argparse.ArgumentParser(description="Sobel filter")
parser.add_argument("image", nargs=1, help = "Path to image")
parser.add_argument('--showX', "-x", action='store_true', help = "Show Sobel filter for X coordinate")
parser.add_argument('--showY', "-y", action='store_true', help = "Show Sobel filter for Y coordinate")
parser.add_argument("--save", action='store_true', help = "Save result image as src_image_enhanced.gif")
args = parser.parse_args()

im = Image.open(args.image[0])
im = im.convert("L")  # covert to grayscale

(xSobel, ySobel, fullSobel) = sobel.full_sobels(im)

if args.showX:
    xSobel.show()
if args.showY:
    ySobel.show()
fullSobel.show()
if args.save:
        base_image_name = os.path.splitext(os.path.basename(args.image[0]))[0]
        fullSobel.save(base_image_name + "_enhanced11.gif", "GIF")
