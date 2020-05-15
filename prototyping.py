import cv2
import numpy as np
from utils import *
import pickle

# putanje do slika
rgbImgSrcPath = "yellowSrc.bmp"
rgbImgRefPath = "yellowRef.bmp"

############################################################################################################################################################################################################

# učitavanje slika
rgbImgSrc = cv2.imread(rgbImgSrcPath)
rgbImgRef = cv2.imread(rgbImgRefPath)

############################################################################################################################################################################################################

# # generiranje potrebnih polja/matrica
# height, width, colorLayer = rgbImgSrc.shape
# hsvImgSrc = np.zeros((height, width, colorLayer), dtype='uint8')
# hsvImgRef = np.zeros((height, width, colorLayer), dtype='uint8')
# roi = np.zeros((height, width, colorLayer), dtype='uint8')

# # definiranje granica za boje
# lowerRed = np.array([140, 100, 100])
# upperRed = np.array([179, 255, 255])

# lowerYellow = np.array([20, 70, 150])
# upperYellow = np.array([30, 255, 255])


# lowerGreen = np.array([36, 90, 100])
# upperGreen = np.array([86, 255, 255])


# lowerBlue = np.array([94, 80, 80])
# upperBlue = np.array([126, 255, 255])

# ############################################################################################################################################################################################################

# # pretvorba slike u hsv
# hsvImgSrc = convToHSV(rgbImgSrc, hsvImgSrc)
# hsvImgRef = convToHSV(rgbImgRef, hsvImgRef)

# ############################################################################################################################################################################################################


# # redMaskSrc = cv2.inRange(hsvImgSrc, lowerRed, upperRed)
# # hsvBitWiseSrc = cv2.bitwise_and(rgbImgSrc, rgbImgSrc, mask=redMaskRef)

# # dobivanje maski
# redMaskRef = cv2.inRange(hsvImgRef, lowerRed, upperRed)
# redMaskSrc = cv2.inRange(hsvImgSrc, lowerRed, upperRed)

# yellowMaskRef = cv2.inRange(hsvImgRef, lowerYellow, upperYellow)
# yellowMaskSrc = cv2.inRange(hsvImgSrc, lowerYellow, upperYellow)

# greenMaskRef = cv2.inRange(hsvImgRef, lowerGreen, upperGreen)
# greenMaskSrc = cv2.inRange(hsvImgSrc, lowerGreen, upperGreen)

# blueMaskRef = cv2.inRange(hsvImgRef, lowerBlue, upperBlue)
# blueMaskSrc = cv2.inRange(hsvImgSrc, lowerBlue, upperBlue)


# # detektiranje točaka
# redSrcI, redSrcJ = getPoints(redMaskSrc, "red")
# yellowSrcI, yellowSrcJ = getPoints(yellowMaskSrc, "yellow")
# greenSrcI, greenSrcJ = getPoints(greenMaskSrc, "green")
# blueSrcI, blueSrcJ = getPoints(blueMaskSrc, "blue")

# redRefI, redRefJ = getPoints(redMaskRef, "red")
# yellowRefI, yellowRefJ = getPoints(yellowMaskRef, "yellow")
# greenRefI, greenRefJ = getPoints(greenMaskRef, "green")
# blueRefI, blueRefJ = getPoints(blueMaskRef, "blue")

# # pohrana točaka
# srcPts = np.array([[redSrcJ, redSrcI], [yellowSrcJ, yellowSrcI], [greenSrcJ, greenSrcI], [blueSrcJ, blueSrcI]])
# refPts = np.array([[redRefJ, redRefI], [yellowRefJ, yellowRefI], [greenRefJ, greenRefI], [blueRefJ, blueRefI]])

# # h, status = cv2.findHomography(srcPts, refPts)
# matH = findMatrixH(srcPts, refPts)


# # with open('matH.pkl', 'wb') as handle:
# #     pickle.dump(matH, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('matH.pkl', 'rb') as handle:
    matH = pickle.load(handle)

angle = 10
deltaX = 50
deltaY = -25

cosTheta = math.cos(angle * math.pi / 180)
sinTheta = math.sin(angle * math.pi / 180)

warpMat = [[cosTheta, -sinTheta, deltaX], [sinTheta, cosTheta, deltaY], [0, 0, 1]]

warpedImg = cv2.warpPerspective(rgbImgSrc, matH, (rgbImgSrc.shape[1], rgbImgSrc.shape[0]))
myWarp = warpImg(rgbImgSrc, matH)
fakeWarp = warpImg(rgbImgSrc, warpMat)
# netWarp = fix_image(rgbImgSrc, warpMat)

cv2.imshow("prije", rgbImgSrc)
cv2.imshow("poslje", myWarp)
cv2.imshow("rucniPoslje", fakeWarp)
# cv2.imshow("netWarp", netWarp)
cv2.imwrite("original.jpg", rgbImgSrc)
cv2.imwrite("matH.jpg", myWarp)
cv2.imwrite("myValues.jpg", fakeWarp)

# hCv, cvStat = cv2.findHomography(mouseSrcPts, mouseRefPts)
# warpedImgCv = cv2.warpPerspective(rgbImgSrc, hCv, (hsvImgSrc.shape[1], hsvImgSrc.shape[0]))
# cv2.imshow("UnStitched", warpedImg)
# cv2.waitKey(0)

# rec = warpedImg
# imgStitch(rec, rgbImgRef)

# cv2.imshow("Stitched", warpedImg)
# cv2.imshow("warpedImgCv", warpedImgCv)

cv2.waitKey(0)