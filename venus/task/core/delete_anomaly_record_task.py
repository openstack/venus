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
from venus.i18n import _LE, _LI


TASK_NAME = "delete_anomaly_record"


class DeleteAnomalyRecordTask(object):
    """delete anomaly record task"""

    def __init__(self):
        self.config_api = CustomConfigCore()
        self.anomaly_api = AnomalyDetectCore()

    def delete_outdated_anomaly_records(self):
        len_d = self.config_api.get_config("anomaly_record_save_days")
        if len_d is None:
            LOG.error(_LE("anomaly_record_save_days do not exist"))
            return

        LOG.info(_LI("anomaly record save days: %s"), len_d)
        try:
            params = {}
            params["page_num"] = "1"
            params["page_size"] = "999999"
            params["end_time"] = str(int(time.time()) - 86400 * int(len_d))
            records = self.anomaly_api.get_record_list(params)
            for r in records:
                self.anomaly_api.delete_record(r.id)
        except Exception as e:
            LOG.error(_LE("delete anomaly records, catch exception:%s"),
                      str(e))

    def start_task(self):
        try:
            self.delete_outdated_anomaly_records()
            LOG.info(_LI("delete anomaly records task done"))
        except Exception as e:
            LOG.error(_LE("delete anomaly records task, catch exception:%s"),
                      str(e))
