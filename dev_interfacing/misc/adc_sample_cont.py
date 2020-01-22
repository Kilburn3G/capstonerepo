# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Wilke Alex
import time
import pdb
import bluetooth
import csv

# Import the ADS1x15 module.
import Adafruit_ADS1x15


GAIN = 1
DATA_RATE = 860 #samples per second
MAX_SAMPLETIME = 3 # Max sample time in seconds
list_samples = []

adc = Adafruit_ADS1x15.ADS1115()

print('Reading ADS1115 values')
print('Sampling for %s seconds.' %MAX_SAMPLETIME)
print('Sampling at %s samples per second.' %DATA_RATE)

# Main loop.
start = time.time()
time.sleep(1)


adc.start_adc(0, gain=GAIN,data_rate=DATA_RATE)

print('Sampling')

while (time.time() - start) <= MAX_SAMPLETIME:

    value = adc.get_last_result()
    list_samples.append(value)




print('SAMPLING COMPLETE')
print('WRITING SAMPLES to CSV')
with open('samples.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(list_samples)
print('Written outsamples.csv')



print('Program finished')