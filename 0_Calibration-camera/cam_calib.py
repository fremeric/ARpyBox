# Camera calibration using a checker pattern
# From cam images
 
import cv2
import numpy as np 
import glob

# **********************************************************
# Store 3D points for checker images (world coordinate frame)
object_points = []

# Number of interior corners along x-axis
nX = 9
# Number of interior corners along y-axis
nY = 6
# Length of the side of a square in meters in the scene (paper)
square_size = 0.024
# Define 3D coordinates for corners in the checker pattern
object_points_3D = np.zeros((nX * nY, 3), np.float32)
# Object points are (0,0,0), (1,0,0), (2,0,0) ...., (5,8,0)
object_points_3D[:,:2] = np.mgrid[0:nY, 0:nX].T.reshape(-1, 2)
object_points_3D = object_points_3D * square_size

# **********************************************************
# Get the file path for images in the current directory
images = glob.glob('img_checker/*.jpg')
# Corners detection on checker for each image
# Store 2D points for checker images (camera coordinate frame)
image_points = []
for image_file in images:
    # Load the image
    image = cv2.imread(image_file)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Find the corners on the checker
    success, corners = cv2.findChessboardCorners(gray, (nY, nX), None)
    # If the corners are found by the algorithm, store them
    if success == True:
      # Append object points
      object_points.append(object_points_3D)
      # Append image points
      image_points.append(corners)

# ********** Compute camera calibration  *******************************
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points,\
                            image_points, gray.shape[::-1], None, None)
 
# Save mtx internal camera matrix
np.save('cam_mint.npy', mtx)
# Save distorsion coef of internal camera
np.save('cam_distcoef.npy', dist)
