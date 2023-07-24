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
import uuid

from venus.db.api import get_session
from venus.modules.anomaly_detect.backends import models


class AnomalyDetectSql(object):

    def add_rule(self, title, desc, keyword, match_num, module):
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        session = get_session()
        with session.begin():
            rule = models.AnomalyRules(
                id = uuid.uuid4().hex,
                title = title,
                desc = desc,
                keyword = keyword,
                match_num = match_num,
                module = module,
                flag = 1,
                create_time = t,
                update_time = t
            )
            session.add(rule)
