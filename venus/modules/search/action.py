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

import datetime
import json
import time

from oslo_utils import timeutils

from venus.common import utils
from venus.conf import CONF
from venus.modules.search import es_template


class SearchCore(object):
    def __init__(self):
        self.elasticsearch_url = CONF.elasticsearch.url
        self.flog_index_prefix = "flog"
        self.slog_index_prefix = "slog"
        super(SearchCore, self).__init__()

    def get_all_index(self, index_prefix):
        url = self.elasticsearch_url + '/_cat/indices/' + \
            index_prefix + '-*?format=json'
        index_names = []
        status, indexes = utils.request_es(url, 'GET')
        if status != 200:
            utils.LOG.error("failed to get all es indexes")
            return ""
        indexes_array = json.loads(indexes)
        for index in indexes_array:
            index_name = index["index"]
            index_names.append(index_name)

        return index_names

    def get_index_names(self, index_prefix, start_time, end_time):
        start_time, end_time = start_time.date(), end_time.date()
        exist_index_names = self.get_all_index(index_prefix)
        names = []
        t = start_time
        while t <= end_time:
            name = index_prefix + "-" + t.strftime('%Y.%m.%d')
            if name in exist_index_names:
                names.append(name)
            t = t + datetime.timedelta(days=1)
        if len(names) == 0:
            return None

        index_names = ",".join(names)
        return index_names

    def get_interval(self, start_time, end_time):
        diff = end_time - start_time
        per_diff = diff / 60
        if per_diff <= 1:
            return "1s", "1秒", "1second"
        elif per_diff <= 10:
            return "10s", "10秒", "10seconds"
        elif per_diff <= 30:
            return "30s", "30秒", "30seconds"
        elif per_diff <= 60:
            return "1m", "1分钟", "1minute"
        elif per_diff <= 600:
            return "10m", "10分钟", "10minutes"
        elif per_diff <= 1800:
            return "30m", "30分钟", "30minutes"
        elif per_diff <= 3600:
            return "1h", "1小时", "1hour"
        elif per_diff <= 14400:
            return "3h", "3小时", "3hours"
        elif per_diff <= 21600:
            return "6h", "6小时", "6hours"
        elif per_diff <= 43200:
            return "12h", "12小时", "12hours"
        else:
            return "24h", "1天", "1day"

    def params(self, type, module_name, index_type):
        if type == "host_name":
            field = "Hostname.keyword"
        elif type == "level":
            field = "log_level.keyword"
        elif type == "program_name":
            field = "programname.keyword"
        elif type == "module_name":
            field = "Logger.keyword"
        else:
            return {"code": -1, "msg": "invalid param"}

        gen_params = {}
        if module_name:
            gen_params["Logger.keyword"] = module_name
        must_params = self.generate_must(gen_params)

        if index_type is None:
            index_type = self.flog_index_prefix
        if (index_type != self.flog_index_prefix and
                index_type != self.slog_index_prefix):
            return {"code": -1, "msg": "invalid param"}

        end_time = timeutils.utcnow()
        start_time = end_time - datetime.timedelta(days=7)
        index_prefix = index_type
        index_names = self.get_index_names(index_prefix,
                                           start_time, end_time)
        if index_names is None:
            return {"code": 0, "msg": "no data, no index"}
        url = self.elasticsearch_url + '/' + index_names + '/_search'
        data = es_template.search_params(field, must_params)

        values = []
        status, text = utils.request_es(url, "POST", data)
        if status != 200:
            return {"code": -1, "msg": "internal error, bad request"}
        res = json.loads(text)

        aggr = res.get("aggregations")
        if aggr is None:
            return {"code": 0, "msg": "no data, no aggregations"}
        search_values = aggr.get("search_values")
        if search_values is None:
            return {"code": 0, "msg": "no data, no values"}
        buckets = search_values.get("buckets")
        if buckets is None:
            return {"code": 0, "msg": "no data, no buckets"}
        for bucket in buckets:
            if type == "level":
                v = bucket["key"]
                vu = v.upper()
                if vu not in values:
                    values.append(vu)
            else:
                values.append(bucket["key"])

        values.sort()
        if type == "level":
            values.append("NO EXIST")

        return {"code": 1, "msg": "OK", "values": values}

    def generate_must(self, params):
        must_params = []
        for (k, v) in params.items():
            if k == "log_level.keyword":
                terms = {}
                field = {}
                vs = []
                vs.append(v)
                if v.islower():
                    vs.append(v.upper())
                else:
                    vs.append(v.lower())
                field[k] = vs
                terms["terms"] = field
                must_params.append(terms)
            else:
                match = {}
                field = {}
                q = {}
                q["query"] = v
                field[k] = q
                match["match_phrase"] = field
                must_params.append(match)
        return must_params

    def generate_must_not(self, params):
        must_not = []
        for (k, v) in params.items():
            if k == "log_level.keyword":
                terms = {}
                field = {}
                field["field"] = v
                terms["exists"] = field
                must_not.append(terms)
        return must_not

    def logs(self, host_name, module_name, program_name,
             level, user_id, project_id, query, index_type,
             start_time, end_time, page_num, page_size):
        if (start_time is None or end_time is None or
                page_num is None or page_size is None):
            return {"code": -1, "msg": "invalid param"}

        if index_type is None:
            index_type = self.flog_index_prefix
        if (index_type != self.flog_index_prefix and
                index_type != self.slog_index_prefix):
            return {"code": -1, "msg": "invalid param"}

        size = int(page_size)
        from_i = (int(page_num) - 1) * size
        gen_params = {}
        gen_not_params = {}
        if host_name:
            gen_params["Hostname.keyword"] = host_name

        if module_name:
            gen_params["Logger.keyword"] = module_name

        if program_name:
            gen_params["programname.keyword"] = program_name

        if level:
            if level == "NO EXIST":
                gen_not_params["log_level.keyword"] = "log_level"
            else:
                gen_params["log_level.keyword"] = level

        if user_id:
            gen_params["user_id.keyword"] = user_id

        if project_id:
            gen_params["project_id.keyword"] = project_id

        must_params = self.generate_must(gen_params)
        must_not_params = self.generate_must_not(gen_not_params)

        if query is not None and query != "":
            match = {}
            field = {}
            field["all_fields"] = True
            field["analyze_wildcard"] = True
            query = query.replace('"', '\\"')
            field["query"] = '"' + query + '"'
            match["query_string"] = field
            must_params.append(match)

        match = {}
        field = {}
        q = {}
        q["format"] = "epoch_millis"
        q["gte"] = int(start_time) * 1000
        q["lte"] = int(end_time) * 1000
        field["@timestamp"] = q
        match["range"] = field
        must_params.append(match)

        t_start_time = datetime.datetime.utcfromtimestamp(int(start_time))
        t_end_time = datetime.datetime.utcfromtimestamp(int(end_time))

        index_prefix = index_type
        index_names = self.get_index_names(index_prefix,
                                           t_start_time, t_end_time)
        if index_names is None:
            return {"code": 0, "msg": "no data, no index"}
        interval, interval_cn, interval_en = \
            self.get_interval(int(start_time), int(end_time))
        url = self.elasticsearch_url + '/' + index_names + '/_search'
        data = es_template.search_logs(must_params, must_not_params,
                                       start_time, end_time, interval,
                                       from_i, size)

        data_count = []
        res_values = []
        status, text = utils.request_es(url, "POST", data)
        if status != 200:
            return {"code": -1, "msg": "internal error, bad request"}
        res = json.loads(text)

        aggr = res.get("aggregations")
        if aggr is None:
            return {"code": 0, "msg": "no data, no aggregations"}
        search_values = aggr.get("data_count")
        if search_values is None:
            return {"code": 0, "msg": "no data, no count data"}
        buckets = search_values.get("buckets")
        if buckets is None:
            return {"code": 0, "msg": "no data, no buckets"}
        for bucket in buckets:
            data_count.append(bucket)
        hits1 = res.get("hits")
        if hits1 is None:
            return {"code": 0, "msg": "no data, no hit"}
        hits = hits1.get("hits")
        total = hits1.get("total", 0)
        if hits is None:
            return {"code": 0, "msg": "no data, no hit"}
        for hit in hits:
            d = {}
            _source = hit.get("_source")
            if _source is not None:
                d["host_name"] = _source.get("Hostname", "")
                d["time"] = _source.get("@timestamp", "")
                d["level"] = _source.get("log_level", "")
                d["desc"] = _source.get("Payload", "")
                if d["desc"] == "":
                    d["desc"] = _source.get("message", "")
                d["program_name"] = _source.get("programname", "")
                d["user_id"] = _source.get("user_id", "")
                d["project_id"] = _source.get("project_id", "")
                d["module_name"] = _source.get("Logger", "")
            res_values.append(d)

        ds = {}
        ds["count"] = data_count
        ds["interval_cn"] = interval_cn
        ds["interval_en"] = interval_en
        d = {}
        d["total"] = total
        d["values"] = res_values
        return {"code": 1, "msg": "OK", "data_stats": ds, "data": d}

    def analyse_logs(self, group_name, host_name, module_name,
                     program_name, level, start_time, end_time):
        gen_params = {}
        gen_not_params = {}
        title_cn_params = []
        title_en_params = []

        if group_name == "host_name":
            g_name = "Hostname.keyword"
            title_cn = "Host Log Analysis Histogram TOP5"
            title_en = "Host Log Analysis Histogram TOP5"
        elif group_name == "program_name":
            g_name = "programname.keyword"
            title_cn = "Program Log Analysis Histogram TOP5"
            title_en = "Program Log Analysis Histogram TOP5"
        else:
            return {"code": -1, "msg": "invalid param"}

        if host_name:
            gen_params["Hostname.keyword"] = host_name
            title_cn_params.append("host=" + host_name)
            title_en_params.append("host=" + host_name)

        if module_name:
            gen_params["Logger.keyword"] = module_name
            title_cn_params.append("module=" + module_name)
            title_en_params.append("module=" + module_name)

        if program_name:
            gen_params["programname.keyword"] = program_name
            title_cn_params.append("program=" + program_name)
            title_en_params.append("program=" + program_name)

        if level:
            if level == "NO EXIST":
                gen_not_params["log_level.keyword"] = "log_level"
            else:
                gen_params["log_level.keyword"] = level
            title_cn_params.append("level=" + level)
            title_en_params.append("level=" + level)

        if len(title_cn_params) > 0:
            title_cn = title_cn + " (" + " ".join(title_cn_params) + ")"
        if len(title_en_params) > 0:
            title_en = title_cn + " (" + " ".join(title_en_params) + ")"

        must_params = self.generate_must(gen_params)
        must_not_params = self.generate_must_not(gen_not_params)

        match = {}
        field = {}
        q = {}
        q["format"] = "epoch_millis"
        q["gte"] = int(start_time) * 1000
        q["lte"] = int(end_time) * 1000
        field["@timestamp"] = q
        match["range"] = field
        must_params.append(match)

        t_start_time = datetime.datetime.utcfromtimestamp(int(start_time))
        t_end_time = datetime.datetime.utcfromtimestamp(int(end_time))
        index_names = self.get_index_names(self.flog_index_prefix,
                                           t_start_time, t_end_time)
        if index_names is None:
            return {"code": 0, "msg": "no data, no index"}
        url = self.elasticsearch_url + '/' + index_names + '/_search'
        data = es_template.search_analyse_logs(must_params,
                                               must_not_params,
                                               g_name)

        status, text = utils.request_es(url, "POST", data)
        if status != 200:
            return {"code": -1, "msg": "internal error, bad request"}
        res = json.loads(text)
        aggr = res.get("aggregations")
        if aggr is None:
            return {"code": 0, "msg": "no data, no aggregations"}
        search_values = aggr.get("data_count")
        if search_values is None:
            return {"code": 0, "msg": "no data, no count data"}
        buckets = search_values.get("buckets")
        if buckets is None:
            return {"code": 0, "msg": "no data, no buckets"}
        data_count = buckets

        d = {}
        d["count"] = data_count
        d["title_cn"] = title_cn
        d["title_en"] = title_en

        return {"code": 1, "msg": "OK", "data": d}

    def typical_logs(self, type, start_time, end_time):
        gen_params = {}
        if type == "error_stats":
            gen_params["log_level.keyword"] = "ERROR"
            group_name = "programname.keyword"
            return self. typical_stats(
                gen_params, group_name, start_time, end_time)
        elif type == "rabbitmq_error_stats":
            gen_params["log_level.keyword"] = "ERROR"
            rabbit_driver = "oslo.messaging._drivers.impl_rabbit"
            gen_params["python_module.keyword"] = rabbit_driver
            group_name = "programname.keyword"
            return self. typical_stats(
                gen_params, group_name, start_time, end_time)
        elif type == "mysql_error_stats":
            gen_params["log_level.keyword"] = "ERROR"
            gen_params["python_module.keyword"] = "oslo_db.sqlalchemy.engines"
            group_name = "programname.keyword"
            return self. typical_stats(
                gen_params, group_name, start_time, end_time)
        elif type == "novalidhost_error_stats":
            gen_params["log_level.keyword"] = "ERROR"
            gen_params["query"] = "No valid host was found"
            group_name = "programname.keyword"
            return self. typical_stats(
                gen_params, group_name, start_time, end_time)
        else:
            return {"code": -1, "msg": "invalid param"}

    def typical_stats(self, gen_params, group_field, start_time, end_time):
        must_params = self.generate_must(gen_params)
        match = {}
        field = {}
        q = {}
        q["format"] = "epoch_millis"
        q["gte"] = int(start_time) * 1000
        q["lte"] = int(end_time) * 1000
        field["@timestamp"] = q
        match["range"] = field
        must_params.append(match)

        t_start_time = datetime.datetime.utcfromtimestamp(int(start_time))
        t_end_time = datetime.datetime.utcfromtimestamp(int(end_time))
        index_names = self.get_index_names(self.flog_index_prefix,
                                           t_start_time, t_end_time)
        if index_names is None:
            return {"code": 0, "msg": "no data, no index"}

        interval, interval_cn, interval_en = \
            self.get_interval(int(start_time), int(end_time))
        url = self.elasticsearch_url + '/' + index_names + '/_search'
        data = es_template.search_typical_logs(must_params, group_field,
                                               start_time, end_time, interval)

        data_stats = []
        status, text = utils.request_es(url, "POST", data)
        if status != 200:
            return {"code": -1, "msg": "internal error, bad request"}
        res = json.loads(text)

        aggr = res.get("aggregations")
        if aggr is None:
            return {"code": 0, "msg": "no data, no aggregations"}
        data_group = aggr.get("data_group")
        if data_group is None:
            return {"code": 0, "msg": "no data, no data group"}
        buckets = data_group.get("buckets")
        if buckets is None:
            return {"code": 0, "msg": "no data, no buckets"}
        for bucket in buckets:
            d = {}
            d["key"] = bucket.get("key", "")
            d["total"] = bucket.get("doc_count", 0)
            data_count = bucket.get("data_count")
            if data_count is None:
                continue
            sub_buckets = data_count.get("buckets")
            if sub_buckets is None:
                continue
            d["count"] = sub_buckets
            data_stats.append(d)

        ds = {}
        ds["stats"] = data_stats
        ds["interval_cn"] = interval_cn
        ds["interval_en"] = interval_en
        return {"code": 1, "msg": "OK", "data": ds}

    def stat_instance_created_compute(self, request_id, uuid, index_names,
                                      start_time, end_time):
        gen_params = {}
        gen_not_params = {}
        gen_params["request_id.keyword"] = request_id
        gen_params["programname.keyword"] = "nova-compute"
        must_params = self.generate_must(gen_params)
        must_not_params = self.generate_must_not(gen_not_params)

        match = {}
        field = {}
        field["all_fields"] = True
        field["analyze_wildcard"] = True
        field["query"] = '"' + uuid + '"'
        match["query_string"] = field
        must_params.append(match)
        url = self.elasticsearch_url + '/' + index_names + '/_search'
        data = es_template.search_logs(must_params, must_not_params,
                                       start_time, end_time, "24h",
                                       0, 10000)
        status, text = utils.request_es(url, "POST", data)
        if status != 200:
            return None, "internal error, bad request"
        res = json.loads(text)
        hits1 = res.get("hits")
        if hits1 is None:
            return [], "no data, no hit"
        hits = hits1.get("hits")
        if hits is None:
            return [], "no data, no hit"
        hostinfos = {}
        for hit in hits:
            info = {}
            _source = hit.get("_source")
            if _source is not None:
                hostname = _source.get("Hostname", "")
                if hostinfos.get(hostname) is None:
                    hostinfos[hostname] = []
                info["payload"] = _source.get("Payload", "")
                info["time"] = _source.get("@timestamp", "")
                hostinfos[hostname].append(info)

        res = []
        for (k, v) in hostinfos.items():
            r = {}
            r["hostname"] = k
            start_time = ""
            end_time = ""
            is_success = 0
            for i in v:
                payload = i.get("payload")
                if "Took" in payload and "seconds to build" in payload:
                    end_time = i.get("time", "")
                    is_success = 1
                if ("Enter inspur build_and_run_instance" in payload and
                        start_time == ""):
                    start_time = i.get("time", "")

            if is_success == 0 and len(v) > 0:
                end_time = v[0].get("time", "")
                start_time = v[len(v) - 1].get("time", "")

            r["is_success"] = is_success
            r["start_time"] = start_time
            r["end_time"] = end_time
            res.append(r)

        def sort_time(e):
            return e.get('start_time')
        res.sort(key=sort_time)

        return res, None

    def stat_instance_created_other(self, index_names, params):
        data = es_template.search_all_logs(params)
        url = self.elasticsearch_url + '/' + index_names + '/_search'
        status, text = utils.request_es(url, "POST", data)
        if status != 200:
            return [], "internal error, bad request"
        json_text = json.loads(text)
        hits1 = json_text.get("hits")
        if hits1 is None:
            return [], "no data, no hit"
        hits = hits1.get("hits")

        hostinfos = {}
        for hit in hits:
            info = {}
            _source = hit.get("_source")
            if _source is not None:
                hostname = _source.get("Hostname", "")
                if hostinfos.get(hostname) is None:
                    hostinfos[hostname] = []
                info["level"] = _source.get("log_level", "")
                info["time"] = _source.get("@timestamp", "")
                hostinfos[hostname].append(info)

        res = []
        for (k, v) in hostinfos.items():
            r = {}
            r["hostname"] = k
            error_num = 0
            start_time = ""
            end_time = ""
            for i in v:
                level = i.get("level")
                if level == "ERROR" or level == "error":
                    error_num += 1

            if len(v) > 0:
                start_time = v[0].get("time", "")
                end_time = v[len(v) - 1].get("time", "")

            r["log_num"] = len(v)
            r["error_log_num"] = error_num
            r["start_time"] = start_time
            r["end_time"] = end_time
            res.append(r)

        def sort_time(e):
            return e.get('start_time')
        res.sort(key=sort_time)

        return res, None

    def instance_call_chain(self, request_id, uuid):
        end_time = int(time.time())
        start_time = end_time - 86400 * 365

        t_start_time = datetime.datetime.utcfromtimestamp(int(start_time))
        t_end_time = datetime.datetime.utcfromtimestamp(int(end_time))
        index_names = self.get_index_names(self.flog_index_prefix,
                                           t_start_time, t_end_time)
        if index_names is None:
            return {"code": 0, "msg": "no data, no index"}

        programs = ["nova-api", "nova-conductor", "nova-scheduler"]
        res = {}
        msg = "OK"
        code = 1
        for p in programs:
            gen_params = {}
            gen_params["request_id.keyword"] = request_id
            gen_params["programname.keyword"] = p
            params = self.generate_must(gen_params)
            match = {}
            field = {}
            q = {}
            q["format"] = "epoch_millis"
            q["gte"] = start_time * 1000
            q["lte"] = end_time * 1000
            field["@timestamp"] = q
            match["range"] = field
            params.append(match)

            d, r = self.stat_instance_created_other(index_names, params)
            res[p] = d
            if r is not None:
                msg = r
                code = -1

        # for nova-compute
        d, r = self.stat_instance_created_compute(
            request_id, uuid, index_names, start_time, end_time)
        res["nova-compute"] = d
        if r is not None:
            msg = r
            code = -1

        return {"code": code, "msg": msg, "data": res}
