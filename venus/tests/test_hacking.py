#
# All Rights Reserved.
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

from venus.hacking import checks


class HackingTestCase(unittest.TestCase):
    def test_no_log_warn(self):
        code = """
                  LOG.warn("LOG.warn is deprecated")
               """
        self.assertEqual(1, len(list(checks.no_log_warn(code))))
        code = """
                  LOG.warning("LOG.warn is deprecated")
               """
        self.assertEqual(0, len(list(checks.no_log_warn(code))))

    def test_dict_constructor_with_list_copy(self):
        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "    dict([(i, connect_info[i])"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "    attrs = dict([(k, _from_json(v))"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "        type_names = dict((value, key) for key, value in"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "   dict((value, key) for key, value in"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "foo(param=dict((k, v) for k, v in bar.items()))"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            " dict([[i,i] for i in range(3)])"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "  dd = dict([i,i] for i in range(3))"))))

        self.assertEqual(0, len(list(checks.dict_constructor_with_list_copy(
            "        kwargs = dict(name=test,"))))

        self.assertEqual(0, len(list(checks.dict_constructor_with_list_copy(
            "      self._render_dict(xml, data_el, data.__dict__)"))))

    def test_use_timeutils_utcnow(self):
        file_name = '/tools/tool.py'
        line = 'datetime.now()'
        self.assertEqual(0, len(list(checks.use_timeutils_utcnow(line,
                                                                 file_name))))

        file_name = 'action.py'
        line = 'datetime.now()'
        self.assertEqual(1, len(list(checks.use_timeutils_utcnow(line,
                                                                 file_name))))

        line = 'timeutils.utcnow()'
        self.assertEqual(0, len(list(checks.use_timeutils_utcnow(line,
                                                                 file_name))))

    def test_assert_true_isinstance(self):
        self.assertEqual(1, len(list(checks.assert_true_isinstance(
            "self.assertTrue(isinstance(e, "
            "exception.InvalidContentType))"))))

        self.assertEqual(
            0, len(list(checks.assert_true_isinstance("self.assertTrue()"))))

    def test_no_mutable_default_args(self):
        self.assertEqual(1, len(list(checks.no_mutable_default_args(
            "def get_info_from_bdm(virt_type, bdm, mapping=[])"))))

        self.assertEqual(0, len(list(checks.no_mutable_default_args(
            "defined = []"))))

        self.assertEqual(0, len(list(checks.no_mutable_default_args(
            "defined, undefined = [], {}"))))

    def test_assert_equal_in(self):
        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual(a in b, True)"))), 1)

        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual('str' in 'string', True)"))), 1)

        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual(any(a==1 for a in b), True)"))), 0)

        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual(True, a in b)"))), 1)

        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual(True, 'str' in 'string')"))), 1)

        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual(True, any(a==1 for a in b))"))), 0)

        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual(a in b, False)"))), 1)

        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual('str' in 'string', False)"))), 1)

        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual(any(a==1 for a in b), False)"))), 0)

        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual(False, a in b)"))), 1)

        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual(False, 'str' in 'string')"))), 1)

        self.assertEqual(len(list(checks.assert_equal_in(
            "self.assertEqual(False, any(a==1 for a in b))"))), 0)

    def test_check_explicit_underscore_import(self):
        self.assertEqual(len(list(checks.check_explicit_underscore_import(
            "msg = _('My message')",
            "venus/tests/other_files.py"))), 1)
        self.assertEqual(len(list(checks.check_explicit_underscore_import(
            "from venus.i18n import _",
            "venus/tests/other_files.py"))), 0)
        self.assertEqual(len(list(checks.check_explicit_underscore_import(
            "msg = _('My message')",
            "venus/tests/other_files.py"))), 0)
        self.assertEqual(len(list(checks.check_explicit_underscore_import(
            "from venus.i18n import _",
            "venus/tests/other_files2.py"))), 0)
        self.assertEqual(len(list(checks.check_explicit_underscore_import(
            "msg = _('My message')",
            "venus/tests/other_files2.py"))), 0)
        self.assertEqual(len(list(checks.check_explicit_underscore_import(
            "_ = translations.ugettext",
            "venus/tests/other_files3.py"))), 0)
        self.assertEqual(len(list(checks.check_explicit_underscore_import(
            "msg = _('My message')",
            "venus/tests/other_files3.py"))), 0)

    def test_import_stock_mock(self):
        self.assertEqual(1, len(list(checks.import_stock_mock(
            'import mock'))))
        code = """
                    from unittest import mock
                    import unittest.mock
               """
        self.assertEqual(0, len(list(checks.import_stock_mock(code))))

    def test_no_xrange(self):
        line = 'xrange(10)'
        self.assertEqual(1, len(list(checks.no_xrange(line))))

    def test_assert_equal_not_none(self):
        line = 'assertEqual(A is not None)'
        self.assertEqual(1, len(list(checks.assert_equal_not_none(line))))
