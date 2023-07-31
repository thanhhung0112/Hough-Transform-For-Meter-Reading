## Introduction
This repository aims to determine the value of analog gauge using some traditional algorithms via OpenCV-Python.

---
## Getting started
You can use any analog gauge on the internet and run experiments with this source code, provided that the gauge must be captured directly without any distortion or oblique capturing angle.
Running the following command line to clone and install some necessary library
```bash
git clone https://github.com/thanhhung0112/Hough-Transform-For-Meter-Reading.git
cd Hough-Transform-For-Meter-Reading
pip install -r requirements.txt
```

There are 2 ways to run this repo:
* Executing directly main file:
  + You have to modify the target image which you want to read meter, just change directly inside `detect.py`
```bash
python detect.py
```
* Executing api endpoint via `Flask`
  + This will show the link of website to access, website interface is designed via `HTML`, you can absolutely modify it if you want
  + You have to modify `camera.py` to get an image following the way you want. In this source code, i connect to camera ip and get the frame of it when clicking to the button on the website. 
```bash
python my_api.py
```
