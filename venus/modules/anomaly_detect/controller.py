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

"""The template api."""

from venus.api.openstack import wsgi
from venus.modules.anomaly_detect.action import AnomalyDetectCore


class AnomalyDetectController(wsgi.Controller):
    def __init__(self, ext_mgr):
        self.ext_mgr = ext_mgr
        self.api = AnomalyDetectCore()
        super(AnomalyDetectController, self).__init__()

    @wsgi.wrap_check_policy
    def add_rule(self, req, body):
        if len(req.body) == 0:
            return {"code": -1, "msg": "invalid param"}

        title = body.get("title", None)
        if title is None:
            return {"code": -1, "msg": "invalid param: title is missed"}

        desc = body.get("desc", None)
        if desc is None:
            return {"code": -1, "msg": "invalid param: desc is missed"}

        keyword = body.get("keyword", None)
        if keyword is None:
            return {"code": -1, "msg": "invalid param: keyword is missed"}

        log_type = body.get("log_type", None)
        if log_type is None:
            return {"code": -1, "msg": "invalid param: log_type is missed"}

        module = body.get("module", None)
        if module is None:
            return {"code": -1, "msg": "invalid param: module is missed"}

        params = {}
        params["title"] = title
        params["desc"] = desc
        params["keyword"] = keyword
        params["log_type"] = log_type
        params["module"] = module
        self.api.add_rule(params)

        return {"code": 0, "msg": "OK"}

    @wsgi.wrap_check_policy
    def get_rule(self, req, id):
        r = self.api.get_rule(id)
        if r is None:
            return {"code": -1, "msg": "not found"}

        rule = dict()
        rule["id"] = r.id
        rule["title"] = r.title
        rule["desc"] = r.desc
        rule["keyword"] = r.keyword
        rule["log_type"] = r.log_type
        rule["module"] = r.module
        rule["flag"] = r.flag
        rule["create_time"] = r.create_time
        rule["update_time"] = r.update_time
        return {"code": 0, "msg": "OK", "rule": rule}

    @wsgi.wrap_check_policy
    def get_rule_list(self, req):
        params = {}
        params["title"] = req.params.get("title", None)
        params["module"] = req.params.get("module", None)
        params["flag"] = req.params.get("flag", None)
        params["page_num"] = req.params.get("page_num", "1")
        params["page_size"] = req.params.get("page_size", "10")
        res = self.api.get_rule_list(params)
        rules = []
        for r in res:
            rule = dict()
            rule["id"] = r.id
            rule["title"] = r.title
            rule["desc"] = r.desc
            rule["keyword"] = r.keyword
            rule["log_type"] = r.log_type
            rule["module"] = r.module
            rule["flag"] = r.flag
            rule["create_time"] = r.create_time
            rule["update_time"] = r.update_time
            rules.append(rule)

        return {"code": 0, "msg": "OK", "rules": rules}

    @wsgi.wrap_check_policy
    def update_rule(self, req, body, id):
        if len(req.body) == 0:
            return {"code": -1, "msg": "invalid param"}

        params = {}
        params["id"] = id
        params["title"] = body.get("title", None)
        params["desc"] = body.get("desc", None)
        params["keyword"] = body.get("keyword", None)
        params["log_type"] = body.get("log_type", None)
        params["module"] = body.get("module", None)
        params["flag"] = body.get("flag", None)
        rule = self.api.update_rule(params)
        if rule is None:
            return {"code": 0, "msg": "OK"}
        else:
            return {"code": -1, "msg": "no found"}

    @wsgi.wrap_check_policy
    def delete_rule(self, req, id):
        self.api.delete_rule(id)
        return {"code": 0, "msg": "OK"}

    @wsgi.wrap_check_policy
    def get_record_list(self, req):
        params = {}
        params["title"] = req.params.get("title", None)
        params["module"] = req.params.get("module", None)
        params["log_type"] = req.params.get("log_type", None)
        params["start_time"] = req.params.get("start_time", None)
        params["end_time"] = req.params.get("end_time", None)
        params["page_num"] = req.params.get("page_num", "1")
        params["page_size"] = req.params.get("page_size", "10")
        res = self.api.get_record_list(params)

        records = []
        for r in res:
            record = dict()
            record["id"] = r.id
            record["title"] = r.title
            record["desc"] = r.desc
            record["keyword"] = r.keyword
            record["log_type"] = r.log_type
            record["module"] = r.module
            record["logs"] = r.logs
            record["start_time"] = r.create_time
            record["end_time"] = r.create_time
            record["create_time"] = r.create_time
            records.append(record)

        return {"code": 0, "msg": "OK", "records": records}

    @wsgi.wrap_check_policy
    def delete_record(self, req, id):
        self.api.delete_record(id)
        return {"code": 0, "msg": "OK"}


def create_resource(ext_mgr):
    return wsgi.Resource(AnomalyDetectController(ext_mgr))
