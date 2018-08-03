# -*- coding: utf-8 -*-
import os
from app.module.TimedTask import TimedTask
from config import ROOT_PATH


class Builder:
    def __init__(self, id):
        self.id = id
        self.build_no = 1
        self.task_name = ""
        self.task_dir = ""
        self.hash_case = False

    def build(self):
        self.build_task()

    def build_task(self):
        task = TimedTask.get_by_id(id)

        if task:
            self.task_dir = os.path.join(ROOT_PATH, "logs", self.id)
            self.task_name = task.name

            if os.path.exists(self.task_dir) is False:
                os.makedirs(self.task_dir)

            L = []
            dirs = os.listdir(self.task_dir)

            for d in dirs:
                if d.isdigit():
                    L.append(int(d))

            L.sort()

            self.build_no = 1
            if len(L) !=0:
                self.build_no = int(L[-1]) +1

            log_dir = os.path.join(self.task_dir, self.build_no)
            os.makedirs(log_dir)

    def run_case(self):
        """
        运行用例
        :return:
        """
        # TODO


