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
from venus.common.utils import LOG
from venus.modules.custom_config.action import CustomConfigCore


class CustomConfigController(wsgi.Controller):
    def __init__(self, ext_mgr):
        self.ext_mgr = ext_mgr
        self.config_api = CustomConfigCore()
        super(CustomConfigController, self).__init__()

    @wsgi.wrap_check_policy
    def get_config(self, req):
        result = dict()
        result["log_save_days"] = self.config_api.get_config("log_save_days")
        return result

    @wsgi.wrap_check_policy
    def set_config(self, req, body):
        LOG.debug(req)
        if len(req.body) == 0:
            return {"code": -1, "msg": "invalid param"}
        LOG.debug(body)
        id = body.get("id", None)
        value = body.get("value", None)
        if id is None or value is None:
            return {"code": -1, "msg": "invalid param: id or value is missed"}
        self.config_api.set_config(id, value)
        return {"code": 0, "msg": "OK"}


def create_resource(ext_mgr):
    return wsgi.Resource(CustomConfigController(ext_mgr))
