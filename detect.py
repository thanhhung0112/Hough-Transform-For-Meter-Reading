#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2 as cv
import numpy as np

def determine_avg_circles(circles, b):
    avg_x=0
    avg_y=0
    avg_r=0
    for i in range(b):
        #optional - average for multiple circles (can happen when a gauge is at a slight angle)
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    avg_x = int(avg_x/(b))
    avg_y = int(avg_y/(b))
    avg_r = int(avg_r/(b))
    return avg_x, avg_y, avg_r

def compute_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calibrate_gauge(path):
    clock = cv.imread(path)
    height, width = clock.shape[:2]

    gray = cv.cvtColor(clock, cv.COLOR_BGR2GRAY)
    img = cv.medianBlur(gray, 11)
    kernel_sharpening = np.array([[-1,-1,-1], 
                              [-1, 9,-1],
                              [-1,-1,-1]])
    img = cv.filter2D(img, -1, kernel_sharpening)
    
    try:
        circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT, 1, 20, param1=100, param2=35, minRadius=int(height*0.25), maxRadius=int(height*0.5))
    except:
        return
    
    circles = np.uint16(np.around(circles))
    a, b, c = circles.shape
    x, y, r = determine_avg_circles(circles, b)

    # draw center and circle
    cv.circle(clock, (x, y), r, (0, 0, 255), 3, cv.LINE_AA)  # draw circle
    cv.circle(clock, (x, y), 2, (0, 255, 0), 3, cv.LINE_AA)  # draw center of circle


    separation = 10.0 #in degrees
    interval = int(360 / separation)
    p1 = np.zeros((interval,2))  #set empty arrays
    p2 = np.zeros((interval,2))
    p_text = np.zeros((interval,2))
    for i in range(0,interval):
        for j in range(0,2):
            if (j%2==0):
                p1[i][j] = x + 0.9 * r * np.cos(separation * i * 3.14 / 180) #point for lines
            else:
                p1[i][j] = y + 0.9 * r * np.sin(separation * i * 3.14 / 180)
    text_offset_x = 10
    text_offset_y = 5
    for i in range(0, interval):
        for j in range(0, 2):
            if (j % 2 == 0):
                p2[i][j] = x + r * np.cos(separation * i * 3.14 / 180)
                p_text[i][j] = x - text_offset_x + 1.1 * r * np.cos((separation) * (i+9) * 3.14 / 180) #point for text labels, i+9 rotates the labels by 90 degrees
            else:
                p2[i][j] = y + r * np.sin(separation * i * 3.14 / 180)
                p_text[i][j] = y + text_offset_y + 1.1* r * np.sin((separation) * (i+9) * 3.14 / 180)  # point for text labels, i+9 rotates the labels by 90 degrees

    #add the lines and labels to the image
    for i in range(0,interval):
        cv.line(clock, (int(p1[i][0]), int(p1[i][1])), (int(p2[i][0]), int(p2[i][1])),(0, 255, 0), 2)
        cv.putText(clock, '%s' %(int(i*separation)), (int(p_text[i][0]), int(p_text[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.3,(0,0,0),1,cv.LINE_AA)
    
    cv.imwrite('detected_circle.png', clock)

    
    # cv.imshow('detected circles', clock)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return x, y, r

def get_current_value(path, min_angle, max_angle, min_value, max_value, x, y, r):
    img = cv.imread(path)
#     height, width = img.shape[:2]
#     height, width = int(np.around(height*1.5)), int(np.around(width*1.5))

#     img = cv.resize(img, (height, width))
    gray2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    thresh = 100
    maxValue = 255
    
    _, dst2 = cv.threshold(gray2, thresh, maxValue, cv.THRESH_BINARY_INV)
    
    try:
        lines = cv.HoughLinesP(image=dst2, rho=3, theta=np.pi / 180, threshold=100, minLineLength=10, maxLineGap=0)
    except:
        return
    
    final_line_list = []

    diff1LowerBound = 0.0 # diff1LowerBound and diff1UpperBound determine how close the line should be from the center
    diff1UpperBound = 0.2
    diff2LowerBound = 0.5 # diff2LowerBound and diff2UpperBound determine how close the other point of the line should be to the outside of the gauge
    diff2UpperBound = 1.0
    
    for i in range(lines.shape[0]):
        for x1, y1, x2, y2 in lines[i]:
            diff1 = compute_distance(x, y, x1, y1)
            diff2 = compute_distance(x, y, x2, y2)
            
            if diff1 > diff2:
                diff1, diff2 = diff2, diff1
                
            if (((diff1<diff1UpperBound*r) and (diff1>diff1LowerBound*r) and (diff2<diff2UpperBound*r)) and (diff2>diff2LowerBound*r)):
                line_length = compute_distance(x1, y1, x2, y2)
                # add to final list
                final_line_list.append([x1, y1, x2, y2])
                
    res = []
    for x1, y1, x2, y2 in final_line_list:
        dist_pt_0 = compute_distance(x, y, x1, y1)
        dist_pt_1 = compute_distance(x, y, x2, y2)
        
        if (dist_pt_0 > dist_pt_1):
            x_angle = x1 - x
            y_angle = y - y1
        else:
            x_angle = x2 - x
            y_angle = y - y2
        
        degree = np.arctan(np.divide(float(y_angle), float(x_angle)))
        degree = np.rad2deg(degree)
        final_angle = 0
        if x_angle > 0 and y_angle > 0:  #in quadrant I
            final_angle = float(270 - degree)
        if x_angle < 0 and y_angle > 0:  #in quadrant II
            final_angle = float(90 - degree)
        if x_angle < 0 and y_angle < 0:  #in quadrant III
            final_angle = float(90 - degree)
        if x_angle > 0 and y_angle < 0:  #in quadrant IV
            final_angle = float(270 - degree)
        
        value = ((max_angle-final_angle)/(max_angle-min_angle)) * min_value + ((final_angle-min_angle)/(max_angle-min_angle)) * max_value
        
        res.append(value)

    for x1, y1, x2, y2 in final_line_list:
        cv.line(img, (x1, y1), (x2, y2),(0, 255, 0), 2)
    
    # cv.imwrite('detected_line.png', img)
    
    return np.array(res).mean(), img

if __name__ == '__main__':
    x, y, r = calibrate_gauge('static/test3.png')


