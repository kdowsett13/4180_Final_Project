#Hackbot.py
#Just a little test code to run around the floor a bit

import RPi.GPIO as GPIO
import time

#a couple of delay constants
leg = 2
turn = 0.5

#set up control pins for motor driver
STBY = 31
AIN1 = 33
AIN2 = 35
PWMA = 37
BIN1 = 32
BIN2 = 36
PWMB = 38

GPIO.setmode(GPIO.BOARD) #use board pin numbers

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

GPIO.output(AIN1, GPIO.HIGH)
GPIO.output(AIN2, GPIO.LOW)
GPIO.output(PWMA, GPIO.HIGH)

GPIO.output(BIN1, GPIO.HIGH)
GPIO.output(BIN2, GPIO.LOW)
GPIO.output(PWMB, GPIO.HIGH)

#movement is governed by the 4
#following functions.  These will
#go into their own library, ultimately.
def go_forward(run_time):
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)

    GPIO.output(STBY, GPIO.HIGH) #start
    time.sleep(run_time)
    GPIO.output(STBY, GPIO.LOW) #stop

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

#Then we make a simple driving patern and loop    
try:
    while True:

        #go forward
        go_forward(leg)

        #turn right?
        turn_right(turn)

        #go forward
        go_forward(leg)

        #turn right?
        turn_right(turn)

        #go forward
        go_forward(leg)

        #turn left
        turn_left(turn)

        #go forward
        go_forward(leg)

        #turn left
        turn_left(turn)

        #reverse
        reverse(leg)

except KeyboardInterrupt:
    print("exit script")
    GPIO.cleanup()

