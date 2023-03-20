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
from http import client

import webob.dec

import webob.exc

from venus.common.utils import LOG

from venus import exception

from venus.wsgi import common as base_wsgi

from oslo_serialization import jsonutils

import functools


JSON_ENCODE_CONTENT_TYPES = {'application/json', 'application/json-home'}


def middleware_exceptions(method):
    @functools.wraps(method)
    def _inner(self, request):
        try:
            return method(self, request)
        except Exception as e:
            LOG.exception(str(e))
            return render_exception(e,
                                    request=request)

    return _inner


class ForwardUnionFilter(base_wsgi.Middleware):
    def process_request(self, req):
        if req.headers.get('FORWARD_UNION') == 'ALL':
            return self.union(req)
        else:
            return self.forward(req)

    @webob.dec.wsgify(RequestClass=base_wsgi.Request)
    @middleware_exceptions
    def __call__(self, req):
        forward_union = req.headers.get('FORWARD_UNION')
        if forward_union is None or forward_union == '':
            response = req.get_response(self.application)
            return self.process_response(response)

        else:
            response = self.process_request(req)
            return response

    def forward(self, req):
        return None

    def union(self, req):
        return None


def render_exception(error, context=None, request=None, user_locale=None):

    if hasattr(error, 'code'):
        if error.code is None or error.code == '':
            error = exception.VenusException
    else:
        if '401' in str(error):
            error = exception.AuthFail
        else:
            error = exception.VenusException

    body = {'error': {
        'code': error.code,
        'title': client.responses[error.code],
        'message': error.message,
    }}

    headers = []

    return render_response(
        status=(error.code, client.responses[error.code]),
        body=body,
        headers=headers)


def render_response(body=None, status=None, headers=None, method=None):
    if headers is None:
        headers = []
    else:
        headers = list(headers)
    headers.append(('Vary', 'X-Auth-Token'))

    if body is None:
        body = b''
        status = status or (client.NO_CONTENT,
                            client.responses[client.NO_CONTENT])
    else:
        content_types = [v for h, v in headers if h == 'Content-Type']
        if content_types:
            content_type = content_types[0]
        else:
            content_type = None

        if content_type is None or content_type in JSON_ENCODE_CONTENT_TYPES:
            body = jsonutils.dump_as_bytes(body, cls=SmarterEncoder)
            if content_type is None:
                headers.append(('Content-Type', 'application/json'))
        status = status or (client.OK, client.responses[client.OK])

    def _convert_to_str(headers):
        str_headers = []
        for header in headers:
            str_header = []
            for value in header:
                if not isinstance(value, str):
                    str_header.append(str(value))
                else:
                    str_header.append(value)
            # convert the list to the immutable tuple to build the headers.
            # header's key/value will be guaranteed to be str type.
            str_headers.append(tuple(str_header))
        return str_headers

    headers = _convert_to_str(headers)

    resp = webob.Response(body=body,
                          status='%s' % status,
                          headerlist=headers)

    if method and method.upper() == 'HEAD':

        stored_headers = resp.headers.copy()
        resp.body = b''
        for header, value in stored_headers.items():
            resp.headers[header] = value

    return resp


class SmarterEncoder(jsonutils.json.JSONEncoder):
    """Help for JSON encoding dict-like objects."""

    def default(self, obj):
        if not isinstance(obj, dict) and hasattr(obj, 'iteritems'):
            return dict(obj.iteritems())
        return super(SmarterEncoder, self).default(obj)
