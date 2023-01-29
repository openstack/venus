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
    """delete es index task."""

    def __init__(self):
        self.elasticsearch_url = CONF.elasticsearch.url
        self.config_api = CustomConfigCore()
        self.search_lib = ESSearchObj()

    def delete_index(self, name):
        url = self.elasticsearch_url + '/' + name
        status, text = utils.request_es(url, "DELETE")
        if status != 200:
            LOG.error(_LE("failed to delete es index"))
            return

    def delete_es_history_index(self):
        len_d = self.config_api.get_config("es_index_length")
        if len_d is None:
            LOG.error(_LE("es_index_length no exist"))
            return
        LOG.info("the elasticsearch indexes keep days {}".format(len_d))
        today = time.strftime('%Y-%m-%d')
        try:
            indexes_array = self.search_lib.get_all_index()
            for index in indexes_array:
                index_name = index["index"]

                index_day = index_name.split('-')[1]
                today_start = datetime.datetime.strptime(today, "%Y-%m-%d")
                index_start = datetime.datetime.strptime(index_day, '%Y.%m.%d')
                diff_day = today_start - index_start
                if diff_day.days >= int(len_d):
                    LOG.info("delete index {}, diff_day {}"
                             .format(index_name, diff_day))
                    self.delete_index(index_name)
                else:
                    LOG.info("no delete index {}, diff_day {}"
                             .format(index_name, diff_day))

        except Exception as e:
            LOG.error("try delete es inidex error" + str(e))

    def start_task(self):
        try:
            self.delete_es_history_index()
            LOG.info(_LI("delete es index task done"))
        except Exception as e:
            LOG.error(_LE("delete es index task, catch exception:%s"),
                      str(e))
