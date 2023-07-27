# Copyright 2020 Inspur
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""A Timer Task With APScheduler."""
from apscheduler.schedulers.blocking import BlockingScheduler
from venus.task import adapter


sched = BlockingScheduler()

TRIGGER_INTERVAL = 'interval'
TRIGGER_CRON = 'cron'
TRIGGER_DATE = 'date'


def init_advanced_timer():
    add_jobs()
    sched.start()


def add_jobs():
    sched.add_job(adapter.delete_es_index_job, TRIGGER_INTERVAL,
                  seconds=60, id='delete_es_index_job')
    sched.add_job(adapter.delete_anomaly_record_job, TRIGGER_INTERVAL,
                  seconds=600, id='delete_anomaly_record_job')
    sched.add_job(adapter.anomaly_detect_job, TRIGGER_INTERVAL,
                  seconds=60, id='anomaly_detect_job')
