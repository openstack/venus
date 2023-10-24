# Copyright 2023 Inspur
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
import venus.api.common as api_common


class TestCommon(unittest.TestCase):
    def setUp(self):
        self.common = api_common
        super(TestCommon, self).setUp()

    def test_validate_key_names(self):
        result = self.common.validate_key_names([])
        self.assertEqual(result, True)
        result = self.common.validate_key_names(['Test-1.1', 'Test:1_2'])
        self.assertEqual(result, True)
        result = self.common.validate_key_names(['Test 1'])
        self.assertEqual(result, False)
        result = self.common.validate_key_names(['Test1', 'Test2?'])
        self.assertEqual(result, False)
