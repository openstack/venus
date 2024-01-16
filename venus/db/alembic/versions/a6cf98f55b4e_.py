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

Revision ID: a6cf98f55b4e
Revises:
Create Date: 2024-01-16 17:07:05.546734
"""

from alembic import op
from oslo_utils import timeutils


# revision identifiers, used by Alembic.
revision = 'a6cf98f55b4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql = "INSERT INTO {} (id, value, update_time) VALUES ('{}', '{}', '{}')"
    sql = sql.format('t_mo_regitster_task',
                     'log_max_gb',
                     '100',
                     str(timeutils.utcnow()))
    op.execute(sql)
