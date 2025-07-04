import cv2             # basically used for image manipulation or changing like greyscale or anything
import cvzone          # its used for image and video processing kinda
import numpy as np     # basically we use here to change the binary values and to give out whether a car can go or not
import pickle          # basically save a obeject to a file and it will save and reload to made any adjustments

width, height = 107, 48   # the measurements for rectangle for the basic car parking

cap = cv2.VideoCapture('carPark.mp4')  # change the image to the video

def parkingspace(imgPro):     # we basically use the defining the function and use the for loop to give the rect,

    spaceCounter = 0


    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y+height, x:x+width]
        #cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y+height-3), scale=1.0, thickness=2, offset=0)

        if count < 1000:            # we use this for to find whether its red or green so that can car park
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    cvzone.putTextRect(img, f'Free space:{spaceCounter}/{len(posList)}', (100, 50), scale=3.0, thickness=5, offset=20, colorR=(0, 0, 0))
                                 # we use the for how much number spaces there and how much its free





with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

while True:    # we use this to create the small images to binary then we get to final product
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)   # this is for changing to color black and white
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3),1)  # used for changing for the gaussian blur effect which result gives better a value
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5) # the fornt two lines used for to reduce the black and white noise in the image
    kernel = np.ones((3, 3), np.uint8)     # used in numpy where the function changes the binary to 8bit values
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    parkingspace(imgDilate)    # expands the shape in binary





    cv2.imshow("Image", img)  # give the final solution
    # cv2.imshow("ImageBlur", imgBlur)  # gives the black and white
    # cv2.imshow("imgThreshold", imgThreshold)
    # cv2.imshow("imgMedian", imgMedian)   # above 2 lines gives the small car output and gauss image
    cv2.waitKey(10)  # time complexity of the output can change speed or slow
