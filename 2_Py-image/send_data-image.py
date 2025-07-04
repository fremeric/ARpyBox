# send data to UDP server for augmented image
# input : image of the scene with aruco marker, cam_mint, cam_distcoef
# output : data send to UDP server to be used in a game engine
#           data sent = cam image + inv_rot matrix + inv_trans vector

import socket
import cv2
import numpy as np
import json

# ************** function 'detect_marker' ******************
# Function : 'detect_marker' : based on Aruco Library

# Pose estimation based on Aruco marker
# input : image, size of marker (length of the aruco black square in meters)
# output :  - pts_3D of the marker (knowing its size)
#           - pts_2D detected in the image (thanks to Aruco Library) 

def detect_marker(image, marker_size):
    import cv2.aruco as aruco
    
    # Load the dictionary that was used to generate the marker
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    # Initialize the detector parameters
    param =  aruco.DetectorParameters()
    # Define an object aruco
    obj_aruco = aruco.ArucoDetector(dictionary, param)
    
    # Dectect Aruco Marker with their ID in the image for the aruco object
    m_Corn, m_Id, reject = obj_aruco.detectMarkers(image)
    
    # Arrangement of marker corners 2D points for PnP operation
    pts_2D = np.array(m_Corn)
    pts_2D = np.squeeze(pts_2D, axis=1)

    return pts_2D
# **********************************************

# Load of the Mint matrix (internal camera matrix)
cam_mint = np.load('cam_mint.npy')
# Load of distortion camera parameters (from camera calibration)
cam_distcoef = np.load('cam_distcoef.npy')

# load of image
image = cv2.imread('image.jpg')
# marker size (length of the aruco black square in meters)
marker_size = 0.096
# Defining 3D corners coordinates of Aruco Marker in the 3D scene
a = marker_size/2 
pts_3D = np.array([[-a,a,0], [a,a,0], [a,-a,0], [-a,-a,0]])

# Call of the function 'detect_marker' to compute the 4 corners of the marker
# in the marker (pts_3D) and in the image (pts_2D)
pts_2D = detect_marker(image, marker_size)

# Computation of pose estimation using solvePnP
retval, rvec, tvec = cv2.solvePnP(pts_3D, pts_2D, cam_mint, cam_distcoef)

# ***********************************************
# Computation of Position and Orientation of Camera 
#               in the marker (Aruco) reference

# input : (rvec, tvec) vectors
# output : (inv_rot matrix, inv_trans vector)

# given M = [R T] from (rvec, tvec), then : P(cam_ref) = M . P(aruco_ref)
# then : P(aruco_ref) = inv_M . P(cam_ref)
# [inv_M] = [inv_rot, inv_trans]

# computation of rotation matrix from rotation vector
rot_mat, _ = cv2.Rodrigues(rvec)

# computation of inverse_rotation matrix
inv_rot = rot_mat.T
# computation of inverse translation vector
inv_trans = np.dot(-inv_rot, tvec)
# ***********************************************

# initialization of socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = "127.0.0.1"
port_im = 4242
port_mtx = 4240

# shaping of data (pose of the camera) to be sent to UDP server
r1 = np.ravel(inv_rot, order='F')
t1 = np.ravel(inv_trans)

tmat_cod = {"r1x":r1[0], "r1y":r1[1], "r1z":r1[2],\
            "r2x":r1[3], "r2y":r1[4], "r2z":r1[5],\
            "r3x":r1[6], "r3y":r1[7], "r3z":r1[8], \
           "tx":t1[0], "ty":t1[1], "tz":t1[2]}
# encoding of data to JSON format
encod_tmat = json.dumps(tmat_cod)

# encoding of image
_, encoded_image = cv2.imencode(".jpg", image)

# sending of the data (position and orientation of camera)
client_socket.sendto(encod_tmat.encode(), (server_ip, port_mtx))

# sending of image (for AR image)
client_socket.sendto(encoded_image, (server_ip, port_im))
