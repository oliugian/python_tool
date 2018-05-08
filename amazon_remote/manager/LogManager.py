import time


def log_info(*info_log):
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" INFO "+ "".join(info_log)

def log_error(*error_log):
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" ERROR "+"".join(error_log)
