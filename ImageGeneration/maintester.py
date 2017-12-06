from ImageGeneration.Generator import Generator
from webbrowser import open
from traceback import print_exc
import os
from timeit import Timer


def bob():
    try:
        images, labels = Generator(tbgenerated=1)
    except BaseException as e:
        open("http://stackoverflow.com/search?q=[python]+" + str(e), new=2, autoraise=True)
        print_exc()
        raise

bob()

#for x in range(0, len(images) - 1):
#    images[x].save(join("Images", "saved", "id:{}_type:{}.png".format(str(x), labels[x])))
