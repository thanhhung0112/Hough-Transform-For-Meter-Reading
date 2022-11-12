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
min_angle = 17
max_angle = 340
min_value = 0
max_value = 150
loop = 8
url = "http://192.168.1.8:8080/shot.jpg"

@app.route('/', methods=['POST', 'GET'])
@cross_origin(origin='*')
def detect_temperature():
    global loop
    if request.method == "POST":
        try:
            while True:
                # image = request.files['file']
                image = camera.get_frame(url, loop)

                # path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], f'test{loop}.png')

                print("Save = ", path_to_save)
                # image.save(path_to_save)

                x, y, r, circle = detect.calibrate_gauge(image)

                res, img = detect.get_current_value(image, circle, min_angle, max_angle, min_value, max_value, x, y, r)

                if not(isinstance(res, type(None))):
                    break

            cv.imwrite(path_to_save, img)
            # loop += 1

            # return render_template('index.html', user_image=image.filename, rand=str(random()), msg='Success', res=res)
            return render_template('index.html', user_image=f'test{loop}.png', rand=str(random()), msg='Success', res=res)
        except:
            print("something's wrong, fix bug")
            return render_template('index.html', msg='Không nhận diện được nhiệt độ', loop=loop)

    else:
        return render_template('index.html', loop=loop)

# Start backend
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
