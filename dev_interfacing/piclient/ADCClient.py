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
MAX_SAMPLETIME = 30 # Max sample time in seconds
STOP_SIG = "0"


outfilecsv = 'samples.csv'
list_samples = []
adc = Adafruit_ADS1x15.ADS1115()

def startClient():
    SLEEP_FAILED = 5;

    ''' Start the client, and try to connect to the server listening on the specified port'''

    global sock
    print("Client started. Attempting to connect to server.")

    try:
        sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        sock.connect((SERVER_ADDR, PORT))
        print("Connection established on port %s" %PORT)
        return False

    except:
        print("Connection Failed, no server. Attempting to reconnect in %d seconds..." %SLEEP_FAILED)
        time.sleep(SLEEP_FAILED)
        return True


def startSampling():
    DIVIDER = 0.000125

    print('Sampling for %s seconds.' %MAX_SAMPLETIME)
    start = time.time()
    adc.start_adc(0, gain=GAIN,data_rate=DATA_RATE)


    #Don't send first 3 seconds of samples
    while (time.time() - start < 3):
        value = adc.get_last_result()
       
    while (time.time() - start) <= MAX_SAMPLETIME:
        
        value = adc.get_last_result()
        value = value*DIVIDER        
    
        tosend = '{0:.5f}'.format(value) 
        print("Sending message %s" %tosend)
        sock.send( "%s" %tosend )
        list_samples.append(tosend)
    
    adc.stop_adc()
    sock.send(STOP_SIG)

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

    while startClient():
        pass
   
    startSampling()
    #writeToCSV()
    time.sleep(5)
    closeServer()

main()

print('Program finished')
