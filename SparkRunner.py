import keras
import numpy as np
import os

from keras import optimizers

from ImageGeneration import ImageLoader
from KerasModel import StrideConvolutionalNetwork as theThing

from pyspark import SparkContext, SparkConf

modelExt = ".hem"
modelFilename = os.path.join(*theThing.__name__.split('.')) + modelExt
print(modelFilename)

# loadImages() here ???

def trainModel(x, modelTuple):

    print("Training model: %i" % x)
    config, weights = modelTuple

    model = keras.models.Sequential.from_config(config)
    model.set_weights(weights)

    optimizer = optimizers.adam(lr=1e-4, decay=1e-6)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

    images, labels = ImageLoader.loadImages()

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

        taskDummy = sc.parallelize(range(64))

        changedWeights = taskDummy.map(lambda x: trainModel(x, sharedModel.value))

        combinedCount, combinedWeights = changedWeights.reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]))

        finalWeights = combinedWeights / combinedCount

        model.set_weights(finalWeights)
        model.save(modelFilename)

        print("TRAINING TEMP ON MASTER!!!!!")
        print(model.metrics_names)
        trainModel(1337,(model.get_config(), model.get_weights()))
