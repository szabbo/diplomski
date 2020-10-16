import cv2
import math
import numpy as np

def createHsvPixel(hue, saturation, value):

    tmpHSV = []
    tmpList = list()
    hue = int(hue)
    saturation = int(saturation)

    tmpHSV.extend([hue, saturation, value])
    tmpList.append(tmpHSV)
    hsvPixel = np.array(tmpHSV)

    return hsvPixel

def calcHSV(r, g, b):

    newR = r / 255
    newG = g / 255
    newB = b / 255

    mx = max(newR, newG, newB)
    mn = min(newR, newG, newB)
    v = mx
    delta = mx - mn

    if mx == 0:
        s = 0
    else:
        s = delta / mx

    if mx == mn:
        h = 0
    else:
        if mx == newR:
            h = (newG - newB) / delta
            if newG <= newB:
                h += 6
            else:
                h += 0

        elif mx == newG:
            h = ((newB - newR) / delta) + 2

        elif mx == newB:
            h = ((newR - newG) / delta) + 4

        h /= 6

        if h * 180 == 180:
            h = 0

    return h * 180, s * 255, v * 255

def convToHSV(inImg, outImg):
    for i in range(inImg.shape[0]):
        for j in range(inImg.shape[1]):
            rgbPixel = inImg[i][j]
            h, s, v = calcHSV(rgbPixel[2], rgbPixel[1], rgbPixel[0])
            hsvPixel = createHsvPixel(h, s, v)
            outImg[i][j] = hsvPixel

    return outImg

def getPoints(imgMask):
    rCnt = 0
    yCnt = 0
    gCnt = 0
    bCnt = 0
    isFound = False

    for i in range(imgMask.shape[0]):
        for j in range(imgMask.shape[1]):
            pixel = imgMask[i][j]
        
            if i <= imgMask.shape[0] / 2:
                if j > 0 and j <= (imgMask.shape[1] / 2) and pixel == 255: # red
                    ptsI = i
                    ptsJ = j
                    if rCnt == 32:
                        isFound = True
                    rCnt += 1
                elif j > (imgMask.shape[1] / 2) and j <= imgMask.shape[1] and pixel == 255: # yellow
                    ptsI = i
                    ptsJ = j
                    if yCnt == 32:
                        isFound = True
                    yCnt += 1
            if i > imgMask.shape[0] / 2: 
                if j > (imgMask.shape[1] / 2) and j <= imgMask.shape[1] and pixel == 255: # green
                    ptsI = i
                    ptsJ = j
                    if gCnt == 32:
                        isFound = True
                    gCnt += 1
                elif j > 0 and j <= (imgMask.shape[1] / 2) and pixel == 255: # blue
                    ptsI = i
                    ptsJ = j
                    if bCnt == 32:
                        isFound = True
                    bCnt += 1
            if isFound:
                break

    print("I: ", ptsI)
    print("J: ", ptsJ)

    return
    return ptsI, ptsJ

def findMatrixH(srcPts, refPts):
    eq =[
    [-srcPts[0][0], -srcPts[0][1], -1, 0, 0, 0, srcPts[0][0] * refPts[0][0], srcPts[0][1] * refPts[0][0], refPts[0][0]],
    [0, 0, 0, -srcPts[0][0], -srcPts[0][1], -1, srcPts[0][0] * refPts[0][1], srcPts[0][1] * refPts[0][1], refPts[0][1]],
    [-srcPts[1][0], -srcPts[1][1], -1, 0, 0, 0, srcPts[1][0] * refPts[1][0], srcPts[1][1] * refPts[1][0], refPts[1][0]],
    [0, 0, 0, -srcPts[1][0], -srcPts[1][1], -1, srcPts[1][0] * refPts[1][1], srcPts[1][1] * refPts[1][1], refPts[1][1]],
    [-srcPts[2][0], -srcPts[2][1], -1, 0, 0, 0, srcPts[2][0] * refPts[2][0], srcPts[2][1] * refPts[2][0], refPts[2][0]],
    [0, 0, 0, -srcPts[2][0], -srcPts[2][1], -1, srcPts[2][0] * refPts[2][1], srcPts[2][1] * refPts[2][1], refPts[2][1]],
    [-srcPts[3][0], -srcPts[3][1], -1, 0, 0, 0, srcPts[3][0] * refPts[3][0], srcPts[3][1] * refPts[3][0], refPts[3][0]],
    [0, 0, 0, -srcPts[3][0], -srcPts[3][1], -1, srcPts[3][0] * refPts[3][1], srcPts[3][1] * refPts[3][1], refPts[3][1]],
    [0, 0, 0, 0, 0, 0, 0, 0, 1]]

    solution = [0, 0, 0, 0, 0, 0, 0, 0, 1]

    eq = np.array(eq, float)
    solution = np.array(solution, float)

    n = len(solution)

    for k in range(n):
        if np.fabs(eq[k, k]) < 1.0e-12:
            for i in range(k + 1, n):
                if np.fabs(eq[i, k]) > np.fabs(eq[k, k]):
                    for j in range(k, n):
                        eq[k, j], eq[i, j] = eq[i, j], eq[k, j]

                    solution[k], solution[i] = solution[i], solution[k]
                    break

        pivot = eq[k, k]

        for j in range(k, n):
            eq[k, j] /= pivot

        solution[k] /= pivot

        for i in range(n):
            if i ==k or eq[i, k] == 0:
                continue

            factor = eq[i, k]

            for j in range(k, n):
                eq[i, j] -= factor * eq[k, j]

            solution[i] -= factor * solution[k]

    solutionList = np.array([[solution[0], solution[1], solution[2]], [solution[3], solution[4], solution[5]], [solution[6], solution[7], solution[8]]])

    return solutionList

def warpImg(img, warpMat):
    height, width, colorLayer = img.shape
    warpedImg = np.zeros((height, width, colorLayer), dtype='uint8')
    
    for i in range(warpedImg.shape[0]):
        for j in range(warpedImg.shape[1]):
            org = [i, j, 1]

            transformed = np.dot(warpMat, org)
            depth = transformed[2]
            xTrans = transformed[0]
            yTrans = transformed[1]

            if xTrans / depth <= 0:
                newX = int(0)
            elif xTrans / depth >= 1280:
                newX = int(1280)
            else:
                newX = int(round(transformed[0] / depth))
            
            if yTrans / depth <= 0:
                newY = int(0)
            elif yTrans / depth >= 1280:
                newY = int(1280)
            else:
                newY = int(round(transformed[1] / depth))

            if newX < warpedImg.shape[0] and newY < warpedImg.shape[1]:
                warpedImg[newX][newY] = img[i][j]

    return fixMissPixel(warpedImg, img, warpMat)

def fixMissPixel(img, orgImg, matH):
    height, width, colorLayer = img.shape
    interpolatedImg = np.zeros((height, width, colorLayer), dtype='uint8')

    matH_inv = np.linalg.inv(matH)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            interpolatedImg[i, j, :] = nearest_neighbors(i, j, orgImg, matH_inv)
            

    return interpolatedImg

def nearest_neighbors(i, j, img, invMatH):
    x_max, y_max = img.shape[0] - 1, img.shape[1] - 1
    # x, y, _ = invMatH @ np.array([i, j, 1])
    x, y, _ = invMatH.dot(np.array([i, j, 1]))

    # tu si stao dovrsi
    if np.floor(x) == x and np.floor(y) == y:
        x, y = int(x), int(y)
        return img[x, y]

    if np.abs(np.floor(x) - x) < np.abs(np.ceil(x) - x):
        x = int(np.floor(x))

    else:
        x = int(np.ceil(x))

    if np.abs(np.floor(y) - y) < np.abs(np.ceil(y) - y):
        y = int(np.floor(y))

    else:
        y = int(np.ceil(y))

    if x > x_max:
        x = x_max

    if y > y_max:
        y = y_max

    return img[x, y,]