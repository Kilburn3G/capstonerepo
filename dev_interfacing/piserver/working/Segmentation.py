"""
Authors: Aydan, Alex

"""

import time
import numpy as np
import pdb
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.signal import butter, lfilter
#from Multithreading import divideAndProcess
import multiprocessing

IN_FILE = r'test_samples/samples_josh1.csv'
#!# Not implemented unless script is run as a stand alone script.

#Constants (need import)
WINDOW_SIZE=51;

DIVIDER = 0.000125
SAMPLING_FREQ = 475

#Used to decide if E is low enough
E_THRESH = 0.0007;

#Used to decide if A is high enough
A_THRESH = -0.00005


def loadSamples():
    """
    Using file io, open IN_FILE and return as a numpy array
    """
    data = np.genfromtxt(IN_FILE, dtype=float, delimiter=',') 

    print('%d samples loaded' %len(data))
    return data


def preprocessData(V, divider = None):
    """
    Used to filter and remove baseline wander for V. If ADC Values are still in their byteform, 
    convert to voltage using DIVIDER.
    
    Return: Filtered signal
    """

    if divider is not None:
        V = V*divider
    
    
    #Pass through filter
    b, a = butter(16,.1)
    y = lfilter(b, a, V)
    
    return y
    
def initplots():
    '''Used in testing indv script'''
    global fig, ax
    fig, ax = plt.subplots()


def getPeaks(V,E,A, a_thr = A_THRESH, e_thr = E_THRESH):
    """Get the peaks using the error curve E, and opening coefficents A
    
    a_thr : A_Threshhold to use for comparisons

    e_thr : E_Threshhold to use for comparisons

    Return: List of center indicies for peaks found in V
    """


    peaks = []

    for center in range(2,len(E-2)):
        C = E[center]
        C1 = E[center-1]
        C2 = E[center-2]
        
        if C2 > C1 and C1 < C and A[center] < a_thr and C < e_thr:

            peaks += [center]

    print('Peaks found : %d' %len(peaks))
    return peaks

def processSamples(V, wind_sz= WINDOW_SIZE):
    """
    Process the np.array V using the linear regression method.
    
    wind_sz : Window size to use

    Return : E, A as np.arrays for the error and opening coefficents
    """
    print('Processing %d samples' %len(V))
    E = np.array([0.0]*(len(V)));
    A = np.array([0.0]*(len(V)));

    window_center = int((wind_sz-1)/2)

    x = np.linspace(window_center-wind_sz+1,window_center,wind_sz)
    x = np.power(x,2)

    for window_start in range(1,len(V)-wind_sz):  
            
        window_end = window_start+wind_sz-1
        window_center = int(window_start + (wind_sz-1) /2)
        V_window = V[window_start:window_end+1]; # adjusting the window for the next iteration

        # calculation of a 
        a1 = wind_sz * np.sum(x*V_window) - np.sum(x) * np.sum(V_window);
        a2 = wind_sz * np.sum(np.power(x,2)) -  np.power(np.sum(x),2) 
        a = (a1 / a2) ;
            
        v1 = np.sum(np.power(x,2)) * np.sum(V_window) - np.sum(x*V_window) * np.sum(x)
        v2 = wind_sz * np.sum(np.power(x,2)) - np.power(np.sum(x),2) ;
        v = v1 / v2;

        V_prime = (a * x) + v;

        E_vector = (1.0 / wind_sz) * np.sum(np.power((V_window- V_prime),2))

        E[window_center] = float(E_vector);
        A[window_center] = float(a);    

    return E, A




def processSamplesThread1():
    print("Starting Thread 1")
    E,A = processSamples(sharedSampels1)
    print('Thread1 : Processed %d samples' %len(sharedSample1))
    return


def processSamplesThread2():
    print("Starting Thread 2")
    E,A = processSamples(sharedSampels2)
    print('Thread2 : Processed %d samples' %len(sharedSample2))
    return
    


def plotSegments(V, peaks , fig, ax):
    """
    Plots segments overtop of eachother. Needs initialized fig and ax

    V : np.array of our signal

    peaks : list of locations for peaks
    """
    
    if len(peaks) > 0:
        avg_samples = np.sum(np.diff(peaks))/len(np.diff(peaks))
        print('Average Samples between peaks : %d' %avg_samples)

        pdb.set_trace()
        for i in range(0,len(peaks)): 
            if peaks[i] - int(avg_samples/2) > 0 and peaks[i]+int(avg_samples/2) < len(V):
                ax.plot(V[peaks[i]-int(avg_samples/2):peaks[i]+int(avg_samples/2)])
            elif peaks[i] - int(avg_samples/2) < 0:
                ax.plot(V[peaks[i]-int(avg_samples/2):peaks[i]+int(avg_samples/2)])
            elif peaks[i]+avg_samples > len(V):
                pdb.set_trace()
                ax.plot(V[peaks[i]-int(avg_samples/2):len(V)])
        plt.show()
        
    else:
        print('Could not plot, no peaks found')





V=loadSamples()

V = preprocessData(V,divider=DIVIDER)
E , A = processSamples(V)
peaks = getPeaks(V,E,A)

initplots()
plotSegments(V,peaks,fig,ax)
plt.show()
