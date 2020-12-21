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

from oslo_config import cfg


core_opts = [
    cfg.StrOpt('api_paste_config',
               default="api-paste.ini",
               help='File name for the paste.'
                    'deploy config for venus-api'),
    cfg.StrOpt('state_path',
               default='/var/lib/venus',
               deprecated_name='pybasedir',
               help="Top-level directory for "
                    "maintaining venus's state"),
]


def register_opts(conf):
    conf.register_cli_opts(core_opts)
