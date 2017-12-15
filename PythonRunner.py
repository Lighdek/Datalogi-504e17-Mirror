import keras
import numpy as np
import os
from ImageGeneration import ImageLoader
from KerasModel import Log2ConvolutionalNetwork as theThing

modelExt = ".hem"
modelFilename = os.path.join(*theThing.__name__.split('.')) + modelExt
print(modelFilename)
batchsize = 50

if __name__ == '__main__':
    try:
        model = keras.models.load_model(modelFilename)
    except OSError as e:
        print(e)
        model = theThing.init()

    model.summary()

    #images, labels = ImageLoader.loadImagesOld(count=5000) #ImageGenerator.Generator(200)

    for i in range(100):#!!!!== SparkRunner for loop værdi!!!!
        images, labels = ImageLoader.loadImages(datasets = [(2800, 'GenLicenseOnBackground')])

        model.fit(np.array(images), labels, batch_size=batchsize, epochs=1, verbose=1,
                  validation_split=0, shuffle=True)

    #model.evaluate(np.array(images), labels, batch_size=50, verbose=1)

    model.save(modelFilename+"_Special_Edition")
