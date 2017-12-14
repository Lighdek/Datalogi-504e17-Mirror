import keras
import numpy as np
import os

from ImageGeneration import ImageLoader
from KerasModel import StrideConvolutionalNetwork as theThing

modelExt = ".hem"
modelFilename = os.path.join(*theThing.__name__.split('.')) + modelExt
print(modelFilename)

if __name__ == '__main__':
    try:
        model = keras.models.load_model(modelFilename)
    except OSError as e:
        print(e)
        model = theThing.init()

    model.summary()

    images, labels = ImageLoader.loadImages(count=5000) #ImageGenerator.Generator(200)

    model.fit(np.array(images), labels, batch_size=20, epochs=100, verbose=1, validation_split=0.10)

    model.save(modelFilename)
