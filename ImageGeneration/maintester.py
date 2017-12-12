from ImageGeneration.Generator import Generator
from webbrowser import open
import os, errno, platform
import argparse
import time


def main(save_root, innerloop, outterloop, size):
    if not save_root.startswith(".."):
        save_root = os.path.join("..", save_root)
    try:
        os.makedirs(os.path.join(save_root))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    counter = 0
    counter = len(os.listdir(save_root)) + 1

    start_amount_of_files = counter
    start_time = time.time()
    for u in range(0, outterloop):
        print(f"Start itteration: {u + 1}")

        print(f"Start creation of images.")
        try:
            images, labels = Generator(tbgenerated=innerloop, size=size)
        except BaseException as e:
            open("http://stackoverflow.com/search?q=[python]+" + str(e), new=2, autoraise=True)
            raise

        print(f"Generation end. Start saving process.")
        length = len(images)
        for x in range(0, len(images)):
            savepath = save_shit(save_root, counter,labels[x])

            images[x].save(savepath)
            counter += 1

        print(f"Images saved. In path: {save_root}")
    print(f"Generation completed!!!  Good job boiiii!"
          f"The total generated images is:                            {innerloop * outterloop}"
          f"The total images is:                                      {os.listdir(save_root) - start_amount_of_files}"
          f"If these does not add up.. Something went wrong."
          f"Total amount of time it took to complete the generation:   {time.time() - start_time}")

def save_shit(save_root, counter, label):
    return os.path.join(save_root, "id{}_type{}.png".format(str(counter), label))

ap = argparse.ArgumentParser(description="Image generator.", epilog="Hem is a lollicon, Joakim er til traps and Maas er Hitler CONFIRMED!!")

ap.add_argument("-in", "--innerloop", help="The inner loop of the function. Default is 100", type=int, default=100,
                nargs='?', const=1)
ap.add_argument("-ou", "--outerloop", help="The outer loop of the function. Default is 30", type=int, default=100,
                nargs='?', const=1)
ap.add_argument("-sf", "--savefolder", help="What folder the images should be saved as."
                                            "If the folder already exsists, then you also "
                                            "need to specify the start number of the file. "
                                            "Defailt is your computer name.",
                type=str, default=platform.node(), nargs='?', const=1)
ap.add_argument("-si", "--size", help="Define the size of the image to be generated.",
                type="cord", default="256,256", nargs=3)



args = ap.parse_args()
try:
    x, y = map(int, ap.parse_args().split(','))
except:
    raise argparse.ArgumentTypeError("Must be XXX,XXX")


main(save_root=args.savefolder, innerloop=args.innerloop, outterloop=args.outerloop, size=(int(x),int(y)))


