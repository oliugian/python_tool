# -*- coding: utf-8 -*-
import os
from CSVFileManager import *
from model.Task import *


class ConfigManager:

    def __init__(self):
        self.configPath = os.path.abspath("./config")
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


"""
    def initConfigFromFile(self):
        f = open(self.configDataPath, 'r')

        for line in f.readlines():
            line = line.strip()
            if line.startswith("#") or line == "\n" or line == "":
                continue
            key,value = line.split("=")
            if value == "":
                continue
            if key == "use_proxy":
                self.config.use_proxy = value
                log_info("### user_proxy:"+value)
            elif key == "task_count":
                self.config.task_count = value
                log_info("### task_count:" + value)
            elif key == "start_time":
                self.config.start_time = value
            elif key == "end_time":
                self.config.end_time = value
            elif key == "task_type":
                self.config.task_type = value
            elif key == "run_count":
                self.config.run_count = value
            if self.config.task_type == "shopping_cart_wish":
                if key == "key_word":
                    self.config.key_word = value
                    log_info("### key_word:" + value)
                elif key == "search_type":
                    self.config.search_type = value
                elif key == "max_page":
                    self.config.max_page = value
                elif key == "asin_id":
                    self.config.asin_id = value
                    log_info("### asin_id:" + value)
                elif key == "select_child_product":
                    self.config.select_child_product = value
                elif key == "child_asin_id":
                    self.config.child_asin_id = value.split("|")
                elif key == "like_5_point_comment":
                    self.config.like_5_point_comment = value
                    log_info("### like_5_point_comment:" + value)
                elif key == "add_to_wish":
                    self.config.add_to_wish = value
                    log_info("### add_to_wish:" + value)
                elif key == "add_to_cart":
                    self.config.add_to_cart = value
                    log_info("### add_to_cart:" + value)
            if self.config.task_type == "look_and_look":
                if key == "look_and_look_time_interval":
                    self.config.look_and_look_time_interval = value
                    log_info("### look_and_look_time_interval:" + value)

        f.close()
"""