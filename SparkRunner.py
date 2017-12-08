import keras

import help_functions
from ImageGeneration import Generator as ImageGenerator
import numpy as np
import os

from KerasModel import printModel, StrideConvolutionalNetwork as theThing

from pyspark import SparkContext, SparkConf

modelExt = ".hem"
modelFilename = os.path.join(*theThing.__name__.split('.')) + modelExt
print(modelFilename)


def trainModel(x, modelTuple):

    print("Training model: %i" % x)
    config, weights = modelTuple

    model = keras.models.Sequential.from_config(config)
    model.set_weights(weights)

    images, labels = ImageGenerator.Generator(200)

    metrics = model.train_on_batch(np.array(images), labels)

    return 1, np.array(model.get_weights())


if __name__ == '__main__':

    try:
        model = keras.models.load_model(modelFilename)
    except OSError as e:
        print(e)
        model = theThing.init()

    conf = SparkConf().setAppName(theThing.__name__)
    sc = SparkContext(conf=conf)

    for i in range(100):

        ##pmodel = sc.parallelize(model)
        sharedModel = sc.broadcast((model.get_config(), model.get_weights()))

        taskDummy = sc.parallelize(range(64))

        changedWeights = taskDummy.map(lambda x: trainModel(x, sharedModel))

        combinedCount, combinedWeights = changedWeights.reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]))

        finalWeights = combinedWeights / combinedCount

        model.set_weights(finalWeights)
        model.save(modelFilename)




def __nothing():
        print("generating images")
        images, labels = ImageGenerator.Generator(200)
        print("done generating")
        #print(images.shape)
        #print(labels.shape)

        for image in images:
            help_functions.print_picture(image)

        metrics = model.train_on_batch(np.array(images), labels)  # TODO: look at class_weight and sample_weight
        # model.fit(np.array(images), labels, batch_size=50, epochs=1, verbose=1, validation_split=0.25)
        # model.summary()

        for i in range(len(metrics)):
            print("%s: %s" % (model.metrics_names[i], metrics[i]))

        #if i % 25 == 0:
            #printModel(model)

        model.save(modelFilename)
