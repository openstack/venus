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

"""
SQLAlchemy models for venus data.
"""

from oslo_config import cfg
from oslo_db.sqlalchemy import models
from oslo_utils import timeutils
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, Integer, String
CONF = cfg.CONF
BASE = declarative_base()


class VenusBase(models.TimestampMixin,
                models.ModelBase):
    """Base class for Venus Models."""

    __table_args__ = {'mysql_engine': 'InnoDB'}

    # TODO(rpodolyaka): reuse models.SoftDeleteMixin in the next stage
    #                   of implementing of BP db-cleanup
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    # deleted = Column(Boolean, default=False)
    deleted = Column(String(1), default=0)
    metadata = None

    def delete(self, session):
        """Delete this object."""
        self.deleted = True
        self.deleted_at = timeutils.utcnow()
        self.save(session=session)


def register_models():
    """Rvenuster Models and create metadata.

    Called from venus.db.sqlalchemy.__init__ as part of loading the driver,
    it will never need to be called explicitly elsewhere unless the
    connection is lost and needs to be reestablished.
    """
    from sqlalchemy import create_engine

    models = ()
    engine = create_engine(CONF.database.connection, echo=False)
    for model in models:
        model.metadata.create_all(engine)


class AnomalyRules(BASE):
    __tablename__ = 't_mo_anomaly_rules'
    id = Column(String(64), primary_key=True)
    title = Column(String(1024))
    desc = Column(String(1024))
    keyword = Column(String(1024))
    log_type = Column(String(1024))
    module = Column(String(1024))
    flag = Column(Integer)
    create_time = Column(DateTime())
    update_time = Column(DateTime())


class AnomalyRecords(BASE):
    __tablename__ = 't_mo_anomaly_records'
    id = Column(String(64), primary_key=True)
    title = Column(String(1024))
    desc = Column(String(1024))
    keyword = Column(String(1024))
    log_type = Column(String(1024))
    module = Column(String(1024))
    logs = Column(String(10240))
    start_time = Column(DateTime())
    end_time = Column(DateTime())
    create_time = Column(DateTime())
