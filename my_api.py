from flask import Flask, render_template
from flask_ngrok import run_with_ngrok
from flask_cors import CORS, cross_origin
from flask import request
import cv2 as cv
import os
from random import random
import camera
import detect
import get_time

# Initialize back end server
app = Flask(__name__)

# Apply flask cors
# CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = 'static'
run_with_ngrok(app)

# The Specifications of clock
min_angle = 17
max_angle = 340
min_value = 0
max_value = 150
loop = 0
url = "http://192.168.43.151:8080/shot.jpg" # using ip webcam app in ch play to get the ip of camera

@app.route('/', methods=['POST', 'GET'])
@cross_origin(origin='*')
def detect_temperature():
    """
    The function is called when the user clicks the "Detect" button on the web page. 
    
    The function will detect the temperature of the object in the image and save the result to a text
    file. 
    
    The function will also save the detected image to the server. 
    
    The function will return the detected image and the result to the web page. 
    
    The function will also return the message to the web page. 
    
    The function will also return the alarm message to the web page if the temperature is higher than 70
    degrees. 
    
    The function will also return the loop value to the web page. 
    
    The loop value is used to save the detected images at 5 corners. 
    
    The loop value is also used to save the result to the text file. 
    
    The loop value is also used to return the message to the web page. 
    
    The loop value is also used to return the alarm message
    :return: the result of the render_template function.
    """
    global loop
    if request.method == "POST":
        try:
            loop += 1 # update the loop value to save different detected images (particularly 5 images at 5 corner)

            if loop > 5:
                loop = 1

            # using while loop to get the res value which is the real number
            # ignore the cases which only detected the lines or the circle
            while True:              
                # any detected image on the web is saved at this path
                path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], f'góc_thứ_{loop}.png')
                path_result_file = os.path.join(app.config['UPLOAD_FOLDER'], 'result.txt')
                
                if os.path.isfile(f'./test_image/góc_thứ_{loop}.png') == True:
                    os.system(f'rm ./test_image/góc_thứ_{loop}.png')
                image = camera.get_frame(url, loop)

                x, y, r, circle = detect.detect_circle(image)

                res, img = detect.detect_line(image, circle, min_angle, max_angle, min_value, max_value, x, y, r)

                # check the error cases
                if not(isinstance(res, type(None))):
                    break

            if os.path.isfile(path_to_save) == True:
                os.system(f'rm {path_to_save}')
            cv.imwrite(path_to_save, img)
            time_current = get_time.get_current_time()

            if os.path.isfile(path_result_file) == False:
                with open(path_result_file, 'w') as f:
                    if loop == 1:
                        f.write(f'\ngóc_thứ_{loop} - Nhiệt độ: {res} - Time: {time_current}\n')
                    elif loop == 5:
                        f.write(f'góc_thứ_{loop} - Nhiệt độ: {res} - Time: {time_current}\n\n')
                    else:
                        f.write(f'góc_thứ_{loop} - Nhiệt độ: {res} - Time: {time_current}\n')
            else:
                with open(path_result_file, 'a') as f:
                    if loop == 1:
                        f.write(f'\ngóc_thứ_{loop} - Nhiệt độ: {res} - Time: {time_current}\n')
                    elif loop == 5:
                        f.write(f'góc_thứ_{loop} - Nhiệt độ: {res} - Time: {time_current}\n\n')
                    else:
                        f.write(f'góc_thứ_{loop} - Nhiệt độ: {res} - Time: {time_current}\n')

            if res < 70:
                return render_template('index.html', user_image=f'góc_thứ_{loop}.png', rand=str(random()), msg=f'Góc thứ {loop}: Success', res=res)
            elif res > 70:
                return render_template('index.html', user_image=f'góc_thứ_{loop}.png', rand=str(random()), msg=f'Góc thứ {loop}: Success', alarm=res)

        except:
            print("something's wrong, fix bug")
            return render_template('index.html', msg=f'Góc thứ {loop}: Unsuccess', loop=loop)

    else:
        return render_template('index.html', loop=loop)

# Start backend
if __name__ == '__main__':
    app.run()
