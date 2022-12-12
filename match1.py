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

im1 = load_obj(image1_name)
im2 = load_obj(image2_name)
matches  = 0
for i in range(len(im1)):
    for j in range(len(im2)):
        if (im1[i][0] == im2[j][0]) and (im1[i][1] == im2[j][1]) and (im1[i][2] == im2[j][2] ):
            matches = matches + 1
            im1[i] = [-1,-1,-1]
            im2[j] = [-2,-2,-2]
            break
matches = matches
if  matches >= 85:
    print len(im1),len(im2),matches, 'MATCH'
else:
    print len(im1),len(im2),matches, 'Not Match'
#print matches, len(im1), len(im2)  basic








