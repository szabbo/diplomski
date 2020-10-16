#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int randomNum(int lower, int upper) 
{ 
    return (rand() % (upper - lower + 1)) + lower;
}

void multiply(int **imgPtr, double **warpPtr, int *pixelCoordinates, int *newPixelCoordinates)
{
    *(newPixelCoordinates) = (*(*(warpPtr)) * *(pixelCoordinates)) + (*(*(warpPtr) + 1) * *(pixelCoordinates + 1)) + (*(*(warpPtr) + 2) * *(pixelCoordinates + 2));
    *(newPixelCoordinates + 1) = (*(*(warpPtr + 1)) * *(pixelCoordinates)) + (*(*(warpPtr + 1) + 1) * *(pixelCoordinates + 1)) + (*(*(warpPtr + 1) + 2) * *(pixelCoordinates + 2));
    *(newPixelCoordinates) = (*(*(warpPtr + 2)) * *(pixelCoordinates)) + (*(*(warpPtr + 2) + 1) * *(pixelCoordinates + 1)) + (*(*(warpPtr + 2) + 2) * *(pixelCoordinates + 2));    
}

int main()
{
    int **imgPtr, **newImgPtr, i, j, pixel[3], newPixel[3];
    double **warpPtr;

    //alokacija  
    warpPtr = (double**)malloc(3 * sizeof(double*));
    for (i = 0; i < 3; i++)
        *(warpPtr + i) = (double*)malloc(3 * sizeof(double));
    

    imgPtr = (int**)malloc(10 * sizeof(int*));
    newImgPtr = (int**)malloc(10 * sizeof(int*));
    for (i = 0; i < 10; i++)
    {
        *(imgPtr + i) = (int*)malloc(10 * sizeof(int));
        *(newImgPtr + i) = (int*)malloc(10 * sizeof(int));
    }

    // inicijalizacija random brojevima
    for (i = 0; i < 10; i++)
        for (j = 0; j < 10; j++)
        {
            if (i <= 2 && j <= 2)
                *(*(warpPtr + i) + j) = randomNum(1, 10);
            
            *(*(imgPtr + i) + j) = randomNum(1, 10);
            
        }
    
    for (i = 0; i < 10; i++)
    {
        for (j = 0; j < 10; j++)
        {
            pixel[0] = i;   pixel[1] = j;   pixel[2] = 1;
            multiply(imgPtr, warpPtr, pixel, newPixel);

            *(*(newImgPtr + newPixel[0]) + newPixel[1]) = *(*(imgPtr + i) + j);
        }
        
    }

    printf("StaraSlika!\n");
    for (i = 0; i < 10; i++)
    {
        for (j = 0; j < 10; j++)
        {
            printf("%d\t", *(*(imgPtr + i) + j));
        }
        printf("\n");
    }

    printf("NovaSlika!\n");
    for (i = 0; i < 10; i++)
    {
        for (j = 0; j < 10; j++)
        {
            printf("%d\t", *(*(newImgPtr + i) + j));
        }
        printf("\n");
    }
    

    // dealokacija
    for (i = 0; i < 3; i++)
        free(*(warpPtr + i));
    free(warpPtr);

    for (i = 0; i < 10; i++)
    {      
        free(*(imgPtr + i));
        free(*(newImgPtr + i));
    }
    free(imgPtr);
    free(newImgPtr);
    
    return 0;
}