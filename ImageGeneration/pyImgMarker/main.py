from ImageGeneration.pyImgMarker.image_handler import main_imgs
from webbrowser import open
from traceback import print_exc

settings_path = "imgSettings.JSON"
image_root = "images"

main_imgs(settings_path, image_root)


try:
   pass
except BaseException as e:
    open("http://stackoverflow.com/search?q=[python]+" + str(e) , new=2, autoraise=True)
    print_exc()

