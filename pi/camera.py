'''
    Simple socket server using threads
'''
 
import socket
import sys
import time
import picamera
import serial

ser = serial.Serial('/dev/ttyAMA0', 9600)
print ser.readline()
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    #take photo
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        # Get timestamp to make unique name for photo
        timeStamp = str(time.time())
        # Remove decimal from timestamp
        timeStampArray = timeStamp.split('.')
        timeStamp = timeStampArray[0]
        imgLocation = 'images/img' + timeStamp + '.jpg'
        camera.capture(imgLocation)
    
s.close()
