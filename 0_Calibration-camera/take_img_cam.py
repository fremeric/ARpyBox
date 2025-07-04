# Code for capturing and recording images
# images recorded in the file "img_checker"
# to be put in the same file as this .py code
# images indexed and named as : 'im_23.jpg'
# touch i = capture one image
# touch q = quit

import cv2
index = 0
path = 'img_checker/im'

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    
    key = cv2.waitKey(1)
    if key == ord('i'):
        # Write the image in a JPG file
        #cv2.imwrite('images/im_i.jpg', frame)
        cv2.imwrite('{}_{}.{}'.format(path, str(index), 'jpg'),frame)
        index += 1
            
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
