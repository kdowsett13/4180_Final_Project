# coding: utf-8
'''
Developer:Jose Sanchez
Date: 04/14/2020
notes: this will be our main code that will execute:
1.sonar distance check for obstacle avoidance
2.will keep track of the path 
3.drive the motor and steer 
4. use open CV for image deteccting along with zbar



'''
# import the necessary packages for video
from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import cv2
import sys

from time import sleep
import datetime
#from firebase import firebase

#import urllib2, urllib, httplib
import json
import os 
from functools import partial

exit = False

#----------------
#this is for time and passing arg
import argparse
import time
#this is for threads 
import threading
from threading  import Lock,Thread
#------------------------------------------------------------------------------------------motors
import RPi.GPIO as GPIO
import time

#a couple of delay constants time to 
leg = .01# this tells me to keep it on 
turn = 0.33# how long the motors are on

#set up control pins for motor driver
STBY = 31
AIN1 = 33
AIN2 = 35
PWMA = 37
BIN1 = 32
BIN2 = 36
PWMB = 38

GPIO.setmode(GPIO.BOARD)#use board pin numbers

#led
Blue = 16
Green = 22
Red = 40


#-----------------audio 
class Buzzer(object):
 def __init__(self):
  GPIO.setmode(GPIO.BOARD)  
  self.buzzer_pin = 29 #set to GPIO pin 5
  GPIO.setup(self.buzzer_pin, GPIO.IN)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  print("buzzer ready")

 def __del__(self):
  class_name = self.__class__.__name__
  print (class_name, "finished")

 def buzz(self,pitch, duration):   #create the function “buzz” and feed it the pitch and duration)
 
  if(pitch==0):
   time.sleep(duration)
   return
  period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
  delay = period / 2     #calcuate the time for half of the wave  
  cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency

  for i in range(cycles):    #start a loop from 0 to the variable “cycles” calculated above
   GPIO.output(self.buzzer_pin, True)   #set pin 18 to high
   time.sleep(delay)    #wait with pin 18 high
   GPIO.output(self.buzzer_pin, False)    #set pin 18 to low
   time.sleep(delay)    #wait with pin 18 low

 def play(self, tune):
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  x=0

  print("Playing tune ",tune)
  if(tune==1):
    pitches=[262,294,330,349,392,440,494,523, 587, 659,698,784,880,988,1047]
    duration=0.1
    for p in pitches:
      self.buzz(p, duration)  #feed the pitch and duration to the function, “buzz”
      time.sleep(duration *0.5)
    for p in reversed(pitches):
      self.buzz(p, duration)
      time.sleep(duration *0.5)

  elif(tune==2):
    pitches=[262,330,392,523,1047]
    duration=[0.2,0.2,0.2,0.2,0.2,0,5]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the function, “buzz”
      time.sleep(duration[x] *0.5)
      x+=1
  elif(tune==3):
    pitches=[392,294,0,392,294,0,392,0,392,392,392,0,1047,262]
    duration=[0.2,0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.8,0.4]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1

  elif(tune==4):
    pitches=[1047, 988,659]
    duration=[0.1,0.1,0.2]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1

  elif(tune==5):
    pitches=[1047, 988,523]
    duration=[0.1,0.1,0.2]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1

  GPIO.setup(self.buzzer_pin, GPIO.IN)

#--------------------end audio 
GPIO.setup(Blue,GPIO.OUT)
GPIO.output(Blue,1)
GPIO.setup(Green,GPIO.OUT)
GPIO.output(Green,1)
GPIO.setup(Red,GPIO.OUT)
GPIO.output(Red,1)




#set the GPIO's to outputs
GPIO.setup(STBY, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)

#set initial condiions, STBY
#is low, so no motors running
GPIO.output(STBY, GPIO.LOW)
#Defining PWM
GPIO.output(AIN1, GPIO.HIGH)
GPIO.output(AIN2, GPIO.LOW)
GPIO.output(PWMA, GPIO.HIGH)#left
#GPIO.PWM(PWMA, 300)

GPIO.output(BIN1, GPIO.HIGH)
GPIO.output(BIN2, GPIO.LOW)
GPIO.output(PWMB, GPIO.HIGH)#right
#GPIO.PWM(PWMB, 800)

#go into their own library, ultimately.
def go_forward(run_time):
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)

    GPIO.output(STBY, GPIO.HIGH) #start
    time.sleep(run_time)
    GPIO.output(STBY, GPIO.LOW) #stop
    time.sleep(.04)
def turn_left(run_time):
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)

    GPIO.output(STBY, GPIO.HIGH) #start
    time.sleep(run_time)
    GPIO.output(STBY, GPIO.LOW) #stop

def turn_right(run_time):
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)

    GPIO.output(STBY, GPIO.HIGH) #start
    time.sleep(run_time)
    GPIO.output(STBY, GPIO.LOW) #stop

def reverse(run_time):
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)

    GPIO.output(STBY, GPIO.HIGH) #start
    time.sleep(run_time)
    GPIO.output(STBY, GPIO.LOW) #stop


#------------------------------------------------------------------------------------------sonar
#set GPIO Pins
GPIO_TRIGGER = 12
GPIO_ECHO = 18
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
dist=0#global distacle value
lock = Lock()
def distance():
    while exit == False:
        global dist
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
     
        StartTime = time.time()
        count = time.time()
        StopTime=time.time()
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0 and time.time()-count<0.1  and exit == False:
            StartTime = time.time()
            #print("first",time.time()-count)
     
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1  and exit == False:
            StopTime = time.time()
            #print("second", time.time()-StopTime)
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        lock.acquire()
        dist = (TimeElapsed * 34300) / 2
        lock.release()
        #print ("Measured Distance = %.1f cm" % dist)
        time.sleep(1)

    
 
    


#------------------------------------------------------------------------------------------video
# initialize the video stream and allow the camera sensor to warm up
print("starting video stream..")
#vs = VideoStream(src=0).start()# this is for testing with a web cam not in use. We didn't have anymore equipment
#vs = VideoStream(usePiCamera=True).start()
#time.sleep(2.0)

#------------------------------------------------------------------------------------------
   



path= list()# global list so that we can keep track of the paths we are on





#define a function that will capture video for us 

def imageRec():
    #wrapping it in a try loop incase the camera fails
    while exit==False:
        # grab the frame from the threaded video stream and resize it to  have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)
        # loop over the detected barcodes 
        for barcode in barcodes:
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
              print(path)
            

                        
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

    
       





#create threads
#videoThread = threading.Thread(target=imageRec) 

distaceThread = threading.Thread(target=distance) 


#starting the thread
#videoThread.start()
distaceThread.start()




stage_one=False
stage_two=True
stage_three=False


#make the driving decisions  
avg=0
tick=0
home=False
out=True
try:
    while out:
        
        #--------------------------------------------
        
        while (len(path)==0 ):
            stage_one=False
            print("Scann QR one ")
            if len(path)==0 :
              time.sleep(.01)
              path.append("right")
        if len(path)==1 and tick ==0:
            time.sleep(0.1)
            tick=1
            print("tick",tick)



        #print("this is len",len(path))
        if stage_one == True:
            print("st1 out dist",dist)
            if dist  > 30 or dist < 0 :#this lets us move fwr is nothing has been found in path
                go_forward(leg)
                print("stage one fwr")
            else:
                print("str else dist",dist)
               
                if dist < 30 and dist > 0:
                    stage_one=False
                    stage_two=True
                    stage_three=False



                
        #--------------------------------------------
        if stage_two == True:
            print("stage2")
            print(dist)

   
            if dist  > 30 or dist < 0 :# if nothing is in path move fwr
                #add a possible shake here 
                go_forward(leg)
            elif dist < 30 and dist > 0:#this goes in when we hit the wall
                while len(path)<2:
                    print("in stg2 scan 2 QR")

                    stage_two=False
                    stage_three=True
                    if len(path)==1 :
                      time.sleep(5)
                      path.append("stop sign")

                if path[0]== "left":#this checks if the first scanns 
                    turn_left(turn)
                    time.sleep(10)
                elif path[0]=="right":#this checks if need to turn right
                    turn_right(turn)
                    time.sleep(10)

         #--------------------------------------------
        if stage_three == True:#final stage we are going home
            print("stage 3")
            print(dist)
            print(home)
            if dist > 30 and dist < 0 and home==False:
                go_forward(leg)
                print("fwr")
                
            elif dist < 30 and dist > 0:
                #might add a while loop to read the QR code
                #we are home so we shake 
                turn_right(2)
                turn_left(2)
                print("home")
                home=True#we made it home 
                stage_three=False#we exit stage 3
                out=False#this is we are done 
    light=[0,1,0,1,1,1,0,0,1,1,1,0]
    l=[0,3,6,9]
    for a in l:
      GPIO.output(Blue,light[a])
      GPIO.output(Green,light[a+1])
      GPIO.output(Red,light[a+2])
      print(light[a],light[a+1],light[a+2])
      time.sleep(2)
    audio= [1,5,2,4,3]
    buzzer = Buzzer()
    for a in audio:
        buzzer.play(int(a))


except KeyboardInterrupt:
    exit=True
    #videoThread.join()
    print("thread vide done")
    distaceThread.join()
    print("distance done")
    print(path)
    GPIO.cleanup()
    print("Ok ok, quitting")
    #sys.exit(1)

finally:
    exit=True
    #videoThread.join()
    print("thread vide done")
    distaceThread.join()
    print("distance done")
    print(path)
    GPIO.cleanup()
    print("finall out")
    #sys.exit(1)



