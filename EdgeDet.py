import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import PIL

img = cv2.imread("myrx8_2.jpg", cv2.IMREAD_GRAYSCALE)

# parameters to adjust the threshold for calculating major edges in the image
edges = cv2.Canny(img,350,350)

titles = ['image', 'Canny']
images = [img, edges]

# Loop to display the images corresponding to their title
for i in range(2):
    plt.subplot(1, 2, i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()


# saves the image to the current working directory
filName = 'canny1.jpg'
cv2.imwrite(filName, edges)

