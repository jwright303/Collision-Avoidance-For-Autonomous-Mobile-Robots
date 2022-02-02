import cv2
import numpy as np

camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()


    laplacian = cv2.Laplacian(frame, cv2.CV_64F)

    #threshold for detecting/calculating major edges 
    edges = cv2.Canny(frame, 100, 100)

    #shows original, laplacian, and canny(edges)
    cv2.imshow('original', frame)
    cv2.imshow('laplacian', laplacian)
    cv2.imshow('Canny', edges)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
camea.release()
