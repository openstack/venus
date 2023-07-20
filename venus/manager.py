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

"""Base Manager class.

Managers will often provide methods for initial setup of a host or periodic
tasks to a wrapping service.

This module provides Manager, a base class for managers.

"""

from oslo_config import cfg
from oslo_log import log as logging
import oslo_messaging as messaging
from oslo_service import periodic_task

from venus.db import base
from venus import version

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class PeriodicTasks(periodic_task.PeriodicTasks):
    def __init__(self):
        super(PeriodicTasks, self).__init__(CONF)


class Manager(base.Base, PeriodicTasks):
    # Set RPC API version to 1.0 by default.
    RPC_API_VERSION = '1.0'

    target = messaging.Target(version=RPC_API_VERSION)

    def __init__(self, host=None, db_driver=None):
        if not host:
            host = CONF.host
        self.host = host
        self.additional_endpoints = []
        super(Manager, self).__init__(db_driver)

    def periodic_tasks(self, context, raise_on_error=False):
        """Tasks to be run at a periodic interval."""
        return self.run_periodic_tasks(context, raise_on_error=raise_on_error)

    def init_host(self):
        """Handle initialization if this is a standalone service.

        A hook point for services to execute tasks before the services are made
        available (i.e. showing up on RPC and starting to accept RPC calls) to
        other components.  Child classes should override this method.

        """
        pass

    def init_host_with_rpc(self):
        """A hook for service to do jobs after RPC is ready.

        Like init_host(), this method is a hook where services get a chance
        to execute tasks that *need* RPC. Child classes should override
        this method.

        """
        pass

    def service_version(self):
        return version.version_string()

    def service_config(self):
        config = {}
        for key in CONF:
            config[key] = CONF.get(key, None)
        return config

    def is_working(self):
        """Method indicating if service is working correctly.

        This method is supposed to be overriden by subclasses and return if
        manager is working correctly.
        """
        return True

    @periodic_task.periodic_task
    def test_periodictask0(self, context):
        """Ensure that instances are not stuck in build."""
        LOG.info("test_periodictask0")
        LOG.info(context)
