import os
import glob
import time
import RPi.GPIO as GPIO
from bluetooth import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT)
GPIO.setwarnings(False)

print "Starting"
server_socket = BluetoothSocket(RFCOMM)


print "Port stuff"
server_socket.bind(("", PORT_ANY))
print "Bound and listening"
server_socket.listen(1)

port = server_socket.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service(server_socket, 
        "I am nifty", 
        service_id = uuid,
        service_classes = [ uuid, SERIAL_PORT_CLASS ],
        profiles = [ SERIAL_PORT_PROFILE ], 
        #protocols = [ OBEX_UUID ] 
        )


try:
    print "Waiting for connection on FRCOMM channel %d" % port
    client_socket, client_info = server_socket.accept()
    print "Accepted connection from: ", client_info
    while True:
        data = client_socket.recv(1024)
        print "Received: %s" % data
        if(int(data) == 0):
            GPIO.output(3, 0)
        if(int(data) == 1):
            GPIO.output(3, 1)
finally:
    print("Cleaning up")
    GPIO.cleanup()
    client_socket.close()
    server_socket.close()

