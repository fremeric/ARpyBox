# send data to Godot for augmented image
# input : cam image of the scene with aruco marker, cam_mint, cam_distcoef
# output : data send to UDP server to be used in Godot (or other game engine)
#           data sent = cam image + inv_rot matrix + inv_trans vector

import socket
import cv2
import numpy as np
import json
import cv2.aruco as aruco

# Load of the Mint matrix (internal camera matrix)
cam_mint = np.load('cam_mint.npy')
# Load of distortion camera parameters (from camera calibration)
cam_distcoef = np.load('cam_distcoef.npy')

# Load the dictionary that was used to generate the marker
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
# Initialize the detector parameters
param =  aruco.DetectorParameters()
# Define an object aruco
obj_aruco = aruco.ArucoDetector(dictionary, param)

# Defining 3D corners coordinates of Aruco Marker in the 3D scene
# marker size (length of the aruco black square in meters)
marker_size = 0.096
a = marker_size/2
pts_3D = np.array([[-a,a,0], [a,a,0], [a,-a,0], [-a,-a,0]])

# initialization of socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = "127.0.0.1"
port_im = 4242
port_mtx = 4240

cap = cv2.VideoCapture('video.avi')
while True:
    ret, image = cap.read()
    if not ret:
        print("Error: failed to capture image")
        break
    # Detect Marker and ID
    m_Corn, m_Id, reject = obj_aruco.detectMarkers(image)
    
    # operate if only one marker is detected (4 corners)
    if (len(np.ravel(m_Corn)) == 8) and (len(m_Id) > 0):
        # Arrangement of marker corners 2D points for PnP operation
        pts_2D = np.array(m_Corn)
        pts_2D = np.squeeze(pts_2D, axis=1)   
        # Computation of pose estimation using solvePnP
        retval, rvec, tvec = cv2.solvePnP(pts_3D, pts_2D, cam_mint, cam_distcoef)
        
        # computation of rotation matrix from rotation vector
        rot_mat, _ = cv2.Rodrigues(rvec)
        # computation of inverse_rotation matrix
        inv_rot = rot_mat.T
        # computation of inverse translation vector
        inv_trans = np.dot(-inv_rot, tvec)
        
        r1 = np.ravel(inv_rot, order='F')
        t1 = np.ravel(inv_trans)

        tmat_cod = {"r1x":r1[0], "r1y":r1[1], "r1z":r1[2],\
                    "r2x":r1[3], "r2y":r1[4], "r2z":r1[5],\
                    "r3x":r1[6], "r3y":r1[7], "r3z":r1[8], \
                    "tx":t1[0], "ty":t1[1], "tz":t1[2]}

        encod_tmat = json.dumps(tmat_cod)
        _, encoded_image = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY,70])

        client_socket.sendto(encoded_image, (server_ip, port_im))
        client_socket.sendto(encod_tmat.encode(), (server_ip, port_mtx))
        
        cv2.waitKey(10)
        

