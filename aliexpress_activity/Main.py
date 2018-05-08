# -*- coding: utf-8 -*-


from action.RobotBrowser import *
from manager.ConfigManager import *

config = ConfigManager()
all_tasks = config.get_all_tasks()
robot = RobotBrowser()


def check_is_login():
    robot.openUrl(robot.aliexpress_index, "top-lighthouse")
    robot.set_cookies()
    robot.openUrl(robot.aliexpress_index, "top-lighthouse")
    if robot.checkIsLogin():
        return True
    else:
        return False
if __name__ == '__main__':

    try:
        username=r""
        passwd=r""
        while not check_is_login():
            robot.sign_in(username,passwd)
        for task in all_tasks:
            log_info("start to create discount: "+task.name)
            robot.createStoreDiscount(task)
            log_info("create discount: " + task.name+" success.")
    except Exception, e:
        print e.message
        sys.exit(1)
