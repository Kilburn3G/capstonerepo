import bluetooth
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import re
import pdb


PORT = 3
list_samples= []
outfile = 'samples.csv'


# Plot labels
plt.title('EKG Sampler')
plt.xlabel('Samples')
plt.ylabel('Relative Voltage')


def plotSegments(V,peaks):


    avg_samples = np.sum(np.diff(peaks))/len(np.diff(peaks))
    print('Average Samples between peaks : %d' %avg_samples)

    plt.hold(True)
    for i in range(1,len(V),avg_samples):    
        ax.plot(V.loc[i:i+avg_samples])
        plt.show()
        
    plt.hold(False)

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



def resetStartPos():
    global start_pos
    start_pos = 0;


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


def writeCSV():
    print("Writing CSV as %s "%outfile)
    with open(outfile, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(list_samples)

    print('Written %s' %outfile)

 
def closeServerSockets():
    print('Closing server sockets.')
    client_socket.close()
    server_socket.close()


############################################
########### PLOTTING #######################
############################################
    
# Parameters
x_len = 500         # Number of points to display
y_range = [0, 0.3]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, x_len))
ys = [0] * x_len
ax.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

def updateList(ys,data):
    global start_pos, next_start
    
    ys_len = len(ys)
    data_len = len(data)
   
    next_start = start_pos+data_len



    if next_start >= ys_len:
        start_pos=0
    else:
        for i in range(data_len):
            ys[start_pos+i] = data[i]
        start_pos=next_start

    return ys
    
def animate(i, ys):
    
    

    # Add y to list
    
    data = readByte()

    ys = updateList(ys,parseDataList(data))
  
    print(ys)
    # # Limit y list to set number of items
    # ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

# def gatherSamples(numSamples):

#     while
#     data = readByte()
#     ys = updateList(ys,parseDataList(data))
  
def main():
    
    global start_pos
    resetStartPos()
    startServer()
    start_pos = 0
    next_start = 0


    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig,
        animate,
        fargs=(ys,),
        interval=50,
        blit=True)
    plt.show()

    #closeServerSockets()



main()
print('Program finished')

