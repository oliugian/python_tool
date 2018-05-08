# -*- coding: utf-8 -*-

from manager.ConfigManager import *
from action.TaskAction import *
from manager.TimeManager import *

def run_work(all_tasks):
    for task in all_tasks:
        task_action = TaskAction(task)
        task_action.start_action_work()

if __name__ == '__main__':
    config_manager = ConfigManager()
    all_tasks = config_manager.get_all_tasks()
    run_work(all_tasks)
    log_info("#####################")
    log_info("all tasks run finish.")
    log_info("#####################")
    while True:
        waitSeconds(3000)
