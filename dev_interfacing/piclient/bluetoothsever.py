import bluetooth

server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
 
port = 3
server_socket.bind(("",port))
server_socket.listen(3)
 
client_socket,address = server_socket.accept()
print "Accepted connection from ",address

while data != "0":
    

    data = client_socket.recv(1024)
    print ("Received: %s" % data)
    list_samples.append(data)

with open('recieved.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(list_samples)

print('Written recieved.csv')



print('Program finished')
 
client_socket.close()
server_socket.close()