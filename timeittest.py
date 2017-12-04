import timeit
from ImageGeneration.image_effects import quickBlur
from PIL import Image, ImageFilter
from os.path import join
from help_functions import loadImageMatrix, clamp

image = Image.open(join("ImageGeneration", "Images", "backgrounds", "1.jpg"))
image2 = Image.open(join("ImageGeneration", "Images", "backgrounds", "1.jpg"))
image3 = Image.open(join("ImageGeneration", "Images", "backgrounds", "1.jpg"))
def stupidtest1():
    quickBlur(image)
    quickBlur(image2)
    quickBlur(image3)


def stupidtest2():
    image.filter(ImageFilter.BLUR)
    image2.filter(ImageFilter.BLUR)
    image3.filter(ImageFilter.BLUR)

def stupidtest3():
    image.filter(ImageFilter.BLUR)
    image2.filter(ImageFilter.BLUR)
    image3.filter(ImageFilter.GaussianBlur(radius=100))

print("Alright lads, and ladies. Let the test commit. Firstly we will test quickBlur by Skov")
print("Let the test commit.")
print(timeit.timeit('stupidtest1()',setup="from __main__ import stupidtest1", number=1))
print("Wow. That took some time. Next up we've got Pillow, with the already generated filter called ImageFilter.BLUR")
print(timeit.timeit('stupidtest2()',setup="from __main__ import stupidtest2", number=1))
print("Wow. That took some time. Last but not least we've got Pillow again, this time with the filter called ImageFilter.GaussianBlur and a radius of 2")
print(timeit.timeit('stupidtest3()',setup="from __main__ import stupidtest3", number=1))

print("That's it ladies and gents. Trhanks for tonight. Hope you die just as awfully as I did performing these tests.")