#from PIL import Image
#import numpy as np


# def _normalized(a, axis=-1, order=2):
#     l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
#     l2[l2 == 0] = 1
#     return a / np.expand_dims(l2, axis)
#
# def printModel(model):
#     mw = model.layers[0].get_weights()[0]
#     for k in range(mw.shape[3]):
#         # thek = (mw[:,:,:,k]+0)*1024
#         thek = _normalized(mw[:, :, :, k] + 1, axis=-1) * 255
#         # thek = _normalized(_normalized(normalized(mw[:,:,:,k]+1, axis=2), axis=1), axis=0)*255 #TODO: testing norm axis=2
#         # thek = _normalized(mw[:, :, :, k] + 1, axis=2)
#         print(thek)
#         print_picture(Image.frombuffer("RGB", thek.shape[0:2], thek))