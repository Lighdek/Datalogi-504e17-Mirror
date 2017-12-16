from ImageGeneration.Generator import Generator
from webbrowser import open
from humanfriendly import format_timespan
import os, errno, platform, uuid, time, argparse


def main(save_root, innerloop, outterloop, size, max_noise, set_amount_of_noise, rotate_degrees,
         size_difference_noise, size_difference_license, wlicense, nolicar, nothing, blur,
         rndom_noise, blur_amount_random, noise_amount_random):

    if not save_root.startswith(".."):
        save_root = os.path.join("..", save_root)

    try:
        os.makedirs(os.path.join(save_root))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    try:
        os.makedirs(os.path.join(save_root, "T"))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    try:
        os.makedirs(os.path.join(save_root, "F"))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    start_time = time.time()

    for u in range(0, outterloop):
        new_time = time.time()
        print(f"Start itteration: {u + 1}")

        print(f"Start creation of images.")
        try:
            images, labels = Generator(tbgenerated=innerloop, max_noise = max_noise, set_amount_of_noise = set_amount_of_noise, rotate_degrees = rotate_degrees,
              size_difference_noise = size_difference_noise, size_difference_license = size_difference_license,  wlicence = wlicense,
              nolicar = nolicar, nothing = nothing, size=size, blur = blur, rndom_noise = rndom_noise, blur_amount_random = blur_amount_random,
              noise_amount_random = noise_amount_random)
        except BaseException as e:
            open("http://stackoverflow.com/search?q=[python]+" + str(e), new=2, autoraise=True)
            raise

        print(f"Generation end. Start saving process.")
        length = len(images)
        for x in range(0, len(images)):
            savepath = save_shit(save_root, labels[x])

            images[x].save(savepath)

        print(f"Images saved. In path:      {save_root}\n"
              f"Time for this iteration:    {format_timespan(time.time() - new_time)}")

    print(f"Generation completed!!!  Good job boiiii!"
          f"The total generated images is:                           {innerloop * outterloop}\n\n"
          f"If these does not add up.. Something went wrong.\n\n"
          f"Final time it took was: {format_timespan(time.time() - start_time)}")


def save_shit(save_root, label):
    subfolder = str(label)[0]
    return os.path.join(save_root, subfolder ,f"{str(uuid.uuid4())}.png")

ap = argparse.ArgumentParser(description="Image generator.", epilog="Hem is a lollicon, Joakim er til traps and Maas er Hitler CONFIRMED!!")

ap.add_argument("-in", "--innerloop", help="The inner loop of the function. Default is 50", type=int, default=30,
                nargs='?', const=1)
ap.add_argument("-ou", "--outerloop", help="The outer loop of the function. Default is 100", type=int, default=100,
                nargs='?', const=1)
ap.add_argument("-sf", "--savefolder", help="What folder the images should be saved as."
                                            "If the folder already exsists, then you also "
                                            "need to specify the start number of the file. "
                                            "Defailt is your computer name.",
                type=str, default=platform.node(), nargs='?', const=1)

ap.add_argument("-mn", "--max_noise", help="Maximum value for how much noise there can be in a picture.", type=int, default=4,
                nargs='?', const=1)
ap.add_argument("-san", "--set_amount_of_noise", help="If this is set, it will make sure that each picture has this much noise in one picture.", type=int, default=False,
                nargs='?', const=1)
ap.add_argument("-wl", "--wlicense", help="The ratio of with / without license. Default is .5", type=float, default=.5,
                nargs='?', const=1)
ap.add_argument("-nc", "--nolicar", help="The amount of noise that is a car without license plate. Default is .75", type=float, default=.75,
                nargs='?', const=1)
ap.add_argument("-no", "--nothing", help="The amount of pictures with no noise. Only background. Default is .5", type=float, default=.5,
                nargs='?', const=1)
ap.add_argument("-bl", "--blur", help="Chance of getting a blurred image. Default is .3", type=float, default=.3,
                nargs='?', const=1)
ap.add_argument("-rn", "--random_noise", help="Chance of getting random noise on the image. Default is .3", type=float, default=.3,
                nargs='?', const=1)

ap.add_argument("-rd", "--rotation", help="Defines the rotation degree. Inseret one integer, and it will be negated, eg: 5 creates a random degree between -5 and 5", type=int, default=5,
                nargs='?', const=1)

ap.add_argument("-si", "--size", help="Define the size of the image to be generated.",
                type=str, default="512,512", nargs='?')

ap.add_argument("-sdn", "--size_difference_noise", help="Define the amount the noise should be scaled. eg: 1.5,3.",
                type=str, default="1.5,3", nargs='?')
ap.add_argument("-sdl", "--size_difference_license", help="Define the amount the license should be scaled. eg: 1.5,3.",
                type=str, default="1.3,2", nargs='?')
ap.add_argument("-sar", "--noise_amount_random", help="Define the interval that can be randomised for noise. eg 3,10.",
                type=str, default="3,10", nargs='?')
ap.add_argument("-bar", "--blur_amount_random", help="Define the interval that can be randomised for noise. eg 0,2.",
                type=str, default="0,2", nargs='?')


args = ap.parse_args()
try:
    x, y = args.size.split(',')
    size = (int(x), int(y))
except:
    raise argparse.ArgumentTypeError("Must be XXX,XXX")

passed_rotation = args.rotation

rotation = (-1 * passed_rotation, passed_rotation)
try:
    x, y = args.size_difference_noise.split(',')
    size_difference_noise = (float(x), float(y))
except:
    raise argparse.ArgumentTypeError("Must be XX,XX")

try:
    x, y = args.size_difference_license.split(',')
    size_difference_license = (float(x), float(y))
except:
    raise argparse.ArgumentTypeError("Must be XX,XX")

try:
    x, y = args.noise_amount_random.split(',')
    noise_amount_random = (int(x), int(y))
except:
    raise argparse.ArgumentTypeError("Must be XX,XX")

try:
    x, y = args.size.split(',')
    blur_amount_random = (int(x), int(y))
except:
    raise argparse.ArgumentTypeError("Must be XX,XX")




main(save_root=args.savefolder, innerloop=args.innerloop, outterloop=args.outerloop, size=size,
     max_noise = args.max_noise, set_amount_of_noise = args.set_amount_of_noise,
     rotate_degrees = rotation, size_difference_noise = size_difference_noise,
     size_difference_license = size_difference_license, wlicense = args.wlicense,
     nolicar = args.nolicar, nothing = args.nothing, blur = args.blur,
     rndom_noise = args.random_noise, blur_amount_random = blur_amount_random,
     noise_amount_random = noise_amount_random)


