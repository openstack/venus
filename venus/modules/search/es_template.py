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

"""Implementation of Search Template."""


def search_params(field, must_params):
    data = {
        "aggs": {
            "search_values": {
                "terms": {
                    "field": field,
                    "size": 10000
                }
            }
        },
        "query": {
            "bool": {
                "must": must_params
            }
        },
        "size": 0,
        "version": True
    }
    return data


def search_logs(must_params, must_not_params, start_time,
                end_time, interval, from_i, size):
    data = {
        "aggs": {
            "data_count": {
                "date_histogram": {
                    "field": "@timestamp",
                    "interval": interval,
                    "min_doc_count": 0,
                    "time_zone": "Asia/Shanghai",
                    "extended_bounds": {
                        "min": int(start_time) * 1000,
                        "max": int(end_time) * 1000
                    }
                }
            }
        },
        "query": {
            "bool": {
                "must": must_params,
                "must_not": must_not_params
            }
        },
        "script_fields": {},
        "from": from_i,
        "size": size,
        "sort": [
            {
                "@timestamp": {
                    "order": "desc",
                    "unmapped_type": "boolean"
                }
            }
        ]
    }
    return data


def search_analyse_logs(must_params, must_not_params, g_name):
    data = {
        "aggs": {
            "data_count": {
                "terms": {
                    "field": g_name,
                    "order": {
                        "_count": "desc"
                    },
                    "size": 5
                }
            }
        },
        "query": {
            "bool": {
                "must": must_params,
                "must_not": must_not_params
            }
        },
        "size": 0
    }
    return data


def search_typical_logs(must_params, group_field, start_time,
                        end_time, interval):
    data = {
        "aggs": {
            "data_group": {
                "aggs": {
                    "data_count": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "interval": interval,
                            "min_doc_count": 0,
                            "time_zone": "Asia/Shanghai",
                            "extended_bounds": {
                                "min": int(start_time) * 1000,
                                "max": int(end_time) * 1000
                            }
                        }
                    }
                },
                "terms": {
                    "field": group_field,
                    "order": {
                        "_count": "desc"
                    },
                    "size": 10000
                }
            }
        },
        "query": {
            "bool": {
                "must": must_params
            }
        },
        "size": 0,
        "version": True
    }
    return data


def search_request_ids():
    data = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "Payload": "build_and_run_instance"
                        }
                    }
                ]
            }
        },
        "from": 0,
        "size": 10000
    }
    return data


def search_all_logs(must_params):
    data = {
        "query": {
            "bool": {
                "must": must_params
            }
        },
        "size": 10000,
        "version": True,
        "sort": [
            {
                "@timestamp": {
                    "order": "asc",
                    "unmapped_type": "boolean"
                }
            }
        ]
    }

    return data
