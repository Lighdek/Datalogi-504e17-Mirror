import os
import random
import re
import pickle
from PIL import Image
import numpy as np
from os import path, listdir


def loadImages(datasets: list=None, shuffle: bool=False, folderPath: str="OurImages/") -> tuple:
    if datasets is None:
        datasets = [
            (100, 'RealFrontBack'),
            (100, 'GenLicenseOnBackground')
        ]

    imagePools = {}
    for (count, setName) in datasets:
        dirT = listdir(path.join(folderPath, setName, "T"))
        dirF = listdir(path.join(folderPath, setName, "F"))

        if shuffle:
            random.shuffle(dirT)
            random.shuffle(dirF)

        imagePools[setName] = (
            dirT[:count//2 + count % 2],
            dirF[:count//2]
        )

    imgs = []
    labels = []

    for setName, pool in imagePools.items():
        print("Loading dataset %s of size %i" % (setName, len(pool[0])+len(pool[1])))
        for i in range(len(pool[0])):
            imgs.append(
                np.asarray(
                    Image.open(path.join(folderPath, setName, "T", pool[0][i])).resize((512, 512))
                )
            )
            labels.append(True)
            if i < len(pool[1]):
                imgs.append(
                    np.asarray(
                        Image.open(path.join(folderPath, setName, "F", pool[1][i])).resize((512, 512))
                    )
                )
                labels.append(False)

    return np.array(imgs), np.array(labels)


folderPathOld = "OurImages/512_512/"
def loadImagesOld(count=200, shano=False):
    files = os.listdir(folderPathOld)
    imgs = []
    labels = []

    if count < 1:
        raise ValueError("Tried to load 0 images")
    if len(files) < 1:
        raise OSError("No images in folder %s " % folderPathOld)

    if shano:
        with open("OurImages/plateScanner/DhatPlate.pickle", "rb") as fil:
            sourceLabel = pickle.load(fil)
        if len(sourceLabel) < 1:
            raise ValueError("No labels loaded")

    chosen = random.choices(files, k=count)

    for f in chosen:

        if shano:
            assert sourceLabel


            image = np.asarray(
                Image.open("OurImages/plateScanner/cars_train/" + f).resize((512, 512))
                )
            if image.ndim < 3 or image.shape[2] < 3:
                continue

            imgs.append(
                image[:, :, :3]
            )
            labels.append(sourceLabel[f])
        else:
            match = re.search('type(\d+)', f)
            if match:
                imgs.append(
                    np.asarray(
                        Image.open(folderPathOld + f).resize((512, 512))
                    )[:, :, :3]
                )

                labels.append(match.group(1) == "0")

    if len(imgs) < 1:
        raise ValueError("No images matched regex type(\d+)")
    print(np.array(labels).sum()/len(np.array(labels)))
    return np.array(imgs), np.array(labels)

