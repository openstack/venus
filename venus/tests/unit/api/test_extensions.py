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
from venus.api.extensions import ExtensionDescriptor
from venus.api.extensions import ExtensionManager


class TestExtensions(unittest.TestCase):
    def setUp(self):
        self.extension_descriptor = ExtensionDescriptor(ExtensionManager())
        super(TestExtensions, self).setUp()

    def test_get_resources(self):
        result = self.extension_descriptor.get_resources()
        self.assertEqual(result, [])

    def test_get_controller_extensions(self):
        result = self.extension_descriptor.get_controller_extensions()
        self.assertEqual(result, [])
