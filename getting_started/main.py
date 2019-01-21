from helper import *
from utilities import *

directory = os.getcwd()
directory = directory + '/'
imagename = 'thriller'
imagetype = '.jpg'
input_image =  directory + imagename + imagetype
print(input_image)

img = cv2.imread(input_image)
plt.imshow(img)
plt.show()
