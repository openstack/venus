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

from pbr import version as pbr_version

VENUS_VENDOR = "OpenStack Foundation"
VENUS_PRODUCT = "OpenStack Venus"
VENUS_PACKAGE = None

loaded = False
version_info = pbr_version.VersionInfo('openstack-venus')
version_string = version_info.version_string
