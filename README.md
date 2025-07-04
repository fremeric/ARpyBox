# ARpyBox
open source augmented reality - python - Godot

## Presentation

The project ARpyBox has the following goals:
- propose an open source solution for Augmented Reality (AR)
- provide information on AR issues
- keep the code as simple as possible to make it easier to get started

The code is mainly done under Python and Godot to facilitate the appropriation.
Basic code enables beginners to understand and master AR concepts and tools.
This base can then be used to easily add elaborate functionalities.

## Description of the project

The aim of this project is to provide a starter kit for building augmented reality applications based on easy-to-use open source solutions (Python and Godot).
The project consists of trhee parts:
-   Part 1: AR on a static image
-   Part 2: AR on a video
-   Part 3: AR on live image (your own camera)

The pipeline of AR application consists of the following steps:
-   Camera calibration (the solution provided by OpenCV has been used)
-   Pose estimation (in Python):
    - Detection of marker (use of Aruco package)
    - Estimation of the pose of the camera (use of PnP function in OpenCV)
    - Send data (orientation matrix and translation vector of camera pose in marker reference) to Godot by socket
-   Creation and display of AR image (in Godot)

These 3 main pipelines are described in the PDF file “*ARpybox_pipelines.pdf*”.

# List of features

-   Camera calibration (OpenCV in Python)
-   Marker detection (Aruco library in Python)
-   Camera pose estimation (OpenCV in Python)
-   Data exchange via socket (UDP)
-   AR image (Godot)

## Requirements
-   Python (Python librairies: opencv-python, numpy, socket, json)
-   Godot (https://godotengine.org)

## Steps
For an overview, start with Part1 (AR on static image) and Part2 (AR on video) then go to Part3 (AR on live cam) to be fully autonomous with your own camera in your real environment (and go further).

The main folder contains 5 folders:
-   0_Camera-calibration
-   1_Godot-AR
-   2_Py-image
-   3_Py-video
-   4_Py-livecam

For an easy use, it is recommended to copy and paste them on your computer (with the proposed structure).

### Part 1: AR on a static image
For this Part 1, no need to calibrate the camera as the image is provided (image.jpg) as well as the internal camera parameters (cam_distcoef.npy and cam_mint.npy) used for the image.
-   Step1: 
    - Identify the folder “**1_Godot-AR**”
    - Identify the file “*project.godot*” in the folder “1_Godot-AR”
    - execute Godot project: “*project.godot*” in Godot
-   Step2: 
    - Identify the folder “**2_Py-image**”
    - Identify the file “*send_data-image.py*” in the folder “2_Py-image”
    - Execute Python code: “*send_data-image.py*” in Python
    - After the second step, the AR image will be displayed in Godot.

### Part 2: AR on a video
For this Part2, no need to calibrate the camera as the video is provided (video.avi) as well as the internal camera parameters (cam_distcoef.npy and cam_mint.npy) used for the video.
-   Step1: 
    - Identify the folder “**1_Godot-AR**”
    - Identify the file “*project.godot*” in the folder “1_Godot-AR”
    - Execute Godot project: “*project.godot*” in Godot
-   Step2: 
    - Identify the folder “**3_Py-video**”
    - Identify the file “*send_data-video.py*” in the folder “3_Py-video”
    - Execute Python code: “*send_data-video.py*” in Python
    - After the second step, the AR video will be displayed in Godot.

### Part 3: AR on live image
For this Part 3, you use your own camera for AR. So, you need to calibrate your camera (computation of the internal camera parameters ("*cam_distcoef.npy*" and "*cam_mint.npy*").
-   Step 1 (calibration of the camera):
    - Identify the folder “**0_Camera_calibration**”
    - In this folder, you should have a folder named “**images**” without any images for the moment…
    - Print the document “*OpenCV_checker.pdf*” and measure the size of a square (in meters)
    - Execute Python code “*take_img_cam.py*” in Python. This code will take an image each time you press the touch “i” (and quit the application with the touch “q”). Each image is registered in the folder “**images**”. Take several images of the printed document “*OpenCV_checker.pdf*” for different points of view.
    - Identify the file “*calib_cam.py*”. In the code (line 17), set the size of a square of the checker (in meters). For instance, my checker has squares of 2.4 cm.
    - Execute Python code “*calib_cam.py*” in Python. This code will calculate the internal parameters of the camera using images of the checker. As an output, this function will generate 2 files in the current folder “*cam_mint.npy*” and “*cam_distcoef.npy*”. You need to calibrate the camera just once per camera.
    - Copy the 2 files “*cam_mint.npy*” and “*cam_distcoef.npy*” in the folder “4_Py-livecam”. 
-   Step 2: 
    - Identify the folder “**1_Godot-AR**”
    - Identify the file “*project.godot*” in the folder “1_Godot-AR”
    - Execute Godot project: “*project.godot*” in Godot
-   Step 3: 
    - Identify the folder “**4_Py-livecam**”
    - Print the document “*Aruco_Marker.pdf*” and measure the size of the black square (in meters)
    - Identify the file “*send_data-cam.py*” in the folder “4_Py-livecam”. In the code (line 26), set the size of the marker (in meters). For instance, my marker is 9.6 cm.
    - Execute Python code: “*send_data-cam.py*” in Python
    - After the third step, the AR will be display in Godot according to the image provided by the camera (in streaming). The marker should be entirely viewed by the camera.

## Acknowledgments
This project benefited from some very useful OpenCV documentation. The Aruco library was very useful as well.

https://docs.opencv.org/

The Godot Documentation was useful also for socket exchange.

https://docs.godotengine.org 
