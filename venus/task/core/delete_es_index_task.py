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

import datetime
import time

from venus.common import utils
from venus.common.utils import LOG
from venus.conf import CONF
from venus.modules.custom_config.action import CustomConfigCore
from venus.modules.search.search_lib import ESSearchObj
from venus.i18n import _LE, _LI


TASK_NAME = "delete_es_index"


class DeleteESIndexTask(object):
    """delete es index task"""

    def __init__(self):
        self.elasticsearch_url = CONF.elasticsearch.url
        self.config_api = CustomConfigCore()
        self.search_lib = ESSearchObj()

    def delete_index(self, name):
        try:
            url = self.elasticsearch_url + '/' + name
            status, text = utils.request_es(url, "DELETE")
            if status != 200:
                LOG.error(_LE("failed to delete es index: %s"), name)
                return
        except Exception as e:
            LOG.error(_LE("delete es index:%s, catch exception:%s"),
                      name, str(e))

    def delete_es_outdated_index(self):
        days = self.config_api.get_config("log_save_days")
        if days is None:
            LOG.error(_LE("the config of log_save_days do not exist"))
            return

        LOG.info(_LI("es indexes(log) save days: %s"), days)
        today = time.strftime('%Y-%m-%d')
        try:
            indexes_array = self.search_lib.get_all_index()
            for index in indexes_array:
                index_name = index["index"]
                index_day = index_name.split('-')[1]
                dt_today = datetime.datetime.strptime(today, "%Y-%m-%d")
                dt_index = datetime.datetime.strptime(index_day, '%Y.%m.%d')
                dt_diff = dt_today - dt_index

                if dt_diff.days >= int(days):
                    LOG.info(_LI("deleted index %s, diff day %d"),
                             index_name, dt_diff.days)
                    self.delete_index(index_name)
                else:
                    LOG.debug(_LI("reserved index %s, diff day %d"),
                              index_name, dt_diff.days)

        except Exception as e:
            LOG.error(_LE("delete es index, catch exception:%s"), str(e))

    def parse_index_size(self, size_str):
        size_f = 0.0
        if "kb" in size_str:
            size_f = float(size_str.replace("kb", "").strip())
            size_f = size_f * 1024
        elif "mb" in size_str:
            size_f = float(size_str.replace("mb", "").strip())
            size_f = size_f * 1024 * 1024
        elif "gb" in size_str:
            size_f = float(size_str.replace("gb", "").strip())
            size_f = size_f * 1024 * 1024 * 1024
        elif "tb" in size_str:
            size_f = float(size_str.replace("tb", "").strip())
            size_f = size_f * 1024 * 1024 * 1024 * 1024
        else:
            pass

        return size_f

    def delete_es_oversize_index(self):
        log_max = self.config_api.get_config("log_max_gb")
        if log_max is None:
            LOG.error(_LE("the config of log_max_gb do not exist"))
            return

        LOG.info(_LI("es indexes(log) max(GB): %s"), log_max)
        log_max_int = float(log_max) * 1024 * 1024 * 1024
        now_log_total = 0
        today = time.strftime('%Y-%m-%d')
        try:
            indexes_array = self.search_lib.get_all_index()
            for index in indexes_array:
                size_str = index["store.size"].lower()
                size_f = self.parse_index_size(size_str)
                now_log_total = now_log_total + size_f

            while now_log_total > log_max_int:
                max_diff_days = -1
                todo_delete_index = None
                for index in indexes_array:
                    index_name = index["index"]
                    index_d = index_name.split('-')[1]
                    size_str = index["store.size"].lower()
                    size_f = self.parse_index_size(size_str)
                    dt_today = datetime.datetime.strptime(today, "%Y-%m-%d")
                    dt_index = datetime.datetime.strptime(index_d, '%Y.%m.%d')
                    dt_diff = dt_today - dt_index
                    if dt_diff.days > max_diff_days:
                        max_diff_days = dt_diff.days
                        todo_delete_index = index_name

                if todo_delete_index:
                    LOG.info(_LI("deleted index %s"), index_name)
                    self.delete_index(todo_delete_index)
                    now_log_total = now_log_total - size_f
        except Exception as e:
            LOG.error(_LE("delete es index, catch exception:%s"), str(e))

    def start_task(self):
        try:
            self.delete_es_outdated_index()
            self.delete_es_oversize_index()
            LOG.info(_LI("delete es index task done"))
        except Exception as e:
            LOG.error(_LE("delete es index task, catch exception:%s"), str(e))
