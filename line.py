import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import time
Blue = 16
Green = 22
Red = 40




GPIO.setup(Blue,GPIO.OUT)
GPIO.output(Blue,1)
GPIO.setup(Green,GPIO.OUT)
GPIO.output(Green,1)
GPIO.setup(Red,GPIO.OUT)
GPIO.output(Red,1)



try:
  while True:
      light=[0,1,0,1,1,1,0,0,1,1,1,0]
      l=[0,3,6,9]
      for a in l:
          GPIO.output(Blue,light[a])
          GPIO.output(Green,light[a+1])
          GPIO.output(Red,light[a+2])
          print(light[a],light[a+1],light[a+2])
          time.sleep(2)
    

finally:
  print('clean up')
  GPIO.cleanup()
  
