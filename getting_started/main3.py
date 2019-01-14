from helper import *

#------------------------------------------------------------------------------
directory = os.getcwd()
directory = directory + '/'
imagename = 'thriller'
imagetype = '.jpg'
input_image =  directory + imagename + imagetype
img = cv2.imread(input_image)

#second image
imagename = 'thriller_flip'
imagetype = '.png'
image2 = directory + imagename + imagetype

#convert to rgb
rgbimage = convert2rgb(img)
#get rid of axis
f, ax = plt.subplots()
ax.axis('off')

#do overlay
v1 = 0.5; v2 = 0.5; v3 = 0
result = overlay(input_image, v1, image2, v2, v3)
#show result
plt.imshow(result)
plt.show()
