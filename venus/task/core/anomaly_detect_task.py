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
from venus.modules.search.action import SearchCore
from venus.i18n import _LE, _LI


TASK_NAME = "anomaly_detect"


class AnomalyDetectTask(object):
    """anomaly detect task"""

    def __init__(self):
        self.config_api = CustomConfigCore()
        self.anomaly_api = AnomalyDetectCore()
        self.search_api = SearchCore()

    def anomaly_detect(self):
        now_timestamp = int(time.time())
        last_timestamp = self.config_api.get_config("last_detect_timestamp")
        if last_timestamp:
            last_timestamp = int(last_timestamp)
            if now_timestamp - last_timestamp > 300:
                last_timestamp = last_timestamp - 300
        else:
            last_timestamp = now_timestamp - 60

        self.anomaly_detect_logs("flog", last_timestamp, now_timestamp)
        self.anomaly_detect_logs("slog", last_timestamp, now_timestamp)

        self.config_api.set_config("last_detect_timestamp", str(now_timestamp))

    def anomaly_detect_logs(self, log_type, start_timestamp, end_timestamp):
        try:
            logs_res = self.search_api.logs(None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            log_type,
                                            start_timestamp,
                                            end_timestamp,
                                            1,
                                            10000)

            data = logs_res.get("data", None)
            if data is None:
                return
            logs = data.get("values", None)
            if logs is None:
                return

            params = {}
            params["page_num"] = 1
            params["page_size"] = 999999
            params["log_type"] = log_type
            rules = self.anomaly_api.get_rule_list(params)
            LOG.debug(_LE("get %s rule num:%s"), log_type, str(len(rules)))

            for log in logs:
                for r in rules:
                    context = ""
                    if log_type == "flog":
                        context = log["desc"]
                    elif log_type == "flog":
                        context = log["programname"]
                    else:
                        pass

                    if r.module != log["module_name"]:
                        continue
                    if r.keyword not in context:
                        continue
                    p = {}
                    p["title"] = r.title
                    p["desc"] = r.desc
                    p["keyword"] = r.keyword
                    p["log_type"] = log_type
                    p["module"] = r.module
                    p["logs"] = context
                    ss_str = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(start_timestamp))
                    p["start_time"] = ss_str
                    es_str = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(end_timestamp))
                    p["end_time"] = es_str
                    self.anomaly_api.add_record(p)
        except Exception as e:
            LOG.error(_LE("detect %s logs, catch exception:%s"),
                      log_type, str(e))

    def start_task(self):
        try:
            self.anomaly_detect()
            LOG.info(_LI("anomaly detect task done"))
        except Exception as e:
            LOG.error(_LE("anomaly detect task, catch exception:%s"),
                      str(e))
