'''
David Rodriguez

Goal: Continuously looping while to perform valve actions at specified times, 
introduce substance at a specific ratio based on flow data, recording 
and saving flow data, and actuating a flush at a specified time.

Inputs: A schedule of events based on entered times.

Outputs: Sequence of events to a screen as they happen. 
daily flow rate data
'''
#An object for events

import datetime
import time

import Adafruit_BBIO.GPIO as GPIO

class Event:
    startTime = datetime.time()
    flushType = ""
    
    def __init__(self, start):
        self.startTime = start
        self.flushType = ""
    
    def setFlushFull(self):
        self.flushType = "Full"
    
    def displayEvent(self):
        return "%s %s" % (str(self.startTime), self.flushType)
    
    def storeEvent(self):
        saveEvent = "%s %s" % (str(self.startTime), self.flushType)
        return saveEvent