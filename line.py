import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

Blue = 16
Green = 18
Red = 40




GPIO.setup(Blue,GPIO.OUT)
GPIO.output(Blue,1)
GPIO.setup(Green,GPIO.OUT)
GPIO.output(Green,1)
GPIO.setup(Red,GPIO.OUT)
GPIO.output(Red,1)

light=[0,1,0,1,1,1,0,0,1,1,1,0]
l=[1,1,1,1]
for a in l:
  GPIO.output(Blue,light[a])
  GPIO.output(Green,[a+1])
  GPIO.output(Red,[a+2])

try:
  while True:
    if GPIO.input(18):
      print("white")
    else:
      print("black")

finally:
  print('clean up')
  GPIO.cleanup()
  
