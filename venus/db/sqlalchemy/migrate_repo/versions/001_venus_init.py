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

"""WSGI Routers for the Identity service."""

import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker


def upgrade(migrate_engine):
    meta = sql.MetaData()
    meta.bind = migrate_engine

    t_mo_regitster_task = sql.Table(
        't_mo_regitster_task',
        meta,
        sql.Column('Id', sql.Integer, nullable=False,
                   primary_key=True),
        sql.Column('task_name', sql.String(255), nullable=True,
                   primary_key=False),
        sql.Column('host_name', sql.String(255), nullable=True,
                   primary_key=False),
        sql.Column('update_time', sql.DateTime, nullable=True,
                   primary_key=False, default='0000-00-00 00:00:00'),
        sql.Column('created_at', sql.DateTime,
                   nullable=True, primary_key=False),
        sql.Column('updated_at', sql.DateTime,
                   nullable=True, primary_key=False),
        sql.Column('deleted', sql.String(1),
                   nullable=True, primary_key=False),
        sql.Column('deleted_at', sql.DateTime,
                   nullable=True, primary_key=False),

        mysql_engine='InnoDB',
        mysql_charset='utf8')

    t_mo_regitster_task.create(migrate_engine, checkfirst=True)

    new_data = {
        'Id': '1',
        'task_name': 'delete_es_index',
        'host_name': '',
        'update_time': '1900-01-01 00:00:00'
    }
    maker = sessionmaker(bind=migrate_engine)
    session = maker()
    t_mo_regitster_task = sql.Table('t_mo_regitster_task', meta, autoload=True)
    row = t_mo_regitster_task.insert().values(**new_data)
    session.execute(row)
    session.commit()

    t_mo_custom_config = sql.Table(
        't_mo_custom_config',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('value', sql.String(10240), nullable=False),
        sql.Column('update_time', sql.DateTime),
        mysql_engine='InnoDB',
        mysql_charset='utf8')

    t_mo_custom_config.create(migrate_engine, checkfirst=True)
    new_data = {
        'id': 'es_index_length',
        'value': '30',
        'update_time': '1900-01-01 00:00:00'
    }
    maker = sessionmaker(bind=migrate_engine)
    session = maker()
    t_mo_custom_config = sql.Table('t_mo_custom_config', meta, autoload=True)
    row = t_mo_custom_config.insert().values(**new_data)
    session.execute(row)

    session.commit()
    session.close()
