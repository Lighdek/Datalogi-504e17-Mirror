from ImageGeneration.Generator import Generator
from webbrowser import open
import os, errno, platform
import argparse


def main(save_root, innerloop, outterloop):
    if not save_root.startswith(".."):
        save_root = os.path.join("..", save_root)
    try:
        os.makedirs( save_root)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    counter = len(os.listdir(save_root)) + 1

    for u in range(0, outterloop):
        print(f"Start itteration: {u + 1}")

        print(f"Start creation of images.")
        try:
            images, labels = Generator(tbgenerated=innerloop)
        except BaseException as e:
            open("http://stackoverflow.com/search?q=[python]+" + str(e), new=2, autoraise=True)
            raise

        print(f"Generation end. Check if folder exsists.")

        print(f"Folder checked. Start saving process.")

        for x in range(0, len(images) - 1):
            counter += 1
            images[x].save(os.path.join(save_root, "id:{}_type:{}.png".format(str(counter), labels[x])))
        print(f"Images saved.")


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

args = ap.parse_args()

main(save_root=args.savefolder, innerloop=args.innerloop, outterloop=args.outerloop)


