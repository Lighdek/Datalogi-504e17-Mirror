import numpy as np
import os

from ImageGeneration import ImageLoader
from KerasModel import StrideConvolutionalNetwork as theThing

modelExt = ".hem"
modelFilename = os.path.join(*theThing.__name__.split('.')) + modelExt
print(modelFilename)

if __name__ == '__main__':
    model = theThing.init()

    i = 1
    while True:
        images, labels = ImageLoader.loadImages() #ImageGenerator.Generator(200)

        model.fit(np.array(images), labels, batch_size=150, epochs=1, verbose=1, validation_split=0.25)
        model.summary()

        #if i % 25 == 0:
            #printModel(model)

        i += 1

        model.save(modelFilename)