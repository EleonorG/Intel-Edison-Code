# Import openCV libraries
import cv2

# Connect to video camera
cap = cv2.VideoCapture(0)

# Grab a frame from the camera
ret, frame = cap.read()

# Write that frame out to a file
cv2.imwrite('blah.png',frame)

# And don't forget to release the camera!
cap.release()
