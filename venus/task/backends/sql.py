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

"""Implementation of SQLAlchemy backend."""
import socket
import time

from oslo_db import options
from oslo_log import log as logging

from venus.conf import CONF
from venus.db.common import _create_facade_lazily
from venus.i18n import _LE
from venus.task.backends import models

# abc
CONF.import_group("profiler", "venus.service")
log = logging.getLogger(__name__)
options.set_defaults(CONF, connection='sqlite:///$state_path/venus.sqlite')


def get_session(**kwargs):
    facade = _create_facade_lazily()
    return facade.get_session(**kwargs)


class TaskSql(object):
    def check_task(self, t_name):
        session = get_session()
        with session.begin():
            hostname = socket.gethostname()
            now = time.time()
            tasks = session.query(models.RegitsterTask).filter_by(
                task_name=t_name).with_lockmode('update').all()
            if len(tasks) != 1:
                log.error(_LE("unsupported task type:%s, please check it"),
                          t_name)
                return False

            if tasks[0].update_time is None or (now - time.mktime(
                    time.strptime(str(tasks[0].update_time),
                                  '%Y-%m-%d %H:%M:%S'))) > 600:
                tasks[0].host_name = hostname
                tasks[0].update_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(now))
                res = True
            else:
                if tasks[0].host_name == hostname:
                    tasks[0].update_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                         time.localtime(now))
                    res = True
                else:
                    res = False
            return res
