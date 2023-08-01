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

from venus.modules.anomaly_detect.backends.sql import AnomalyDetectSql


class AnomalyDetectCore(object):
    def __init__(self):
        self.sql = AnomalyDetectSql()
        super(AnomalyDetectCore, self).__init__()

    def add_rule(self, params):
        res = self.sql.add_rule(params)
        return res

    def get_rule(self, id):
        res = self.sql.get_rule(id)
        return res

    def get_rule_list(self, params):
        res = self.sql.get_rule_list(params)
        return res

    def update_rule(self, params):
        res = self.sql.update_rule(params)
        return res

    def delete_rule(self, id):
        res = self.sql.delete_rule(id)
        return res

    def add_record(self, params):
        res = self.sql.add_record(params)
        return res

    def get_record_list(self, params):
        res = self.sql.get_record_list(params)
        return res

    def delete_record(self, id):
        res = self.sql.delete_record(id)
        return res
