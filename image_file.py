from PIL import Image

class DizImage():
    name = None
    image_file_path = None

    def __init__(self,name, image):
        self.name = name
        self.image_file_path = image
        return

    def get_name(self):

        return self.name

    def get_image(self):

        return Image.open(self.image_file_path)






