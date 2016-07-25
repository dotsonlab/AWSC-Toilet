'''
David Rodriguez

Goal: Continuously looping while to perform valve actions at specified times,
introduce substance at a specific ratio based on flow data, recording
and saving flow data, and actuating a flush at a specified time.

Inputs: A schedule of events based on entered times.

Outputs: Sequence of events to a screen as they happen.
daily flow rate data
'''
from toiletschedule import Schedule
from flow import Flow
import datetime
import time

workingSchedule = Schedule()
midnight = datetime.time()
nextStartTime = datetime.time()
nextEndTime = datetime.time()
meter = Flow()
counter = 1


meter.disableStepper() # prevent the motor for burning up
while True:
    print "\n1: Run Schedule"
    print "2: Manage Schedules"
    print "3: Exit"
    option = int(raw_input("\nPlease select an option.\n"))

    #run schedule: set midnight time, set flow enable to high (off).
    #Import a schedule or sort and use current schedule
    if option == 1:
        currentTime = datetime.datetime.time(datetime.datetime.now()).replace(microsecond = 0)
        midnight = currentTime.replace(hour = 23, minute = 59, second = 59)
        meter.currentTime = datetime.datetime.now().replace(microsecond = 0)
        #meter.log()# start logging

        print "\n\nCtrl + Pause/Break at any time to stop operation.\n"

        if not workingSchedule.eventCount:#if no objects ask for a schedule to import
            workingSchedule.importSchedule()
            workingSchedule.displaySchedule()
        else:#sort and run
            workingSchedule.eventList.sort(key = lambda event: event.startTime)
            workingSchedule.displaySchedule()
        print ""

        nextEvent = workingSchedule.eventList[0]#grab first event
        nextStartTime = nextEvent.startTime
        print nextEvent.displayEvent() + " loaded."

        while True:# infinite loop
            currentTime = datetime.datetime.time(datetime.datetime.now())
            currentTime = currentTime.replace(microsecond = 0)#current time ignore microseconds

            if (nextStartTime < currentTime and counter < (len(workingSchedule.eventList))):
                print "Event is in the past, loading next event.\n"
                nextEvent = workingSchedule.eventList[counter]
                nextStartTime = nextEvent.startTime
                counter += 1
                print nextEvent.displayEvent() + " loaded."

            elif nextStartTime == currentTime:
                meter.toiletTrigger(nextEvent.flushType)
                time.sleep(1)#hold a second so that the event isn't triggered multiple times

                if (counter == len(workingSchedule.eventList)):
                    print "Last event of the day, waiting until midnight to reset.\n"
                time.sleep(1)#hold a second so event isn't triggered multiple times

            elif currentTime == midnight:
                    self.counter = 1
                    nextEvent = workingSchedule.eventList[0]
                    nextStartTime = nextEvent.startTime
                    print "\nMidnight! Resetting.\n"
                    workingSchedule.displaySchedule()
                    meter.reset()
                    time.sleep(1)
                    print nextEvent.displayEvent() + " loaded."
            else:
                meter.checkFlow()#if no events to trigger; check flow

#Import, save, edit a schedule or create a new one.
    elif option == 2:
        while True:
            workingSchedule.displayMenu()
            selection = 0
            while selection == 0:
                input = raw_input("\nPlease select an option.\n")
                if input.isdigit():
                    selection = int(input)

            if selection == 1:
                workingSchedule.importSchedule()
                workingSchedule.displaySchedule()
            elif selection == 2:
                workingSchedule.addEvent()
            elif selection == 3:
                if not workingSchedule.eventCount:
                    print "There are no events to remove."
                else:
                    print ""
                    workingSchedule.displaySchedule()
                    item = -1

                    while item == -1:
                        toRemove = raw_input(("\nSelect an event to remove.\n"))
                        if toRemove.isdigit():
                            item = int(toRemove) - 1

                    workingSchedule.eventList.pop(item)
                    workingSchedule.eventCount -= 1
            elif selection == 4:
                if not workingSchedule.eventCount:
                    print "The current schedule has no events."
                else:
                    print "\nEvents in this schedule are:"
                    workingSchedule.displaySchedule()
            elif selection == 5:
                workingSchedule.saveSchedule()
            elif selection == 6:
                option = 0
                break
            else:
                print "\nThat is not a valid option please make another selection.\n"
    elif option == 3:
        print("Exiting...\n")
        break
    else:
        print("You did not enter a valid option please try again.\n")
