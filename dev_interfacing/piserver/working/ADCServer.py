from Segmentation import processSamples, getPeaks, WINDOW_SIZE, DIVIDER, A_THRESH, E_THRESH
from Plotting import animate, initplots, updateList, plotSegments
from scipy.signal import butter, lfilter

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import pandas as pd
import numpy as np

import bluetooth
import time

import re
import pdb
import csv


list_samples= [] #Not used in implementation unless continuous sampling
PORT = 3 #Bluetooth port to operate on
OUTFILE = r'out/samples_%d.csv' %int(time.time()) #Filename for recorded samples
DEC_RES = 5 #How many decimal places should be accepted for parsing rec data. 


def parseDataList(data_str):
    """
    The recv buffer (data_str) needs to be parsed correctly in order to use the data gathered. 
    parseDataList will take data_str, remove any unnecessary decimals from the string, and parse the string
    into a list of each element being a float. 

    Return: A list, parsed to DEC_RES decimal places. Only the First digit before the decimal point is read. 
    """
    pattern = r'(?=(\d\.\d{1,%d}))' %DEC_RES
    rslt = re.findall(pattern, str(data_str))
    float_data = list(float(v) for v in rslt)
    return float_data


def startServer():
    """
    Start server, and starting listing on the port specified by const PORT
    """
    global client_socket, server_socket
    print("Waiting for connections")

    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    server_socket.bind(("",PORT))
    server_socket.listen(PORT)

    
    client_socket,address = server_socket.accept()

    print ("Accepted connection from " , address)

def readBuffer():
    '''
    Read the bluetooth recv buffer.

    Return: An ugly string in byte form. Needs to be parsed
    '''

    data = client_socket.recv(1024)
    print ("Received: %s" % data)
    return data

    
def readContinuousData():
    '''Continue to read data until a STOP_SIG is sent. Not tested. gbl list_samples is appended to'''

    global list_samples

    STOP_SIG = "0"
    data= ""
    while STOP_SIG in data != True:
        data = client_socket.recv(1024)
        print ("Received: %s" % data)
        list_samples.append(data)


def writeCSV(lst_samples):
    """Write samples to a CSV from list lst_samples. Output specified by OUTFILE"""
    print("Writing CSV as %s " %OUTFILE)
    with open(OUTFILE, 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(lst_samples)

    print('Written %s' %OUTFILE)

 
def closeServerSockets():
    print('Closing server sockets.')
    client_socket.close()
    server_socket.close()


def gatherSamples(numSamples):
    """    
    Gather AT LEAST numSamples samples, return as a list. The len of the list may exceed the numSamples

    Return: parsed list of samples in float form
    """

    
    samples = []
    while len(samples) < numSamples:
        data = readBuffer()
        samples += parseDataList(data)
    
    return samples

def main():
    
    startServer()
    
    samples = gatherSamples(1000)
    writeCSV(samples)

    #Get V, E, and A
    V = np.array(samples,dtype=float) # Required for further processing
    E, A = processSamples(V, WINDOW_SIZE)

    peaks = getPeaks(V,E,A,E_THRESH,A_THRESH)
    fig, ax = initplots()
    plotSegments(V,peaks,fig,ax)
    closeServerSockets()



main()
print('Program finished')

