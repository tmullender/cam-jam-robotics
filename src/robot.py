import RPi.GPIO as GPIO

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set variables for the GPIO motor pins
pinMotorAForwards = 9
pinMotorABackwards = 10
pinMotorBForwards = 8
pinMotorBBackwards = 7

# How many times to turn the pin on and off each second
frequency = 20
# How long the pin stays on each cycle, as a percent (here, it's 30%)
aDutyCycle = 80
bDutyCycle = 78
# Setting the duty cycle to 0 means the motors will not turn
stop = 0
turningFactor = 2

# Set the GPIO Pin mode to be Output
GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinMotorABackwards, GPIO.OUT)
GPIO.setup(pinMotorBForwards, GPIO.OUT)
GPIO.setup(pinMotorBBackwards, GPIO.OUT)

# Set the GPIO to software PWM at 'Frequency' Hertz
pwmMotorAForwards = GPIO.PWM(pinMotorAForwards, frequency)
pwmMotorABackwards = GPIO.PWM(pinMotorABackwards, frequency)
pwmMotorBForwards = GPIO.PWM(pinMotorBForwards, frequency)
pwmMotorBBackwards = GPIO.PWM(pinMotorBBackwards, frequency)

# Start the software PWM with a duty cycle of 0 (i.e. not moving)
pwmMotorAForwards.start(stop)
pwmMotorABackwards.start(stop)
pwmMotorBForwards.start(stop)
pwmMotorBBackwards.start(stop)


def update(a, b):
    a_forwards = a if a > 0 else stop;
    a_backwards = -a if a < 0 else stop;
    b_forwards = b if b > 0 else stop;
    b_backwards = -b if b < 0 else stop;
    pwmMotorAForwards.ChangeDutyCycle(a_forwards)
    pwmMotorABackwards.ChangeDutyCycle(a_backwards)
    pwmMotorBForwards.ChangeDutyCycle(b_forwards)
    pwmMotorBBackwards.ChangeDutyCycle(b_backwards)


# Turn all motors off
def stop_motors():
    update(stop, stop)


# Turn both motors forwards
def forwards():
    update(aDutyCycle, bDutyCycle)


# Turn both motors backwards
def backwards():
    update(-aDutyCycle, -bDutyCycle)


# Turn left
def left():
    update(-aDutyCycle/turningFactor, bDutyCycle/turningFactor)


# Turn Right
def right():
    update(aDutyCycle/turningFactor, -bDutyCycle/turningFactor)


def cleanup():
    stop_motors()
    GPIO.cleanup()
