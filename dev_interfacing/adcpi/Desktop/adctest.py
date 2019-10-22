import spidev
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT) # CS Pin



spi = spidev.SpiDev() # create spi object
spi.open(0, 1) # open spi port 0, device (CS) 1
spi.mode = 1

resp = spi.xfer2([0xAA]) # transfer one byte
time.sleep(0.5) # sleep for 0.1 seconds

print('Finished')
spi.close() 
