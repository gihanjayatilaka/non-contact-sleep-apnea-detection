import numpy as np
import matplotlib.pyplot as plt

def d(a,b):
    dd=np.power(a[0]-b[0],2)+np.power(a[1]-b[1],2)
    return np.sqrt(dd)

def gaussKer(a,b,param):
    return np.exp(-1*param*d(a,b))

def pca(data):
    mean = np.mean(data, 0)
    ddd = data - mean
    [e_val, e_vec] = LA.eig(np.dot(ddd.T, ddd))
    return e_val[1], e_vec[1, :]


def sgn(x):
    if x<0:
        return -1
    elif x>0:
        return 1
    return 0

#<<<<<<<<<<<<<< End of functions


SOM=np.zeros((20,2),np.float64)


cenX=int(input('Center X'))
cenY=int(input('Center Y'))
radX=int(input('Radius X'))
radY=int(input('Radius Y'))

for x in range(20):
    SOM[x, 0] = cenX + np.sin(2 * np.pi * x / 20) * radX
    SOM[x, 1] = cenY + np.cos(2 * np.pi * x / 20) * radY


while(True):
    cog_x,cog_y=map(int,input("newX newY").split(" "))


    param = 1

    for i in range(20):
        SOM[i, 0] = SOM[i, 0] + (cog_x - SOM[i, 0]) * gaussKer(SOM[i, :], [cog_x, cog_y], param)
        SOM[i, 1] = SOM[i, 1] + (cog_y - SOM[i, 1]) * gaussKer(SOM[i, :], [cog_x, cog_y], param)
    plt.close()
    plt.scatter(cog_x, cog_y, color='red')
    plt.scatter(SOM[:, 0], SOM[:, 1], color='blue')
    plt.draw()
    plt.show(block=False)