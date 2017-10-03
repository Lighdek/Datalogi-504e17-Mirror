from help_functions import loadImageMatrix,print_picture,combinePics
from PIL import Image
from Generator import *
from BlurManipulation import bluring_start
import itertools
import time


#
# filepaths = ["TestFolder/Backgrounds", "TestFolder/WithLicence","TestFolder/WithoutLicence"]
# dir = generator(filepaths,tbgenerated=20).items()
#
# for pictures in dir:
#     print_picture(loaded_image=pictures[1][0])



img1 = "picz/V_The_Hierophant.jpg"
img2 = "picz/XI_Justice.jpg"
img3 = "picz/XII_The_Hanged_Man.jpg"
img4 = "picz/XIII_Death.jpg"
img5 = "picz/XIX_The_Sun.jpg"
img6 = "picz/XV_The_Devil.jpg"
img7 = "picz/XVII_The_Star.jpg"
img8 = "picz/XVIII_The_Moon.jpg"
img9 = "picz/god_emperor.jpg"
img10 = "picz/whereisstuff.png"
img11 = "TestFolder/Backgrounds/CUENCA-1-790x527.jpg"
pathes = [img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11]


# print(loadImageMatrix(filepath="whereisstuff.png"))


# print_picture(loaded_image=img)
# img = []
# for i in pathes:
#     img.append(Image.open(i))
for x in range(0,10):
    print_picture(loaded_image=bluring_start(Image.open(img11)))
    time.sleep(2)


#
# combinePics(filepathes=img1)
# combinePics(filepathes=pathes)


def derp():
    print("This is where we code and fuck hookers")
    time.sleep(2)

def main():
    derp()


