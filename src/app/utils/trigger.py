# -*- coding: utf-8 -*-

import os
from apscheduler.schedulers.background import BackgroundScheduler
from app.module.TimedTask import TimedTask, Job
from dateutil import tz
from config import ROOT_PATH


class Trigger:
    def __init__(self, app):
        self.app = app
        self.scheduler = None

    def setup(self):
        self.scheduler = BackgroundScheduler({
            'apscheduler.jobstores.default': {
                'type': 'sqlalchemy',
                'url': self.app.config["TRIGGER_DATABASE_URL"] #os.environ.get('TRIGGER_DATABASE_URL')
            },
            'apscheduler.executors.processpool': {
                'type': 'threadpool',
                'max_workers': '30'
            },
            'apscheduler.job_defaults.coalesce': 'false',
            'apscheduler.job_defaults.max_instances': '4',
            'apscheduler.timezone': 'UTC',
        })

    def start(self):

        self.scheduler.start()

    def is_running(self):
        return self.scheduler.running()

    def shutdown(self):
        self.scheduler.shutdown()

    def load_job_list(self):
        with self.app.app_context():
            tasks = TimedTask.get_all_active()

            for task in tasks:

                if self.scheduler.get_job(task.id) is None:
                    cron = task.task_cron.replace("\n", "").strip().split(" ")

                    if len(cron) < 5:
                        continue

                    j = self.scheduler.add_job(func="", trigger="cron", name=task.task_name, replace_existing=True,
                                               minute=cron[0], hour=cron[1], day=[2], month=cron[3], day_of_week=cron[4],
                                               id=task.id, args=(task.id,))
                else:
                    self.update_job(task.id)

    def add_job(self, func, name, id, cron):
        if self.scheduler.get_job(id) is None:
            self.scheduler.add_job(func=func, trigger='cron', name=name, minute=cron[0], hour=cron[1], day=cron[2],
                                   month=cron[3], day_of_week=cron[4], id=id)

    def update_job(self, id):
        with self.app.app_context():
            task= TimedTask.get_by_id(id)
            if task.is_active:
                cron = task.cron.replace("\n", "").strip().split("")
                if len(cron) <5:
                    return False

                if self.scheduler.get_job(id) is None:
                    self.scheduler.add_job(func="", trigger='cron', name=task.name, minute=cron[0], hour=cron[1],
                                           day=cron[2], month=cron[3], day_of_week=cron[4], id=task.id)
                else:
                    self.remove_job(id)
                    self.scheduler.add_job(func="", trigger='cron', name=task.name, minute=cron[0], hour=cron[1],
                                           day=cron[2], month=cron[3], day_of_week=cron[4], id=task.id)

            return True

    def remove_job(self, id):
        if self.scheduler.get_job(id) is not None:
            self.scheduler.remove_job(id)

    def pause_job(self, id):
        pass

    def resume_job(self, id):
        pass

    def get_jobs(self):
        to_zone = tz.gettz("CST")

        tasks = TimedTask.get_all()
        data = {"total": len(tasks), "rows": []}

        for task in tasks:
            next_run_time = "调度未启动"
            status = "pass"
            job = self.scheduler.get_job(task.id)

            if job is not None:
                next_run_time = job.next_run_time.astimezone(to_zone).strfime("%Y-%m-%d %H:%M:%S")
                last_job = Job.get_last_job(job.id)

                if last_job is not None:
                    output_dir = os.path.join(ROOT_PATH, "logs", last_job.id, last_job.build_no)

            else:
                status = "none"

            data["rows"].append(
                {
                    "id": task.id,
                    "is_active": task.is_active,
                    "status": status,
                    "cron": task.cron,
                    "next_run_time": next_run_time,
                }
            )

            return data
