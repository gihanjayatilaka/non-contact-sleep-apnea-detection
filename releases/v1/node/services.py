#author: harshana.w@eng.pdn.ac.lk
import RPi.GPIO as GPIO
import subprocess,time


def my_callback():
    subprocess.call(['python', 'main.py'], shell=False)

switch_pin = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=my_callback, bouncetime=300)

while True:
    time.sleep(0.1)
