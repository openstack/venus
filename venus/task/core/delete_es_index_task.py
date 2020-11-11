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
import six
import time

from oslo_config import cfg
from oslo_log import log as logging

from venus.common import utils
from venus.modules.custom_config.backends.sql import CustomConfigSql
from venus.i18n import _LE, _LI
from venus.task.backends.sql import TaskSql

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

"""
config the elasticsearch info
from /etc/venus/venus.conf
if not exists ,default
"""
elasticsearch_group = cfg.OptGroup(name='elasticsearch',
                                   title='elasticsearch')

elasticsearch_opts = [
    cfg.StrOpt('url',
               default='',
               help='the es url'),
    cfg.StrOpt('username',
               default='',
               help='the es username'),
    cfg.StrOpt('password',
               default='',
               help='the es password')
]
CONF.register_group(elasticsearch_group)
CONF.register_opts(elasticsearch_opts, elasticsearch_group)

TASK_NAME = "delete_es_index"


class DeleteESIndexTask(object):
    """delete es index task."""

    def __init__(self):
        self.elasticsearch_url = CONF.elasticsearch.url
        self.custom_sql = CustomConfigSql()
        self.task_sql = TaskSql()

    def delete_index(self, name):
        url = self.elasticsearch_url + '/' + name
        status, text = utils.request_es(url, "DELETE")
        if status != 200:
            LOG.error(_LE("failed to delete es index"))
            return

    def delete_es_history_index(self):
        len_d = self.custom_sql.get_config("es_index_length")
        if len_d is None:
            LOG.error(_LE("es_index_length no exist"))
            return

        today = time.strftime('%Y-%m-%d')
        url = self.elasticsearch_url + '/_cat/indices/*log-*'
        status, indexes = utils.request_es(url, "GET")
        if status != 200:
            LOG.error(_LE("failed to get es indexes"))
            return
        indexes_array = indexes.split('\n')
        for index in indexes_array:
            index_name = index.split(' ')[2]
            index_day = index_name.split('-')[1]
            diff_day = datetime.datetime.strptime(today, "%Y-%m-%d") - \
                datetime.datetime.strptime(index_day, '%Y.%m.%d')
            if diff_day.days >= int(len_d):
                self.delete_index(index_name)

    def start_task(self):
        try:
            LOG.info(_LI("delete es index task started"))
            ret = self.task_sql.check_task(TASK_NAME)
            if ret is not True:
                LOG.info(_LI("delete es index task not need execute"))
                return

            if CONF.elasticsearch.url == "":
                LOG.info(_LI("not deploy es and not need execute"))
                return

            try:
                self.delete_es_history_index()
            except Exception as e:
                LOG.error(_LE("delete es index, catch exception:%s"),
                          six.text_type(e))
            LOG.info(_LI("delete es index task done"))
        except Exception as e:
            LOG.error(_LE("delete es index task, catch exception:%s"),
                      six.text_type(e))
