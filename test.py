# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
#from google.cloud import storage 


# initialize the video stream and allow the camera sensor to warm up
print("starting video stream...")
#vs = VideoStream(src=0).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)




#------------------

from time import sleep
import datetime
#from firebase import firebase

#import urllib2, urllib, httplib
import json
import os 
from functools import partial


'''
firebase = firebase.FirebaseApplication('https://ptsd-9c288.firebaseio.com/', None)

#client = storage.Client()
#bucket = client.get_bucket('gs://ptsd-9c288.appspot.com')
#packageImg = bucket.blob("/")
'''


#----------------

# I am going to set up the buzzer next few lines of code
import time # this is to add a time delay
import RPi.GPIO as GPIO

pin = 11 # Raspberry Pi Pin 17-GPIO 17 this is just for testing 

def setup():
    global pin
    GPIO.setmode(GPIO.BOARD) # Set GPIO Pin As Numbering
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin ,GPIO.HIGH)
    GPIO.setwarnings(False) 

def on():
    GPIO.output(pin, GPIO.LOW)

def off():
    GPIO.output(pin, GPIO.HIGH)
    

def beep(x):
    on()
    time.sleep(x)
    off()
    time.sleep(x)

def destroy():
    global pin
    GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup() # Release resource

count=1

setup()
# loop over the frames from the video stream
try:
    while True:
            # grab the frame from the threaded video stream and resize it to  have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)
                    # loop over the detected barcodes 
            for barcode in barcodes:
                cv2.imwrite("frame%d.jpg" % count, frame)# this saves an image into local path
                    
                    # extract the bounding box location of the barcode and draw
                    # the bounding box surrounding the barcode on the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # if the barcode text is currently not in our CSV file, write
                # the timestamp + barcode to disk and update the set
                
                csv.write("{},{}\n".format(datetime.datetime.now(),barcodeData))
                csv.flush()
		    
                            

                            #print(barcodeData)
                            #-----fire base
                            
                            #data = {"CodeString": barcodeData,"Date Recieved":datetime.datetime.now(),"UpdateMode":"off","status":"recieved"}
                            #firebase.post('/QRcodescanned', data)
                            
                beep(.2)# this beeps when we read a code
                print("ping")

                            
             #this is just to put the window where we want it for testing                        
            windowName="Robot Cam"
            cv2.namedWindow(windowName)#name the window
           # cv2.moveWindow(windowName,1200,10)#move and create the window
            cv2.imshow(windowName, frame)#display our window
            key = cv2.waitKey(1) & 0xFF # I added this to quit gracefully from keyboard
            #print(key)
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                    break
# close the output CSV file do a bit of cleanup
    print("cleaning up...")
    cv2.destroyAllWindows()
    vs.stop()#this kills the camera
except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
    destroy()
