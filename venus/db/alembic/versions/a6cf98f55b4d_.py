# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Initial revision

Revision ID: c6214ca60943
Revises:
Create Date: 2023-03-22 18:04:02.387269
"""

from alembic import op
from oslo_utils import timeutils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6cf98f55b4d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # create task table and init data
    t_mo_regitster_task = op.create_table(
        't_mo_regitster_task',
        sa.Column('Id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('task_name', sa.String(255), nullable=True,
                  primary_key=False),
        sa.Column('host_name', sa.String(255), nullable=True,
                  primary_key=False),
        sa.Column('update_time', sa.DateTime, nullable=True,
                  primary_key=False, default='0000-00-00 00:00:00'),
        sa.Column('created_at', sa.DateTime, nullable=True, primary_key=False),
        sa.Column('updated_at', sa.DateTime, nullable=True, primary_key=False),
        sa.Column('deleted', sa.String(1), nullable=True, primary_key=False),
        sa.Column('deleted_at', sa.DateTime, nullable=True, primary_key=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

    now = timeutils.utcnow()
    new_data1 = {
        'Id': '1',
        'task_name': 'delete_es_index',
        'host_name': '',
        'update_time': now
    }

    new_data2 = {
        'Id': '2',
        'task_name': 'anomaly_detect',
        'host_name': '',
        'update_time': now
    }

    new_data3 = {
        'Id': '3',
        'task_name': 'delete_anomaly_record',
        'host_name': '',
        'update_time': now
    }

    op.bulk_insert(
        t_mo_regitster_task,
        [
            new_data1,
            new_data2,
            new_data3
        ],
    )

    # create config table and init data
    t_mo_custom_config = op.create_table(
        't_mo_custom_config',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('value', sa.String(10240), nullable=False),
        sa.Column('update_time', sa.DateTime),
        mysql_engine='InnoDB',
        mysql_charset='utf8')

    new_data1 = {
        'id': 'log_save_days',
        'value': '30',
        'update_time': now
    }

    new_data2 = {
        'id': 'anomaly_record_save_days',
        'value': '30',
        'update_time': now
    }

    op.bulk_insert(
        t_mo_custom_config,
        [
            new_data1,
            new_data2
        ],
    )

    # create anomaly rule table
    op.create_table(
        't_mo_anomaly_rules',
        sa.Column('id', sa.String(64), nullable=False, primary_key=True),
        sa.Column('title', sa.String(1024), nullable=True,
                  primary_key=False),
        sa.Column('desc', sa.String(1024), nullable=True,
                  primary_key=False),
        sa.Column('keyword', sa.String(1024), nullable=True,
                  primary_key=False),
        sa.Column('log_type', sa.String(1024), nullable=True,
                  primary_key=False),
        sa.Column('module', sa.String(1024), nullable=True,
                  primary_key=False),
        sa.Column('flag', sa.Integer, nullable=True, primary_key=False),
        sa.Column('create_time', sa.DateTime, nullable=True,
                  primary_key=False, default='0000-00-00 00:00:00'),
        sa.Column('update_time', sa.DateTime, nullable=True,
                  primary_key=False, default='0000-00-00 00:00:00'),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

    # create anomaly record table
    op.create_table(
        't_mo_anomaly_records',
        sa.Column('id', sa.String(64), nullable=False, primary_key=True),
        sa.Column('title', sa.String(1024), nullable=True,
                  primary_key=False),
        sa.Column('desc', sa.String(1024), nullable=True,
                  primary_key=False),
        sa.Column('keyword', sa.String(1024), nullable=True,
                  primary_key=False),
        sa.Column('log_type', sa.String(1024), nullable=True,
                  primary_key=False),
        sa.Column('module', sa.String(1024), nullable=True,
                  primary_key=False),
        sa.Column('logs', sa.String(10240), nullable=True,
                  primary_key=False),
        sa.Column('start_time', sa.DateTime, nullable=True,
                  primary_key=False, default='0000-00-00 00:00:00'),
        sa.Column('end_time', sa.DateTime, nullable=True,
                  primary_key=False, default='0000-00-00 00:00:00'),
        sa.Column('create_time', sa.DateTime, nullable=True,
                  primary_key=False, default='0000-00-00 00:00:00'),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )
