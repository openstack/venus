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

    def add_rule(self, params):
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        session = get_session()
        with session.begin():
            rule = models.AnomalyRules(
                id = uuid.uuid4().hex,
                title = params["title"],
                desc = params["desc"],
                keyword = params["keyword"],
                log_type = params["log_type"],
                module = params["module"],
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

    def get_rule_list(self, params):
        title = params.get("title", None)
        module = params.get("module", None)
        flag = params.get("flag", None)
        log_type = params.get("log_type", None)
        page_num = int(params["page_num"])
        page_size = int(params["page_size"])

        session = get_session()
        with session.begin():
            query = session.query(models.AnomalyRules)
            if title:
                query = query.filter(models.AnomalyRules.title.like(
                    "%{}%".format(title), escape='|'))
            if module:
                query = query.filter(models.AnomalyRules.module == module)
            if flag:
                query = query.filter(models.AnomalyRules.flag == int(flag))
            if log_type:
                query = query.filter(models.AnomalyRules.log_type == log_type)

            query = query.limit(page_size).offset((page_num - 1) * page_size)
            res = query.all()
            return res

    def update_rule(self, params):
        id = params["id"]
        title = params["title"]
        desc = params["desc"]
        keyword = params["keyword"]
        log_type = params["log_type"]
        module = params["module"]
        flag = params["flag"]
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        session = get_session()
        with session.begin():
            rule = session.query(models.AnomalyRules).filter_by(id=id).first()
            if rule is None:
                return "error"
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
            return None

    def delete_rule(self, id):
        session = get_session()
        with session.begin():
            session.query(models.AnomalyRules).filter_by(id=id).delete()

    def add_record(self, params):
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        session = get_session()
        with session.begin():
            rule = models.AnomalyRecords(
                id = uuid.uuid4().hex,
                title = params["title"],
                desc = params["desc"],
                keyword = params["keyword"],
                log_type = params["log_type"],
                module = params["module"],
                logs = params["logs"],
                start_time = params["start_time"],
                end_time = params["end_time"],
                create_time = t,
            )
            session.add(rule)

    def get_record_list(self, params):
        title = params.get("title", None)
        module = params.get("module", None)
        ltype = params.get("log_type", None)
        start_time = params.get("start_time", None)
        end_time = params.get("end_time", None)
        page_num = int(params.get("page_num", "1"))
        page_size = int(params.get("page_size", "10"))

        session = get_session()
        with session.begin():
            query = session.query(models.AnomalyRecords)
            if title:
                query = query.filter(models.AnomalyRecords.title.like(
                    "%{}%".format(title), escape='|'))
            if module:
                query = query.filter(models.AnomalyRecords.module == module)
            if ltype:
                query = query.filter(models.AnomalyRecords.log_type == ltype)
            if start_time:
                lt = time.localtime(int(start_time))
                t = time.strftime('%Y-%m-%d %H:%M:%S', lt)
                query = query.filter(models.AnomalyRecords.create_time >= t)
            if end_time:
                lt = time.localtime(int(end_time))
                t = time.strftime('%Y-%m-%d %H:%M:%S', lt)
                query = query.filter(models.AnomalyRecords.create_time <= t)

            query = query.limit(page_size).offset((page_num - 1) * page_size)
            res = query.all()
            return res

    def delete_record(self, id):
        session = get_session()
        with session.begin():
            session.query(models.AnomalyRecords).filter_by(id=id).delete()
