# Import necessary libraries
import cv2
import urllib

# Grab the image
urllib.urlretrieve("http://stephaniemoyerman.com/wp-content/uploads/2015/06/DSC_0713_linkedin.jpg", "Steph.jpg")

# And grab the config file for facial recognition
urllib.urlretrieve("https://raw.githubusercontent.com/Itseez/opencv/master/data/haarcascades/haarcascade_frontalface_alt.xml","haarcascade_frontalface_alt.xml")

# Use openCV to load the image
img = cv2.imread("Steph.jpg")

# And convert to gray-scale for processing
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Create the classifier and run the algorithm
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

# For each face found in the image, draw a box around it
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

# Write the image back out to a file
cv2.imwrite("BK_facefound.png",img)
