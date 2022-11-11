# Copyright 2022 Inspur
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

import unittest
from unittest import mock

from elasticsearch import Elasticsearch
from venus.api import extensions
from venus.modules.search.controller import SearchController
from venus.tests.unit import fakes


class TestSearchController(unittest.TestCase):
    @mock.patch('elasticsearch.Elasticsearch')
    def setUp(self, mock_es):
        mock_es.return_value = Elasticsearch()
        self.controller = SearchController(extensions.ExtensionManager)
        self.req = fakes.HTTPRequest.blank('')
        super(TestSearchController, self).setUp()

    @mock.patch('venus.modules.search.action.SearchCore.params')
    def test_search_params_invalid_type(self, action_params):
        ret = {"code": -1, "msg": "invalid param"}
        action_params.return_value = ret
        req = fakes.HTTPRequest.blank('?type=test')
        res1 = self.controller.search_params(req)
        self.assertEqual(ret, res1)

    @mock.patch('venus.modules.search.action.SearchCore.params')
    def test_search_params_valid_type(self, action_params):
        ret = {'code': 0, 'msg': 'no data, no index'}
        action_params.return_value = ret
        req = fakes.HTTPRequest.blank('?type=host_name')
        res1 = self.controller.search_params(req)
        self.assertEqual(ret, res1)
