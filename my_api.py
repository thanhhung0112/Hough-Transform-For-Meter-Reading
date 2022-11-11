from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask import request
import cv2 as cv
import os
from random import random
# import core
# import serial
# import time 
import camera
import detect

# Initialize back end server
app = Flask(__name__)

# Apply flask cors
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = 'static'

# The Specifications of clock
min_angle = 40
max_angle = 310
min_value = -10
max_value = 50
loop = 8
url = "http://192.168.0.191:8080/shot.jpg"

@app.route('/', methods=['POST', 'GET'])
@cross_origin(origin='*')
def detect_temperature():
    global loop
    if request.method == "POST":
        try:
            # image = request.files['file']
            image = camera.get_frame(url, loop)

            if not(isinstance(image, type(None))):
            # if 1:
                # Lưu file
                # path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], f'test{loop}.png')

                print("Save = ", path_to_save)
                # image.save(path_to_save)

                x, y, r, circle = detect.calibrate_gauge(image)

                res, img = detect.get_current_value(image, circle, min_angle, max_angle, min_value, max_value, x, y, r)

                cv.imwrite(path_to_save, img)
                # loop += 1

                # return render_template('index.html', user_image=image.filename, rand=str(random()), msg='Success', res=res)
                return render_template('index.html', user_image=f'test{loop}.png', rand=str(random()), msg='Success', res=res)
            else:
                # Nếu không có file thì yêu cầu tải file
                return render_template('index.html', msg='Không nhận diện được nhiệt độ', loop=loop)
        except:
            print("something's wrong, fix bug")
            return render_template('index.html', msg='Không kết nối được với camera', loop=loop)

    else:
        return render_template('index.html', loop=loop)

# Start backend
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
