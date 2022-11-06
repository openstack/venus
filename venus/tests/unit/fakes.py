# Copyright 2022 Inspur
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from venus.api.openstack import wsgi as os_wsgi
from venus import context


FAKE_UUID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
FAKE_PROJECT_ID = '6a6a9c9eee154e9cb8cec487b98d36ab'
FAKE_USER_ID = '5fae60f5cf4642609ddd31f71748beac'


class FakeRequestContext(context.RequestContext):
    def __init__(self, *args, **kwargs):
        kwargs['auth_token'] = kwargs.get('auth_token', 'fake_auth_token')
        super(FakeRequestContext, self).__init__(*args, **kwargs)


class HTTPRequest(os_wsgi.Request):

    @classmethod
    def blank(cls, *args, **kwargs):
        defaults = {'base_url': 'http://localhost/v2'}
        use_admin_context = kwargs.pop('use_admin_context', False)
        project_id = kwargs.pop('project_id', FAKE_PROJECT_ID)
        defaults.update(kwargs)
        out = super(HTTPRequest, cls).blank(*args, **defaults)
        out.environ['venus.context'] = FakeRequestContext(
            user_id='fake_user',
            project_domain_id=project_id,
            project_id=project_id,
            is_admin=use_admin_context)
        return out
