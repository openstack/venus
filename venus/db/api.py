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


from oslo_db.sqlalchemy import enginefacade
from oslo_log import log as logging
from venus.conf import CONF


_facade = None
db_context = enginefacade.transaction_context()
LOG = logging.getLogger(__name__)


def get_facade():
    global _facade
    if _facade is None:

        # FIXME: get_facade() is called by the test suite startup,
        # but will not be called normally for API calls.
        # osprofiler / oslo_db / enginefacade currently don't have hooks
        # to talk to each other, however one needs to be added to oslo.db
        # to allow access to the Engine once constructed.
        db_context.configure(**CONF.database)
        _facade = db_context.get_legacy_facade()

    return _facade


def get_engine():
    return get_facade().get_engine()


def get_session():
    return get_facade().get_session()
