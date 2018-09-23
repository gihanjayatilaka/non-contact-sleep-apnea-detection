import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt
from scipy import signal
import numpy.linalg as LA

cap = cv2.VideoCapture('1.avi')


def d(a, b):
    dd = np.power(a[0] - b[0], 2) + np.power(a[1] - b[1], 2)
    return np.sqrt(dd)


def gaussKer(a, b, param):
    return np.exp(-1 * param * d(a, b))


def pca(data):
    mean = np.mean(data, 0)
    ddd = data - mean
    [e_val, e_vec] = LA.eig(np.dot(ddd.T, ddd))
    return e_val[1], e_vec[1, :]


def sgn(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0


arr_size = 1000

arr = np.zeros(arr_size)
cog_x_arr = np.zeros(arr_size)
cog_y_arr = np.zeros(arr_size)
v_x_arr = np.zeros(arr_size)
v_y_arr = np.zeros(arr_size)
print(arr)

# plt.ion()

print('a')
count = 0

breathTime = np.zeros(25)
b = 1
state = 0

# y, x = 457, 220
# k = 5
# x1, y1, x2, y2 = x - k, y - k, x + k, y + k
'''Put points here'''
y1, x1 = 151, 211
y2, x2 = 192, 277

for x in range(200):
    cap.read()

corners = [5000, -5000, 5000, -5000]  # [xMin,xMax,yMin,yMax]
SOM = np.zeros((20, 2))

fig = plt.figure()

for x in range(200):
    cap.read()

while (1):

    ret, frame = cap.read()
    if ret == True:

        gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
        # cv2.imshow('Original', frame)
        edged_frame = cv2.Canny(frame, 100, 200)
        cv2.rectangle(edged_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # cv2.imshow('Edges', edged_frame)

        win = edged_frame[x1:x2, y1:y2]
        h, w = win.shape

        cog_x = np.sum(win * np.arange(w)) / max(1, np.sum(win))
        cog_y = np.sum(win * np.arange(h).reshape(h, 1)) / max(1, np.sum(win))

        cog_x_arr[1:arr_size] = cog_x_arr[:arr_size - 1]
        cog_x_arr[0] = cog_x
        cog_y_arr[1:arr_size] = cog_y_arr[:arr_size - 1]
        cog_y_arr[0] = cog_y

        v_x_arr[1:arr_size] = v_x_arr[:arr_size - 1]
        v_x_arr[0] = cog_x_arr[1] - cog_x_arr[0]
        v_y_arr[1:arr_size] = v_y_arr[:arr_size - 1]
        v_y_arr[0] = cog_y_arr[1] - cog_y_arr[0]

        count += 1
        print(count)


        if (count < 100):
            corners[0] = np.minimum(corners[0], cog_x)
            corners[1] = np.maximum(corners[1], cog_x)
            corners[2] = np.minimum(corners[2], cog_y)
            corners[3] = np.maximum(corners[3], cog_y)
        elif count == 100:
            cenX = (corners[0] + corners[1]) / 2
            cenY = (corners[2] + corners[3]) / 2
            radX = cenX - corners[0]
            radY = cenY - corners[2]

            for x in range(20):
                SOM[x, 0] = cenX + np.sin(2 * np.pi * x / 20) * radX
                SOM[x, 1] = cenY + np.cos(2 * np.pi * x / 20) * radY


        else:
            param = 2

            for i in range(20):
                SOM[i, 0] = SOM[i, 0] + (cog_x - SOM[i, 0]) * gaussKer(SOM[i, :], [cog_x, cog_y], param)
                SOM[i, 1] = SOM[i, 1] + (cog_y - SOM[i, 1]) * gaussKer(SOM[i, :], [cog_x, cog_y], param)

            #
            '''plt.close()

            plt.scatter(SOM[:, 0], SOM[:, 1], color='black')
            '''
            #
            fig.hold()
            fig.clear()

            fig.scatter(SOM[:, 0], SOM[:, 1], color='black')
            fig.scatter(cog_x, cog_y, color='red')
            fig.show(block=False)

        print("corners=", corners)
        print("cogxc cogy=", cog_x, cog_y)

        '''k = cv2.waitKey(30) & 0xff
        if k == 27:
            break'''
    else:
        break
cap.release()
# cv2.destroyAllWindows()

