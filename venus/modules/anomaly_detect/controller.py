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

        match_num = body.get("match_num", None)
        if match_num is None:
            return {"code": -1, "msg": "invalid param: match_num is missed"}

        module = body.get("module", None)
        if module is None:
            return {"code": -1, "msg": "invalid param: module is missed"}

        self.api.add_rule(title, desc, keyword, match_num, module)
        return {"code": 0, "msg": "OK"}

    @wsgi.wrap_check_policy
    def get_rule(self, req, id):
        r = self.api.get_rule(id)
        if r is None:
            return {"code": -1, "msg": "not found"}

        rule = dict()
        rule["title"] = r.title
        rule["desc"] = r.desc
        rule["keyword"] = r.keyword
        rule["match_num"] = r.match_num
        rule["module"] = r.module
        rule["create_time"] = r.create_time
        rule["update_time"] = r.update_time
        return {"code": 0, "msg": "OK", "rule": rule}

    @wsgi.wrap_check_policy
    def update_rule(self, req, body, id):
        if len(req.body) == 0:
            return {"code": -1, "msg": "invalid param"}

        title = body.get("title", None)
        desc = body.get("desc", None)
        keyword = body.get("keyword", None)
        match_num = body.get("match_num", None)
        module = body.get("module", None)
        flag = body.get("module", None)

        self.api.update_rule(id,
                             title,
                             desc,
                             keyword,
                             match_num,
                             module,
                             flag)
        return {"code": 0, "msg": "OK"}

    @wsgi.wrap_check_policy
    def delete_rule(self, req, id):
        self.api.delete_rule(id)
        return {"code": 0, "msg": "OK"}


def create_resource(ext_mgr):
    return wsgi.Resource(AnomalyDetectController(ext_mgr))
