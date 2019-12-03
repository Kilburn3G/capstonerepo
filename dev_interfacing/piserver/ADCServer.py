import bluetooth
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

PORT = 3
list_samples= []
outfile = 'samples.csv'


# Plot labels
plt.title('EKG Sampler')
plt.xlabel('Samples')
plt.ylabel('Relative Voltage')



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
x_len = 200         # Number of points to display
y_range = [0, 5]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, x_len))
ys = [0] * x_len
ax.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

def animate(i, ys):
    
    # Add y to list
    ys.append(readByte())

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)

    return line,


def main():
    startServer()

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig,
        animate,
        fargs=(ys,),
        interval=50,
        blit=True)
    plt.show()

    closeServerSockets()




main()
print('Program finished')

