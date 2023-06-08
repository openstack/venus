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

import time

from venus.db.api import get_session
from venus.modules.custom_config.backends import models


class CustomConfigSql(object):

    def get_config(self, id):
        session = get_session()
        with session.begin():
            config = session.query(models.CustomConfig).filter_by(
                id=id).first()
            if config is None:
                return None
            else:
                return config.value

    def set_config(self, id, value):
        session = get_session()
        with session.begin():
            config = session.query(models.CustomConfig).filter_by(
                id=id).first()
            if config is None:
                s_instance = models.CustomConfig(
                    id=id,
                    value=value,
                    update_time=time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.localtime(time.time())))

                session.add(s_instance)
            else:
                config.value = value
                config.update_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                   time.localtime(time.time()))
