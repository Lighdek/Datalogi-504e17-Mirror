from help_functions import loadImageMatrix,print_picture,combinePics
from Generator import *
from image_effects import quickBlur

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
img12 = "hentai.png"
pathes = [img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11]


print_picture(loaded_image=quickBlur(Image.open(img12)))

#quickBlur(Image.open(img12)).save("hentai_even_more_censored.png")


