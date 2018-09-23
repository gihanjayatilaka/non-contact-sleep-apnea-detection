'''
python Starfish.py 3.mp4 0 100


'''
import numpy as np
import argparse
import cv2
import sys
from time import sleep
import matplotlib
import matplotlib.pyplot as plt

def mouse_callback(event, x, y, flags, params):
    global centerBelly_X
    global centerBelly_Y
    if centerBelly_X==0:
        if event==1:
            centerBelly_X=x
            centerBelly_Y=y

            print("(x,y)=",(centerBelly_X,centerBelly_Y))

def isRisingZero(x):
    if x[0]<0 and x[2]>0:
        return True
    else:
        return False

def isFallingZero(x):
    if x[0]>0 and x[2]<0:
        return True
    else:
        return False

def isPeak(x):
    if x[0]<x[1] and x[1]>=x[2]:
        return True
    elif x[0]<=x[1] and x[1]>x[2]:
        return True
    else:
        return False
if __name__== "__main__":
    centerBelly_X = 0
    centerBelly_Y = 0

    np.random.seed(0)
    FILENAME = (sys.argv[1])

    START_FRAME=int(sys.argv[2])
    END_FRAME=int(sys.argv[3])

    ROWS=int(sys.argv[4])
    COLS=int(sys.argv[5])



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
                    if centerBelly_X > 0:
                        break
                    else:
                        cv2.waitKey(1)

                cv2.circle(frame,(centerBelly_X,centerBelly_Y),5,(0,0,0),5)
                cv2.imshow("OriginalVideo",frame)
                cv2.waitKey(1000)
                cv2.destroyWindow("OriginalVideo")


                #edgeVideo=np.zeros((END_FRAME-START_FRAME+1,frame.shape[0],frame.shape[1]))
                #cogVideo=np.zeros((END_FRAME-START_FRAME+1,2),dtype=np.int32)
                timeSeries=np.zeros((END_FRAME-START_FRAME))
                ret=False
                while not ret:
                    ret, frame = cap.read()

            i=0
            while True:
                WINDOW_HEIGHT=5
                THRESHOLD=50
                currentMean = np.zeros((3), dtype=np.float32)
                nextMean = np.zeros((3), dtype=np.float32)

                for x in range(WINDOW_HEIGHT):
                    currentMean[:]+=frame[centerBelly_Y-(i+x),centerBelly_X,:]
                    nextMean[:] += frame[centerBelly_Y - (i + x+1), centerBelly_X, :]

                if np.sum(np.abs(nextMean-currentMean)) < THRESHOLD:
                    i+=1
                else:
                    break

                if centerBelly_Y - (i + 4+1) ==0:
                    break

            cv2.circle(frame, (centerBelly_X, centerBelly_Y), 2, (0, 0, 0), 2)

            for ii in range(i):
                cv2.circle(frame, (centerBelly_X, centerBelly_Y-ii), 1, (256, 0, 0), 1)

            timeSeries[t]=i


            cv2.imshow("OriginalVideo", frame)
            cv2.waitKey(1)

    #After processing the video
    print(timeSeries)
    plt.figure()
    plt.plot(np.arange(0,timeSeries.shape[0]),timeSeries)
    plt.show()
    cv2.waitKey(1000)



