import keras
import os
import metrics as m
from ImageGeneration import ImageLoader
from KerasModel import StrideConvolutionalNetwork as theThing

modelExt = ".hem"
modelFilename = os.path.join(*theThing.__name__.split('.')) + modelExt
print(modelFilename)
batchsize = 40

if __name__ == '__main__':
    try:
        model = keras.models.load_model(modelFilename, custom_objects={'f1measure': m.f1measure,
                                                                       'f_half_measure': m.f_half_measure,
                                                                       'precision': m.precision,
                                                                       'recall': m.recall})
        model.summary()

        images, labels = ImageLoader.loadImages(datasets=[(1000, 'RealFrontBack'), (0, 'GenLicenseOnBackground')])

        scores = model.evaluate(images, labels, batch_size=batchsize, verbose=1)
        print(model.metrics_names)

        print('loss=%f acc=%f, f1=%f, f½=%f pre=%f rec=%f' % (
        scores[0], scores[1], scores[2], scores[3], scores[4], scores[5]))

    except OSError as e:
        print(e)
