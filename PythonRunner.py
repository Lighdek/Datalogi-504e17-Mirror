import keras
import os
import metrics as m
import random
from ImageGeneration import ImageLoader
from KerasModel import MatiasStrideConvolutionalNetwork as theThing

modelExt = ".hem"
testExt = "1x"
modelFilename = os.path.join(*theThing.__name__.split('.')) + modelExt
print(modelFilename)
batchsize = 40

if __name__ == '__main__':
    try:
        model = keras.models.load_model(modelFilename, custom_objects={'f1measure': m.f1measure,
                                                                       'f_half_measure': m.f_half_measure,
                                                                       'precision': m.precision,
                                                                       'recall': m.recall})
    except OSError as e:
        print(e)
        model = theThing.init()

    model.summary()

    callback = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=batchsize,
                                           write_graph=True, write_grads=True, write_images=True, embeddings_freq=0,
                                           embeddings_layer_names=None, embeddings_metadata=None, )

    #images, labels = ImageLoader.loadImagesOld(count=5000) #ImageGenerator.Generator(200)

    images, labels = ImageLoader.loadImages(datasets = [(1100, 'RealFrontBack'), (8900, 'GenLicenseOnBackground')])

    model.fit(images, labels, batch_size=batchsize, epochs=100, verbose=1,
              validation_split=0.10, shuffle=True, callbacks=[callback])

    #scores = model.evaluate(images, labels, batch_size=50, verbose=1)
    #print('loss=%f acc=%f, f1=%f, f½=%f pre=%f rec=%f' % (scores[0], scores[1], scores[2], scores[3], scores[4], scores[5]))
    model.save(os.path.join(*theThing.__name__.split('.')) + testExt + modelExt)
