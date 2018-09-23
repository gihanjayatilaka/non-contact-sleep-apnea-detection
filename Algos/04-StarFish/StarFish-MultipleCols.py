'''
python Starfish.py 3.mp4 0 100 10


'''
import numpy as np
import argparse
import cv2
import sys
from time import sleep
import matplotlib
import matplotlib.pyplot as plt

def mouse_callback(event, x, y, flags, params):
    global bellyCenters
    global bellyCenterIndex
    if event==1:
        bellyCenters[bellyCenterIndex, 0] = x
        bellyCenters[bellyCenterIndex, 1] = y

        #print("(x,y)=",(bellyCenters[bellyCenterIndex, 0],bellyCenters[bellyCenterIndex, 1]))
        print(bellyCenters)
        bellyCenterIndex+=1

if __name__== "__main__":
    np.random.seed(0)
    FILENAME = (sys.argv[1])

    START_FRAME=int(sys.argv[2])
    END_FRAME=int(sys.argv[3])

    COLS=int(sys.argv[4])
    bellyCenters = np.zeros((COLS,2),dtype=np.int32)
    bellyCenterIndex=0
    cap = cv2.VideoCapture(FILENAME)


    for x in range(0,START_FRAME-1):
        ret,frame=cap.read()


    for t in range(END_FRAME-START_FRAME):
        ret,frame=cap.read()
        if ret:
            if t==0:
                cv2.imshow("OriginalVideo",frame)
                cv2.setMouseCallback('OriginalVideo', mouse_callback)
                while True:
                    if bellyCenterIndex >= COLS:
                        break
                    else:
                        print(bellyCenterIndex)
                        cv2.waitKey(1)

                for bellyCenterIndex in range(COLS):
                    cv2.circle(frame,(100,100),5, (0, 0, 0), 5)


                cv2.imshow("OriginalVideo",frame)
                #cv2.waitKey(0)
                cv2.destroyWindow("OriginalVideo")

                #edgeVideo=np.zeros((END_FRAME-START_FRAME+1,frame.shape[0],frame.shape[1]))
                #cogVideo=np.zeros((END_FRAME-START_FRAME+1,2),dtype=np.int32)

                timeSeries=np.zeros((END_FRAME-START_FRAME,COLS))
                ret=False
                while not ret:
                    ret, frame = cap.read()


            for col in range(COLS):
                i=0
                while True:
                    WINDOW_HEIGHT=5
                    THRESHOLD=50
                    currentMean = np.zeros((3), dtype=np.float32)
                    nextMean = np.zeros((3), dtype=np.float32)

                    for x in range(WINDOW_HEIGHT):
                        currentMean[:]+=frame[bellyCenters[col,1]-(i+x),bellyCenters[col,0],:]
                        nextMean[:] += frame[bellyCenters[col,1] - (i + x+1), bellyCenters[col,0], :]

                    if np.sum(np.abs(nextMean-currentMean)) < THRESHOLD:
                        i+=1
                    else:
                        break

                    if bellyCenters[col,1] - (i + 4+1) ==0:
                        break

                cv2.circle(frame, (bellyCenters[col,0], bellyCenters[col,1]), 2, (0, 0, 0), 2)

                for ii in range(i):
                    cv2.circle(frame, (bellyCenters[col,0], bellyCenters[col,1]-ii), 1, (256, 0, 0), 1)

                timeSeries[t,col]=i


            cv2.imshow("OriginalVideo", frame)
            cv2.waitKey(1)

    #After processing the video
    print(timeSeries)
    plt.figure()
    plt.plot(np.arange(0,timeSeries.shape[0]),timeSeries)
    plt.show()
    cv2.waitKey(1000)



