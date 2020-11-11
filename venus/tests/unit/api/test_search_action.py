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

import unittest

from venus.modules.search.action import SearchCore


class TestSearchAction(unittest.TestCase):
    def test_get_interval(self):
        action = SearchCore()

        want1 = "1s"
        want2 = "1秒"
        want3 = "1second"
        end_time = 100000000
        start_time = end_time - 50
        res1, res2, res3 = action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "10s"
        want2 = "10秒"
        want3 = "10seconds"
        start_time = end_time - 500
        res1, res2, res3 = action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "30s"
        want2 = "30秒"
        want3 = "30seconds"
        start_time = end_time - 1500
        res1, res2, res3 = action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "1m"
        want2 = "1分钟"
        want3 = "1minute"
        start_time = end_time - 50 * 60
        res1, res2, res3 = action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "10m"
        want2 = "10分钟"
        want3 = "10minutes"
        start_time = end_time - 500 * 60
        res1, res2, res3 = action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "30m"
        want2 = "30分钟"
        want3 = "30minutes"
        start_time = end_time - 1500 * 60
        res1, res2, res3 = action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "1h"
        want2 = "1小时"
        want3 = "1hour"
        start_time = end_time - 50 * 3600
        res1, res2, res3 = action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "3h"
        want2 = "3小时"
        want3 = "3hours"
        start_time = end_time - 150 * 3600
        res1, res2, res3 = action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "6h"
        want2 = "6小时"
        want3 = "6hours"
        start_time = end_time - 300 * 3600
        res1, res2, res3 = action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "12h"
        want2 = "12小时"
        want3 = "12hours"
        start_time = end_time - 700 * 3600
        res1, res2, res3 = action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)

        want1 = "24h"
        want2 = "1天"
        want3 = "1day"
        start_time = end_time - 50 * 86400
        res1, res2, res3 = action.get_interval(start_time, end_time)
        self.assertEqual(want1, res1)
        self.assertEqual(want2, res2)
        self.assertEqual(want3, res3)


if __name__ == "__main__":
    unittest.main()
