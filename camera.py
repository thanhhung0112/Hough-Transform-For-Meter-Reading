# Import essential libraries
import requests
import cv2
import numpy as np
import random as rd

# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = "http://192.168.1.5:8080/shot.jpg"

def get_frame(url, loop):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    cv2.imwrite(f'test_image/test{loop}.png', img)
    return img
