import RPi.GPIO as GPIO

# Set variables for the GPIO motor pins
PIN_MOTOR_B_BWD = 7
PIN_MOTOR_B_FWD = 8
PIN_MOTOR_A_FWD = 9
PIN_MOTOR_A_BWD = 10
STOP = 0
TURNING_FACTOR = 2
INCREMENT = 20
MAXIMUM_VALUE = 100
MOTOR_OFFSET = 1


class DutyCycle:
    def __init__(self, initial):
        self.initial = initial
        self.value = initial

    def increment(self, turn=False):
        increment = INCREMENT/TURNING_FACTOR if turn else INCREMENT
        if self.value + increment < MAXIMUM_VALUE:
            self.value += increment

    def decrement(self, turn=False):
        increment = INCREMENT/TURNING_FACTOR if turn else INCREMENT
        if self.value - increment > -MAXIMUM_VALUE:
            self.value -= increment

    def stop(self):
        self.value = self.initial

    def __eq__(self, other):
        return self.value == other.value


class Robot:
    def __init__(self):
        # Set the GPIO modes
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # How many times to turn the pin on and off each second
        frequency = 40
        # How long the pin stays on each cycle, as a percent (here, it's 30%)
        self.aDutyCycle = DutyCycle(0)
        self.bDutyCycle = DutyCycle(MOTOR_OFFSET)

        # Set the GPIO Pin mode to be Output
        GPIO.setup(PIN_MOTOR_A_FWD, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_A_BWD, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_B_FWD, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_B_BWD, GPIO.OUT)

        # Set the GPIO to software PWM at 'Frequency' Hertz
        self.pwmMotorAForwards = GPIO.PWM(PIN_MOTOR_A_FWD, frequency)
        self.pwmMotorABackwards = GPIO.PWM(PIN_MOTOR_A_BWD, frequency)
        self.pwmMotorBForwards = GPIO.PWM(PIN_MOTOR_B_FWD, frequency)
        self.pwmMotorBBackwards = GPIO.PWM(PIN_MOTOR_B_BWD, frequency)

        # Start the software PWM with a duty cycle of 0 (i.e. not moving)
        self.pwmMotorAForwards.start(STOP)
        self.pwmMotorABackwards.start(STOP)
        self.pwmMotorBForwards.start(STOP)
        self.pwmMotorBBackwards.start(STOP)

    def update(self):
        a_forwards = self.aDutyCycle.value if self.aDutyCycle.value > 0 else STOP;
        a_backwards = -self.aDutyCycle.value if self.aDutyCycle.value < 0 else STOP;
        b_forwards = self.bDutyCycle.value if self.bDutyCycle.value > 0 else STOP;
        b_backwards = -self.bDutyCycle.value if self.bDutyCycle.value < 0 else STOP;
        self.pwmMotorAForwards.ChangeDutyCycle(a_forwards)
        self.pwmMotorABackwards.ChangeDutyCycle(a_backwards)
        self.pwmMotorBForwards.ChangeDutyCycle(b_forwards)
        self.pwmMotorBBackwards.ChangeDutyCycle(b_backwards)

    # Turn all motors off
    def stop_motors(self):
        self.aDutyCycle.stop()
        self.bDutyCycle.stop()
        self.update()

    # Turn both motors forwards
    def forwards(self):
        if self.bDutyCycle.value - self.aDutyCycle.value == MOTOR_OFFSET:
            self.aDutyCycle.increment()
            self.bDutyCycle.increment()
        else:
            self.aDutyCycle.value = self.bDutyCycle.value - MOTOR_OFFSET
        self.update()

    # Turn both motors backwards
    def backwards(self):
        if self.bDutyCycle.value - self.aDutyCycle.value == MOTOR_OFFSET:
            self.aDutyCycle.decrement()
            self.bDutyCycle.decrement()
        else:
            self.aDutyCycle.value = self.bDutyCycle.value - MOTOR_OFFSET
        self.update()

    # Turn left
    def left(self):
        self.aDutyCycle.decrement(True)
        self.bDutyCycle.increment(True)
        self.update()

    # Turn Right
    def right(self):
        self.aDutyCycle.increment(True)
        self.bDutyCycle.decrement(True)
        self.update()

    def cleanup(self):
        self.stop_motors()
        GPIO.cleanup()
