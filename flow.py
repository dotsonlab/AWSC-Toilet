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
import threading
import Adafruit_BBIO.GPIO as GPIO


class Flow:
    GPIO.setup("P8_7", GPIO.OUT) #stepper direction
    GPIO.setup("P8_9", GPIO.OUT) #step
    GPIO.setup("P8_11", GPIO.OUT) #(0: enabled, 1: disabled)
    GPIO.setup("P8_15", GPIO.OUT) #Direction for actuator 1
    GPIO.setup("P8_17", GPIO.OUT) #PWM for actuator 1
    GPIO.setup("P8_16", GPIO.OUT) #Direction for actuator 2
    GPIO.setup("P8_18", GPIO.OUT) #PWM for actuator 2
    GPIO.setup("P9_41", GPIO.IN) #flow sensor
    GPIO.output("P8_7", GPIO.LOW) #set stepper motor direction
    GPIO.add_event_detect("P9_41", GPIO.RISING)
    tag = ""
    currentTime = datetime.datetime.now()
    lastDetected = datetime.datetime()
    shortTimer = threading.Timer()
    longTimer = threading.Timer()
    eventPulses = 0
    totalPulses = 0
    steps = 28250
    speed = .001

    def checkFlow(self):
        self.currentTime = datetime.datetime.now().replace(microsecond = 0)
        if GPIO.event_detected("P9_41"):
            self.lastDetected = datetime.datetime.now().replace(microsecond = 0)
            self.totalPulses = self.totalPulses + 1
            self.eventPulses = self.eventPulses + 1
            if self.longTimer != None:
                self.longTimer.cancel()
                self.log()
        elif isFlowing() == False:
            if self.shortTimer != None:
                self.shortTimer.cancel()
                self.log()

    def isFlowing():
        timeDelta = self.currentTime - self.lastDetected
        if timeDelta.second < 5:
            return True
        else:
            return False

    def reset():
        self.totalPulses = 0

    def log(self):
        day = datetime.date.today()
        time = self.currentTime.isoformat()
        liters = self.computeLiters(self.totalPulses)
        LPM = self.computeLiters(self.eventPulses)
        LPM = LPM*12
        self.eventPulses = 0

        filename = "%s_Toilet.csv" % day.isoformat()
        target = open(filename, 'a')
        target.write("%s, %f, %f\n" % (time, LPM, liters))
        target.close()
        if isFlowing() == True:
           self.shortTimer = threading.Timer(1.0, self.log).start()
        else:
           self.longTimer = threading.Timer(900.0, self.log).start()

    def computeLiters(self, numberOfPulses):
        self.liters = numberOfPulses / 2200.0
        return self.liters

    def enableStepper(self):
        GPIO.output("P8_11", GPIO.LOW)

    def disableStepper(self):
        GPIO.output("P8_11", GPIO.HIGH)

    def triggerStepper(self, numberOfTimes):
        time.sleep(.5)
        for i in range(0, numberOfTimes):
            GPIO.output("P8_9", GPIO.HIGH)
            print "Step: %d" % i
            time.sleep(self.speed)
            GPIO.output("P8_9", GPIO.LOW)
            time.sleep(self.speed)

    def toiletTrigger(self, flushType):
        if flushType == "Full":
            self.toiletFull()
        else:
            self.toiletUrine()

    def toiletUrine(self):
        print "Toilet Urine Triggered"
        self.enableStepper()
        self.triggerStepper(self.steps)
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
        self.triggerStepper(self.steps)
        GPIO.output("P8_18", GPIO.HIGH) #pwm on
        GPIO.output("P8_16", GPIO.LOW) #extend actuator
        time.sleep(.65)
        GPIO.output("P8_16", GPIO.HIGH) #retract actuator
        time.sleep(1)
        GPIO.output("P8_18", GPIO.LOW) #pwm on
        self.disableStepper()
