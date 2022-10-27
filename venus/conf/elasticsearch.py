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

from oslo_config import cfg

elasticsearch_group = cfg.OptGroup(name='elasticsearch',
                                   title='elasticsearch')

elasticsearch_opts = [
    cfg.StrOpt('url',
               default='http://localhost:9200',
               help='the es url'),
    cfg.StrOpt('username',
               default='elastic',
               help='the es username'),
    cfg.StrOpt('password',
               default='admin',
               help='the es password'),
    cfg.IntOpt('es_index_days',
               default=30,
               help='the es log store days')
]


def register_opts(conf):
    conf.register_group(elasticsearch_group)
    conf.register_opts(elasticsearch_opts, elasticsearch_group)
