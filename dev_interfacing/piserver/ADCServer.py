import bluetooth
import csv

PORT = 3
list_samples= []
outfile = 'samples.csv'

def startServer():
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    server_socket.bind(("",PORT))
    server_socket.listen(PORT)

    print("Waiting for connections")
    client_socket,address = server_socket.accept()
    print "Accepted connection from ",address

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

    print('Written %s' %soutfile)

 
def closeServerSockets():
    print('Closing server sockets.')
    client_socket.close()
    server_socket.close()


def main():
    startServer()
    readContinuousData()
    writeCSV()
    closeServerSockets()


main()
print('Program finished')