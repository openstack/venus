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
from venus.modules.search.action import SearchCore
from venus.modules.search.search_lib import ESSearchObj


class SearchController(wsgi.Controller):
    def __init__(self, ext_mgr):
        self.ext_mgr = ext_mgr
        self.search_api = SearchCore()
        self.search_lib = ESSearchObj()
        super(SearchController, self).__init__()

    @wsgi.wrap_check_policy
    def search_params(self, req):
        type = req.params.get("type")
        module_name = req.params.get("module_name")
        index_type = req.params.get("index_type")
        text = self.search_api.params(type, module_name, index_type)
        return text

    @wsgi.wrap_check_policy
    def search_logs(self, req):
        host_name = req.params.get("host_name")
        module_name = req.params.get("module_name")
        program_name = req.params.get("program_name")
        level = req.params.get("level")
        user_id = req.params.get("user_id")
        project_id = req.params.get("project_id")
        query = req.params.get("query")
        index_type = req.params.get("index_type")
        start_time = req.params.get("start_time")
        end_time = req.params.get("end_time")
        page_num = req.params.get("page_num")
        page_size = req.params.get("page_size")
        text = self.search_api.logs(host_name, module_name, program_name,
                                    level, user_id, project_id, query,
                                    index_type, start_time, end_time,
                                    page_num, page_size)
        return text

    @wsgi.wrap_check_policy
    def search_analyse_logs(self, req):
        group_name = req.params.get("group_name")
        host_name = req.params.get("host_name")
        module_name = req.params.get("module_name")
        program_name = req.params.get("program_name")
        level = req.params.get("level")
        start_time = req.params.get("start_time")
        end_time = req.params.get("end_time")
        text = self.search_api.analyse_logs(group_name, host_name,
                                            module_name, program_name,
                                            level, start_time, end_time)
        return text

    @wsgi.wrap_check_policy
    def search_typical_logs(self, req):
        type = req.params.get("type")
        start_time = req.params.get("start_time")
        end_time = req.params.get("end_time")
        text = self.search_api.typical_logs(type, start_time, end_time)
        return text

    @wsgi.wrap_check_policy
    def instance_call_chain(self, req):
        request_id = req.params.get("request_id")
        uuid = req.params.get("uuid")
        text = self.search_api.instance_call_chain(request_id, uuid)
        return text

    @wsgi.wrap_check_policy
    def search_global_id(self, req):
        global_id = req.params.get("global_id")
        text = self.search_lib.get_global_log(global_id)
        return text


def create_resource(ext_mgr):
    return wsgi.Resource(SearchController(ext_mgr))
