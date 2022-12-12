# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageDraw
import utils
import argparse
import math


def get_hough_image(im):
    (x, y) = im.size
    x *= 1.0
    y *= 1.0

    im_load = im.load()

    result = Image.new("RGBA", im.size, 0)
    draw = ImageDraw.Draw(result)

    for i in range(0, im.size[0]):
        for j in range(0, im.size[1]):
            if im_load[i, j] > 220:
                line = lambda t: (t, (-(i / x - 0.5) * (t / x) + (j / y - 0.5)) * x)
                draw.line([line(0), line(x)], fill=(50, 0, 0, 10))

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hough transform")
    parser.add_argument("image", nargs=1, help = "Path to image")
    args = parser.parse_args()

    im = Image.open(args.image[0])
    im = im.convert("L")  # covert to grayscale
    im.show()

    hough_img = get_hough_image(im)
    hough_img.show()






import pickle
import argparse

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

parser = argparse.ArgumentParser(description="match")
parser.add_argument("image", nargs=2, help = "Skeleton image")
args = parser.parse_args()

image1_name = args.image[0]
image2_name = args.image[1]

for m in range(1,3):
    for n in range(1,11):
        image2_name = "C" + str(m) + "00" + str(n)
        im1 = load_obj(image1_name)
        im2 = load_obj(image2_name)

        matches  = 0
        for i in range(len(im1)):
            for j in range(len(im2)):
                if (im1[i][0] == im2[j][0]) and (im1[i][1] == im2[j][1]) and (im1[i][2] == im2[j][2]):
                    matches = matches + 1
                    im1[i] = [-1,-1,-1]
                    im2[j] = [-2,-2,-2]
                    break

        print matches, len(im1), len(im2)
