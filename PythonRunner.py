import keras
import os
from ImageGeneration import ImageLoader
from KerasModel import MatiasStrideConvolutionalNetwork as theThing

modelExt = ".hem"
testExt = "1x"
modelFilename = os.path.join(*theThing.__name__.split('.')) + modelExt
print(modelFilename)
batchsize = 40

if __name__ == '__main__':
    model = theThing.init()

    model.summary()

    callback = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=batchsize,
                                           write_graph=True, write_grads=True, write_images=True, embeddings_freq=0,
                                           embeddings_layer_names=None, embeddings_metadata=None, )

    #images, labels = ImageLoader.loadImagesOld(count=5000) #ImageGenerator.Generator(200)

    images, labels = ImageLoader.loadImages(datasets = [(1100, 'RealFrontBack'), (8900, 'GenLicenseOnBackground')])

    model.fit(images, labels, batch_size=batchsize, epochs=20, verbose=1,
              validation_split=0.10, shuffle=True, callbacks=[callback])

    model.save(os.path.join(*theThing.__name__.split('.')) + testExt + modelExt)
