import keras
import os
import metrics as m
from ImageGeneration import ImageLoader
from KerasModel import Log2ConvolutionalNetwork as theThing

modelExt = ".hem"
modelFilename = os.path.join(*theThing.__name__.split('.')) + modelExt
print(modelFilename)
batchsize = 35

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

    #callback = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=batchsize,
    #                                       write_graph=True, write_grads=True, write_images=True, embeddings_freq=0,
    #                                       embeddings_layer_names=None, embeddings_metadata=None, )

    callback = keras.callbacks.CSVLogger("logs/SparkEquivalent", append=True)

    for i in range(50):
        images, labels = ImageLoader.loadImages(datasets = [(4200, 'GenLicenseOnBackground')]) #35*2*48/.8

        model.fit(images, labels, batch_size=batchsize, epochs=1, verbose=1,
              validation_split=0.20, shuffle=True, callbacks=[callback])

    #model.evaluate(np.array(images), labels, batch_size=50, verbose=1)

    model.save(modelFilename+"SparkEquivalent")
