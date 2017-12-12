import os
import re
from PIL import Image
import numpy as np

folderPath = "OurImages"

def loadImages(count=200):
    files = os.listdir(folderPath)
    imgs = []
    labels = []

    if count < 1:
        raise ValueError("Tried to load 0 images")
    if len(files) < 1:
        raise OSError("No images in folder %s " % folderPath)

    for i in range(min(count, len(files))):
        # TODO: currently only loading count first files
        match = re.search('type(\d+)', files[i])
        if match:
            imgs.append(np.asarray(Image.open("OurImages/" + files[i]).resize((256, 256)))[:, :, :3])
            labels.append(match.group(1) == "0")

    if len(imgs) < 1:
        raise ValueError("No images matched regex type(\d+)")

    return np.array(imgs), np.array(labels)
