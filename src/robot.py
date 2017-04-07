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


# Turn all motors off
def stop_motors():
    pwmMotorAForwards.ChangeDutyCycle(stop)
    pwmMotorABackwards.ChangeDutyCycle(stop)
    pwmMotorBForwards.ChangeDutyCycle(stop)
    pwmMotorBBackwards.ChangeDutyCycle(stop)


# Turn both motors forwards
def forwards():
    pwmMotorAForwards.ChangeDutyCycle(aDutyCycle)
    pwmMotorABackwards.ChangeDutyCycle(stop)
    pwmMotorBForwards.ChangeDutyCycle(bDutyCycle)
    pwmMotorBBackwards.ChangeDutyCycle(stop)


# Turn both motors backwards
def backwards():
    pwmMotorAForwards.ChangeDutyCycle(stop)
    pwmMotorABackwards.ChangeDutyCycle(aDutyCycle)
    pwmMotorBForwards.ChangeDutyCycle(stop)
    pwmMotorBBackwards.ChangeDutyCycle(bDutyCycle)


# Turn left
def left():
    pwmMotorAForwards.ChangeDutyCycle(stop)
    pwmMotorABackwards.ChangeDutyCycle(aDutyCycle/2)
    pwmMotorBForwards.ChangeDutyCycle(bDutyCycle/2)
    pwmMotorBBackwards.ChangeDutyCycle(stop)


# Turn Right
def right():
    pwmMotorAForwards.ChangeDutyCycle(aDutyCycle/2)
    pwmMotorABackwards.ChangeDutyCycle(stop)
    pwmMotorBForwards.ChangeDutyCycle(stop)
    pwmMotorBBackwards.ChangeDutyCycle(bDutyCycle/2)


def cleanup():
    stop_motors()
    GPIO.cleanup()
