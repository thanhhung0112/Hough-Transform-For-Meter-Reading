import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import copy
import serial
import time
import os
import cluster
import detect

url = '?'
cap = cv.VideoCapture(url)

arduino = serial.Serial('COM3', 9600)
i = 0

while True:
    arduino_data = arduino.readline()
    arduino_data = list(arduino_data.decode())
    
    flag = arduino_data[?]
    
    if flag:
        _, img = cap.read()
        cv.imwrite(f'position_{i}.png', img)
        x, y, r = detect.calibrate_gauge(f'position_{i}.png')
        min_angle = float(input('Min angle (lowest possible angle of dial) - in degrees: ')) # the lowest possible angle
        max_angle = float(input('Max angle (highest possible angle) - in degrees: ')) # highest possible angle
        min_value = float(input('Min value: ')) # usually zero
        max_value = float(input('Max value: ')) # maximum reading of the gauge
        units = input('Enter units: ') # degree of oil
        value = detect.get_current_value(f'position_{i}.png', min_angle, max_angle, min_value, max_value, x, y, r)
        value = cluster.determine_cluster(value)

        if (i == 0) and os.path.isfile('result.txt') == True:
            with open('result.txt', 'w') as f:
                f.write(value)
        else:
            with open('result.txt', 'a') as f:
                f.write(value)
        i += 1

    if i == 4: 
        break
        
cap.release()
cv.destroyAllWindows()

