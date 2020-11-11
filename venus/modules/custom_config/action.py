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

from oslo_config import cfg
from oslo_log import log as logging
from venus.modules.custom_config.backends.sql import CustomConfigSql

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class CustomConfigCore(object):
    def __init__(self):
        self.config_sql = CustomConfigSql()
        super(CustomConfigCore, self).__init__()

    def get_config(self, id):
        res = {}
        res["value"] = self.config_sql.get_config(id)
        return res

    def set_config(self, id, value):
        return self.config_sql.set_config(id, value)
