# -*- coding: utf-8 -*-

import json
from multiprocessing.context import SpawnContext, Process


from threading import Thread, Timer
from flask import current_app
from app.auto.builder import Builder
from app.module.TimedTask import TimedTask, Job
from app import db


def robot_run(id):
    app = current_app._get_current_object()
    if len(app.config["RESULTS"]) > int(app.config["AUTO_PROCESS_CONT"]):
        return json.dumps({"status": "busying", "msg": u"任务池已满！！！"})

    builder = Builder(id)
    builder.build()

    # 运行任务
    # TODO

    return json.dumps({"status": "success", "msg": "任务启动成功！！！"})


def robot_async_run(id):
    app = current_app._get_current_object()

    builder = Builder(id)
    builder.build()

    # todo
    thread = Thread(target=builder.run_case, args=[])

    thread.start()

    return json.dumps({"status": "success", "msg":"任务启动成功！！！"})


def check_process_status(app):

    with app.app_context():
        try:
            for runner in app.config["RUNNERS"]:
                if runner.is_finish():
                    runner.write_result()
                    app.config["RUNNERS"].remove(runner)
        except Exception as e:
            print(e)


def debug_run(id):
    builder = Builder(id)
    builder.build()


class Runner:

    def __init__(self, process_count):
        self.proc_pool = {} # 记录创建的所有子进程
        self.process_count = process_count

    def run(self, task_id, build_no):
        name = TimedTask.get_by_id(task_id).name
        job = Job()
        job.task_id = task_id
        job.build_no = build_no
        job.status = "running"

        p = Process(target=self.run_case)

        p.start()

        while len(self.proc_pool) >= self.process_count:
            p.join(timeout=1)

        self.proc_pool[p.pid] = p

        return {"status": "success",
                "msg": "任务启动成功",
                "task_id": task_id,
                "build_no": build_no}

    def run_case(self):
        pass

    def stop(self, pid):
        process = self.proc_pool.pop(pid, None)

        if process:
            process.terminate()
            process.join()

            return {
                "status": "success",
                "msg": "停止%s成功".format(pid)
            }
        else:
            return {
                "status": "success",
                "msg": "%s不存在".format(pid)
            }

    def stop_all(self):
        """
        停止所有的case？
        :return:
        """
        pass

    # def is_finish(self):
    #     return self._process.is_finished()


class InterfaceRunner(Runner):

    def run_case(self):
        pass
