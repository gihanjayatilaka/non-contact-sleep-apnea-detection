'''
python MultipleSignalFusion.py 3.mp4 0 100 5 5


'''
import numpy as np
import argparse
import cv2
import sys
from time import sleep

if __name__== "__main__":
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
                edgeVideo=np.zeros((END_FRAME-START_FRAME+1,frame.shape[0],frame.shape[1]))
                cogVideo=np.zeros((END_FRAME-START_FRAME+1,ROWS,COLS,2),dtype=np.int32)

                print("Initialized")


            grey_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
            #cv2.imshow('Original', frame)
            edgedFrame = cv2.Canny(frame, 200, 10)
            #print(edged_frame.shape)


            HEIGHT=grey_vid.shape[0]
            WIDTH=grey_vid.shape[1]



            for r in range(ROWS):
                for c in range(COLS):
                    x1=int(WIDTH/COLS)*c
                    x2 = (int(WIDTH / COLS)) * (c+1)
                    y1=int(HEIGHT/ROWS) * r
                    y2 = (int(HEIGHT/ ROWS)) * (r+1)

                    #print(np.shape(edgedFrame[y1:y2,x1:x2]))

                    sigma_my=np.dot(np.sum(edgedFrame[y1:y2,x1:x2],axis=1),np.arange(y1,y2))
                    sigma_mx=np.dot(np.sum(edgedFrame[y1:y2,x1:x2],axis=0).transpose(),np.arange(x1,x2))
                    sigma_m=np.sum(np.sum(edgedFrame[y1:y2,x1:x2]))

                    if sigma_m>0:
                        cog_y=int(sigma_my/sigma_m)
                        cog_x=int(sigma_mx/sigma_m)
                        cv2.circle(edgedFrame, (cog_y, cog_x), 1, (60, 60, 60), 1)
                        cv2.circle(edgedFrame, (cog_y, cog_x), 3, (60, 60, 60), 1)

                    else:
                        if t==0:
                            cog_y=int((y1+y2)/2)
                            cog_x = int((x1 + x2) / 2)

                        else:
                            cog_y=cogVideo[t-1,r,c,0]
                            cog_x = cogVideo[t - 1,r,c, 1]
                            cv2.circle(edgedFrame, (cog_y, cog_x), 3, (60, 60, 60), 1)

                    cogVideo[t,r,c, 0]=cog_y
                    cogVideo[t,r,c ,1] =cog_x

                    cv2.rectangle(edgedFrame,(x1, y1), (x2, y2), (255,0,0), 2)

            print(cogVideo[t,:,:,:])



            edgeVideo[t]=edgedFrame

            cv2.imshow('Edges', edgeVideo[t, :, :])
            cv2.waitKey(1000)

            statusMsg='\t '+str(t+1)+' frames of '+str(END_FRAME-START_FRAME+1)+' ompleted'
            print(statusMsg)



    '''for t in range(1,edgeVideo.shape[0]-1):
        for y in range(1,edgeVideo.shape[1]-1):
            for x in range(1, edgeVideo.shape[2] - 1):
                if edgeVideo[t,y,x]==1:
                    edgeVideo[t,y,x]=sum(sum(edgeVideo[t,y-1:y+1,x-1:x+1]))
                if edgeVideo[t, y, x] >0:
                    edgeVideo[t, y, x]=1
        print('t=',t)'''

    for x in range(edgeVideo.shape[0]):
        cv2.imshow('Edges', edgeVideo[x,:,:])
        cv2.waitKey(1000)


