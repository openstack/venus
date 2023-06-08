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
    t_mo_regitster_task = op.create_table(
        't_mo_regitster_task1',
        sa.Column('Id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('task_name', sa.String(255), nullable=True,
                  primary_key=False),
        sa.Column('host_name', sa.String(255), nullable=True,
                  primary_key=False),
        sa.Column('created_at', sa.DateTime, nullable=True, primary_key=False),
        sa.Column('updated_at', sa.DateTime, nullable=True, primary_key=False),
        sa.Column('deleted', sa.String(1), nullable=True, primary_key=False),
        sa.Column('deleted_at', sa.DateTime, nullable=True, primary_key=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

    now = timeutils.utcnow()
    new_data = {
        'Id': '1',
        'task_name': 'delete_es_index',
        'host_name': '',
        'update_time': now
    }

    op.bulk_insert(
        t_mo_regitster_task,
        [
            new_data,
        ],
    )
