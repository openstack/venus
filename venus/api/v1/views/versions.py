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

import copy
import os

from venus.conf import CONF


def get_view_builder(req):
    base_url = CONF.public_endpoint or req.application_url
    return ViewBuilder(base_url)


class ViewBuilder(object):
    def __init__(self, base_url):
        """Initialize ViewBuilder.

        :param base_url: url of the root wsgi application
        """
        self.base_url = base_url

    def build_choices(self, versions, req):
        version_objs = []
        for version in versions:
            version = versions[version]
            version_objs.append({
                "id": version['id'],
                "status": version['status'],
                "links": [{"rel": "self",
                           "href": self.generate_href(version['id'],
                                                      req.path), }, ],
                "media-types": version['media-types'], })

        return dict(choices=version_objs)

    def build_versions(self, versions):
        version_objs = []
        for version in sorted(versions.keys()):
            version = versions[version]
            version_objs.append({
                "id": version['id'],
                "status": version['status'],
                "updated": version['updated'],
                "links": self._build_links(version), })

        return dict(versions=version_objs)

    def build_version(self, version):
        reval = copy.deepcopy(version)
        reval['links'].insert(0, {
            "rel": "self",
            "href": self.base_url.rstrip('/') + '/', })
        return dict(version=reval)

    def _build_links(self, version_data):
        """Generate a container of links that refer to the provided version."""
        href = self.generate_href(version_data['id'])

        links = [{'rel': 'self',
                  'href': href, }, ]

        return links

    def generate_href(self, version, path=None):
        """Create an url that refers to a specific version_number."""
        if version.find('v1.') == 0:
            version_number = 'v1'
        else:
            raise Exception("Error version of %s" % version)

        if path:
            path = path.strip('/')
            return os.path.join(self.base_url, version_number, path)
        else:
            return os.path.join(self.base_url, version_number) + '/'
