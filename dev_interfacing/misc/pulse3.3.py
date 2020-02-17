import spidev
import time
import sys
import RPi.GPIO as GPIO
 


#GPIO pin decloration
GPIO_DRIVER  = 13


def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False);

    #Set pin direction
    GPIO.setup(GPIO_DRIVER,GPIO.OUT)

def pulse(ton,toff):
    print('Pulse')
    GPIO.output(GPIO_DRIVER,GPIO.HIGH)
    time.sleep(ton)
    
    GPIO.output(GPIO_DRIVER,GPIO.LOW)
    time.sleep(toff)


init()
while(True):
    pulse(1,2)
