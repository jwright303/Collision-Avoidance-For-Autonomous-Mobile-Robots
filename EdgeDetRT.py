import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)

camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()


    #gray_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    blur_image = cv2.GaussianBlur(frame, (5, 5), 0)


    #Creates canny edge detection image of the camera frame
    canny = cv2.Canny(blur_image, 40, 150)

    
    (contours, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    outlines = frame.copy()
    cv2.drawContours(outlines, contours, -1, (255, 0, 0), 2)

    #applies contours to bounding edges detected
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(outlines,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow('canny edge detect', outlines)
    #plt.show()



    #laplacian = cv2.Laplacian(frame, cv2.CV_64F)

    #threshold for detecting/calculating major edges 
    #edges = cv2.Canny(frame, 100, 150)

    #shows original, laplacian, and canny(edges)
    #cv2.imshow('original', frame)
    #cv2.imshow('laplacian', laplacian)
    #cv2.imshow('Canny', edges)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
camea.release()
