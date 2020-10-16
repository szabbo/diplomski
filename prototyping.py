import cv2
import numpy as np
from utils import *
import pickle

# putanje do slika
rgbImgSrcPath = "srcImg.bmp"
rgbImgRefPath = "refImg.bmp"

############################################################################################################################################################################################################

# ucitavanje slika
rgbImgSrc = cv2.imread(rgbImgSrcPath)
rgbImgRef = cv2.imread(rgbImgRefPath)

############################################################################################################################################################################################################

# generiranje potrebnih polja/matrica
height, width, colorLayer = rgbImgSrc.shape
hsvImgSrc = np.zeros((height, width, colorLayer), dtype='uint8')
hsvImgRef = np.zeros((height, width, colorLayer), dtype='uint8')
roi = np.zeros((height, width, colorLayer), dtype='uint8')

# definiranje granica za boje
# lowerRed = np.array([140, 100, 100])
# upperRed = np.array([179, 255, 255])

# lowerYellow = np.array([20, 70, 150])
# upperYellow = np.array([30, 255, 255])


# lowerGreen = np.array([36, 90, 100])
# upperGreen = np.array([86, 255, 255])


# lowerBlue = np.array([94, 80, 80])
# upperBlue = np.array([126, 255, 255])


lowerRed = np.array([140, 80, 80])
upperRed = np.array([179, 255, 255])

lowerYellow = np.array([20, 70, 80])
upperYellow = np.array([30, 255, 255])


lowerGreen = np.array([36, 90, 80])
upperGreen = np.array([86, 255, 255])


lowerBlue = np.array([94, 80, 80])
upperBlue = np.array([126, 255, 255])

############################################################################################################################################################################################################

# pretvorba slike u hsv
hsvImgSrc = convToHSV(rgbImgSrc, hsvImgSrc)
hsvImgRef = convToHSV(rgbImgRef, hsvImgRef)

############################################################################################################################################################################################################


# redMaskSrc = cv2.inRange(hsvImgSrc, lowerRed, upperRed)
# hsvBitWiseSrc = cv2.bitwise_and(rgbImgSrc, rgbImgSrc, mask=redMaskRef)

# dobivanje maski
redMaskRef = cv2.inRange(hsvImgRef, lowerRed, upperRed)
redMaskSrc = cv2.inRange(hsvImgSrc, lowerRed, upperRed)

yellowMaskRef = cv2.inRange(hsvImgRef, lowerYellow, upperYellow)
yellowMaskSrc = cv2.inRange(hsvImgSrc, lowerYellow, upperYellow)

greenMaskRef = cv2.inRange(hsvImgRef, lowerGreen, upperGreen)
greenMaskSrc = cv2.inRange(hsvImgSrc, lowerGreen, upperGreen)

blueMaskRef = cv2.inRange(hsvImgRef, lowerBlue, upperBlue)
blueMaskSrc = cv2.inRange(hsvImgSrc, lowerBlue, upperBlue)


# detektiranje tocaka
redSrcI, redSrcJ = getPoints(redMaskSrc)
yellowSrcI, yellowSrcJ = getPoints(yellowMaskSrc)
greenSrcI, greenSrcJ = getPoints(greenMaskSrc)
blueSrcI, blueSrcJ = getPoints(blueMaskSrc)

redRefI, redRefJ = getPoints(redMaskRef)
yellowRefI, yellowRefJ = getPoints(yellowMaskRef)
greenRefI, greenRefJ = getPoints(greenMaskRef)
blueRefI, blueRefJ = getPoints(blueMaskRef)

# pohrana tocaka
srcPts = np.array([[redSrcJ, redSrcI], [yellowSrcJ, yellowSrcI], [greenSrcJ, greenSrcI], [blueSrcJ, blueSrcI]])
refPts = np.array([[redRefJ, redRefI], [yellowRefJ, yellowRefI], [greenRefJ, greenRefI], [blueRefJ, blueRefI]])

# h, status = cv2.findHomography(srcPts, refPts)
matH = findMatrixH(srcPts, refPts)

print("NEW MAT H: ", matH)

# # with open('matH.pkl', 'wb') as handle:
# #     pickle.dump(matH, handle, protocol=pickle.HIGHEST_PROTOCOL)

# # with open('matH.pkl', 'rb') as handle:
# #     matH = pickle.load(handle)

# # print(matH)

warpedImg = cv2.warpPerspective(rgbImgSrc, matH, (rgbImgSrc.shape[1], rgbImgSrc.shape[0]))
myWarp = warpImg(rgbImgSrc, np.transpose(matH))

cv2.imshow("prije", rgbImgSrc)
cv2.imshow("poslje", myWarp)

cv2.imwrite("original.jpg", rgbImgSrc)
cv2.imwrite("matH.jpg", myWarp)

cv2.waitKey(0)