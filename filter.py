import cv2
import numpy as np
import matplotlib.pyplot as plt

def implement_filter(image, n):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # kernel_sharpen = np.array([[-1, -1, -1],
    #                            [-1, 9, -1],
    #                            [-1, -1, -1]])
    kernel_lap = np.array([[0, 1, 0],
                           [1, -4, 1],
                           [0, 1, 0]])

    image = cv2.GaussianBlur(image, (n, n), 0)
    # image = cv2.filter2D(image, -1, kernel_sharpen)
    laplacian = cv2.filter2D(image, -1, kernel_lap)
    _, laplacian = cv2.threshold(laplacian, 7, 255, cv2.THRESH_BINARY)

    return laplacian

if __name__ == '__main__':
    image = cv2.imread('test_image/test3.png', 1)
    image = implement_filter(image, 5)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.show()