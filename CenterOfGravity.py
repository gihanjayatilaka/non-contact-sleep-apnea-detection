import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt
from scipy import signal

def mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

cap = cv2.VideoCapture('test.mp4')
cv2.namedWindow('Edges')
cv2.setMouseCallback('Edges', mouse)


arr_size = 1000

arr = np.zeros(arr_size)
cog_x_arr = np.zeros(arr_size)
cog_y_arr = np.zeros(arr_size)
v_x_arr = np.zeros(arr_size)
v_y_arr = np.zeros(arr_size)
print(arr)

#plt.ion()

print('a')
count = 0

breathTime=np.zeros(25)
b=1
state=0


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
        #cv2.imshow('Original', frame)
        edged_frame = cv2.Canny(frame, 100, 200)
        cv2.rectangle(edged_frame, (x1, y1), (x2, y2), (255,0,0), 2)
        cv2.imshow('Edges', edged_frame)


        win = edged_frame[x1:x2, y1:y2]
        h, w = win.shape

        cog_x = np.sum(win*np.arange(w))/np.sum(win)
        cog_y = np.sum(win*np.arange(h).reshape(h, 1))/np.sum(win)

        '''
        arr [1:arr_size] = arr[:arr_size-1]
        arr[0] = edged_frame[x, y]*1 + 0*arr[1]
        '''

        cog_x_arr[1:arr_size] = cog_x_arr[:arr_size - 1]
        cog_x_arr[0] = cog_x
        cog_y_arr[1:arr_size] = cog_y_arr[:arr_size - 1]
        cog_y_arr[0] = cog_y

        v_x_arr[1:arr_size] = v_x_arr[:arr_size - 1]
        v_x_arr[0] = cog_x_arr[1] - cog_x_arr[0]
        v_y_arr[1:arr_size] = v_y_arr[:arr_size - 1]
        v_y_arr[0] = cog_y_arr[1] - cog_y_arr[0]


        '''
        if(arr[1]<100 and arr[0]>100):
            state+=1

            if(state==2):
                breathTime[b]=count-breathTime[b-1]
                state=0
                b+=1
        '''

        #arr[0] = edged_frame[x, y]


        #print(np.sum(edged_frame[x-5: x+5, y-5:y+5]))

        #print(arr[0])
        if (count == arr_size):
            plt.subplot(2, 1, 1)
            plt.plot(v_x_arr)

            plt.subplot(2, 1, 2)
            plt.plot(v_y_arr)

            plt.show()

        count += 1
        print(count,b,arr[0],arr[1])

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()

