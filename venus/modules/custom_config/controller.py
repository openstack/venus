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
from venus.conf import CONF


class CustomConfigController(wsgi.Controller):
    def __init__(self, ext_mgr):
        self.ext_mgr = ext_mgr
        super(CustomConfigController, self).__init__()

    @wsgi.wrap_check_policy
    def get_config(self, req):
        result = dict()
        result["log_save_days"] = CONF.elasticsearch.es_index_days
        return result


def create_resource(ext_mgr):
    return wsgi.Resource(CustomConfigController(ext_mgr))
