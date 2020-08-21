import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import blockmatching

# Main file
# To run use: 
imgL = cv.imread('view1.png',cv.IMREAD_GRAYSCALE)
imgR = cv.imread('view5.png',cv.IMREAD_GRAYSCALE)

# Helper Function to do basic interpolation
def interpolate(dst,i,j):
     neighbours = []
     if i > 0: 
          neighbours.append(dst[i-1][j])
          if j > 0:
               neighbours.append(dst[i-1][j-1])
               neighbours.append(dst[i][j-1])
          if j < len(imgL[0]) -1:
               neighbours.append(dst[i-1][j+1])
     if i < len(imgL) - 1:
          neighbours.append(dst[i+1][j])
          if j > 0:
               neighbours.append(dst[i+1][j-1])
          if j < len(imgL[0]) -1:
               neighbours.append(dst[i][j+1])
               neighbours.append(dst[i+1][j+1])
     return neighbours

# Step 1 Generate Disparity Map
#stereo = cv.StereoSGBM_create(numDisparities=16, blockSize=5)   # StereoSGBM
#disparity = stereo.compute(imgL,imgR) #

disparity = cv.imread('disp5.png',cv.IMREAD_GRAYSCALE) #just load good disparity map

# Step 2 Embed Watermark
#embed = blockmatching.disparityMap(imgL,dst)
embed = cv.imread('S.png',cv.IMREAD_GRAYSCALE) # change watermark here, make sure it is of appropriate size (< 1/5)

for i in range(0,len(embed)):
    for j in range(0,len(embed[0])):
        if embed[i][j] == 0:
             disparity[2+5*i][2 + 5*j] = disparity[2 + 5*i][2 + 5*j]  + 128 # To remove watermark, set this line to True


# Step 3 Create new Left Image
dst = np.zeros((len(imgL),len(imgL[0]))) 

for i in range(0,len(imgR)):
     for j in range(0,len(imgR[0])):
          d = disparity[i][j]
          cC = j + (d//16)#scale the disparity
          if d > 0 and cC > 0 and cC < len(imgL[0]):
               dst[i][cC] = imgR[i][j]
# Fill Holes in Image
for i in range(0,len(dst)):
     for j in range(0,len(dst[0])):
          if dst[i][j] == 0:
               dst[i][j] = max(interpolate(dst,i,j))


# Step 4: Recreate Disparity Map
disparity2 = blockmatching.disparityMap(imgL,dst)#stereo.compute(dst.astype(np.uint8),imgR.astype(np.uint8))

# Step 5: Recover Watermark
watermark = np.zeros((len(embed),len(embed[0]))) 

for i in range(0,len(embed)):
     for j in range(0,len(embed[0])):
          test = disparity2[2+5*i][1 + 5*j]
          # If watermark is present, there should be a noticable difference in the block value when including it in the SAD calculation
          if abs(disparity2[2 + 5*i][2 + 5*j] - test) > 2: 
               watermark[i][j] = 0
          else:
               watermark[i][j] = 255

# Print Result Images
plt.imshow(imgL,'gray')
plt.show()
plt.imshow(imgR,'gray')
plt.show()
plt.imshow(embed,'gray')
plt.show()
plt.imshow(dst,'gray')
plt.show()
plt.imshow(disparity2,'gray')
plt.show()
plt.imshow(watermark,'gray')
plt.show()



