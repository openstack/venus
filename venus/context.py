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

"""RequestContext: context for requests that persist through all of venus."""

import copy

from oslo_context import context
from oslo_utils import timeutils

from venus.common.utils import LOG
from venus.conf import CONF
from venus.i18n import _, _LW


class RequestContext(context.RequestContext):
    """Security context and request information.

    Represents the user taking a given action within the system.

    """

    def __init__(self, user_id, project_id, is_admin=None, read_deleted="no",
                 roles=None, project_name=None, remote_address=None,
                 timestamp=None, request_id=None, auth_token=None,
                 quota_class=None, service_catalog=None,
                 domain=None, user_domain=None, project_domain=None,
                 **kwargs):
        """Initialize RequestContext.

        :param read_deleted: 'no' indicates deleted records are hidden, 'yes'
            indicates deleted records are visible, 'only' indicates that
            *only* deleted records are visible.

        :param kwargs: Extra arguments that might be present, but we ignore
            because they possibly came in from older rpc messages.
        """

        super(RequestContext, self).__init__(auth_token=auth_token,
                                             user=user_id,
                                             tenant=project_id,
                                             domain=domain,
                                             user_domain=user_domain,
                                             project_domain=project_domain,
                                             is_admin=is_admin,
                                             request_id=request_id)
        self.roles = roles or []
        self.project_name = project_name
        self.read_deleted = read_deleted
        self.remote_address = remote_address
        if not timestamp:
            timestamp = timeutils.utcnow()
        elif isinstance(timestamp, str):
            timestamp = timeutils.parse_isotime(timestamp)
        self.timestamp = timestamp
        self.quota_class = quota_class

        if service_catalog:
            # Only include required parts of service_catalog
            self.service_catalog = [s for s in service_catalog
                                    if s.get('type') in
                                    ('identity', 'compute', 'object-store')]
        else:
            # if list is none
            self.service_catalog = []

        # # We need to have RequestContext attributes defined
        # # when policy.check_is_admin invokes request logging
        # # to make it loggable.
        # if self.is_admin is None:
        #     self.is_admin = policy.check_is_admin(self.roles, self)
        # elif self.is_admin and 'admin' not in self.roles:
        #     self.roles.append('admin')

    def _get_read_deleted(self):
        return self._read_deleted

    def _set_read_deleted(self, read_deleted):
        if read_deleted not in ('no', 'yes', 'only'):
            raise ValueError(_("read_deleted can only be one of 'no', "
                               "'yes' or 'only', not %r") % read_deleted)
        self._read_deleted = read_deleted

    def _del_read_deleted(self):
        del self._read_deleted

    read_deleted = property(_get_read_deleted, _set_read_deleted,
                            _del_read_deleted)

    def to_dict(self):
        result = super(RequestContext, self).to_dict()
        result['user_id'] = self.user_id
        result['project_id'] = self.project_id
        result['project_name'] = self.project_name
        result['domain'] = self.domain
        result['read_deleted'] = self.read_deleted
        result['roles'] = self.roles
        result['remote_address'] = self.remote_address
        result['timestamp'] = self.timestamp.isoformat()
        result['quota_class'] = self.quota_class
        result['service_catalog'] = self.service_catalog
        result['request_id'] = self.request_id
        return result

    @classmethod
    def from_dict(cls, values):
        return cls(**values)

    def elevated(self, read_deleted=None, overwrite=False):
        """Return a version of this context with admin flag set."""
        context = self.deepcopy()
        context.is_admin = True

        if 'admin' not in context.roles:
            context.roles.append('admin')

        if read_deleted is not None:
            context.read_deleted = read_deleted

        return context

    def deepcopy(self):
        return copy.deepcopy(self)

    # NOTE(sirp): the openstack/common version of RequestContext uses
    # tenant/user whereas the Venus version uses project_id/user_id.
    # NOTE(adrienverge): The Venus version of RequestContext now uses
    # tenant/user internally, so it is compatible with context-aware code from
    # openstack/common. We still need this shim for the rest of Venus's
    # code.
    @property
    def project_id(self):
        return self.tenant

    @project_id.setter
    def project_id(self, value):
        self.tenant = value

    @property
    def user_id(self):
        return self.user

    @user_id.setter
    def user_id(self, value):
        self.user = value


def get_admin_context(read_deleted="no"):
    return RequestContext(user_id=None,
                          project_id=None,
                          is_admin=True,
                          read_deleted=read_deleted,
                          overwrite=False)


def get_internal_tenant_context():
    """Build and return the Venus internal tenant context object

    This request context will only work for internal Venus operations. It will
    not be able to make requests to remote services. To do so it will need to
    use the keystone client to get an auth_token.
    """
    project_id = CONF.venus_internal_tenant_project_id
    user_id = CONF.venus_internal_tenant_user_id

    if project_id and user_id:
        return RequestContext(user_id=user_id,
                              project_id=project_id,
                              is_admin=True)
    else:
        LOG.warning(_LW('Unable to get internal tenant context: Missing '
                        'required config parameters.'))
        return None
