import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# Calculate Cost of disparity with SAD
#Block size fixed at 5
def calcCost(img1,img2,pixel,i):
     sad = 0
     #blocksize of 
     for k in range(pixel[0] -2,pixel[0] + 3):
          for j in range(pixel[1] -2, pixel[1] + 3):
               #Edge Costs are wacky
               if k > 0 and k+i < len(img1)-1 :
                    if j > 0 and j < len(img1[0])-1:
                         sad = sad + abs(img1[k][j] - img2[i + k][j])
     return sad

# Calculate Cost of disparity of just middle value with SAD
#Block size fixed at 5
def calcCostMid(img1,img2,pixel,i):
     sad = 0
     #blocksize of 
     #Edge Costs are wacky
     if pixel[0] > 0 and pixel[0]+i < len(img1)-1 :
          if pixel[1] > 0 and pixel[1] < len(img1[0])-1:
               sad = sad + abs(img1[pixel[0]][pixel[1]] - img2[i + pixel[0]][pixel[1]])
     return sad

# Calculate Cost of disparity of all but middle value with SAD
#Block size fixed at 5
def calcCost_noMid(img1,img2,pixel,i):
     sad = 0
     #blocksize of 
     for k in range(pixel[0] -2,pixel[0] + 3):
          for j in range(pixel[1] -2, pixel[1] + 3):
               #Edge Costs are wacky
               if k > 0 and k+i < len(img1)-1 :
                    if j > 0 and j < len(img1[0])-1:
                         if k != pixel[0] and j != pixel[1]:
                              sad = sad + abs(img1[k][j] - img2[i + k][j])
     return sad

#Calculate Disparity value for a block
def calcDisparity(img1,img2,pixel,blockrange):
     best_cost = [0,1000000]
     for i in range(1,blockrange):
          c = calcCost(img1,img2,pixel,i)
          if c < best_cost[1]:
               best_cost = [i,c]
     disparity = best_cost[0]
     return disparity

#Calculate Disparity value for a pixel
def calcDisparityMid(img1,img2,pixel,blockrange):
     best_cost = [0,1000000]
     for i in range(1,blockrange):
          c = calcCostMid(img1,img2,pixel,i)
          if c < best_cost[1]:
               best_cost = [i,c]
     disparity = best_cost[0]
     return disparity

#Calculate Disparity value for a block without middle pixel
def calcDisparityNoMid(img1,img2,pixel,blockrange):
     best_cost = [0,1000000]
     for i in range(1,blockrange):
          c = calcCost_noMid(img1,img2,pixel,i)
          if c < best_cost[1]:
               best_cost = [i,c]
     disparity = best_cost[0]
     return disparity

# Calculate a Disparity Map
def disparityMap(img1,img2):
     # check if same size
     # create empty map
     dst = np.zeros((len(img1),len(img1[0]))) 
     blockrange = 16
     # For each pixel in img, find disparity and store to map
     for i in range(2,len(img1),5):
          for j in range(2,len(img1[0]),5):
               x = calcDisparityNoMid(img1,img2,[i,j],blockrange)
               y = calcDisparity(img1,img2,[i,j],blockrange)
               for k in range(i -2,i + 3):                    
                    for m in range(j -2, j + 3):
                         if k == i and m == j:
                              dst[k][m] = int(y)
                         else:
                              dst[k][m] = int(x)
     return dst
