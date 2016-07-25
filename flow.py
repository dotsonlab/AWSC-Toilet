'''
David Rodriguez

Goal: Continuously looping while to perform valve actions at specified times,
introduce substance at a specific ratio based on flow data, recording
and saving flow data, and actuating a flush at a specified time.

Inputs: A schedule of events based on entered times.

Outputs: Sequence of events to a screen as they happen.
daily flow rate data
'''
#logic testing Below is the functional portion
import datetime
import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

class Flow:
    GPIO.setup("P8_7", GPIO.OUT) #stepper direction
    GPIO.setup("P9_16", GPIO.OUT) #step
    GPIO.setup("P8_11", GPIO.OUT) #(0: enabled, 1: disabled)
    GPIO.setup("P8_15", GPIO.OUT) #Direction for actuator 1
    GPIO.setup("P8_17", GPIO.OUT) #PWM for actuator 1
    GPIO.setup("P8_16", GPIO.OUT) #Direction for actuator 2
    GPIO.setup("P8_18", GPIO.OUT) #PWM for actuator 2
    GPIO.output("P8_7", GPIO.LOW) #set stepper motor direction
    tag = ""

    def enableStepper(self):
        GPIO.output("P8_11", GPIO.LOW)

    def disableStepper(self):
        GPIO.output("P8_11", GPIO.HIGH)

    def triggerStepper(self):
        time.sleep(0.5)
        PWM.start("P9_16", 25, 100, 1)
        time.sleep(2)
        PWM.set_frequency("P9_16", 250)
        time.sleep(90)
        PWM.stop("P9_16")
        PWM.cleanup()

    def toiletTrigger(self, flushType):
        if flushType == "Full":
            self.toiletFull()
        else:
            self.toiletUrine()

    def toiletUrine(self):
        print "Toilet Urine Triggered"
        self.enableStepper()
        self.triggerStepper()
        GPIO.output("P8_17", GPIO.HIGH) #pwm on
        GPIO.output("P8_15", GPIO.LOW)  #extend actuator
        time.sleep(.65)
        GPIO.output("P8_15", GPIO.HIGH) #retract actuator
        time.sleep(2)
        GPIO.output("P8_17", GPIO.LOW) #pwn off
        self.disableStepper()

    def toiletFull(self):
        print "Toilet Full Triggered"
        self.enableStepper()
        self.triggerStepper()
        GPIO.output("P8_18", GPIO.HIGH) #pwm on
        GPIO.output("P8_16", GPIO.LOW) #extend actuator
        time.sleep(.65)
        GPIO.output("P8_16", GPIO.HIGH) #retract actuator
        time.sleep(1)
        GPIO.output("P8_18", GPIO.LOW) #pwm on
        self.disableStepper()
