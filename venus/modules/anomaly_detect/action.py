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

    def add_rule(self, title, desc, keyword, log_type, module):
        res = self.sql.add_rule(title, desc, keyword, log_type, module)
        return res

    def get_rule(self, id):
        res = self.sql.get_rule(id)
        return res

    def get_rule_list(self,
                      title,
                      module,
                      flag,
                      page_num,
                      page_size):
        res = self.sql.get_rule_list(self,
                                     title,
                                     module,
                                     flag,
                                     page_num,
                                     page_size)
        return res

    def update_rule(self, id, title, desc, keyword, log_type, module, flag):
        res = self.sql.update_rule(title,
                                   desc,
                                   keyword,
                                   log_type,
                                   module,
                                   flag)
        return res

    def delete_rule(self, id):
        res = self.sql.delete_rule(id)
        return res
