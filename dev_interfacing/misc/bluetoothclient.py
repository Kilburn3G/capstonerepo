import bluetooth
import random 
bd_addr = "B8:27:EB:F6:78:C3"

port = 3
print("Client started. Attempting to connect.")
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
print("Connection established")

while(True):
    msg = random.random()
    print("Sending message %s" %msg)
    sock.send(" %s" %msg)

sock.close()