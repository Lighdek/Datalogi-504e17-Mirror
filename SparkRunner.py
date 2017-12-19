import random

import keras
import numpy as np
import os

from PIL import Image
from keras import optimizers
from os import path, listdir

from KerasModel import StrideConvolutionalNetwork as theThing

from pyspark import SparkContext, SparkConf

### Start metrics

from keras import backend as K

def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def fbeta_score(y_true, y_pred, beta=1):
    if beta < 0:
        raise ValueError('The lowest choosable beta is zero (only precision).')

    # If there are no true positives, fix the F score at 0 like sklearn.
    if K.sum(K.round(K.clip(y_true, 0, 1))) == 0:
        return 0

    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    bb = beta ** 2
    fbeta_score = (1 + bb) * (p * r) / (bb * p + r + K.epsilon())
    return fbeta_score


def f1measure(y_true, y_pred):
    return fbeta_score(y_true, y_pred, beta=1)

def f_half_measure(y_true, y_pred):
    return fbeta_score(y_true, y_pred, beta=0.5)

#### end metrics

def loadImages(datasets: list=None, shuffle: bool=True, folderPath: str="/home/user/OurImages/") -> tuple:
    if datasets is None:
        datasets = [
            #(100, 'RealFrontBack'),
            (2800, 'GenLicenseOnBackground')
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
                    Image.open(path.join(folderPath, setName, "T", pool[0][i]))
                )
            )
            labels.append(True)
            if i < len(pool[1]):
                imgs.append(
                    np.asarray(
                        Image.open(path.join(folderPath, setName, "F", pool[1][i]))
                    )
                )
                labels.append(False)

    return imgs, labels

    #mode   name,           epochs
    #0      "Average")      1
    #1      "Scale")        1
    #2      "DecayingScale" 1
    #0      "Average5Epoch" 5


runName="Average"
runMode=0
runEpochs=1
modelExt = ".hem"
modelFilename = os.path.join('/home/user', *theThing.__name__.split('.')) + modelExt
print(modelFilename)

batchsize = 35


def trainModel(x, modelTuple):

    print("Training model: %i" % x)
    config, weights = modelTuple

    model = keras.models.Sequential.from_config(config)
    model.set_weights(weights)

    optimizer = optimizers.adam(lr=1e-4, decay=1e-6)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy', f1measure, f_half_measure, precision, recall])

    images, labels = loadImages([(50 ,"GenLicenseOnBackground")])

    #callback = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=batchsize,
    #                                       write_graph=True, write_grads=True, write_images=True, embeddings_freq=0,
    #                                       embeddings_layer_names=None, embeddings_metadata=None, )

    callback = keras.callbacks.CSVLogger("/home/user/logs/"+runName, append=True)

    model.fit(np.array(images), labels, batch_size=batchsize, epochs=runEpochs, verbose=1,
              validation_split=0.3, shuffle=True, callbacks=[callback])

    return 1, np.array(model.get_weights())


def main():
    #try:
    #    model = keras.models.load_model(modelFilename)
    #except OSError as e:
    #   print(e)
    model = theThing.init()

    model.summary()

    conf = SparkConf().setAppName(theThing.__name__)
    sc = SparkContext(conf=conf)

    assert (25//runEpochs)*runEpochs == 25

    for i in range(25//runEpochs):

        sharedModel = sc.broadcast((model.get_config(), model.get_weights()))

        taskDummy = sc.parallelize(range(48))

        changedWeights = taskDummy.map(lambda x: trainModel(x, sharedModel.value))

        combinedCount, combinedWeights = changedWeights.reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]))

        finalWeights = combinedWeights / combinedCount

        if runMode == 1:  # Calculate the change from the average, so we can scale it up
            originalWeights = np.array(model.get_weights())
            deltaWeights = finalWeights - originalWeights
            finalWeights = originalWeights + deltaWeights * combinedCount
        elif runMode == 2: # Some decay of the scaled average
            originalWeights = np.array(model.get_weights())
            deltaWeights = finalWeights - originalWeights
            finalWeights = originalWeights + deltaWeights * (combinedCount / i)

        model.set_weights(finalWeights)
        model.save(modelFilename+runName)


if __name__ == '__main__':
    main()
