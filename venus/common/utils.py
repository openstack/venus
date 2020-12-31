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

"""Implementation of Utils."""

import json
import urllib3

from oslo_log import log as logging

from venus.i18n import _LE


LOG = logging.getLogger(__name__)


def request_es(url, method, data=None):
    http = urllib3.PoolManager(timeout=30.0)
    try:
        if method in ["GET", "DELETE"]:
            resp = http.request(method, url=url)
        elif method == "POST":
            resp = http.request(method, url=url, body=json.dumps(data))
        else:
            return 0, None

        return resp.status, resp.data.strip()

    except Exception as e:
        LOG.error(_LE("request es, catch exception:%s"), str(e))
        return 0, None
