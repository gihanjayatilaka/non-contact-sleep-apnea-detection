#author: harshana.w@eng.pdn.ac.lk

import servo_rotate2

def gihanstuff():
    pass

state = 1
while True:
    print("hello")
    if state:
        rotateServo() # after rotating has ended it will jump to gihans stuff
        state = 0
    else:
        gihanstuff() #gihans stuff should end if they want to rotate the camera
        state = 1
