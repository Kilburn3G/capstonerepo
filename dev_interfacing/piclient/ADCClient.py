# Author: Wilke Alex
import time
import pdb
import bluetooth
import csv

# Import the ADS1x15 module.
import Adafruit_ADS1x15

#Server Parameters
SERVER_ADDR = "B8:27:EB:F6:78:C3"
PORT = 3

#ADC Parameters
GAIN = 1
DATA_RATE = 250 #samples per second
MAX_SAMPLETIME = 5 # Max sample time in seconds


outfilecsv = 'samples.csv'
list_samples = []
adc = Adafruit_ADS1x15.ADS1115()

def startClient():
    print("Client started. Attempting to connect to server.")

    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((SERVER_ADDR, PORT))
    print("Connection established on port %s" %PORT)


def startSampling():
    print('Sampling for %s seconds.' %MAX_SAMPLETIME)

    adc.start_adc(0, gain=GAIN,data_rate=DATA_RATE)

    while (time.time() - start) <= MAX_SAMPLETIME:

        value = adc.get_last_result()
        print("Sending message %s" %value)
        sock.send( "%s" %value )
        list_samples.append(value)

    adc.stop_adc()

def closeServer():
    print('Closing socket')
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    print('Socket closed')

print('Sampling complete')

def writeToCSV():
    
    print('Writing samples to CSV')
    with open(outfilecsv, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(list_samples)
    print('Written %s' %outfilecsv)

def main():
    
    print('Starting Program')
    print('Reading ADS1115 values')
    print('Sampling for %s seconds.' %MAX_SAMPLETIME)
    print('Sampling at %s samples per second.' %DATA_RATE)
    time.sleep(1)

    startClient()
    startSampling()
    writeToCSV()
    closeServer()

main()

print('Program finished')