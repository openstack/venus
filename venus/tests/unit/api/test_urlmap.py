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
from venus.api import urlmap


class TestUrlMap(unittest.TestCase):
    def setUp(self):
        self.urlmap = urlmap
        super(TestUrlMap, self).setUp()

    def test_unquote_header_value(self):
        result = self.urlmap.unquote_header_value('')
        self.assertEqual(result, '')
        result = self.urlmap.unquote_header_value('test')
        self.assertEqual(result, 'test')
        result = self.urlmap.unquote_header_value('"test"')
        self.assertEqual(result, 'test')
        result = self.urlmap.unquote_header_value('"test')
        self.assertEqual(result, '"test')
        result = self.urlmap.unquote_header_value('test"')
        self.assertEqual(result, 'test"')
