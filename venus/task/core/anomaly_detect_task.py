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

import time

from venus.common.utils import LOG
from venus.modules.anomaly_detect.action import AnomalyDetectCore
from venus.modules.custom_config.action import CustomConfigCore
from venus.modules.search.search_lib import ESSearchObj
from venus.i18n import _LE, _LI


TASK_NAME = "anomaly_detect"


class AnomalyDetectTask(object):
    """anomaly detect task"""

    def __init__(self):
        self.config_api = CustomConfigCore()
        self.anomaly_api = AnomalyDetectCore()
        self.search_lib = ESSearchObj()

    def anomaly_detect(self):
        last_timestamp = self.config_api.get_config("last_detect_timestamp")
        last_timestamp = int(last_timestamp)
        now_timestamp = time.time()

        if last_timestamp is None:
            last_timestamp = now_timestamp - 60
        if now_timestamp - last_timestamp > 300:
            last_timestamp = now_timestamp - 300

        try:
            openstack_logs_res = self.search_lib.logs(None,
                                                      None,
                                                      None,
                                                      None,
                                                      None,
                                                      None,
                                                      None,
                                                      "flog",
                                                      last_timestamp,
                                                      now_timestamp,
                                                      1,
                                                      10000)
            openstack_logs = openstack_logs_res["data"]["values"]

            system_logs_res = self.search_lib.logs(None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   "slog",
                                                   last_timestamp,
                                                   now_timestamp,
                                                   1,
                                                   10000)
            system_logs = system_logs_res["data"]["values"]

            params = {}
            params["page_num"] = 1
            params["page_size"] = 999999
            rules = self.anomaly_api.get_rule_list(params)

            for log in openstack_logs:
                for r in rules:
                    if r.module != log["module_name"]:
                        continue
                    if r.keyword not in log["desc"]:
                        continue
                    p = {}
                    p["title"] = r.title
                    p["desc"] = r.desc
                    p["keyword"] = r.keyword
                    p["log_type"] = "flog"
                    p["module"] = r.module
                    p["logs"] = log["desc"]
                    ss_str = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(last_timestamp))
                    p["start_time"] = ss_str
                    es_str = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(now_timestamp))
                    p["end_time"] = es_str
                    self.anomaly_api.add_record(p)

            for log in system_logs:
                for r in rules:
                    if r.module != log["module_name"]:
                        continue
                    if r.keyword not in log["desc"]:
                        continue
                    p = {}
                    p["title"] = r.title
                    p["desc"] = r.desc
                    p["keyword"] = r.keyword
                    p["log_type"] = "slog"
                    p["module"] = r.module
                    p["logs"] = log["desc"]
                    ss_str = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(last_timestamp))
                    p["start_time"] = ss_str
                    es_str = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(now_timestamp))
                    p["end_time"] = es_str
                    self.anomaly_api.add_record(p)

            self.config_api.get_config("last_detect_timestamp",
                                       str(now_timestamp))
        except Exception as e:
            LOG.error(_LE("anomaly detects, catch exception:%s"),
                      str(e))

    def start_task(self):
        try:
            self.anomaly_detect()
            LOG.info(_LI("anomaly detects task done"))
        except Exception as e:
            LOG.error(_LE("anomaly detects task, catch exception:%s"),
                      str(e))
