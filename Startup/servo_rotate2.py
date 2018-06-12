#from picamera.array import PiRGBArray
#from picamera import PiCamera
import time, struct,io,picamera,picamera.array
import cv2
from PIL import Image
import numpy as np
from darkflow.net.build import TFNet
import pigpio

def rotateServo():
    pi = pigpio.pi()

    #initializing hw pwm pins
    pin_gpio_z = 12
    pin_gpio_x = 13
    pi.hardware_PWM(pin_gpio_z, 0, 0)
    pi.hardware_PWM(pin_gpio_x, 0, 0)
    time.sleep(0.1)


    options = {"model": "darkflow/cfg/tiny-yolo.cfg", "load": "darkflow/bin/tiny-yolo.weights", "threshold": 0.2,"config": "darkflow/cfg/","gpu":1.0}
    print("loading TFnet")
    tfnet = TFNet(options)

    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    rawCapture = picamera.array.PiRGBArray(camera, size=(320, 240))
    time.sleep(1)

    z,x=75000,75000
    #cycle through the stream of images from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array #the frame will be stroed in the varible called image    x=75000
        #  find the amount that is needed to rotate
        # #z,x = blackFollow(image,z,x)

        print("Predicting")
        results = tfnet.return_predict(image)
        dz, dx = 0, 0
        print("Found ", len(results),"objects")
        for result in results:
            #cv2.rectangle(image,
            #      (result["topleft"]["x"], result["topleft"]["y"]),
            #      (result["bottomright"]["x"],result["bottomright"]["y"]),
            #      (0, 255, 0), 4)
            #text_x, text_y = result["topleft"]["x"] - 10, result["topleft"]["y"] - 10
            #cv2.putText(image, result["label"], (text_x, text_y),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            if (result["label"] == "person"):
                dz = result["topleft"]["x"] + result["bottomright"]["x"] - image.shape[1] #how much should we rotate to left/right
                dx = result["topleft"]["y"] + result["bottomright"]["y"] - image.shape[0] #how much should we rotate to up/down
                print(result)

        z -= int(10000*(1.0*dz/image.shape[1]))
        x += int(10000*(1.0*dx/image.shape[0]))
        z = max(z,25000)
        z = min(z,125000)
        x = max(x,25000)
        x = min(x,90000)
        print("dz", dz, "dx", dx, "z", z,"x",x)

        # end rotating logic
        if (dz < 10 and dx < 10):
            break

        pi.hardware_PWM(pin_gpio_z, 50, z) #50Hz
        pi.hardware_PWM(pin_gpio_x, 50, x) #50Hz
        time.sleep(0.1)
        rawCapture.truncate(0)
