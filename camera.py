# Import essential libraries
import requests
import cv2
import numpy as np
import random as rd

# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = "http://192.168.1.5:8080/shot.jpg"

def get_frame(url, loop):
    """
    It takes a URL and a loop number, then downloads the image at that URL, converts it to a NumPy
    array, and writes it to a file
    
    :param url: The URL of the IP camera
    :param loop: the number of times the function will run
    """
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    cv2.imwrite(f'test_image/góc_thứ_{loop}.png', img)
    return img

if __name__ == '__main__':
    img = get_frame(url, 1)
    print(img.shape)

