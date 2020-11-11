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

"""
WSGI middleware for OpenStack Venus API.
"""

from oslo_log import log as logging

from venus.api import extensions
import venus.api.openstack
from venus.api.v1 import controller as search
from venus.api import versions
from venus.modules.custom_config import controller as custom_config

LOG = logging.getLogger(__name__)


class APIRouter(venus.api.openstack.APIRouter):
    """Routes requests on the API to the appropriate controller and method."""
    ExtensionManager = extensions.ExtensionManager

    def _setup_routes(self, mapper, ext_mgr):
        # Register resources
        versions_resource = versions.create_resource()
        config_resource = custom_config.create_resource(ext_mgr)
        search_resource = search.create_resource(ext_mgr)

        # Register routers
        mapper.redirect("", "/")

        mapper.connect("versions", "/",
                       controller=versions_resource,
                       action='show')

        mapper.connect("get_custom_config", "/custom_config",
                       controller=config_resource,
                       action='get_config',
                       conditions={'method': ['GET']})

        mapper.connect("get_custom_config", "/custom_config",
                       controller=config_resource,
                       action='set_config',
                       conditions={'method': ['POST']})

        mapper.connect("search_params", "/search/params",
                       controller=search_resource,
                       action='search_params',
                       conditions={'method': ['GET']})

        mapper.connect("search_logs", "/search/logs",
                       controller=search_resource,
                       action='search_logs',
                       conditions={'method': ['GET']})

        mapper.connect("search_analyse_logs", "/search/analyse/logs",
                       controller=search_resource,
                       action='search_analyse_logs',
                       conditions={'method': ['GET']})

        mapper.connect("search_typical_logs", "/search/typical/logs",
                       controller=search_resource,
                       action='search_typical_logs',
                       conditions={'method': ['GET']})

        mapper.connect("instance_call_chain", "/search/instance/callchain",
                       controller=search_resource,
                       action='instance_call_chain',
                       conditions={'method': ['GET']})

        mapper.connect("search_log_by_global_id", "/search/trace_log",
                       controller=search_resource,
                       action='search_global_id',
                       conditions={'method': ['GET']})
