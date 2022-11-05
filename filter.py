import cv2
import numpy as np

def implement_filter(image, n):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[0, 1, 0],
                       [1, -4, 1],
                       [0, 1, 0]])

    image = cv2.GaussianBlur(image, (n, n), 0)
    laplacian = cv2.filter2D(image, -1, kernel)
    _, laplacian = cv2.threshold(laplacian, 7, 255, cv2.THRESH_BINARY)

    return laplacian

# if __name__ == '__main__':
#     image = cv2.imread('test_image/test3.png')
#     image = implement_filter(image)
#
#     cv2.imshow('image', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()