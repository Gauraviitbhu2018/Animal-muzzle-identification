__author__ = 'gkj'
import pickle
import argparse

def load_obj(name):
    with open('objm/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

parser = argparse.ArgumentParser(description="match")
parser.add_argument("image", nargs=2, help = "Skeleton image")
args = parser.parse_args()

image1_name = args.image[0]
image2_name = args.image[1]
im1 = load_obj(image1_name)
im2 = load_obj(image2_name)

print im1[58][102][0]
#print len(im1)
maxim = 0
for i in range(50,200):
    for j in range(50,200):
        for k in range(50,200):
            for l in range(50,200):
                if (im1[i][j][0] == im2[k][l][0]) and (im1[i][j][1] == im2[k][l][1]) and (im1[i][j][2] == im2[k][l][2]):
                    x1=0.0
                    x2=0.0
                    y1=0.0
                    y2=0.0
                    z1=0.0
                    z2=0.0
                    for s in range(maxim,120):
                        r =(s+1)*2
                        if ((i-(s+1))<0) or ((j-(s+1))<0) or ((k-(s+1))<0 )or ((l-(s+1)) <0 ) or ((i+(s+1)) >250 ) or ((j+(s+1)) >250) or ((k+(s+1)) >250 ) or ((l+(s+1)) >250) :
                            break
                        for m in range(r):
                            for n in range(r):
                                x1=im1[i-(s+1)+m][j-(s+1)+n][0]+x1
                                x2=im2[k-(s+1)+m][l-(s+1)+n][0]+x2
                                y1=im1[i-(s+1)+m][j-(s+1)+n][1]+y1
                                y2=im2[k-(s+1)+m][l-(s+1)+n][1]+y2
                                z1=im1[i-(s+1)+m][j-(s+1)+n][2]+z1
                                z2=im2[k-(s+1)+m][l-(s+1)+n][2]+z2
                        if  ( x2>x1+0.25 ) or (x2<x1-0.25) or ( y2>y1+0.25 ) or (y2<y1-0.25) and ( z2>z1+0.25 ) or (z2<z1-0.25):
                            maxim =max(maxim,s)
                            break
            if (maxim>40):
                break
        if (maxim>40):
            break
    if (maxim>40):
        break
if (maxim>40) :
    print image1_name, image2_name,           'MATCH'
else:
    print image1_name, image2_name,           'NOT MATCH'








