import cv2
import numpy as np
import matplotlib.pyplot as plt

def filter_laplacian(image, n):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel_lap = np.array([[0, 1, 0],
                           [1, -4, 1],
                           [0, 1, 0]])

    image = cv2.GaussianBlur(image, (n, n), 0)
    laplacian = cv2.filter2D(image, -1, kernel_lap)
    _, laplacian = cv2.threshold(laplacian, 7, 255, cv2.THRESH_BINARY)
    cv2.imwrite('result_image/filter_image.png', laplacian)

    return laplacian

def filter_clahe(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    image = clahe.apply(image)
    cv2.imwrite('result_image/filter_image2.png', image)

    return image

if __name__ == '__main__':
    image = cv2.imread('test_image/test4.png', 1)
    image = filter_clahe(image)
    image = filter_laplacian(image, 5)
