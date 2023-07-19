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


service_opts = [
    cfg.IntOpt('periodic_interval',
               default=1,
               help='Interval, in seconds, between running periodic tasks'),
    cfg.IntOpt('periodic_fuzzy_delay',
               default=1,
               help='Range, in seconds, to randomly delay when starting the'
                    ' periodic task scheduler to reduce stampeding.'
                    ' (Disable by settings to 0)'),
    cfg.StrOpt('osapi_venus_listen',
               default="0.0.0.0",
               help='IP address on which OpenStack Venus API listens'),
    cfg.IntOpt('osapi_venus_listen_port',
               default=8560,
               min=1, max=65535,
               help='Port on which OpenStack Venus API listens'),
    cfg.IntOpt('osapi_venus_workers',
               help='Number of workers for OpenStack Venus API service. '
                    'The default is equal to the number of CPUs available.'), ]


def register_opts(conf):
    conf.register_opts(service_opts)
