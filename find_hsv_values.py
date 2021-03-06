import cv2
import numpy as np
import configparser

from utils import to_int


config = configparser.ConfigParser()
configFilePath = "/home/shantanu/stuff/projects/virtual-paint/config.ini"
config.read(configFilePath)

# Read frame width and frame height from config file
frameWidth = to_int(config['video']['frameWidth'])
frameHeight = to_int(config['video']['frameWidth'])
brightness = to_int(config['video']['brightness'])

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, brightness)

 
def caller(x):
    pass


cv2.namedWindow("HSV Tracker")
cv2.resizeWindow("HSV Tracker", to_int(config['tracker']['width']), to_int(config['tracker']['height'])) # Resize TrackBars window having size 640 x 240

# Create trackbars
cv2.createTrackbar("Hue Min", "HSV Tracker", 0, 179, caller)
cv2.createTrackbar("Hue Max", "HSV Tracker", 179, 179, caller)
cv2.createTrackbar("Sat Min", "HSV Tracker", 0, 255, caller)
cv2.createTrackbar("Sat Max", "HSV Tracker", 255, 255, caller)
cv2.createTrackbar("Value Min", "HSV Tracker", 0, 255, caller)
cv2.createTrackbar("Value Max", "HSV Tracker", 255, 255, caller)


# Now to get continous value, put it into loop
while True:
    ret, img = cap.read()
    # As in HSV, it is easier to represent a color than in BGR color-space
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Now read trackbars value so it can be applied to image using getTrackbarPos system
    h_min = cv2.getTrackbarPos("Hue Min", "HSV Tracker")
    h_max = cv2.getTrackbarPos("Hue Max", "HSV Tracker")
    s_min = cv2.getTrackbarPos("Sat Min", "HSV Tracker")
    s_max = cv2.getTrackbarPos("Sat Max", "HSV Tracker")
    v_min = cv2.getTrackbarPos("Value Min", "HSV Tracker")
    v_max = cv2.getTrackbarPos("Value Max", "HSV Tracker")

    # Now use these values to filter out image
    lower_limit = np.array([h_min, s_min, v_min])
    upper_limit = np.array([h_max,s_max,v_max])
    # Then to filter out
    mask = cv2.inRange(imgHSV, lower_limit, upper_limit)
    # Till now we have achieved black and white image mask
    # To get a colored one
    imgResult = cv2.bitwise_and(img, img, mask=mask) # And this operation, which will add two images, when both pixel present it will take as 1
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img,mask,imgResult])
    cv2.imshow('Horizontal Stacking', hStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
