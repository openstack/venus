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
from venus.modules.search.search_lib import ESSearchObj
from venus.i18n import _LE, _LI


TASK_NAME = "delete_es_index"


class DeleteESIndexTask(object):
    """delete es index task."""

    def __init__(self):
        self.elasticsearch_url = CONF.elasticsearch.url
        self.search_lib = ESSearchObj()

    def delete_index(self, name):
        url = self.elasticsearch_url + '/' + name
        status, text = utils.request_es(url, "DELETE")
        if status != 200:
            LOG.error(_LE("failed to delete es index"))
            return

    def delete_es_history_index(self):
        len_d = CONF.elasticsearch.es_index_days
        LOG.info("the elasticsearch indexes keep days {}".format(len_d))
        if len_d is None:
            LOG.error(_LE("es_index_length no exist"))
            return
        today = time.strftime('%Y-%m-%d')
        indexes_array = self.search_lib.get_all_index()
        for index in indexes_array:
            try:
                index_name = index["index"]
                index_day = index_name.split('-')[1]
                diff_day = datetime.datetime.strptime(today, "%Y-%m-%d") - \
                    datetime.datetime.strptime(index_day, '%Y.%m.%d')
                if diff_day.days >= int(len_d):
                    LOG.info("delete index {}, diff_day {}"
                             .format(index_name, diff_day))
                    self.delete_index(index_name)
            except Exception as e:
                LOG.error("delete index {} error:{}".format(
                    index["index"], str(e)))

    def start_task(self):
        try:

            if CONF.elasticsearch.url == "":
                LOG.info(_LI("not deploy es and not need execute"))
                return

            try:
                self.delete_es_history_index()
            except Exception as e:
                LOG.error(_LE("delete es index, catch exception:%s"),
                          str(e))
            LOG.info(_LI("delete es index task done"))
        except Exception as e:
            LOG.error(_LE("delete es index task, catch exception:%s"),
                      str(e))
