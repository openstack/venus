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

import datetime
import unittest
from unittest import mock

from venus.modules.search.action import SearchCore


class TestSearchAction(unittest.TestCase):
    def setUp(self):
        self.action = SearchCore()
        super(TestSearchAction, self).setUp()

    def test_get_interval(self):
        want1 = "1s"
        want2 = "1秒"
        want3 = "1second"
        end_time = 100000000
        start_time = end_time - 50
        res1, res2, res3 = self.action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "10s"
        want2 = "10秒"
        want3 = "10seconds"
        start_time = end_time - 500
        res1, res2, res3 = self.action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "30s"
        want2 = "30秒"
        want3 = "30seconds"
        start_time = end_time - 1500
        res1, res2, res3 = self.action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "1m"
        want2 = "1分钟"
        want3 = "1minute"
        start_time = end_time - 50 * 60
        res1, res2, res3 = self.action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "10m"
        want2 = "10分钟"
        want3 = "10minutes"
        start_time = end_time - 500 * 60
        res1, res2, res3 = self.action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "30m"
        want2 = "30分钟"
        want3 = "30minutes"
        start_time = end_time - 1500 * 60
        res1, res2, res3 = self.action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "1h"
        want2 = "1小时"
        want3 = "1hour"
        start_time = end_time - 50 * 3600
        res1, res2, res3 = self.action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "3h"
        want2 = "3小时"
        want3 = "3hours"
        start_time = end_time - 150 * 3600
        res1, res2, res3 = self.action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "6h"
        want2 = "6小时"
        want3 = "6hours"
        start_time = end_time - 300 * 3600
        res1, res2, res3 = self.action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "12h"
        want2 = "12小时"
        want3 = "12hours"
        start_time = end_time - 700 * 3600
        res1, res2, res3 = self.action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "24h"
        want2 = "1天"
        want3 = "1day"
        start_time = end_time - 50 * 86400
        res1, res2, res3 = self.action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

    @mock.patch('venus.common.utils.request_es')
    def test_get_all_index_empty(self, mock_req_es):
        mock_req_es.return_value = (400, '')
        index_names = self.action.get_all_index('test_index')
        self.assertEqual("", index_names)

    @mock.patch('venus.common.utils.request_es')
    def test_get_all_index(self, mock_req_es):
        mock_req_es.return_value = (
            200, '[{"index":"index1"},{"index":"index2"}]')
        index_names = self.action.get_all_index('test_index')
        self.assertEqual(["index1", "index2"], index_names)

    @mock.patch('venus.modules.search.action.SearchCore.get_all_index')
    def test_get_index_names_none(self, mock_get_all_index):
        names = ["test_index-2021.01.03", "test_index-2021.01.04"]
        mock_get_all_index.return_value = names
        end_time = datetime.datetime(2021, 1, 2)
        start_time = datetime.datetime(2021, 1, 1)
        index_names = self.action.get_index_names(
            'test_index', start_time, end_time)
        self.assertIsNone(index_names)

    @mock.patch('venus.modules.search.action.SearchCore.get_all_index')
    def test_get_index_names(self, mock_get_all_index):
        names = ["test_index-2021.01.01", "test_index-2021.01.02"]
        mock_get_all_index.return_value = names
        end_time = datetime.datetime(2021, 1, 2)
        start_time = datetime.datetime(2021, 1, 1)
        index_names = self.action.get_index_names(
            'test_index', start_time, end_time)
        self.assertEqual(",".join(names), index_names)

    def test_params_invalid_param(self):
        result = self.action.params('', '', None)
        expected = {"code": -1, "msg": "invalid param"}
        self.assertEqual(expected, result)
        result = self.action.params('host_name', '', '')
        self.assertEqual(expected, result)

    def test_params_no_index_data(self):
        result = self.action.params('host_name', '', None)
        expected = {'code': 0, 'msg': 'no data, no index'}
        self.assertEqual(expected, result)

    @mock.patch('venus.modules.search.es_template.search_params')
    @mock.patch('venus.modules.search.action.SearchCore.get_index_names')
    @mock.patch('venus.common.utils.request_es')
    def test_params_internal_error(
            self, mock_req_es, mock_get_index_names, mock_search_params):
        mock_get_index_names.return_value = 'flog-2021.01.03,flog-2021.01.04'
        mock_req_es.return_value = (400, {})
        result = self.action.params('host_name', '', None)
        expected = {"code": -1, "msg": "internal error, bad request"}
        self.assertEqual(expected, result)

    @mock.patch('venus.modules.search.es_template.search_params')
    @mock.patch('venus.modules.search.action.SearchCore.get_index_names')
    @mock.patch('venus.common.utils.request_es')
    def test_params_no_aggregations_data(
            self, mock_req_es, mock_get_index_names, mock_search_params):
        mock_get_index_names.return_value = 'flog-2021.01.03,flog-2021.01.04'
        mock_req_es.return_value = (200, '{}')
        result = self.action.params('host_name', '', None)
        expected = {"code": 0, "msg": "no data, no aggregations"}
        self.assertEqual(expected, result)

    @mock.patch('venus.modules.search.es_template.search_params')
    @mock.patch('venus.modules.search.action.SearchCore.get_index_names')
    @mock.patch('venus.common.utils.request_es')
    def test_params_level_type(
            self, mock_req_es, mock_get_index_names, mock_search_params):
        mock_req_es.return_value = (
            200, '{"aggregations": {"search_values": '
                 '{"buckets": [{"key": "val1"}, {"key": "val2"}]}}}')
        mock_get_index_names.return_value = 'flog-2021.01.03,flog-2021.01.04'
        result = self.action.params('level', '', None)
        expected = {'code': 1, 'msg': 'OK',
                    "values": ['VAL1', 'VAL2', 'NO EXIST']}
        self.assertEqual(expected, result)

    @mock.patch('venus.modules.search.es_template.search_params')
    @mock.patch('venus.modules.search.action.SearchCore.get_index_names')
    @mock.patch('venus.common.utils.request_es')
    def test_params_not_level_type(
            self, mock_req_es, mock_get_index_names, mock_search_params):
        mock_req_es.return_value = (
            200, '{"aggregations": {"search_values": '
                 '{"buckets": [{"key": "val1"}, {"key": "val2"}]}}}')
        mock_get_index_names.return_value = 'flog-2021.01.03,flog-2021.01.04'
        result = self.action.params('program_name', '', None)
        expected = {'code': 1, 'msg': 'OK', "values": ['val1', 'val2']}
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
