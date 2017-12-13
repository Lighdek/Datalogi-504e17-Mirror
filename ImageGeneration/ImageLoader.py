import os
import random
import re
from PIL import Image
import numpy as np

folderPath = "OurImages/512_512"


def loadImages(count=200):
    files = os.listdir(folderPath)
    imgs = []
    labels = []

    if count < 1:
        raise ValueError("Tried to load 0 images")
    if len(files) < 1:
        raise OSError("No images in folder %s " % folderPath)

    chosen = random.choices(files, k=count)

    for f in chosen:

        match = re.search('type(\d+)', f)
        if match:
            imgs.append(
                np.asarray(
                    Image.open("OurImages/512_512/" + f).resize((512, 512)))
                [:, :, :3]
            )

            labels.append(match.group(1) == "0")

    if len(imgs) < 1:
        raise ValueError("No images matched regex type(\d+)")

    return np.array(imgs), np.array(labels)
