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

import sqlalchemy

import threading

import time

from oslo_config import cfg

from oslo_db import options

from oslo_db.sqlalchemy import session as db_session

from oslo_log import log as logging

import osprofiler.sqlalchemy

from venus.modules.custom_config.backends import models


CONF = cfg.CONF
CONF.import_group("profiler", "venus.service")
log = logging.getLogger(__name__)
options.set_defaults(CONF, connection='sqlite:///$state_path/venus.sqlite')

_LOCK = threading.Lock()
_FACADE = None


def _create_facade_lazily():
    global _LOCK
    with _LOCK:
        global _FACADE
        if _FACADE is None:
            _FACADE = db_session.EngineFacade(
                CONF.database.connection,
                **dict(CONF.database)
            )

            if CONF.profiler.profiler_enabled:
                if CONF.profiler.trace_sqlalchemy:
                    osprofiler.sqlalchemy.add_tracing(sqlalchemy,
                                                      _FACADE.get_engine(),
                                                      "db")

        return _FACADE


def get_session(**kwargs):
    facade = _create_facade_lazily()
    return facade.get_session(**kwargs)


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
