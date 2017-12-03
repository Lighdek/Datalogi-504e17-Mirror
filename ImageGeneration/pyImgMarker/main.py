from ImageGeneration.pyImgMarker.image_handler import main_imgs
from webbrowser import open
from traceback import print_exc
import platform
from os.path import join



image_root = join("ImageGeneration", "Images", "car")
settings_path = join(image_root, "imgSettings.JSON")


try:
    main_imgs(settings_path, image_root)
except BaseException as e:
    open("http://stackoverflow.com/search?q=[python]+" + str(e), new=2, autoraise=True)
    print_exc()

