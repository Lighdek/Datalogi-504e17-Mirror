import random

import keras
import numpy as np
import os

from PIL import Image
from keras import optimizers
from os import path, listdir

from KerasModel import StrideConvolutionalNetwork as theThing

from pyspark import SparkContext, SparkConf

modelExt = ".h5m"
modelFilename = os.path.join(*theThing.__name__.split('.')) + modelExt
print(modelFilename)

def loadImages(datasets: list=None, shuffle: bool=True, folderPath: str="OurImages/") -> list:
    if datasets is None:
        datasets = [
            (100, 'RealFrontBack'),
            (100, 'GenLicenseOnBackground')
        ]

    imagePools = {}
    for (count, setName) in datasets:
        imagePools[setName] = (
            listdir(path.join(folderPath, setName, "T")[:count//2 + count % 2]),
            listdir(path.join(folderPath, setName, "F")[:count//2])
        )

    imgs = []

    for setName, pool in imagePools.items():
        print("Loading dataset %s" % setName)
        for i in range(len(pool[0])):
            imgs.append(
                Image.open(path.join(folderPath, setName, "T", pool[0][i]))
            )
            if i < len(pool[1]):
                imgs.append(
                    Image.open(path.join(folderPath, setName, "F", pool[1][i]))
                )

    if shuffle:
        random.shuffle(imgs)

    return imgs

def trainModel(x, modelTuple):

    print("Training model: %i" % x)
    config, weights = modelTuple

    model = keras.models.Sequential.from_config(config)
    model.set_weights(weights)

    optimizer = optimizers.adam(lr=1e-4, decay=1e-6)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

    images, labels = loadImages()

    metrics = model.train_on_batch(np.array(images), labels)  # TODO: look at class_weight and sample_weight

    for i in range(len(metrics)):
        print("%s: %s" % (model.metrics_names[i], metrics[i]))

    return 1, np.array(model.get_weights())


if __name__ == '__main__':

    try:
        model = keras.models.load_model(modelFilename)
    except OSError as e:
        print(e)
        model = theThing.init()

    model.summary()

    conf = SparkConf().setAppName(theThing.__name__)
    sc = SparkContext(conf=conf)

    for i in range(100):

        sharedModel = sc.broadcast((model.get_config(), model.get_weights()))

        taskDummy = sc.parallelize(range(56))

        changedWeights = taskDummy.map(lambda x: trainModel(x, sharedModel.value))

        combinedCount, combinedWeights = changedWeights.reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]))

        finalWeights = combinedWeights / combinedCount

        if True:  # Calculate the change from the average, so we can scale it up
            deltaWeights = finalWeights - model.get_weights()
            finalWeights = model.get_weights() + deltaWeights*combinedCount

        model.set_weights(finalWeights)
        model.save(modelFilename)

        print("TRAINING TEMP ON MASTER!!!!!")
        print(model.metrics_names)
        trainModel(1337,(model.get_config(), model.get_weights()))
