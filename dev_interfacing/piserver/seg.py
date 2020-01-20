import numpy as np
import pandas as pd
import pdb
import matplotlib
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

data = pd.read_csv('samples_102.csv',index_col=None)
data = data.apply(pd.to_numeric,errors='coerce')
V = data.iloc[1:1000,1]
V.index = np.arange(1,len(V)+1)
    

def getPeaks(V,E,A):

    E_thresh = 0.01;
    A_thresh = -0.002;

    peaks = []

    for center in range(2,len(E-2)):
        C = E[center]
        C1 = E[center-1]
        C2 = E[center-2]
        
        if C2 > C1 and C1 < C and A[center] < A_thresh:

            peaks += [center]

    print('Peaks found : %d' %len(peaks))
    return peaks


def processSamples(V):
    E = np.array([0.0]*(len(V)));
    A = np.array([0.0]*(len(V)));

    window_size=21;
    window_center = (window_size-1)/2

    x = np.linspace(window_center-window_size+1,window_center,window_size)
    x = np.power(x,2)

    for window_start in range(1,len(V)-window_size):  
            
        window_end = window_start+window_size-1
        window_center = window_start + (window_size-1) /2

        V_window = V.loc[window_start:window_end]; # adjusting the window for the next iteration

        # calculation of a 
        a1 = window_size * np.sum(x*V_window) - np.sum(x) * np.sum(V_window);
        a2 = window_size * np.sum(np.power(x,2)) -  np.power(np.sum(x),2) 
        a = (a1 / a2) ;
            
        v1 = np.sum(np.power(x,2)) * np.sum(V_window) - np.sum(x*V_window) * np.sum(x)
        v2 = window_size * np.sum(np.power(x,2)) - np.power(np.sum(x),2) ;
        v = v1 / v2;

        V_prime = (a * x) + v;

        E_vector = (1.0 / window_size) * np.sum(np.power((V_window- V_prime),2))

        E[window_center] = float(E_vector);
        A[window_center] = float(a);    

    return E, A

def plotSegments(V,peaks):


    avg_samples = np.sum(np.diff(peaks))/len(np.diff(peaks))
    print('Average Samples between peaks : %d' %avg_samples)

    plt.hold(True)
    for i in range(1,len(V),avg_samples):    
        ax.plot(V.loc[i:i+avg_samples])
    plt.show()
        
    plt.hold(False)




E , A = processSamples(V)
peaks = getPeaks(V,E,A)
pdb.set_trace()
plotSegments(V,peaks)