# -*- coding: utf-8 -*-
import sys
from manager.LogManager import *
class Task(object):

    def __init__(self, *all_args):
        args = all_args[0][0].split(";")

        if len(args) != 5:
            log_error("wrong format: " + str(args))
            sys.exit(1)
        self.name = args[0]
        self.begin_date = self.format_date(args[1])
        self.begin_time = self.format_time(args[2])
        self.end_date = self.format_date(args[3])
        self.end_time = 24-int(self.format_time(args[4]))

    def format_date(self,date):
        dates = date.split("/")
        result = dates[0]
        if len(dates[1]) == 1:
            dates[1] = "0"+dates[1]
        result=result+"/"+str(dates[1])
        if len(dates[2]) == 1:
            dates[2] = "0" +dates[2]
        result=result+"/"+dates[2]
        return result
    def format_time(self,time):
        times = time.split(":")
        result = int(times[0])
        if times[1] == "59":
            result = result + 1
        return str(result)
