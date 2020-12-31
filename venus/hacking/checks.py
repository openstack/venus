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

import re

from hacking import core

"""
Guidelines for writing new hacking checks

 - Use only for Magnum specific tests. OpenStack general tests
   should be submitted to the common 'hacking' module.
 - Pick numbers in the range M3xx. Find the current test with
   the highest allocated number and then pick the next value.
   If nova has an N3xx code for that test, use the same number.
 - Keep the test method code in the source file ordered based
   on the M3xx value.
 - List the new rule in the top level HACKING.rst file
 - Add test cases for each new rule to magnum/tests/unit/test_hacking.py

"""
UNDERSCORE_IMPORT_FILES = []

mutable_default_args = re.compile(r"^\s*def .+\((.+=\{\}|.+=\[\])")
assert_equal_in_end_with_true_or_false_re = re.compile(
    r"assertEqual\((\w|[][.'\"])+ in (\w|[][.'\", ])+, (True|False)\)")
assert_equal_in_start_with_true_or_false_re = re.compile(
    r"assertEqual\((True|False), (\w|[][.'\"])+ in (\w|[][.'\", ])+\)")
assert_equal_with_is_not_none_re = re.compile(
    r"assertEqual\(.*?\s+is+\s+not+\s+None\)$")
assert_true_isinstance_re = re.compile(
    r"(.)*assertTrue\(isinstance\((\w|\.|\'|\"|\[|\])+, "
    r"(\w|\.|\'|\"|\[|\])+\)\)")
dict_constructor_with_list_copy_re = re.compile(r".*\bdict\((\[)?(\(|\[)")
assert_xrange_re = re.compile(
    r"\s*xrange\s*\(")
log_translation = re.compile(
    r"(.)*LOG\.(audit|error|critical)\(\s*('|\")")
log_translation_info = re.compile(
    r"(.)*LOG\.(info)\(\s*(_\(|'|\")")
log_translation_exception = re.compile(
    r"(.)*LOG\.(exception)\(\s*(_\(|'|\")")
log_translation_LW = re.compile(
    r"(.)*LOG\.(warning|warn)\(\s*(_\(|'|\")")
custom_underscore_check = re.compile(r"(.)*_\s*=\s*(.)*")
underscore_import_check = re.compile(r"(.)*import _(.)*")
translated_log = re.compile(
    r"(.)*LOG\.(audit|error|info|critical|exception)"
    r"\(\s*_\(\s*('|\")")
string_translation = re.compile(r"[^_]*_\(\s*('|\")")

msg = {
    302: "M302: assertEqual(A is not None) sentences not allowed.",
    310: "M310: timeutils.utcnow() must be used instead of datetime.%s()",
    316: "M316: assertTrue(isinstance(a, b)) sentences not allowed",
    322: "M322: Method's default argument shouldn't be mutable!",
    336: "M336: Must use a dict comprehension instead of a dict "
         "constructor with a sequence of key-value pairs.",
    338: "M338: Use assertIn/NotIn(A, B) rather than "
         "assertEqual(A in B, True/False) when checking "
         "collection contents.",
    339: "M339: Do not use xrange().",
    340: "M340: Found use of _() without explicit import of _ !",
    352: "M352: LOG.warn is deprecated, please use LOG.warning!",
    366: "N366: You must explicitly import python's mock: "
         "``from unittest import mock``"
}


@core.flake8ext
def no_mutable_default_args(logical_line):
    if mutable_default_args.match(logical_line):
        yield 0, msg.get(322)


@core.flake8ext
def assert_equal_not_none(logical_line):
    """Check for assertEqual(A is not None) sentences M302"""
    res = assert_equal_with_is_not_none_re.search(logical_line)
    if res:
        yield 0, msg.get(302)


@core.flake8ext
def assert_true_isinstance(logical_line):
    """Check for assertTrue(isinstance(a, b)) sentences

    M316
    """
    if assert_true_isinstance_re.match(logical_line):
        yield 0, msg.get(316)


@core.flake8ext
def assert_equal_in(logical_line):
    """Check for assertEqual(True|False, A in B), assertEqual(A in B, True|False)

    M338
    """
    res = (assert_equal_in_start_with_true_or_false_re.search(logical_line) or
           assert_equal_in_end_with_true_or_false_re.search(logical_line))
    if res:
        yield 0, msg.get(338)


@core.flake8ext
def no_xrange(logical_line):
    """Disallow 'xrange()'

    M339
    """
    if assert_xrange_re.match(logical_line):
        yield 0, msg.get(339)


@core.flake8ext
def use_timeutils_utcnow(logical_line, filename):
    # tools are OK to use the standard datetime module
    if "/tools/" in filename:
        return

    datetime_funcs = ['now', 'utcnow']
    for f in datetime_funcs:
        pos = logical_line.find('datetime.%s' % f)
        if pos != -1:
            yield pos, msg.get(310) % f


@core.flake8ext
def dict_constructor_with_list_copy(logical_line):
    if dict_constructor_with_list_copy_re.match(logical_line):
        yield 0, msg.get(336)


@core.flake8ext
def no_log_warn(logical_line):
    """Disallow 'LOG.warn('

    Deprecated LOG.warn(), instead use LOG.warning
    https://bugs.launchpad.net/magnum/+bug/1508442

    M352
    """

    if "LOG.warn(" in logical_line:
        yield 0, msg.get(352)


@core.flake8ext
def check_explicit_underscore_import(logical_line, filename):
    """Check for explicit import of the _ function

    We need to ensure that any files that are using the _() function
    to translate logs are explicitly importing the _ function.  We
    can't trust unit test to catch whether the import has been
    added so we need to check for it here.
    """

    # Build a list of the files that have _ imported.  No further
    # checking needed once it is found.
    if filename in UNDERSCORE_IMPORT_FILES:
        pass
    elif (underscore_import_check.match(logical_line) or
          custom_underscore_check.match(logical_line)):
        UNDERSCORE_IMPORT_FILES.append(filename)
    elif (translated_log.match(logical_line) or
          string_translation.match(logical_line)):
        yield 0, msg.get(340)


@core.flake8ext
def import_stock_mock(logical_line):
    """Use python's mock, not the mock library.

    Since we `dropped support for python 2`__, we no longer need to use the
    mock library, which existed to backport py3 functionality into py2.
    Which must be done by saying::

        from unittest import mock

    ...because if you say::

        import mock

    ...you definitely will not be getting the standard library mock. That will
    always import the third party mock library. This check can be removed in
    the future (and we can start saying ``import mock`` again) if we manage to
    purge these transitive dependencies.

    .. __: https://review.opendev.org/#/c/688593/

    N366
    """
    if logical_line == 'import mock':
        yield 0, msg.get(366)
