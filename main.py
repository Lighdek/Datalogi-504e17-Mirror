from writeasarray import loadImageMatrix,print_picture,combinePics
from PIL import Image




img1 = "V_The_Hierophant.jpg"
img2 = "XI_Justice.jpg"
img3 = "XII_The_Hanged_Man.jpg"
img4 = "XIII_Death.jpg"
img5 = "XIX_The_Sun.jpg"
img6 = "XV_The_Devil.jpg"
img7 = "XVII_The_Star.jpg"
img8 = "XVIII_The_Moon.jpg"
img9 = "god_emperor.jpg"
img10 = "whereisstuff.png"
pathes = [img1,img2,img3,img4,img5,img6,img7,img8,img9,img10]


# print(loadImageMatrix(filepath="whereisstuff.png"))


# print_picture(loaded_image=img)
img = []
for i in pathes:
    img.append(Image.open(i))



combinePics(loaded_imagessss=img)
# combinePics(filepathes=pathes)


def derp():
    print("This is where we code and fuck hookers")


def main():
    derp()


