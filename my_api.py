from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask import request
import cv2 as cv
import os
from random import random
# import core
import detect

# Initialize back end server
app = Flask(__name__)

# Apply flask cors
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = 'static'

# The Specifications of clock
min_angle = 45
max_angle = 310
min_value = -34
max_value = 54

@app.route('/', methods=['POST', 'GET'])
@cross_origin(origin='*')
def detect_temperature():
    if request.method == "POST":
        try:
            image = request.files['file']
            if image:
                # Lưu file
                path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                print("Save = ", path_to_save)
                image.save(path_to_save)

                x, y, r = detect.calibrate_gauge(path_to_save)

                res, img = detect.get_current_value(path_to_save, min_angle, max_angle, min_value, max_value, x, y, r)

                cv.imwrite(path_to_save, img)
                return render_template('index.html', user_image=image.filename, rand=str(random()), msg='Success', res=res)
            else:
                # Nếu không có file thì yêu cầu tải file
                return render_template('index.html', msg='Hãy chọn file để tải lên')
        except:
            print('Image format is wrong')
            return render_template('index.html', msg='Không nhận diện được nhiệt độ')

    else:
        return render_template('index.html')

# Start backend
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
