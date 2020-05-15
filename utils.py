import cv2
import math
import numpy as np

maxVal = 0

def mouseHandler(event, x, y, flags, data):
    
    if event == cv2.EVENT_LBUTTONDOWN :
        cv2.circle(data['img'], (x, y), 3, (0, 0, 255), 5, 16)
        cv2.imshow("Image", data['img']);
        if len(data['points']) < 4 :
            data['points'].append([x, y])

def getFourPoints(img):
    
    # Set up data to send to mouse handler
    data = {}
    data['img'] = img.copy()
    data['points'] = []
    
    #Set the callback function for any mouse event
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseHandler, data)
    cv2.waitKey(0)
    
    # Convert array to np.array
    points = np.vstack(data['points']).astype(float)
    
    return points

def rgbToHsv(red, green, blue):

    maxVal = max(red, green, blue)
    minVal = min(red, green, blue)

    value = maxVal

    if value != 0:
        saturation = float((value - minVal) / value) * 255
    else:
        saturation = 0

    if value == red:
        hue = ((60 * (green - blue)) / (value - minVal) / 2)
    elif value == green:
        hue = ((120 + (60 * (blue - red))) / (value - minVal) / 2)
    elif value == blue:
        hue = ((240 + (60 * (red - green))) / (value - minVal) / 2)

    if hue < 0:
        hue += 360  / 2

    if red == green == blue:
        return 0, 0, 0
    else:
        return int(round(hue)), float(saturation), int(round(value))

def createHsvPixel(hue, saturation, value):

    tmpHSV = []
    tmpList = list()
    hue = int(hue)
    saturation = int(saturation)

    tmpHSV.extend([hue, saturation, value])
    tmpList.append(tmpHSV)
    hsvPixel = np.array(tmpHSV)

    return hsvPixel

def testFunction(r, g, b):

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
            h, s, v = testFunction(rgbPixel[2], rgbPixel[1], rgbPixel[0])
            hsvPixel = createHsvPixel(h, s, v)
            outImg[i][j] = hsvPixel

    return outImg

def getPoints(imgMask, color):
    rCnt = 0
    yCnt = 0
    gCnt = 0
    bCnt = 0
    isFound = False

    for i in range(imgMask.shape[0]):
        for j in range(imgMask.shape[1]):
            pixel = imgMask[i][j]
        
            if i <= imgMask.shape[0] / 2:
                if j > 0 and j <= (imgMask.shape[1] / 2) and pixel == 255: # and color == "red":
                    ptsI = i
                    ptsJ = j
                    if rCnt == 32:
                        isFound = True
                    rCnt += 1
                elif j > (imgMask.shape[1] / 2) and j <= imgMask.shape[1] and pixel == 255: # and color == "yellow":
                    ptsI = i
                    ptsJ = j
                    if yCnt == 32:
                        isFound = True
                    yCnt += 1
            if i > imgMask.shape[0] / 2: 
                if j > (imgMask.shape[1] / 2) and j <= imgMask.shape[1] and pixel == 255: # and color == "green":
                    ptsI = i
                    ptsJ = j
                    if gCnt == 32:
                        isFound = True
                    gCnt += 1
                elif j > 0 and j <= (imgMask.shape[1] / 2) and pixel == 255: # and color == "blue":
                    ptsI = i
                    ptsJ = j
                    if bCnt == 32:
                        isFound = True
                    bCnt += 1
            if isFound:
                break

    return ptsI, ptsJ

def imgStitch(srcImg, refImg):
    for i in range(srcImg.shape[0]):
        for j in range(srcImg.shape[1]):
            pixel = srcImg[i][j]

            if pixel.all() == 0:
                srcImg[i][j] = refImg[i][j]

    return srcImg

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
    x, y, _ = invMatH @ np.array([i, j, 1])

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

def fix_image(img, warpMat):
    height, width, colorLayer = img.shape
    warpedImg = np.zeros((height, width, colorLayer), dtype='uint8')

    for i in range(warpedImg.shape[0] - 1):
        for j in range(warpedImg.shape[1] - 1):
            newY = int(((warpMat[0][0] * i) + (warpMat[0][1] * j) + warpMat[0][2]) / ((warpMat[2][0] * i) + (warpMat[2][1] * j) + warpMat[2][2]))
            newX = int(((warpMat[1][0] * i) + (warpMat[1][1] * j) + warpMat[1][2]) / ((warpMat[2][0] * i) + (warpMat[2][1] * j) + warpMat[2][2]))

            if newX > width:
                newX = width
            elif newX < 0:
                newX = 0

            if newY > height:
                newY = height
            elif newY < 0:
                newY = 0

            print("newX: ", newX)
            print("newY: ", newY)

            if newX <= width and newY <= height:
                print("IF")
                warpedImg[newX][newY] = img[i][j]

    return warpedImg