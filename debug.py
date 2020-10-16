import cv2
import numpy as np

def multiply(warpMat, coordinates):
    newC = [0, 0, 0]

    newC[0] = int((warpMat[0][0] * coordinates[0]) + (warpMat[0][1] * coordinates[1]) + (warpMat[0][2] * coordinates[2]))
    newC[1] = int((warpMat[1][0] * coordinates[0]) + (warpMat[1][1] * coordinates[1]) + (warpMat[1][2] * coordinates[2]))
    newC[2] = int((warpMat[2][0] * coordinates[0]) + (warpMat[2][1] * coordinates[1]) + (warpMat[2][2] * coordinates[2]))

    return newC

warpMat = [[1.002024656, -4.29983455e-02, -3.56814304e-06], [7.5826531e-02, 9.98696653e-01, 1.08887277e-05], [0, 0, 1]]
print(warpMat)

img = cv2.imread("yellowSrc.bmp")
height, width, colorLayer = img.shape
print(img.shape[0])
bufferImg = np.zeros((height, width, colorLayer), dtype='uint8')

for i in range(height):
    for j in range(width):
        orgC = [i, j, 1]
        newC = multiply(warpMat, orgC)

        if newC[0] >= height:
            newC[0] = height - 1
        if newC[1] >= width:
            newC[1] = width - 1
        
        if newC[0] < 0:
            newC[0] = 0
        if newC[1] < 0:
            newC[1] = 0

        bufferImg[newC[0]][newC[1]] = img[i][j]


cv2.imshow("test", bufferImg)
cv2.waitKey(0)

# outputPtr = Utils_memAlloc(UTILS_HEAPID_DDR_NON_CACHED_SR0, brElemenata, sizeof(tipPodatka));
# Utils_memFree(UTILS_HEAPID_DDR_NON_CACHED_SR0, outputPtr, 9);
# memcpy(&inPtr[0], &outputPtr, sizeof(outputPtr));

*(newCrd + 0) = (int) round((*(warpPtr + (0 * 3) + 0) * (oldCrd + 0)) + (*(warpPtr + (0 * 3) + 1) * (oldCrd + 1)) + (*(warpPtr + (0 * 3) + 2) * (oldCrd + 2)));
*(newCrd + 1) = (int) round((*(warpPtr + (1 * 3) + 1) * (oldCrd + 1)) + (*(warpPtr + (1 * 3) + 1) * (oldCrd + 1)) + (*(warpPtr + (1 * 3) + 2) * (oldCrd + 2)));
*(newCrd + 2) = (int) round((*(warpPtr + (2 * 3) + 2) * (oldCrd + 2)) + (*(warpPtr + (2 * 3) + 1) * (oldCrd + 1)) + (*(warpPtr + (2 * 3) + 2) * (oldCrd + 2)));