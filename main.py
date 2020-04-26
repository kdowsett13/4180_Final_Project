'''
Developer:Jose Sanchez
Date: 04/14/2020
notes: this will be our main code that will execute:
1.sonar distance check for obstacle avoidance
2.will keep track of the path 
3.drive the motor and steer 
4. use open CV for image deteccting along with zbar



'''
# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import cv2
#this is for time and passing arg
import argparse
import time
#this is for threads 
import threading 





path= list()# global list so that we can keep track of the paths we are on





#define a function that will capture video for us 

def imageRec():
    #------------------------------------------------------------------------------------------
    # initialize the video stream and allow the camera sensor to warm up
    print("starting video stream..")
    #vs = VideoStream(src=0).start()# this is for testing with a web cam not in use. We didn't have anymore equipment
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)# 

    #------------------------------------------------------------------------------------------
    #wrapping it in a try loop incase the camera fails
    try:
        print("try")
        while True:
            print("while")
        
            # grab the frame from the threaded video stream and resize it to  have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)#this is strickly for debug the monitoring the actual device would not have a screen
            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)
            # loop over the detected barcodes
            for barcode in barcodes:
                print("hello")
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
                cv2.putText(frame, text, (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                if barcodeData not in path:
                        path.append(barcodeData)
                        print("type: ", type(barcodeData),"this is the actual data: ",barcodeData)


            #this is just to put the window where we want it for testing                        
            windowName="Robot Cam"
            cv2.namedWindow(windowName)#name the window
            #cv2.moveWindow(windowName,1200,10)#move and create the window
            cv2.imshow(windowName, frame)#display our window

    except KeyboardInterrupt:
        print("cleaning up...")
        cv2.destroyAllWindows()
        vs.stop()#this kills the camera

imageRec()
#create threads
#videoThread = threading.Thread(target=imageRec) 


#starting the thread
#videoThread.start()






