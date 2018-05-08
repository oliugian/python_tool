# -*- coding: utf-8 -*-
import sys
from manager.LogManager import *
class Task(object):

    def __init__(self, *args):
        args = args[0]
        if len(args) != 18:
            log_error("wrong format: " + str(args))
            sys.exit(1)
        self.use_proxy = args[0] if args[0] == "no" else "yes"
        self.key_word = args[1] if args[1] is not None else sys.exit(1)
        self.search_type = args[2]
        self.asin_id = args[3]
        self.max_page = args[4] if args[4] is not None and args[4] != "" else 20
        self.add_to_wish = args[5] if args[5] == "yes" else "no"
        self.add_to_cart = args[6] if args[6] == "yes" else "no"
        self.like_5_point_comment = args[7] if args[7] == "yes" else "no"
        self.task_count = int(args[8]) if args[8] is not None and args[8] != "" else 1
        self.run_count = int(args[9]) if args[9] is not None and args[9] != "" else 10

        self.start_time = args[10]
        self.end_time = args[11]
        self.size = unicode(str(args[12]))
        self.color = unicode(str(args[13]))
        self.task_type = args[14] if args[14] is not None and args[14] != "" else "shopping_cart_wish"
        self.select_child_product = args[15] if args[15] is not None and args[15] != "" else "no"
        self.child_asin_id = args[16].split("|") if args[16] is not None and args[16] != "" else None
        self.isDone = args[17] if args[17] is not None and args[17] != "" else "no"



