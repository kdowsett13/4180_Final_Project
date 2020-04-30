#4180_Final_Project

Idea: The Robot is simulating an autonomous robot at a shipping facility or factory.

## Getting Started



### The code requirements are:

* The Robot should follow a predetermined path.
* We should be able to scan QR codes and interpret them to determine the next action.
* The Robot should avoid obstacles.
* Emit festive audio and blink lights when QR codes are read successfully. 

### Parts used:


1. Raspberry Pi 3
2. Sonar (ultrasonic rangefinder)
3. Pi camera V2
4. Google Cloud
5. RGB LED
6. H-bridge Motor Driver
7. Power Pack (4x AA)
8. DC motors (2x)
9. Speaker w/ 2N3904 NPN Amp

#### 



## Deployment Demo Link

[Demo Link click here ](link)


### Break down

In general, the sonar and H-bridge proved the most diffult to calibrate, given sub-optimal (remote) working conditions.

As is explained further in the following summary and demonstration video, the code in this repository allows a simple mobile robot to navigate a simple environment using a combination of sonar range data and camera feedback.

As can be surmised thru the demonstration, in order to accomplish the simple goal of the demonstration, several aspects were hard-coded to match the specific environment. 

A piece of the code is dedicated to trouble shooting misalignments between target QR codes and the camera’s field of view. 


```
#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
```


## Built With

* [Dropwizard](opencv.org) - Used to decode QR codes
* [Zbar](https://pypi.org/project/zbar/) - Barcode scanning
* [ROME](https://www.raspberrypi.org/) - Used as our micro controller

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.



## Authors

* **Jose Sanchez**
* **Keith Dowsett**


## License

*

## Acknowledgments

* https://www.youtube.com/watch?v=L90WS-ptnvI
* [DC motors](https://www.instructables.com/id/Raspberry-PI-L298N-Dual-H-Bridge-DC-Motor/) - H-bridge setup

