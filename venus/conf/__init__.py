# Copyright 2020, Inspur Electronic Information Industry Co.,Ltd.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg
from venus.conf import api
from venus.conf import common
from venus.conf import core
from venus.conf import db
from venus.conf import elasticsearch
from venus.conf import profiler

CONF = cfg.CONF

api.register_opts(CONF)
common.register_opts(CONF)
core.register_opts(CONF)
elasticsearch.register_opts(CONF)
profiler.register_opts(CONF)
db.register_opts(CONF)
