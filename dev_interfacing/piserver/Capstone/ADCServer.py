import bluetooth
import csv
import numpy as np
import re
import pdb

from Segmentation import getPeaks, plotSegments, processSamples, processSamples

PORT = 3
list_samples= []
outfile = 'samples.csv'


# Plot labels
plt.title('EKG Sampler')
plt.xlabel('Samples')
plt.ylabel('Relative Voltage')



def parseDataList(data_str):
    pattern = r'(\d\.\d\d\d\d\d)'
    rslt = re.findall(pattern, data_str)
    float_data = list(float(v) for v in rslt)
    return float_data


def startServer():
    global client_socket, server_socket

    
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    server_socket.bind(("",PORT))
    server_socket.listen(PORT)

    print("Waiting for connections")
    client_socket,address = server_socket.accept()

    print "Accepted connection from ",address

def readByte():
    STOP_SIG = "0"

    data = client_socket.recv(1024)
    print ("Received: %s" % data)
    return data

    
def readContinuousData():
    STOP_SIG = "0"
    data= ""
    while data != STOP_SIG:
        
        data = client_socket.recv(1024)
        print ("Received: %s" % data)
        list_samples.append(data)


def writeCSV(list_samples):
    print("Writing CSV as %s "%outfile)
    with open(outfile, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(list_samples)

    print('Written %s' %outfile)

 
def closeServerSockets():
    print('Closing server sockets.')
    client_socket.close()
    server_socket.close()


def main():
    
    global start_pos
    resetStartPos()
    startServer()
    start_pos = 0
    next_start = 0

    samples = gatherSamples()
    processSamples(samples)
    # # Set up plot to call animate() function periodically
    # ani = animation.FuncAnimation(fig,
    #     animate,
    #     fargs=(ys,),
    #     interval=50,
    #     blit=True)
    # plt.show()

    #closeServerSockets()



main()
print('Program finished')

