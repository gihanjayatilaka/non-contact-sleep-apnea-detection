'''
python Starfish.py 3.mp4 0 100 5 0.01


'''
import numpy as np
import argparse
import cv2
import sys
from time import sleep
import matplotlib
import matplotlib.pyplot as plt


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

def mouse_callback(event, x, y, flags, params):
    global bellyCenters
    global bellyCenterIndex
    if event==1:
        bellyCenters[bellyCenterIndex, 0] = x
        bellyCenters[bellyCenterIndex, 1] = y

        print("(x,y)=",(bellyCenters[bellyCenterIndex, 0],bellyCenters[bellyCenterIndex, 1]))
        #print(bellyCenters)
        bellyCenterIndex+=1

if __name__== "__main__":
    np.random.seed(0)
    FILENAME = (sys.argv[1])

    START_FRAME=int(sys.argv[2])
    END_FRAME=int(sys.argv[3])

    COLS=int(sys.argv[4])
    LEARNING_RATE=float(sys.argv[5])
    bellyCenters = np.zeros((COLS,2),dtype=np.int32)
    adaptiveAverage=np.zeros((COLS),dtype=np.float32)
    adaptiveVariance = np.zeros((COLS), dtype=np.float32)

    bellyCenterIndex=0
    cap = cv2.VideoCapture(FILENAME)


    DEBUG_Frame01=np.zeros((1))
    DEBUG_FrameLast=np.zeros((1))

    for f in range(0,START_FRAME-1):
        ret,frame=cap.read()


    for t in range(END_FRAME-START_FRAME):
        print("DEBUG: Frame=",t)
        ret,frame=cap.read()
        while not ret:
            ret, frame = cap.read()

        if t==0:
            cv2.imshow("OriginalVideo",frame)
            cv2.setMouseCallback('OriginalVideo', mouse_callback)
            while True:
                if bellyCenterIndex >= COLS:
                    break
                else:
                    #print(bellyCenterIndex)
                    cv2.waitKey(1)

            for bellyCenterIndex in range(COLS):
                cv2.circle(frame,(100,100),5, (0, 0, 0), 5)


            cv2.imshow("OriginalVideo",frame)
            #cv2.waitKey(0)
            cv2.destroyWindow("OriginalVideo")

            #edgeVideo=np.zeros((END_FRAME-START_FRAME+1,frame.shape[0],frame.shape[1]))
            #cogVideo=np.zeros((END_FRAME-START_FRAME+1,2),dtype=np.int32)
            timeSeries=np.zeros((END_FRAME-START_FRAME,COLS),dtype=np.float32)


        if t==1:
            DEBUG_Frame01=np.array(frame,copy=True)

        if t==END_FRAME-START_FRAME-1:
            DEBUG_FrameLast=np.array(frame,copy=True)

        i=np.zeros((COLS),dtype=np.int32)
        for col in range(COLS):

            while True:
                WINDOW_HEIGHT=5
                THRESHOLD=50
                currentMean = np.zeros((3), dtype=np.float32)
                nextMean = np.zeros((3), dtype=np.float32)

                for x in range(WINDOW_HEIGHT):
                    currentMean[:]+=frame[bellyCenters[col,1]-(i[col]+x),bellyCenters[col,0],:]
                    nextMean[:] += frame[bellyCenters[col,1] - (i[col] + x+1), bellyCenters[col,0], :]

                if np.sum(np.abs(nextMean-currentMean)) < THRESHOLD:
                    i[col]+=1
                else:
                    break

                if bellyCenters[col,1] - (i[col] + 4+1) ==0:
                    break







        for col in range(COLS):

            timeSeries[t,col]=i[col]
            if t>0:
                timeSeries[t,col]=timeSeries[t,col]*1.0 + timeSeries[t-1,col]*0.0

                # <<<<<, Draw column graphs
                cv2.circle(frame, (bellyCenters[col, 0], bellyCenters[col, 1]), 2, (0, 0, 0), 2)

                for ii in range(int(timeSeries[t,col])):
                    cv2.circle(frame, (bellyCenters[col, 0], bellyCenters[col, 1] - ii), 1, (256, 0, 0), 1)



            adaptiveVariance[col]=adaptiveVariance[col]*(1.0-LEARNING_RATE)+ np.square(i[col]-adaptiveAverage[col])*LEARNING_RATE
            adaptiveAverage[col]=adaptiveAverage[col]*(1.0-LEARNING_RATE) + i[col]*LEARNING_RATE
            timeSeries[t,col]=(timeSeries[t,col]-adaptiveAverage[col])/np.sqrt(adaptiveVariance[col])





        cv2.imshow("OriginalVideo", frame)
        cv2.waitKey(1)

    cv2.destroyWindow("OriginalVideo")

    #After processing the video

    breathingPattern=np.sum(timeSeries,axis=1)/COLS
    breathingPattern[:250]=np.zeros((250))
    breathingPeak=[]

    for t in range(breathingPattern.shape[0]-4):
        if isRisingZero(breathingPattern[t:t+3]):
            print("DEBUG: Found rising zero")
            for tt in range(t,breathingPattern.shape[0]-2):
                if isFallingZero(breathingPattern[tt:tt+3]):
                    print("DEBUG: Found falling zero")
                    ttt =t+np.argmax(breathingPattern[t:tt])
                    breathingPeak.append(ttt)
                    break

    print(breathingPeak)
    cap.release()

    #<<<<<<<<<<<<<,
            # Replay video with peaks

    cap2 = cv2.VideoCapture(FILENAME)
    for f in range(0,START_FRAME):
        ret,frame=cap2.read()

    cap2.read()

    for t in range(END_FRAME-START_FRAME):
        print("DEBUG: Frame=",t)
        ret,frame=cap2.read()
        while not ret:
            ret, frame = cap2.read()

        if t==1:
            assert (np.sum(np.sum(np.abs(DEBUG_Frame01-frame)))!=0),"Frames missed - Start Check"
        if t==END_FRAME-START_FRAME-1:
            assert (np.sum(np.sum(np.abs(DEBUG_FrameLast-frame)))!=0),"Frames missed - End Check"

        print(breathingPattern[t])
        fast=True
        if t>10 and t<(END_FRAME-START_FRAME-10):
            if breathingPeak.__contains__(t):
                cv2.rectangle(frame, (50, 50), (500, 500), (0, 0, 250), thickness=5)
                fast=False
            else:
                for tt in range(5):
                    if(breathingPeak.__contains__(t+tt)):
                        cv2.rectangle(frame,(50,50),(500,500),(250,0,0),thickness=5)
                        fast=False
                        break
                for tt in range(5):
                    if(breathingPeak.__contains__(t-tt)):
                        cv2.rectangle(frame,(50,50),(500,500),(0,250,0),thickness=5)
                        fast=False
                        break


        cv2.imshow("Video with peaks marked",frame)
        if(fast):
            cv2.waitKey(1)
        else:
            cv2.waitKey(600)
    cv2.destroyWindow("Video with peaks marked")

    #<<<<<<<<<<<<<<<
            #Plot graphs
    plt.figure("Time series of sensors")
    plt.plot(timeSeries[:,:])
    plt.figure("Breathing pattern")
    plt.plot(breathingPattern)


    for t in range(END_FRAME-START_FRAME):
        if t>10 and t<(END_FRAME-START_FRAME-10):
            for tt in range(5):
                if(breathingPeak.__contains__(t+tt)):
                    plt.plot(t, breathingPattern[t], 'b.')
                    #fast=False
                    break
            for tt in range(5):
                if(breathingPeak.__contains__(t-tt)):
                    plt.plot(t, breathingPattern[t], 'g.')
                    #fast=False
                    break

    for t in range(len(breathingPeak)):
        plt.plot(breathingPeak[t],breathingPattern[breathingPeak[t]],'r.')


    plt.show()
    cv2.waitKey(1000)



