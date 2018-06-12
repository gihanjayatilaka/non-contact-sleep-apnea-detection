import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt
from scipy import signal
import numpy.linalg as LA


def mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

cap = cv2.VideoCapture('3.mp4')
cv2.namedWindow('Edges')
cv2.setMouseCallback('Edges', mouse)

def pca(data):
    mean = np.mean(data,0)
    ddd = data - mean
    [e_val,e_vec] = LA.eig(np.dot(ddd.T,ddd))
    return e_val[1],e_vec[1,:]

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


        cog_x_arr[1:arr_size] = cog_x_arr[:arr_size - 1]
        cog_x_arr[0] = cog_x
        cog_y_arr[1:arr_size] = cog_y_arr[:arr_size - 1]
        cog_y_arr[0] = cog_y

        v_x_arr[1:arr_size] = v_x_arr[:arr_size - 1]
        v_x_arr[0] = cog_x_arr[1] - cog_x_arr[0]
        v_y_arr[1:arr_size] = v_y_arr[:arr_size - 1]
        v_y_arr[0] = cog_y_arr[1] - cog_y_arr[0]


    
        if (count == arr_size):


            v_arr=np.concatenate((v_x_arr,v_y_arr), axis=0).reshape((1000,2))

            print("x",v_x_arr)
            print("y",v_y_arr)
            print("arr",v_arr)


            projected=np.zeros((1000))

            for x in range(10,100):
                pca_eig,pca_vec=pca(v_arr[:x,:])
                projected[x]=pca_vec[0]*v_x_arr[x]+pca_vec[1]*v_y_arr[x]



            for x in range(100,arr_size):
                pca_eig,pca_vec=pca(v_arr[x-100:x,:])
                projected[x]=pca_vec[0]*v_x_arr[x]+pca_vec[1]*v_y_arr[x]

            '''
            for x in range(100,arr_size):
                v_x_arr[x]-np.mean(v_x_arr[x-100:x])
                v_y_arr[x]-np.mean(v_y_arr[x-100:x])


            for x in range(1,arr_size):
                v_x_arr[x]=v_x_arr[x-1]*0.8 + v_x_arr[x]*0.2
                v_y_arr[x]=v_y_arr[x-1]*0.8 + v_y_arr[x]*0.2
            '''

            for x in range(1,arr_size):
                projected[x]=projected[x-1]*0.8 + projected[x]*0.2
            

            plt.subplot(3, 1, 1)
            plt.plot(v_x_arr)

            plt.subplot(3, 1, 2)
            plt.plot(projected)

            plt.subplot(3,1,3)
            fs = 30
            f, pow_x = signal.welch(projected, fs, nperseg=1000)
            plt.plot(f, pow_x)


            plt.show()

        count += 1
        print(count)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()

