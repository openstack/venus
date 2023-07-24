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
    def delete_rule(self, req, id):
        self.api.delete_rule(id)
        return {"code": 0, "msg": "OK"}


def create_resource(ext_mgr):
    return wsgi.Resource(AnomalyDetectController(ext_mgr))
