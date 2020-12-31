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
