import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import PIL
import diplib as dip

img_orig = cv2.imread("cliff_back.png", cv2.IMREAD_GRAYSCALE)

# (image [contrast]) --begin--
img = cv2.imread("cliff_back.png", 1)

#--Reading the image---
#cv2.imshow("img",img) 

#--Converting image to LAB-- 
lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
#cv2.imshow("lab",lab)

#--Splitting LAB image to different channels--
l, a, b = cv2.split(lab)
#cv2.imshow('l_channel', l)
#cv2.imshow('a_channel', a)
#cv2.imshow('b_channel', b)

#--Applying CLAHE to L-channel--
clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8))
cl = clahe.apply(l)
#cv2.imshow('CLAHE output', cl)

#--Merge the CLAHE enhanced L-channel with the a and b channel--
limg = cv2.merge((cl,a,b))
#cv2.imshow('limg', limg)

#--Converting image from LAB to RGB--
final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
cv2.imshow('final', final)

# saves the image to the current working directory
filName = 'canny_final_contrast.png'
cv2.imwrite(filName, final)

# image contrast --end--



img3 = cv2.imread("canny_final_contrast.png")


# line detection using hough transform --begin--
img_hough = cv2.imread("cliff_back.png")
gray = cv2.cvtColor(img_hough, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(final, 70, 390)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=1)
for line in lines:
   x1, y1, x2, y2 = line[0]
   cv2.line(img_hough, (x1, y1), (x2, y2), (0, 0, 256), 1)

filName = 'hough_transform.png'
cv2.imwrite(filName, img_hough)

# hough transform --end--

# parameters to adjust the threshold for calculating major edges in the image
#gray_image = cv2.cvtColor(img_orig, cv2.COLOR_RGB2GRAY)
blur_image = cv2.GaussianBlur(img_orig, (5, 5), 2)


#Creates canny edge detection image of the camera frame

# front spec
#canny = cv2.Canny(blur_image, 20, 290, apertureSize=3)

# back spec
canny = cv2.Canny(blur_image, 60, 200, apertureSize=3)

filName = 'canny2.png'
cv2.imwrite(filName, canny)

#culled edges threshold
min_threshold = 320
culled_edge = dip.BinaryAreaOpening(canny > 20, min_threshold)

#converts dip.image back to numpy array
#culled_edge = np.array(culled_edge)

(contours, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

outlines = img_orig.copy()
cv2.drawContours(outlines, contours, -1, (255, 0, 0), 2)

#applies contours to bounding edges detected
for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    cv2.rectangle(outlines,(x,y),(x+w,y+h),(0,255,0),2)

#cv2.imshow('canny edge detect', outlines)
cv2.imshow('outlines', outlines)

titles = ['image_orig_greyscale', 'hough transform', 'outlines','Canny', 'culled_edge']
images = [img_orig,  img_hough, outlines, canny, culled_edge]

# Loop to display the images corresponding to their title
for i in range(5):
    plt.subplot(2, 3, i+1), plt.imshow(images[i])
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

curb1 = plt.show()





