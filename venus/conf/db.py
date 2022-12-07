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
from oslo_db import options

db_driver_opt = cfg.StrOpt('db_driver',
                           default='venus.db',
                           help='Driver to use for database access')


def register_opts(conf):
    options.set_defaults(conf, connection='sqlite:///$state_path/venus.sqlite')
    conf.register_opt(db_driver_opt)
