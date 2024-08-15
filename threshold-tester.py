import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

blur = 5

# Read in image (gray-scale)
img = cv.imread('image.png',0)
img = cv.GaussianBlur(img,(blur,blur), sigmaX=0, sigmaY=0) 

for lo in range(25,126,25):
    for hi in range(lo+25,176,25):
        # Perform Canny Edge Detection
        cur_edges = cv.Canny(img,lo,hi,L2gradient=True)

        # Make new plot
        plt.figure()
        plt.imshow(cur_edges,cmap='gray')
        plt.title(f'{lo},{hi}'),plt.xticks([]),plt.yticks([])

plt.show()