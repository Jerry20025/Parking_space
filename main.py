import cv2
import pickle
import cvzone
import numpy as np

width,height=(157-50),(240-192)
#video feed

cap=cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)


def checkParkingSpace(imgPros):
    spaceCounter = 0
    for pos in posList:
        x,y =pos

        imgCrop=imgPros[y:y+height,x:x+width]
        # cv2.imshow(str(x*y),imgCrop)
        count=cv2.countNonZero(imgCrop)
        #to write the count
        cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1,thickness=2,offset=0,
                           colorR=(0,0,255))
        if(count<900):
            color=(0,255,0);
            thickness=4
            spaceCounter +=1
        else:
            color=(0,0,255)
            thickness=2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),color,thickness)
#just to display the count of space available on image
    cvzone.putTextRect(img, f'Free:{spaceCounter}/{len(posList)}', (100,50), scale=3, thickness=5, offset=10,
                       colorR=(0,255,0))

while True:
    #loop the video,i.e when video reach to final frame count it will reset the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    #to check the region of car whether it is present on not in box we need to convert it
    #in pixels, so we will convert it to grey image

    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(3,3),1) #ksize=kernal size

    #after the blur we will convert into binary image and we will use adaptive threshold

    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    #remove unnessecery dots or blur , use image median
    imgMedian=cv2.medianBlur(imgThreshold,5)

    kernel=np.ones((3,3), np.uint8)

    imgDilate=cv2.dilate(imgMedian,kernel,iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image",img)
    # cv2.imshow("ImageGray",imgGray)
    # cv2.imshow("ImageBlur",imgBlur)
    # cv2.imshow("ImageThres",imgThreshold)
    # cv2.imshow("ImageMedian",imgMedian)
    cv2.waitKey(10) #1 will make the video fast, so  we used 10 to make video slow