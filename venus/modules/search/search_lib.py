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


from datetime import datetime
from elasticsearch import Elasticsearch
import re
from urllib.parse import urlparse

from venus.common.utils import LOG
from venus.conf import CONF


class ESSearchObj(object):

    def __init__(self):
        url = urlparse(CONF.elasticsearch.url)
        self.es = Elasticsearch([url.hostname],
                                http_auth=(CONF.elasticsearch.username,
                                           CONF.elasticsearch.password),
                                port=url.port)

    def get_all_index(self):
        indices = self.es.cat.indices(format="json")
        return indices

    def _create_index(self, index_name):
        all_index = self.get_all_index()
        exist = False
        for index in all_index:
            if index.index == index_name:
                exist = True
                break
        result = None
        if not exist:
            result = self.es.indices.create(index_name)

        return result

    def _get_index_info(self, index):
        pass

    def get_global_log(self, global_id):
        id_format = (r'^req-[a-f0-9]{8}-[a-f0-9]{4}-'
                     r'[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$')

        if not re.match(id_format, global_id):
            return {"error": "the request param is not correct"}

        doc = {
            "query": {
                "term": {
                    "global_id.keyword": global_id
                }
            },
            "size": 10000,
        }
        result = self.es.search(index="flog*", body=doc)
        log_list = self.parse_result(result)
        # self.sort_result_by_time(log_list)

        data = {}
        data["log_size"] = len(log_list)
        data["global_id"] = global_id
        data["analysis"] = log_list

        return data

    def analysis_log(self, log_list):
        data = {}
        for log in log_list:
            logger = log["Logger"]
            if logger in data:
                pass
            else:
                data[logger] = {}

        for log in log_list:
            programname = log["programname"]
            logger = log["Logger"]
            hostname = log["Hostname"]
            loglevel = log["log_level"]
            if programname not in data[logger]:
                data[logger][programname] = {}
                data[logger][programname]["log_list"] = []
                data[logger][programname]["log_list"].append(log)
                data[logger][programname]["host"] = []

                if hostname not in data[logger][programname]["host"]:
                    data[logger][programname]["host"].append(hostname)

                data[logger][programname]["start_time"] = log["timeutc"]
                data[logger][programname]["end_time"] = log["timeutc"]

                data[logger][programname]["log_total"] = 1
                data[logger][programname]["log_error"] = 0

                if self.get_log_level(loglevel) > 0:
                    data[logger][programname]["log_error"] = 1
            else:
                data[logger][programname]["log_list"].append(log)

                if hostname not in data[logger][programname]["host"]:
                    data[logger][programname]["host"].append(hostname)

                data[logger][programname]["end_time"] = log["timeutc"]

                data[logger][programname][
                    "log_total"] = data[logger][programname]["log_total"] + 1

                if self.get_log_level(loglevel) > 0:
                    data[logger][programname]["log_error"] = data[
                        logger][programname]["log_error"] + 1

        return self.sort_deal_data(data)

    def get_log_level(self, log_level):

        log_levels = {"trace": -10,
                      "notset": -8,
                      "debug": -8,
                      "warning": -3,
                      "info": 0,
                      "error": 10,
                      "fatal": 12,
                      "critical": 15}
        if log_level.lower() in log_levels.keys():
            return log_levels[log_level.lower()]
        else:
            LOG.waring("can't find the log level %S", log_level)
            return -1

    def sort_result_by_time(self, log_list):
        for log in log_list:
            log_time = log["Timestamp"].encode("utf-8")
            datetime_obj = datetime.strptime(log_time, "%Y-%m-%d %H:%M:%S.%f")
            log["timeutc"] = datetime_obj

        log_list.sort(key=lambda logcontent: logcontent['timeutc'])

    def parse_result(self, result):
        logs = []
        for log in result["hits"]["hits"]:
            logs.append(log["_source"])
        return logs

    def sort_deal_data(self, data):

        for part in data:
            model_list = []
            for model in data.get(part):
                data.get(part).get(model)["model_name"] = model
                model_list.append(data.get(part).get(model))
                data[part][model] = None
            model_list.sort(key=lambda model: model['start_time'])
            data[part]['model_list'] = model_list
            data[part]['start_time'] = model_list[0]['start_time']
        new_data = {}
        part_list = []
        for part in data:
            data.get(part)["part_name"] = part
            part_list.append(data.get(part))
        part_list.sort(key=lambda part: part['start_time'])
        new_data["part_list"] = part_list

        return new_data
