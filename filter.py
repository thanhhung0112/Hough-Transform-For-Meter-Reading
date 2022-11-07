import cv2
import numpy as np
import matplotlib.pyplot as plt

def implement_filter(image, n):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel_lap = np.array([[0, 1, 0],
                           [1, -4, 1],
                           [0, 1, 0]])

    image = cv2.GaussianBlur(image, (n, n), 0)
    laplacian = cv2.filter2D(image, -1, kernel_lap)
    _, laplacian = cv2.threshold(laplacian, 7, 255, cv2.THRESH_BINARY)

    return laplacian

if __name__ == '__main__':
    image = cv2.imread('test_image/test1.png', 1)
    image = implement_filter(image, 5)

    plt.imshow(image, cmap='gray')
    plt.show()