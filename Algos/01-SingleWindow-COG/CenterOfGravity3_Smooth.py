import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt
from scipy import signal
import numpy.linalg as LA
import scipy.ndimage.filters as filt
import datetime
#import serial
from time import sleep


arr_size = 1000


def findPeaks(ar):
	peaks=np.zeros(ar.shape,dtype=np.int)
	for x in range(1,len(ar)-1):
		if(ar[x-1]<ar[x] and ar[x]>=ar[x+1]):
			peaks[x]=1
	return peaks


def findTime(peaks,fs):
	time=np.nonzero(peaks)[0]
	
	for x in range(len(time)-1,1,-1):
		time[x]=(time[x]-time[x-1])*fs
	time[0]=0

	return time


def printToArduino(str):

    '''test = serial.Serial()
    test.baudrate = 115200
    test.timeout = 0
    test.port = "/dev/ttyUSB0"
    test.open()
    sleep(60)
    test.write(str)'''
    return 0




def mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

cap = cv2.VideoCapture('3.mp4')
cv2.namedWindow('Edges')
#cv2.setMouseCallback('Edges', mouse)

def pca(data):
    mean = np.mean(data,0)
    ddd = data - mean
    [e_val,e_vec] = LA.eig(np.dot(ddd.T,ddd))
    return e_val[1],e_vec[1,:]




arr = np.zeros(arr_size)
cog_x_arr = np.zeros(arr_size)
cog_y_arr = np.zeros(arr_size)
v_x_arr = np.zeros(arr_size)
v_y_arr = np.zeros(arr_size)
projected=np.zeros(arr_size)
smoothened=np.zeros(arr_size)



#plt.ion()

count = 0



#y, x = 457, 220
#k = 5
#x1, y1, x2, y2 = x - k, y - k, x + k, y + k
'''Put points here'''
y1, x1 = 246, 275
y2, x2 = 317, 326


while (1):
    ret, frame = cap.read()
    if ret == True:

        gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
        cv2.imshow('Original', frame)
        edged_frame = cv2.Canny(frame, 100, 200)
        cv2.rectangle(edged_frame, (x1, y1), (x2, y2), (255,0,0), 2)
        cv2.imshow('Edges', edged_frame)


        win = edged_frame[x1:x2, y1:y2]
        h, w = win.shape

        cog_x = np.sum(win*np.arange(w))/np.sum(win)
        cog_y = np.sum(win*np.arange(h).reshape(h, 1))/np.sum(win)


        cog_x_arr[1:arr_size] = cog_x_arr[:arr_size - 1]
        cog_x_arr[0] = cog_x
        cog_y_arr[1:arr_size] = cog_y_arr[:arr_size - 1]
        cog_y_arr[0] = cog_y

        v_x_arr[1:arr_size] = v_x_arr[:arr_size - 1]
        v_x_arr[0] = cog_x_arr[1] - cog_x_arr[0]
        v_y_arr[1:arr_size] = v_y_arr[:arr_size - 1]
        v_y_arr[0] = cog_y_arr[1] - cog_y_arr[0]


    
        if (count == arr_size):


            v_arr=np.concatenate((v_x_arr,v_y_arr), axis=0).reshape((arr_size,2))
            '''
            print("x",v_x_arr)
            print("y",v_y_arr)
            print("arr",v_arr)
			'''


            for x in range(10,100):
                pca_eig,pca_vec=pca(v_arr[:x,:])
                projected[x]=pca_vec[0]*v_x_arr[x]+pca_vec[1]*v_y_arr[x]



            for x in range(100,arr_size):
                pca_eig,pca_vec=pca(v_arr[x-100:x,:])
                projected[x]=pca_vec[0]*v_x_arr[x]+pca_vec[1]*v_y_arr[x]

            for x in range(1,arr_size):
                projected[x]=projected[x-1]*0.8 + projected[x]*0.2
            

            smoothened=filt.gaussian_filter1d(projected,150*np.var(projected))


            plt.subplot(4, 1, 1)
            plt.plot(projected)

            plt.subplot(4, 1, 2)
            
            peaks=findPeaks(smoothened)

            for x in range(len(peaks)):
            	if(peaks[x]==1):
            		plt.plot(x,smoothened[x], 'r.')

			
            plt.plot(smoothened)

            plt.subplot(4,1,3)
            fs = 0.03
            f, pow_x = signal.welch(projected, fs, nperseg=1000)
            plt.plot(f[0:100], pow_x[0:100])

            now = datetime.datetime.now()
            reportName=now.strftime("./report/rep%Y-%m-%d %H:%M.pdf")

            plt.subplot(4,1,4)
            plt.text(0,0,("REPORT : "+reportName+" \nTime for a breath: "+str(findTime(peaks,30))))

            #plt.savefig(reportName)
            printToArduino("JSee report "+reportName+". The condition : good #")

            plt.show()




        count += 1
        print("frame :"+str(count))

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break
cap.release()
#cv2.destroyAllWindows()

