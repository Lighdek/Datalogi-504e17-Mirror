import os
import random
import re
import pickle
from PIL import Image
import numpy as np

folderPath = "OurImages/512_512/"


def loadImages(count=200, shano=False):
    files = os.listdir(folderPath)
    imgs = []
    labels = []

    if count < 1:
        raise ValueError("Tried to load 0 images")
    if len(files) < 1:
        raise OSError("No images in folder %s " % folderPath)

    if shano:
        with open("DhatPlate.pickle", "rb") as fil:
            sourceLabel = pickle.load(fil)
        if len(sourceLabel) < 1:
            raise ValueError("No labels loaded")

    chosen = random.choices(files, k=count)

    for f in chosen:

        if shano:
            assert sourceLabel
            imgs.append(
                np.asarray(
                    Image.open("OurImages/plateScanner/" + f).resize((512, 512)))
                [:, :, :3]
            )
            labels.append(sourceLabel[f])
        else:
            match = re.search('type(\d+)', f)
            if match:
                imgs.append(
                    np.asarray(
                        Image.open(folderPath + f).resize((512, 512)))
                    [:, :, :3]
                )

                labels.append(match.group(1) == "0")

    if len(imgs) < 1:
        raise ValueError("No images matched regex type(\d+)")

    return np.array(imgs), np.array(labels)

