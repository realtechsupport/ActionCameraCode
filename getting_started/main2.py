from helper import *

#------------------------------------------------------------------------------
directory = os.getcwd()
directory = directory + '/'
imagename = 'thriller'
imagetype = '.jpg'
input_image =  directory + imagename + imagetype
print(input_image)
img = cv2.imread(input_image)

#convert to rgb
rgbimage = convert2rgb(img)
#shift image
shiftimage = shift_image(rgbimage, 200, 300)
#get rid of axis
f, ax = plt.subplots()
ax.axis('off')
#show result
plt.imshow(shiftimage)
plt.show()
