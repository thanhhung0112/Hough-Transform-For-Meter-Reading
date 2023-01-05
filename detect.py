import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import filter

# The Specifications of clock
# base on the distributed degree with the detected circle to determine min_angle and max_angle
min_angle = 38 
max_angle = 316
min_value = 0
max_value = 100                     

def determine_avg_circles(circles):
    return np.mean(circles, axis=1, dtype=np.int32).reshape((3,))

def compute_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def detect_circle(image):
    height, width = image.shape[:2]

    residual = int((width - height) / 2) if width > height else 0
    image = image[:, residual:width-residual] # crop image to make width and height equal

    height, width = image.shape[:2]
    
    ratio = 400/height
    height, width = int(height*ratio), int(width*ratio)
    image = cv.resize(image, (width, height)) # desired image 400x400

    img = filter.filter_clahe(image) # improve contrast of image
    img = filter.filter_laplacian(img, 9) # detect edge of image to get information easily

    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT, 1, 35, param2=35, minRadius=int(height*0.35), maxRadius=int(height*0.55))
    if isinstance(circles, type(None)):
        return

    circles = np.uint16(np.around(circles))
    x, y, r = determine_avg_circles(circles)

    # draw center and circle
    cv.circle(image, (x, y), r, (0, 0, 255), 3, cv.LINE_AA)  # draw circle
    cv.circle(image, (x, y), 2, (0, 255, 0), 3, cv.LINE_AA)  # draw center of circle

    # this part is only used to visualize the circle and the distributed degree
    separation = 10.0 #in degrees
    interval = int(360 / separation)
    p1 = np.zeros((interval,2))  #set empty arrays
    p2 = np.zeros((interval,2))
    p_text = np.zeros((interval,2))
    for i in range(0,interval):
        for j in range(0,2):
            if (j%2==0):
                p1[i][j] = x + 0.9 * r * np.cos(separation * i * np.pi / 180) #point for lines
            else:
                p1[i][j] = y + 0.9 * r * np.sin(separation * i * np.pi / 180)
    text_offset_x = 10
    text_offset_y = 5
    for i in range(0, interval):
        for j in range(0, 2):
            if (j % 2 == 0):
                p2[i][j] = x + r * np.cos(separation * i * np.pi / 180)
                p_text[i][j] = x - text_offset_x + 1.1 * r * np.cos((separation) * (i+9) * np.pi / 180) #point for text labels, i+9 rotates the labels by 90 degrees
            else:
                p2[i][j] = y + r * np.sin(separation * i * np.pi / 180)
                p_text[i][j] = y + text_offset_y + 1.1 * r * np.sin((separation) * (i+9) * np.pi / 180)  # point for text labels, i+9 rotates the labels by 90 degrees

    # add the lines and labels to the image
    for i in range(0,interval):
        cv.line(image, (int(p1[i][0]), int(p1[i][1])), (int(p2[i][0]), int(p2[i][1])),(0, 255, 0), 2)
        cv.putText(image, '%s' %(int(i*separation)), (int(p_text[i][0]), int(p_text[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.3,(0,0,0),1,cv.LINE_AA)

    return x, y, r, image

def detect_line(image, circle, min_angle, max_angle, min_value, max_value, x, y, r):
    height, width = image.shape[:2]

    residual = int((width - height) / 2) if width > height else 0
    image = image[:, residual:width-residual] # crop image to make width and height equal

    height, width = image.shape[:2]

    ratio = 400/height
    height, width = int(height*ratio), int(width*ratio)
    img = cv.resize(image, (width, height))

    img = filter.filter_clahe(img)
    dst = filter.filter_laplacian(img, 5)

    lines = cv.HoughLinesP(image=dst, rho=2, theta=np.pi / 180, threshold=100, minLineLength=0, maxLineGap=0)
    if isinstance(lines, type(None)):
        return
    
    # this part is used to select the good line 
    final_line_list = []

    diff1LowerBound = 0.0 # diff1LowerBound and diff1UpperBound determine how close the line should be from the center
    diff1UpperBound = 0.3
    diff2LowerBound = 0.55 # diff2LowerBound and diff2UpperBound determine how close the other point of the line should be to the outside of the gauge
    diff2UpperBound = 1.0
    
    for i in range(lines.shape[0]):
        for x1, y1, x2, y2 in lines[i]:
            diff1 = compute_distance(x, y, x1, y1)
            diff2 = compute_distance(x, y, x2, y2)
            
            if diff1 > diff2:
                diff1, diff2 = diff2, diff1
                
            if (((diff1<diff1UpperBound*r) and (diff1>diff1LowerBound*r) and (diff2<diff2UpperBound*r)) and (diff2>diff2LowerBound*r)):
                final_line_list.append([x1, y1, x2, y2])
                
    # this part is used to determine the real degree
    # using bilinear interpolation to approximate the value of the point between 2 point min and max value of the clock
    res = []
    for x1, y1, x2, y2 in final_line_list:
        dist_pt_0 = compute_distance(x, y, x1, y1)
        dist_pt_1 = compute_distance(x, y, x2, y2)
        
        if (dist_pt_0 > dist_pt_1):
            x_angle1 = x1 - x
            x_angle2 = x1 - x2 
            x_angle = sum([x_angle1, x_angle2]) / 2
            y_angle1 = y - y1
            y_angle2 = y2 - y1
            y_angle = sum([y_angle1, y_angle2]) / 2
        else:
            x_angle1 = x2 - x
            x_angle2 = x2 - x1
            x_angle = sum([x_angle1, x_angle2]) / 2
            y_angle1 = y - y2
            y_angle2 = y1 - y2
            y_angle = sum([y_angle1, y_angle2]) / 2

        degree1 = np.arctan(np.divide(float(y_angle1), float(x_angle1)))
        degree2 = np.arctan(np.divide(float(y_angle2), float(x_angle2)))
        degree = sum([degree1, 3*degree2]) / 4
        degree = np.rad2deg(degree)

        if x_angle > 0 and y_angle > 0:  #in quadrant I
            final_angle = float(270 - degree)
        elif x_angle < 0 and y_angle > 0:  #in quadrant II
            final_angle = float(90 - degree)
        elif x_angle < 0 and y_angle < 0:  #in quadrant III
            final_angle = float(90 - degree)
        elif x_angle > 0 and y_angle < 0:  #in quadrant IV
            final_angle = float(270 - degree)
        
        # bilinear interpolation
        value = ((max_angle-final_angle)/(max_angle-min_angle)) * min_value + ((final_angle-min_angle)/(max_angle-min_angle)) * max_value
        
        res.append(value)

    # only using to visualize the lines 
    for x1, y1, x2, y2 in final_line_list:
        cv.line(circle, (x1, y1), (x2, y2),(0, 255, 0), 2)
    
    cv.imwrite('result_image/detected.png', circle)
    
    if len(res) == 0:
        return None, circle
    return np.median(np.array(res)), circle

if __name__ == '__main__':
    image = cv.imread('test_image/test3.png')
    x, y, r, circle = detect_circle(image)
    res, img = detect_line(image, circle, min_angle, max_angle, min_value, max_value, x, y, r)
    print(res)
