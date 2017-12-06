import timeit
from ImageGeneration.maintester import bob
from PIL import Image, ImageFilter
from os.path import join
from help_functions import loadImageMatrix, clamp

def kim():
    bob()




print("Alright lads, and ladies. Let the test commit. Firstly we will test quickBlur by Skov")
print("Let the test commit.")
print(timeit.timeit('kim()',setup="from __main__ import kim", number=10))
#print("Wow. That took some time. Next up we've got Pillow, with the already generated filter called ImageFilter.BLUR")
#print(timeit.timeit('stupidtest2()',setup="from __main__ import stupidtest2", number=1))
#print("Wow. That took some time. Last but not least we've got Pillow again, this time with the filter called ImageFilter.GaussianBlur and a radius of 2")
#print(timeit.timeit('stupidtest3()',setup="from __main__ import stupidtest3", number=1))

#print("That's it ladies and gents. Trhanks for tonight. Hope you die just as awfully as I did performing these tests.")