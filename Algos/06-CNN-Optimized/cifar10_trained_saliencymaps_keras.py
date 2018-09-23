from __future__ import print_function
import keras
from keras.datasets import cifar10
from keras.models import load_model
import os
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm


import random



'''
LOAD CIFAR10
'''
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# cifar10 category label name
cifar10_labels = np.array([
    'airplane',
    'automobile',
    'bird',
    'cat',
    'deer',
    'dog',
    'frog',
    'horse',
    'ship',
    'truck'])

'''
LOAD MODEL AND PREDICT
'''

# use ResNet
#model = load_model('cifar10_ResNet20v1_model.092.h5')

# use CNN
model = load_model('models/cifar/keras_cifar10_trained_model.h5')

    
def convertCIFER10Data(image):
    img = image.astype('float32')
    img /= 255
    c = np.zeros(32*32*3).reshape((1,32,32,3))
    c[0] = img
    return c



def show_image(image, grayscale=False, ax=None, title=''):
    if ax is None:
        plt.figure()
    plt.axis('off')
    
    if len(image.shape) == 2 or grayscale:
        image = np.sum(np.abs(image), axis=2)
        vmax = np.percentile(image, 99)
        vmin = np.min(image)

        plt.imshow(image, cmap=plt.cm.gray, vmin=vmin, vmax=vmax)
        plt.title(title)
    else:
        image = image*255
        image = image.astype('uint8')
        
        plt.imshow(image)
        plt.title(title)
    
for i in range(100):
    index = random.randint(0, x_test.shape[0])
    image = x_test[index]
    data = convertCIFER10Data(image)

    ret = model.predict(data, batch_size=1) 
    
    bestnum = 0.0
    bestclass = 0
    for n in [0,1,2,3,4,5,6,7,8,9]:
        if bestnum < ret[0][n]:
            bestnum = ret[0][n]
            bestclass = n

    if y_test[index] == bestclass:
        print(cifar10_labels[bestclass])
        
    else:
        print(cifar10_labels[bestclass] + "!=" + cifar10_labels[y_test[index][0]]   )

    

    plt.figure()
    show_image(image,ax=plt.subplot('251')) 

    from CNN_model_Visualization.SaliencyMaps import GradientSaliency
    vanilla = GradientSaliency(model)

    mask = vanilla.get_mask(data.reshape((32,32,3)))               # compute the gradients
    show_image(mask, grayscale=True, ax=plt.subplot('252'), title='vanilla gradient')

    mask = vanilla.get_smoothed_mask(data.reshape((32,32,3)))
    show_image(mask, grayscale=True, ax=plt.subplot('257'), title='smoothed vanilla gradient')
    
    from CNN_model_Visualization.SaliencyMaps import GuidedBackprop
    guided_bprop = GuidedBackprop(model) # A very expensive operation, which hackingly creates 2 new temp models
    
    mask = guided_bprop.get_mask(data.reshape((32,32,3)))
    show_image(mask, grayscale=True, ax=plt.subplot('253'), title='guided backprop')
    
    mask = guided_bprop.get_smoothed_mask(data.reshape((32,32,3)))
    show_image(mask, grayscale=True, ax=plt.subplot('258'), title='smoothed guided backprop')

    from CNN_model_Visualization.SaliencyMaps import IntegratedGradients
    inter_grad = IntegratedGradients(model)

    mask = inter_grad.get_mask(data.reshape((32,32,3)))
    show_image(mask, grayscale=True, ax=plt.subplot('254'), title='integrated grad')

    mask = inter_grad.get_smoothed_mask(data.reshape((32,32,3)))
    show_image(mask, grayscale=True, ax=plt.subplot('259'), title='smoothed integrated grad')

    from CNN_model_Visualization.SaliencyMaps import VisualBackprop
    visual_bprop = VisualBackprop(model)

    #mask = visual_bprop.get_mask(data.reshape((32,32,3)))
    #show_image(mask, grayscale=True, ax=plt.subplot('255'), title='visual backprop')

    #mask = visual_bprop.get_smoothed_mask(data.reshape((32,32,3)))
    #show_image(mask, grayscale=True, ax=plt.subplot(2,5,10), title='smoothed visual backprop')


    
    plt.show()
