import numpy as np
import cv2 as cv

img1 = cv.imread('DST.png',cv.IMREAD_GRAYSCALE)
img2 = cv.imread('DST_nowatermark.png',cv.IMREAD_GRAYSCALE)

mse = 0
for i in range(0,len(img1)):
     for j in range(0,len(img1[0])):
          mse = mse + np.square(img1[i][j] - img2[i][j])
     
mse = mse / (len(img1) * len(img1[0]))
print(mse)
db = 20 * np.log10(255) - 10*np.log10(mse)
print(db)


