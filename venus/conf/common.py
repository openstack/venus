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

import socket

from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import netutils

from venus.i18n import _


global_opts = [
    cfg.StrOpt('my_ip',
               default=netutils.get_my_ipv4(),
               help='IP address of this host'),
    cfg.StrOpt('venusmanager_topic',
               default='venus-venusmanager',
               help='The topic that venusmanager nodes listen on'),
    cfg.BoolOpt('enable_v1_api',
                default=True,
                help=_("DEPRECATED: Deploy v1 of the Venus API.")),
    cfg.BoolOpt('api_rate_limit',
                default=True,
                help='Enables or disables rate limit of the API.'),
    cfg.ListOpt('osapi_venus_ext_list',
                default=[],
                help='Specify list of extensions to load when using '
                     'osapi_venus_extension option with venus.api.'
                     'contrib.select_extensions'),
    cfg.MultiStrOpt('osapi_venus_extension',
                    default=['venus.api.contrib.standard_extensions'],
                    help='osapi venus extension to load'),
    cfg.StrOpt('venusmanager_manager',
               default='venus.venusmanager.'
                       'manager.VenusmanagerManager',
               help='Full class name for '
                    'the Manager for venusmanager'),
    cfg.StrOpt('host',
               default=socket.gethostname(),
               help='Name of this node.  This can be an opaque '
                    'identifier. It is not necessarily a host '
                    'name, FQDN, or IP address.'),
    cfg.StrOpt('rootwrap_config',
               default='/etc/venus/rootwrap.conf',
               help='Path to the rootwrap configuration file to '
                    'use for running commands as root'),
    cfg.BoolOpt('monkey_patch',
                default=False,
                help='Enable monkey patching'),
    cfg.ListOpt('monkey_patch_modules',
                default=[],
                help='List of modules/decorators to monkey patch'),
    cfg.StrOpt('venusmanager_api_class',
               default='venus.venusmanager.api.API',
               help='The full class name of the '
                    'venusmanager API class to use'),
    cfg.StrOpt('auth_strategy',
               default='keystone',
               choices=['noauth', 'keystone', 'deprecated'],
               help='The strategy to use for auth. Supports '
                    'noauth, keystone, '
                    'and deprecated.'),
    cfg.StrOpt('os_privileged_user_name',
               default=None,
               help='OpenStack privileged account username. Used for '
                    'requests to other services (such as Nova) that '
                    'require an account with special rights.'),
    cfg.StrOpt('os_privileged_user_password',
               default=None,
               help='Password associated with the OpenStack '
                    'privileged account.',
               secret=True),
    cfg.StrOpt('os_privileged_user_project',
               default=None,
               help='Project name associated with the OpenStack '
                    'privileged account.'),
    cfg.StrOpt('os_privileged_user_auth_url',
               default=None,
               help='Auth URL associated with the OpenStack '
                    'privileged account.'),
    cfg.StrOpt('os_region_name',
               default='RegionOne',
               help='os region name'),
    cfg.BoolOpt('tcp_keepalive',
                default=True,
                help="Sets the value of TCP_KEEPALIVE (True/False) for each "
                     "server socket."),
    cfg.IntOpt('tcp_keepidle',
               default=600,
               help="Sets the value of TCP_KEEPIDLE in seconds for each "
                    "server socket. Not supported on OS X."),
    cfg.IntOpt('tcp_keepalive_interval',
               help="Sets the value of TCP_KEEPINTVL in seconds for each "
                    "server socket. Not supported on OS X."),
    cfg.IntOpt('tcp_keepalive_count',
               help="Sets the value of TCP_KEEPCNT for each "
                    "server socket. Not supported on OS X."),
    cfg.StrOpt('ssl_ca_file',
               default=None,
               help="CA certificate file to use to verify "
                    "connecting clients"),
    cfg.StrOpt('ssl_cert_file',
               default=None,
               help="Certificate file to use when starting "
                    "the server securely"),
    cfg.StrOpt('ssl_key_file',
               default=None,
               help="Private key file to use when starting "
                    "the server securely"),
    cfg.IntOpt('max_header_line',
               default=16384,
               help="Maximum line size of message headers to be accepted. "
                    "max_header_line may need to be increased when using "
                    "large tokens (typically those generated by the "
                    "Keystone v3 API with big service catalogs)."),
    cfg.IntOpt('client_socket_timeout', default=900,
               help="Timeout for client connections\' socket operations. "
                    "If an incoming connection is idle for this number of "
                    "seconds it will be closed. A value of \'0\' means "
                    "wait forever."),
    cfg.BoolOpt('wsgi_keep_alive',
                default=True,
                help='If False, closes the client socket connection '
                     'explicitly. Setting it to True to maintain backward '
                     'compatibility. Recommended settings is set it '
                     'to False.'),
    cfg.BoolOpt('fatal_exception_format_errors',
                default=False,
                help='Make exception message format errors fatal.'),
    cfg.StrOpt('venus_internal_project_id',
               default=None,
               help='ID of the project which will be used as the Venus '
                    'internal project.'),
    cfg.StrOpt('venus_internal_user_id',
               default=None,
               help='ID of the user to be used'
                    ' in venusmanager operations as the '
                    'Venus internal project.'),
    cfg.StrOpt('db_driver',
               default='venus.db',
               help='Driver to use for database access'),
    cfg.BoolOpt('use_forwarded_for',
                default=False,
                help='Treat X-Forwarded-For as the canonical remote address. '
                     'Only enable this if you have a sanitizing proxy.'),
    # Default request size is 112k
    cfg.IntOpt('osapi_max_request_body_size',
               default=114688,
               help='Max size for body of a request'),
    cfg.StrOpt('public_endpoint', default=None,
               help="Public URL to use for versions endpoint. The default "
                    "is None, which will use the request's host_url "
                    "attribute to populate the URL base. If Venus is "
                    "operating behind a proxy, you will want to change "
                    "this to represent the proxy's URL."),
    cfg.IntOpt('osapi_max_limit',
               default=1000,
               help='The maximum number of items that a collection '
                    'resource returns in a single response'),
    cfg.StrOpt('osapi_venus_base_URL',
               default=None,
               help='Base URL that will be presented to users in links '
                    'to the OpenStack Venus API',
               deprecated_name='osapi_compute_link_prefix'),
    cfg.StrOpt('task_manager',
               default="venus.manager.Manager",
               help='Btask_manager')
]


def register_opts(conf):
    logging.register_options(conf)
    conf.register_opts(global_opts)
