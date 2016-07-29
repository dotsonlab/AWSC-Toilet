#!/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time, sys
import os.path

fixture = "TOILET"

stepperENABLE = 'P8_11'  #high disables driver mosfets, low enables

flowPULSE = 'P9_41' #2200 pulses per liter

#step pin on motor driver to be controlled by PWM below *note changed to P9_16 as not all listed PWM pins appear to function
GPIO.setup(stepperDIR, GPIO.OUT) #direction pin
GPIO.setup(stepperENABLE, GPIO.OUT) #ENABLE motor driver

GPIO.setup(flowPULSE, GPIO.IN) #flowmeter

GPIO.output(stepperENABLE, GPIO.HIGH)
GPIO.output(stepperDIR, GPIO.LOW) #direction

now=time.localtime(time.time())
currentmonth=now.tm_mon
currentday=now.tm_mday
currentyear=now.tm_year
filename = "{0}_{1}_{2}_{3}-flow.csv".format(currentyear, currentmonth, currentday, fixture)

global count
global countIDLE

restart = True
count = 0
countIDLE = 0

totalflow = 0
PWMstarted = 0

def countPulse(channel):
   global count
   count = count+1

GPIO.add_event_detect(flowPULSE, GPIO.RISING, callback=countPulse)

while True:
    try:

        #get current time
        now=time.localtime(time.time())
        pt=time.asctime(now)  #formatted time for file
        currentmonth=now.tm_mon
        currentday=now.tm_mday
        currentyear=now.tm_year
        currenthour=now.tm_hour
        currentminute=now.tm_min
        currentsecond=now.tm_sec

        start_counter = 1
        count=0
        time.sleep(1)
        start_counter = 0
        flow = count * 60.0 / 2200.0
        #if flow >= 4.1: #set maximum flow to restrict miscalculation associated with electrical noise acceptable due to pd pump
        #flow = 4.1
        stepf = flow * 0.02 * 1000 / 60 / 2.36 * 200
        totalflow = totalflow + flow/60
        print '%s%f\t%s%f\t%s%f' % ( "Flow (LPM): ",flow,"Step rate (Hz): ",stepf,"Total Flow (L):",totalflow) #comment out if debugging complete

        if (os.path.isfile(filename) and restart):
            #restart ensures that it will only execute this once.
            restart = False
            #restarting the file
            file = open(filename)
            #grab last non-blank line
            last = None
            for line in (line for line in file if line.rstrip('\n')):
                last = line
            #set totalflow to last known value
            totalflow = float(last.split(",")[2])
        elif not (os.path.isfile(filename)):
            #Initial and daily startup
            totalflow = 0
            file=open(filename,"a")
            #informative messaging for starting storage file
            print "Opening ",filename, " for appending..."
            print "reading analog inputs and storing data..."
            file.write("Time,Flow,TotalFlow\n")
            #add first column date/time stamp
            file.write(pt)
            file.write(",%f,%f\n" % (flow,totalflow))
            file.close()

        if stepf >= 60:
            countIDLE = 0
            #open file to append
            file=open(filename,"a")
            #add first column date/time stamp
            file.write(pt)
            #add next columns with raw reading, and converted voltage
            file.write(",%f,%f\n" % (flow,totalflow))
            file.close()
            #if MM/DD/YR changes, update filename
            #this translates to a new file every day
            ##!!!!header row is dropped from subsequent days
            filename = "{0}_{1}_{2}_{3}-flow.csv".format(currentyear, currentmonth, currentday)

        else:
            countIDLE = countIDLE+1
            # print countIDLE

            if countIDLE == 900:
                countIDLE = 0
                #open file to append
                file=open(filename,"a")
                #add first column date/time stamp
                file.write(pt)
                #add next columns with raw reading, and converted voltage
                file.write(",%f,%f\n" % (flow,totalflow))
                file.close()
                #if MM/DD/YR changes, update filename
                #this translates to a new file every day
                ##!!!!header row is dropped from subsequent days
                filename = "{0}_{1}_{2}_{3}-flow.csv".format(currentyear, currentmonth, currentday)

    except KeyboardInterrupt:
        print '\ncaught keyboard interrupt!, bye'
        GPIO.cleanup()
        sys.exit()
