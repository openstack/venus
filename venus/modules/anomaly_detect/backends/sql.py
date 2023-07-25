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

    def add_rule(self, title, desc, keyword, log_type, module):
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        session = get_session()
        with session.begin():
            rule = models.AnomalyRules(
                id = uuid.uuid4().hex,
                title = title,
                desc = desc,
                keyword = keyword,
                log_type = log_type,
                module = module,
                flag = 1,
                create_time = t,
                update_time = t
            )
            session.add(rule)

    def get_rule(self, id):
        session = get_session()
        with session.begin():
            rule = session.query(models.AnomalyRules).filter_by(id=id).first()
            return rule

    def get_rule_list(self,
                      title,
                      module,
                      flag,
                      page_num,
                      page_size):
        page_num = int(page_num)
        page_size = int(page_size)
        session = get_session()
        with session.begin():
            query = session.query(models.AnomalyRules)
            if title:
                query = query.filter(models.AnomalyRules.title.like(
                    "%{}%".format(title), escape='|'))
            if module:
                query = query.filter(models.AnomalyRules.module == module)
            if flag:
                query = query.filter(models.AnomalyRules.flag == flag)
            query = query.limit(page_size).offset((page_num - 1) * page_num)
            res = query.all()
            return res

    def update_rule(self, id, title, desc, keyword, log_type, module, flag):
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        session = get_session()
        with session.begin():
            rule = session.query(models.AnomalyRules).filter_by(id=id).first()
            if title:
                rule.title = title
            if desc:
                rule.desc = desc
            if keyword:
                rule.keyword = keyword
            if log_type:
                rule.log_type = log_type
            if module:
                rule.module = module
            if flag:
                rule.flag = int(flag)
            rule.update_time = t

    def delete_rule(self, id):
        session = get_session()
        with session.begin():
            session.query(models.AnomalyRules).filter_by(id=id).delete()
