#!/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO
import time, sys

flowPULSE = 'P9_41' #2200 pulses per liter

GPIO.setup(flowPULSE, GPIO.IN) #flowmeter

now=time.localtime(time.time())
currentmonth=now.tm_mon
currentday=now.tm_mday
currentyear=now.tm_year
filename = "{0}_{1}_{2}_toilet-flow.csv".format(currentyear, currentmonth, currentday)

#### informative messaging for starting storage file
print "Opening ",filename, " for appending..."
print "reading analog inputs and storing data..."
file=open(filename,"a")
file.write("Time,Flow,TotalFlow\n")
file.close()

global count
global countIDLE

count = 0
viscount = 0
countIDLE = 0
totalflow = 0

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

        start_counter = 1
        count=0
        time.sleep(1)
        start_counter = 0
        flow = count * 60.0 / 2200.0
	if flow >= 4.1: #set maximum flow to restrict miscalculation associated with electrical noise acceptable due to pd pump
		flow = 4.1
        stepf = flow * 0.02 * 1000 / 60 / 2.36 * 200
        totalflow = totalflow + flow/60
        print '%s%f\t%s%f' % ( "Flow (LPM): ",flow,"Total Flow (L):",totalflow) #comment out if debugging complete
	viscount=viscount+1
	print viscount

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
            filename = "{0}_{1}_{2}_toilet-flow.csv".format(currentyear, currentmonth, currentday)

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
                filename = "{0}_{1}_{2}_toilet-flow.csv".format(currentyear, currentmonth, currentday)

    except KeyboardInterrupt:
        print '\ncaught keyboard interrupt!, bye'
        GPIO.cleanup()
        sys.exit()
