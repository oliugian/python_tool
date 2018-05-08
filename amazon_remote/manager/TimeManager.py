import time
import random
from LogManager import *
import os

def waitRandomSecons(maxCount=5):
    time.sleep(random.randint(0, maxCount))

def waitSeconds(timeTmp=5):
    time.sleep(timeTmp)

def isTimeToGo(target_time):

    if target_time == "" or target_time == None:
        return
    log_count = 0
    while True:
        current_time = str(time.strftime("%Y/%m/%d_%H:%M", time.localtime()))
        if current_time >= target_time:
            log_info("current_time is "+str(current_time)+", start to go.")
            break
        if log_count == 0 or log_count == 30:
            log_info("current time is : " + current_time + " wait to " + target_time + " to start the task.")
            log_count = 0
        log_count = log_count + 1
        time.sleep(30)


def isTimeToEnd(target_time):

    if target_time == "" or target_time is None:
        return False
    current_time = str(time.strftime("%Y/%m/%d_%H:%M", time.localtime()))
    if current_time > target_time:
        log_info("current_time is " + str(current_time) + ", it is time to end.")
        return True
    else:
        return False
