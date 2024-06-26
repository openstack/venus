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

"""Starter script for Venus API."""

import os
import sys

from oslo_log import log as logging

from venus.conf import CONF
from venus import service
from venus import version


def main():
    CONF(sys.argv[1:], project='venus',
         version=version.version_string())
    logdir = CONF.log_dir
    if logdir:
        is_exists = os.path.exists(logdir)
        if not is_exists:
            os.makedirs(logdir)
    logging.setup(CONF, "venus")

    server = service.WSGIService('osapi_venus')
    launcher = service.get_launcher()
    launcher.launch_service(server, workers=server.workers)
    launcher.wait()


if __name__ == "__main__":
    main()
