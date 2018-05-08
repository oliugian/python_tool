# -*- coding: utf-8 -*-
import os
from CSVFileManager import *
from model.Task import *


class ConfigManager:

    def __init__(self):
        self.configPath = os.path.abspath("./data")
        self.taskDataPath = os.path.join(self.configPath, "task.csv")


    def writeTaskData(self):
        pass

    def get_all_tasks(self):
        all_tasks = []
        with open(self.taskDataPath, 'rb') as f:
            csv_reader = UnicodeReader(f)
            csv_reader.next()
            while True:
                try:
                    task_value = csv_reader.next()
                except StopIteration:
                    break
                task_temp = Task(task_value)
                all_tasks.append(task_temp)
        f.close()
        return all_tasks


